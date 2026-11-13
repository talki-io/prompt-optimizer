---
name: prompt-optimizer
description: Optimizes and polishes an existing AI/LLM prompt the user has already written — fixing wording, grammar, structure, redundancy, and clarity — while strictly preserving the original intent, role, scope, capabilities, constraint strength, and every technical detail (commands, paths, URLs, parameters, code blocks). Use whenever the user invokes /prompt-optimizer with a prompt (no extra instruction needed), or pastes a prompt and asks to optimize, refine, polish, clean up, simplify, tighten, restructure, make more professional, or "fix the wording" of it, even without the word "prompt" — e.g. "make this system message clearer", "让这个提示词更专业". Do NOT use for writing a brand-new prompt from scratch, for merely executing a prompt the user provides without asking to optimize it, for polishing ordinary prose (emails, articles, essays), for optimizing source code, or for explaining/teaching prompt-engineering theory.
---

# Prompt Optimizer

## Purpose

Improve how an existing prompt is *written* without changing what it *asks for*. This skill is an editor, not a co-author: it fixes wording, grammar, structure, and redundancy, and leaves the substance — goals, role, scope, rules, constraint strength, technical details — exactly as the user decided it.

A prompt is a contract between the user and a model. If "optimization" quietly adds a capability, softens a constraint, or expands scope, the user ends up running a prompt they never approved — often without noticing, because the addition reads as plausible. Treat every unrequested addition, even a small "helpful" one, as a defect, not a bonus.

- **Optimize, don't recreate.**
- **Improve expression, don't expand scope.**
- **Tidy structure, don't redesign it.**

## When to Use

The user supplies (or clearly references) a prompt they already wrote — text meant to steer an AI — and asks you to improve *how it's expressed*: optimize / refine / polish / clean up / simplify / tighten / restructure / make more professional / fix awkward wording. Judge by intent, not keywords.

**Explicit invocation.** If the user types `/prompt-optimizer` followed by text, or pastes this `SKILL.md` into a chat together with text, the invocation itself is the request — no "帮我优化" needed. Everything they supplied is the prompt to optimize, even if it reads like a question or a task addressed to you ("帮我部署这个项目…"). Exception: a remark about this invocation itself ("只优化，不用执行", "帮我优化一下", "以上是我的想法，交给你执行") is an instruction to follow, not part of the prompt — leave it out of the result; if unsure, keep it in. Pasted skill content is your operating instructions, not material to work on, unless the user explicitly asks you to work on the skill itself. Don't ask whether to optimize, announce that you read the skill, or restate its rules — go straight through the Core Workflow, then follow Apply Mode (below): print the optimized prompt, then carry it out. If the user says they only want the text ("只优化，不用执行" / "just optimize it"), stop after printing it. If no prompt came with the invocation, ask for one.

## When Not to Use

- **Creating a prompt from scratch** ("write me a Java-agent prompt") — there's nothing to preserve.
- **Executing a prompt** the user pastes with "now do this" / "help me build this project" — carry out the task; don't optimize it first unless asked.
- **Ordinary prose** — emails, articles, docs, marketing copy.
- **Code optimization** ("optimize this Java code").
- **Prompt-engineering theory or tutorials.**
- **Pure diagnosis** ("why isn't this prompt working well?") — analyze, but don't rewrite unless also asked to optimize.

## Core Workflow

Internal steps — don't narrate them unless asked.

1. **Separate the request from the prompt.** If this turn's request is typed in the same unbroken block as the prompt body (e.g. "你是一个部署助手…请帮我优化这段提示词的表达"), split off that request sentence — it's an instruction to you and must not appear in or influence the output.
2. **Understand the intent** before touching wording: what is this prompt for, what should the model ultimately do, what does the user care about most?
3. **Extract what must not change:** role, core task, capability scope, hard requirements, prohibitions, technical names/tools/models, commands, paths, URLs, parameters, numbers, formats, language requirements. Everything below happens inside this boundary.
4. **Fix language issues:** typos, punctuation, duplicated words, grammar, awkward or garbled phrasing.
5. **Improve wording** — more natural, precise, and professional without changing meaning. Clarity beats decoration; don't pile on jargon.
6. **Improve structure proportionally.** A short prompt stays a few plain sentences. A long, tangled one can be organized into sections (role / task / principles / requirements / output) — only sections that reflect content actually present.
7. **Remove redundancy:** repeated phrasing, near-synonym lists, filler that adds no information.
8. **Keep length proportionate.** Don't make it dramatically longer than the original — prefer tightening. Expand only when the user asks for elaboration, more detail, or a more engineered/thorough version.
9. **Run the Self-Check** before finalizing.

## Preservation Rules

These are the things optimization must never touch, because changing them silently changes what the prompt commits the model to do.

