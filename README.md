# prompt-optimizer

An [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) that optimizes and polishes an **existing** AI/LLM prompt — without changing what it asks for.

> **Optimize, don't recreate. Improve expression, don't expand scope. Tidy structure, don't redesign it.**

## What it does

Point it at a prompt you've already written and ask to optimize / refine / polish / simplify / restructure / make more professional. It fixes wording, grammar, redundancy, and structure, while strictly preserving:

- the original goal, role, and scope
- the capability list (it will not add tools/technologies you didn't mention)
- constraint strength (可以/can → 建议/suggest → 优先/prefer → 尽量/try to → 应该/should → 必须/must → 禁止/forbidden → 严禁/strictly forbidden — it will not silently strengthen or soften these)
- every technical detail verbatim: commands, paths, URLs, parameters, file names, code blocks, model/tool names
- the original language (Chinese stays Chinese, English stays English, mixed stays mixed)

When you invoke it with `/prompt-optimizer`, it prints the optimized prompt as `优化后提示词：<full optimized prompt>` and then carries it out. When it is triggered by an ordinary "optimize this prompt" request instead, it outputs **only the optimized prompt**. Either way there is no explanation, no before/after and no analysis unless you ask for one, and the prompt is always printed in full, never truncated or shortened with "(rest unchanged)", so you can see exactly what it became.

It deliberately does **not** trigger for: writing a new prompt from scratch, executing a prompt you provide, polishing ordinary prose (emails/articles), optimizing source code, or explaining prompt-engineering theory. See the "When Not to Use" section in `SKILL.md` for the full boundary.

## Install

This is a single-file [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) — all the logic lives in `SKILL.md`, with no scripts, MCP servers, or external dependencies, so it should work in any tool that supports the Agent Skills / `SKILL.md` convention (Claude Code, Codex, etc.).

**Claude Code** (global, all projects):

```bash
mkdir -p ~/.claude/skills/prompt-optimizer
curl -o ~/.claude/skills/prompt-optimizer/SKILL.md \
  https://raw.githubusercontent.com/talki-io/prompt-optimizer/main/SKILL.md
```

Or clone the repo directly into the skills directory:

```bash
git clone https://github.com/talki-io/prompt-optimizer.git ~/.claude/skills/prompt-optimizer
```

**Project-local install** (this project only): put the same file at `.claude/skills/prompt-optimizer/SKILL.md` inside your repo.

**Codex / other Agent Skills-compatible tools:** copy `SKILL.md` into whatever skills directory that tool discovers — the file itself is platform-neutral.

**No install (any chat AI):** paste the full content of `SKILL.md` into the chat together with the prompt you want optimized (no "帮我优化" needed). The AI optimizes your prompt right away, prints it as `优化后提示词：<full optimized prompt>`, and then carries it out. It won't summarize or review the skill text. If you only want the optimized text, add "只优化，不用执行" (just optimize it).

## Usage

Invoke the skill with `/prompt-optimizer` followed by your prompt — no need to add "帮我优化" / "optimize this". Claude optimizes the prompt, prints it as `优化后提示词：<full optimized prompt>`, and then carries it out. Add "只优化，不用执行" (just optimize it) if you only want the text back.

```
You: /prompt-optimizer 你是一名专业提示词优化大师，熟悉各种提示词优化，书写，你主要任务是协助用户完成提示词优化工作

Claude: 优化后提示词：
你是一名专业的提示词优化大师，熟悉各类提示词的优化与撰写，主要任务是协助用户完成提示词优化工作。

（接着按优化后的提示词开始工作）
```

```
You (without invoking the skill): Optimize this prompt: "you are helpful assistant that help user write code and also fix bug and also explain things good"

Claude: You are a helpful assistant that helps users write code, fix bugs, and explain concepts clearly.
```

Want to know what changed? Just ask: "tell me what you changed" or "give me a before/after comparison" — by default the skill stays silent about its edits and just returns the result.

When the skill is triggered by an ordinary "optimize this prompt" request instead of `/prompt-optimizer`, you get the optimized text back and decide what to do with it. If you want to skip the copy-paste round trip and have Claude immediately start operating under the optimized prompt in the same conversation (it prints `优化后提示词：<full prompt>` first, then starts), say so explicitly — e.g. "优化完直接用" / "apply it directly, don't make me paste it back". This only works within the current conversation; a skill has no way to push text into a different chat window or model.

## Design principles

This skill was built to solve a specific failure mode of naive "prompt optimization": an LLM asked to "optimize" a prompt tends to *expand* it — adding capabilities, softening or hardening constraints, inventing process steps, and turning a three-line prompt into a ten-section template. That's prompt *creation* wearing the costume of prompt *editing*, and it quietly changes what the user is committing their AI to do.

`SKILL.md` counters this with an explicit preservation boundary (goal / capability scope / constraint strength / technical content / language) and a self-check the model runs before returning output, rather than relying on the model to intuit restraint on its own.

See `SKILL.md` for the full ruleset — it's the single source of truth and is meant to be read directly.

## License

MIT — see [LICENSE](LICENSE).
