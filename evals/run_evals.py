#!/usr/bin/env python3
"""Regression evals for SKILL.md, run through headless Claude Code (`claude -p`).

  python3 evals/run_evals.py run   --skill SKILL.md --out OUT [--cases id,id] [--model M] [--jobs N] [--runs N]
  python3 evals/run_evals.py grade OUT [OUT ...]

Turn modes in cases.json:
  explicit  - the message Claude Code builds for `/prompt-optimizer <text>` (skill body inlined)
  ordinary  - plain request, with the skill body appended to the system prompt (as if model-loaded)
  plain     - an ordinary follow-up message
Each run is isolated: no tools, no skills/slash commands, no MCP, no user settings/plugins/hooks.
A case's checks apply to all assistant text of its last turn.
"""
import argparse, concurrent.futures as cf, difflib, json, os, re, signal, subprocess, sys, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent


def skill_body(path):
    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    return text.strip("\n")


def explicit_message(body, args):
    return (f"<command-message>prompt-optimizer</command-message>\n"
            f"<command-name>/prompt-optimizer</command-name>\n"
            f"<command-args>{args}</command-args>\n"
            f"Base directory for this skill: ~/.claude/skills/prompt-optimizer\n\n"
            f"{body}\n\n\nARGUMENTS: {args}")


# Tools are off, but Claude Code's system prompt still describes them; without this note the
# model may write fake tool-call markup and invent results, which also bloats/hangs runs.
TEXT_ONLY = ("Test environment note: no tools are available in this session. Never write tool-call "
             "markup or invent tool results; if a task would need tools, say so briefly in plain text.")


def call_claude(message, model, workdir, session, first, system_append):
    """One user turn. Returns (record, session); all assistant text of the turn is joined."""
    for attempt in range(2):  # a headless call occasionally hangs; retry once
        cmd = ["claude", "-p", "--model", model, "--tools", "", "--disable-slash-commands",
               "--strict-mcp-config", "--setting-sources", "project",
               "--output-format", "stream-json", "--verbose", "--append-system-prompt", system_append]
        cmd += ["--session-id", session] if first else ["--resume", session]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, cwd=workdir, start_new_session=True)
        try:
            stdout, stderr = p.communicate(message, timeout=300)
            break
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)  # kill the whole tree so the session lock is released
            p.communicate()
            if attempt:
                return {"result": "", "is_error": True, "error": "timed out twice"}, session
            if first:
                session = str(uuid.uuid4())
    texts, final = [], {}
    for line in stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "assistant":
            texts += [b["text"] for b in e["message"].get("content", []) if b.get("type") == "text"]
        elif e.get("type") == "result":
            final = e
    if not final:
        return {"result": "", "is_error": True, "error": (stderr or stdout)[-2000:]}, session
    u = final.get("usage") or {}
    return {"result": "\n\n".join(texts) or final.get("result", ""), "is_error": final.get("is_error"),
            "input_tokens": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                            + u.get("cache_read_input_tokens", 0),
            "output_tokens": u.get("output_tokens", 0),
            "cost_usd": final.get("total_cost_usd"), "duration_ms": final.get("duration_ms")}, session


def run_case(case, body, model, out, run_idx):
    workdir = out / "_work"
    workdir.mkdir(parents=True, exist_ok=True)
    session = str(uuid.uuid4())
    turns = []
    for i, t in enumerate(case["turns"]):
        extra = TEXT_ONLY
        if t["mode"] == "explicit":
            msg = explicit_message(body, t["text"])
        elif t["mode"] == "ordinary":
            msg = t["text"]
            extra += "\n\nThe `prompt-optimizer` skill is loaded. Its instructions:\n\n" + body
        else:
            msg = t["text"]
        r, session = call_claude(msg, model, workdir, session, i == 0, extra)
        turns.append({"mode": t["mode"], "input": t["text"], **r})
        if r.get("is_error"):
            break
    dest = out / case["id"] / f"run{run_idx}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"case": case["id"], "turns": turns}, ensure_ascii=False, indent=2))
    return case["id"], run_idx, turns[-1].get("is_error")


def cmd_run(a):
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    if a.cases:
        wanted = set(a.cases.split(","))
        unknown = wanted - {c["id"] for c in cases}
        if unknown:
            sys.exit(f"unknown case id(s): {', '.join(sorted(unknown))}")
        cases = [c for c in cases if c["id"] in wanted]
    body, out = skill_body(a.skill), Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "skill.md").write_text(Path(a.skill).read_text(encoding="utf-8"), encoding="utf-8")
    start = {c["id"]: len(list((out / c["id"]).glob("run*.json"))) if (out / c["id"]).exists() else 0
             for c in cases}
    jobs = [(c, start[c["id"]] + k) for c in cases for k in range(a.runs)]
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        futs = [ex.submit(run_case, c, body, a.model, out, k) for c, k in jobs]
        for f in cf.as_completed(futs):
            cid, k, err = f.result()
            print(f"{'ERR ' if err else 'done'} {cid} run{k}", flush=True)


def check(case, text):
    c, fails = case["checks"], []
    for s in c.get("contains", []):
        if s not in text:
            fails.append(f"missing {s!r}")
    for s in c.get("not_contains", []):
        if s in text:
            fails.append(f"has {s!r}")
    for r in c.get("regex", []):
        if not re.search(r, text):
            fails.append(f"no match /{r}/")
    for r in c.get("not_regex", []):
        m = re.search(r, text)
        if m:
            fails.append(f"matched /{r}/ ({m.group(0)!r})")
    orig = case.get("original")
    if orig and "max_ratio" in c and len(text) / len(orig) > c["max_ratio"]:
        fails.append(f"length ratio {len(text) / len(orig):.2f} > {c['max_ratio']}")
    if orig and "min_similarity" in c:
        sim = difflib.SequenceMatcher(None, orig, text.strip()).ratio()
        if sim < c["min_similarity"]:
            fails.append(f"similarity {sim:.2f} < {c['min_similarity']}")
    if "max_chars" in c and len(text) > c["max_chars"]:
        fails.append(f"{len(text)} chars > {c['max_chars']}")
    return fails


def cmd_grade(a):
    cases = {c["id"]: c for c in json.loads((HERE / "cases.json").read_text(encoding="utf-8"))}
    for d in a.outs:
        d = Path(d)
        skill = (d / "skill.md").read_text(encoding="utf-8") if (d / "skill.md").exists() else ""
        print(f"\n== {d.name}  (SKILL.md {len(skill)} chars)")
        passed = total = 0
        for cid, case in cases.items():
            for f in sorted((d / cid).glob("run*.json")) if (d / cid).exists() else []:
                turns = json.loads(f.read_text(encoding="utf-8"))["turns"]
                last = turns[-1]
                fails = ["run error: " + last.get("error", "")[:200]] if last.get("is_error") \
                    else check(case, last["result"])
                total += 1
                passed += not fails
                print(f"  {'PASS' if not fails else 'FAIL'}  {cid}/{f.stem}" + ("" if not fails else "  " + "; ".join(fails)))
        print(f"  -> {passed}/{total} passed")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--skill", default=str(HERE.parent / "SKILL.md"))
    r.add_argument("--out", required=True)
    r.add_argument("--cases")
    r.add_argument("--model", default="claude-opus-5-5")
    r.add_argument("--jobs", type=int, default=4)
    r.add_argument("--runs", type=int, default=1)
    g = sub.add_parser("grade")
    g.add_argument("outs", nargs="+")
    a = ap.parse_args()
    cmd_run(a) if a.cmd == "run" else cmd_grade(a)


if __name__ == "__main__":
    main()