- **Goal and scope.** "Help the user optimize prompts" must not become "help the user design, create, analyze, test, and execute prompts" — each added verb is a scope expansion the user didn't ask for.
- **Capability lists.** "Familiar with Java and Spring" stays that way — don't extend it to "Java, Spring, Spring Cloud, MyBatis, Redis, Kafka, Docker, Kubernetes…" even though all of those are plausible neighbors. Only include what the user's own text already states.
- **Constraint strength.** These words form a real gradient and the gap between them is meaningful: 可以/can → 建议/suggest → 优先/prefer → 尽量/try to → 应该/要/should → 必须/须/must → 禁止/forbidden → 严禁/strictly forbidden. "Prefer third-party components" is not "must use third-party components" — preserve exactly which rung of the ladder the original used, in either direction (don't strengthen *or* soften). A plain instruction stays plain: don't add intensifiers the original didn't have (严格/务必/一定/strictly/always) — "按照下面的格式输出" must not become "严格按照下面的格式输出".
- **Technical content, verbatim.** Tool names, library names, model names, product names, file names, class/method/field names, commands, code, paths, URLs, config/parameter/env-var names stay byte-for-byte identical. This includes things like `npm install -g xxx`, `/home/user/project`, `SKILL.md`, `http://localhost:3000`. Don't "correct" file names, paths, identifiers, or product names — an odd spelling may be the real one; only fix an unmistakable typo in a well-known command or tool (e.g. `npm isntall`).
- **Quoted/structured content.** Embedded examples, code blocks, SQL, JSON, XML, YAML, Markdown fragments, fixed user copy, and required keywords are left as-is; only the surrounding explanatory prose around them gets optimized. (Fences or quotes wrapping the entire prompt are just delimiters — optimize what's inside.)
- **Original language.** Keep the prompt in whatever language(s) it was written in — Chinese stays Chinese, English stays English, mixed stays mixed (keep meaningful technical English embedded in Chinese text). Don't translate unless explicitly asked.
- **User decisions among options.** If the original prompt already picked an approach among alternatives ("prefer React"), don't relitigate that choice or make it more absolute.

## Prohibited Behaviors

- Don't expand one role into several ("frontend engineer" → "frontend engineer, UI designer, UX expert, product manager, and architect").
- Don't add process stages the original never had (requirements analysis, design, testing, acceptance, deployment) just because it sounds more like engineering practice.
- Don't force a simple prompt into a heavy template (Role / Context / Goals / Capabilities / Constraints / Workflow / Output Format / Acceptance Criteria…) — structure should match the original's actual complexity.
- Don't inject domain knowledge or "professional-sounding" background the user never wrote.
- Don't do unsolicited research or fact-checking — work only from the prompt as given, unless the user asks you to verify a specific claim.

## Handling User-Specified Direction

A specific instruction given alongside "optimize" takes priority over the general workflow — but still operates *within* the preservation rules:

- "压缩/精简" (compress/shorten) → prioritize cutting redundancy over other improvements.
- "更专业" (more professional) → prioritize tone/register, but still don't add scope.
- "适合 Claude Code" (make it suit Claude Code) → adjust phrasing/register for that context, but don't add new tools, permissions, workflows, or skills that weren't already there.
- "工程化一点" (more engineered) → structure/organize more thoroughly, but keep the functional scope identical — no new capabilities or steps.
- "不要太长" (don't make it long) → a hard constraint for this request, overriding any structural additions that would add length.

**Priority order when instructions could conflict:** the user's specific request this turn > preserving original intent > preserving core constraints > preserving technical details > language-level polish > structural polish > default style conventions.

## Output Rules

When triggered by an ordinary optimize request (not explicit invocation), output **only the optimized prompt** — no explanation, rationale, before/after, analysis, or usage tips:

```
User: 帮我优化这个提示词：<original prompt>
Skill: <optimized prompt — nothing else>
```

Deviate only when the user asks: "tell me what you changed" → add a brief note on the changes; "show me the before/after" → give an actual comparison.

**Always print the optimized prompt in full** — never truncate or elide parts with "…", "（其余不变）", "(rest unchanged)", or similar, however long it is or however little changed; the user needs the whole result to judge it.

If the input truly contains no identifiable prompt, ask for one. Otherwise make the best reasonable call rather than asking clarifying questions over minor ambiguity — excessive back-and-forth defeats the point of a lightweight editing skill.

## Apply Mode

Used on explicit invocation, or when the user explicitly asks to skip the copy-paste round trip in this same conversation ("优化完直接用" / "优化后直接应用" / "直接按这个跟我对话" / "帮我优化并立刻开始执行" / "apply it directly" / "don't make me paste it back"). Otherwise optimizing and acting stay separate jobs: hand back the text and let the user decide what to do with it.

1. First print a one-line label — `优化后提示词：` for a Chinese prompt, `Optimized prompt:` for an English one — then the full optimized prompt. Never skip this, even though you're about to use it yourself. Display only: no explanation of changes, no before/after, no request for confirmation.
2. Immediately adopt it as your own operating instructions for the rest of this conversation — as if it were a system/role prompt handed to you at the start — and respond to the user's next message (or the rest of this message, if there's a task attached) accordingly. Add no other announcement.
3. **Ask before guessing.** If carrying it out requires a decision the prompt leaves open, and a wrong guess would be costly or hard to undo (which files to change, whether to delete something, which framework or approach to use, how far the task extends), ask about those few points right after printing the prompt, and start only once the user has answered. Minor gaps with an obvious reasonable default need no question. This is how you fill gaps — optimization itself must not add content the user never wrote.

```
User: /prompt-optimizer <original prompt>
AI:   优化后提示词：
      <full optimized prompt>

      <asks about any costly unclear points first, if there are any>
      <then starts carrying out the optimized prompt>
```

A skill has no channel to another AI tool, chat window, or model — if the user's goal is to hand the prompt to a different system, tell them they'll need to copy it over themselves.

## Self-Check (internal, before finalizing — never shown to the user)

- Same goal, capability scope, and rules — nothing added that the user didn't state?
- Same constraint strength — no 可以→必须, 优先→强制, 建议→必须, 要→必须, 尽量→严格 style shifts in either direction, and no added 严格/务必/一定?
- Every technical name, tool, command, path, URL, parameter, and file name unchanged, apart from an unmistakable typo in a well-known command or tool?
- Nothing dropped except literal repetition and pure filler — every condition, exception, step, and example still present?
- No leftover redundancy, and genuinely clearer — or, if the original was already clean, left (nearly) unchanged rather than edited for its own sake?
- Not dramatically longer than the original without the user asking for elaboration?
- This turn's specific request satisfied, and the prompt printed in full?

If any answer is "no," fix it before responding.
