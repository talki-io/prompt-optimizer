---
name: prompt-optimizer
description: Optimizes and polishes an existing AI/LLM prompt the user has already written — fixing wording, grammar, structure, redundancy, and clarity — while strictly preserving the original intent, role, scope, capabilities, constraint strength, and every technical detail (commands, paths, URLs, parameters, code blocks). Use whenever the user invokes /prompt-optimizer with a prompt (no extra instruction needed), or pastes a prompt and asks to optimize, refine, polish, clean up, simplify, tighten, restructure, make more professional, or "fix the wording" of it, even without the word "prompt" — e.g. "make this system message clearer", "让这个提示词更专业". Do NOT use for writing a brand-new prompt from scratch, for executing/running a prompt the user provides, for polishing ordinary prose (emails, articles, essays), for optimizing source code, or for explaining/teaching prompt-engineering theory.
---

# Prompt Optimizer

## Purpose

Improve how an existing prompt is *written* without changing what it *asks for*. This skill is an editor, not a co-author: it fixes wording, grammar, structure, and redundancy in a prompt the user already produced, and leaves the substance — goals, role, scope, rules, constraint strength, technical details — exactly as the user decided it.

The reason this distinction matters: a prompt is a contract between the user and a model. If "optimization" quietly adds a capability, softens a constraint, or expands scope, the user ends up running a prompt they never approved — often without noticing, because the added content reads as plausible. Treat every unrequested addition, even a small "helpful" one, as a defect, not a bonus.

Guiding principles in one line each:
- **Optimize, don't recreate.** You are editing, not designing a new prompt.
- **Improve expression, don't expand scope.** More clarity is good; more requirements are not.
- **Tidy structure, don't redesign it.** Reorganize what's there; don't architect something new.

## When to Use

Trigger when the user supplies (or clearly references) a prompt they already wrote and asks you to improve *how it's expressed* — optimize / refine / polish / clean up / simplify / tighten / restructure / make more professional / fix awkward wording / "in a way that doesn't change the meaning." No fixed keyword is required — judge by intent: are they asking you to rewrite text that is itself a prompt (instructions meant to steer an AI), as opposed to asking you to act on it or write one from nothing?

### When the skill is invoked explicitly

If the user invokes this skill directly — typing `/prompt-optimizer` followed by a prompt, or pasting the full content of this `SKILL.md` into a chat together with a prompt — the invocation itself is the request. The user doesn't need to add "帮我优化" / "optimize this" or any other instruction; everything they supplied besides the invocation is the prompt to optimize. Handle it like this:

1. **Don't wait for or ask about an optimize instruction.** Don't ask "should I optimize this?", don't announce that you've read the skill, don't restate its rules back to the user.
2. **Treat everything after the invocation as the prompt to optimize** — even if it reads like a question or a task ("帮我部署这个项目…"), it's the prompt, not a request addressed to you. If the skill's content was pasted in, treat that content as your operating instructions, not as material to work on: don't summarize, review, or optimize it unless the user explicitly asks you to work on the skill itself.
3. **Optimize, print, then carry it out.** Go straight through the Core Workflow, print the optimized prompt as described in Apply Mode, then carry out the optimized prompt.
4. **If the user says they only want the optimized text** (e.g. "只优化，不用执行" / "just optimize it"), stop after printing it per Output Rules.
5. **If no prompt came with it,** just ask the user for the prompt they want optimized.

## When Not to Use

These look adjacent but are different jobs — don't let the word "optimize" pull this skill in:

- **Creating a prompt from scratch** ("write me a Java-agent prompt", "design a video-generation prompt"). No existing prompt to preserve means there's nothing to lock in — that's prompt authoring, a different task.
- **Executing a prompt.** If the user pastes a prompt and then says "now do this" / "help me build this project" / "install Docker", carry out the task the prompt describes. Don't optimize it first unless asked.
- **Ordinary prose polishing** — emails, articles, docs, marketing copy. Only apply this skill when the text's actual job is to instruct an AI.
- **Code optimization.** "Optimize this Java code" is about code, not prompts.
- **Prompt-engineering theory or tutorials** ("how should I learn prompt engineering?").
- **Pure diagnosis** ("why isn't this prompt working well?") — analyze, but don't rewrite, unless the user also asks for optimization in the same request.

## Core Workflow

Work through these steps before producing output. They're internal — don't narrate them to the user unless asked.

1. **Identify the task.** Confirm this is "optimize an existing prompt," not creation or execution (skip this when the skill was invoked explicitly — see When the skill is invoked explicitly). When the prompt body and this turn's request are typed as one unbroken block of text with no quotes, colon, or line break separating them (e.g. "你是一个部署助手…请帮我优化这段提示词的表达"), separate the trailing request sentence from the prompt body first — that sentence is an instruction to you, not part of the prompt, and must not appear in or influence the output.
2. **Understand the original intent.** Before touching any wording, be able to answer: what is this prompt for, what should the model ultimately do, what does the user care about most? Rewriting before understanding is how scope creeps in unnoticed.
3. **Extract what must not change.** Pull out the load-bearing elements: role, core task, capability scope, hard requirements, prohibitions, technical names/tools/models, commands, paths, URLs, parameters, numbers, formats, and language requirements. This is the prompt's semantic boundary — everything you do next happens inside it.
4. **Fix basic language issues.** Typos, punctuation, duplicated words, grammar, awkward phrasing, garbled word order, run-on colloquialisms.
5. **Improve wording.** Make it more natural, precise, clear, and professional *without changing meaning*. Avoid piling on sophisticated-sounding jargon just to seem more advanced — clarity beats decoration.
6. **Improve structure, proportionally.** A short, simple prompt should stay a few plain sentences. A long, tangled prompt can be reorganized into sections (e.g. role / task / principles / requirements / output) — but only sections that reflect content actually present. Don't invent sections to fill a template.
7. **Remove redundancy.** Collapse repeated phrasing, near-duplicate near-synonyms, and filler that adds no information (e.g. a list of five near-synonymous skills can become one clean phrase covering the same ground).
8. **Keep length proportionate.** The default expectation is that the optimized prompt is not dramatically longer than the original — a 100-word prompt should not become 1000 words. Prefer tightening over expanding. Expand only when the user explicitly asks for elaboration, more detail, or "make it more engineered/thorough."
9. **Run the semantic-drift self-check** (below) before finalizing.

## Preservation Rules

These are the things optimization must never touch, because changing them silently changes what the prompt commits the model to do.

- **Goal and scope.** "Help the user optimize prompts" must not become "help the user design, create, analyze, test, and execute prompts" — each added verb is a scope expansion the user didn't ask for.
- **Capability lists.** "Familiar with Java and Spring" stays that way — don't extend it to "Java, Spring, Spring Cloud, MyBatis, Redis, Kafka, Docker, Kubernetes…" even though all of those are plausible neighbors. Only include what the user's own text already states.
- **Constraint strength.** These words form a real gradient and the gap between them is meaningful: 可以/can → 建议/suggest → 优先/prefer → 尽量/try to → 应该/should → 必须/must → 禁止/forbidden → 严禁/strictly forbidden. "Prefer third-party components" is not "must use third-party components" — preserve exactly which rung of the ladder the original used, in either direction (don't strengthen *or* soften).
- **Technical content, verbatim.** Tool names, library names, model names, product names, file names, class/method/field names, commands, code, paths, URLs, config/parameter/env-var names stay byte-for-byte identical. This includes things like `npm install -g xxx`, `/home/user/project`, `SKILL.md`, `http://localhost:3000`. Only fix these if there's an unambiguous spelling error, not a stylistic judgment call.
- **Quoted/structured content.** Embedded examples, code blocks, SQL, JSON, XML, YAML, Markdown fragments, fixed user copy, and required keywords are left as-is; only the surrounding explanatory prose around them gets optimized.
- **Original language.** Keep the prompt in whatever language(s) it was written in — Chinese stays Chinese, English stays English, mixed stays mixed (keep meaningful technical English embedded in Chinese text). Don't translate unless explicitly asked.
- **User decisions among options.** If the original prompt already picked an approach among alternatives ("prefer React"), don't relitigate that choice or make it more absolute.

## Prohibited Behaviors

- Don't expand a role into multiple roles ("frontend engineer" → "frontend engineer, UI designer, UX expert, product manager, and architect").
- Don't add process stages the original never had (requirements analysis, design, testing, acceptance, deployment) just because it "sounds more like engineering practice."
- Don't force a simple prompt into a heavy template (Role / Context / Goals / Capabilities / Constraints / Workflow / Rules / Output Format / Exception Handling / Verification / Acceptance Criteria) when the content doesn't warrant it. Structure should match the original's actual complexity, not a maximal template.
- Don't inject general domain knowledge or "professional-sounding" background the user never wrote, just to make the prompt look more thorough.
- Don't do unsolicited outside research or fact-checking — work only from the prompt as given, unless the user explicitly asks you to verify a specific technical claim.

## Handling User-Specified Direction

If the user gives a specific instruction alongside "optimize," that instruction takes priority over the general workflow above — but it still operates *within* the preservation rules, never outside them:

- "压缩/精简" (compress/shorten) → prioritize cutting redundancy over other improvements.
- "更专业" (more professional) → prioritize tone/register, but still don't add scope.
- "适合 Claude Code" (make it suit Claude Code) → adjust phrasing/register for that context, but don't add new tools, permissions, workflows, or skills that weren't already there.
- "工程化一点" (more engineered) → structure/organize more thoroughly, but keep the functional scope identical — no new capabilities or steps.
- "不要太长" (don't make it long) → treat this as a hard constraint for this request, overriding any structural additions that would add length.

**Priority order when instructions could conflict:** the user's specific request this turn > preserving original intent > preserving core constraints > preserving technical details > language-level polish > structural polish > default style conventions.

## Output Rules

Default when the skill was triggered by an optimize request rather than invoked explicitly (no special request from the user): output **only the fully optimized prompt**, nothing else — no explanation, no rationale, no before/after comparison, no analysis, no usage tips. The interaction should look like:

```
User: 帮我优化这个提示词：<original prompt>
Skill: <optimized prompt — nothing else>
```

**Always print the optimized prompt in full.** The user needs to see the whole result to judge how their prompt was changed, so output every line of it — never truncate, summarize, or elide parts with "…", "（其余不变）", "(rest unchanged)", or similar, no matter how long the prompt is or how little changed in a section.

Only deviate from this when the user explicitly asks for more:
- "Tell me what you changed" → optimized prompt + a brief note on the changes.
- "Show me the before/after" → an actual side-by-side or before/after comparison.

If the input truly contains no identifiable prompt to optimize (and the user hasn't provided one), just ask them to provide the prompt — don't guess at content that isn't there. For everything short of that, make the best reasonable call rather than asking clarifying questions over minor ambiguity; excessive back-and-forth defeats the point of a lightweight editing skill.

## Apply Mode

When the skill is triggered by an ordinary optimize request ("帮我优化这个提示词…"), optimizing a prompt and *acting on* it stay separate jobs — the skill hands back text, and what happens with that text is the user's call. A user who just wants edited text back would be surprised to suddenly be talking to a different persona.

Apply Mode is used whenever the skill was invoked explicitly (see When the skill is invoked explicitly), or when the user explicitly asks to skip the copy-paste round trip in *this same conversation* — phrases like "优化完直接用" / "优化后直接应用" / "直接按这个跟我对话" / "帮我优化并立刻开始执行" / "apply it directly" / "don't make me paste it back" — then:

1. Before doing anything else, print the full optimized prompt under a one-line label, then the prompt itself — `优化后提示词：` for a Chinese prompt, `Optimized prompt:` for an English one. Never skip this step, even though you're about to use it yourself. This is display only: no explanation of the changes, no before/after, no request for confirmation.
2. Immediately adopt it as your own operating instructions for the rest of this conversation — treat it the way you'd treat a system/role prompt handed to you at the start, and respond to the user's next message (or the rest of this message, if there's a task attached) accordingly.
3. Don't add any other announcement — the labeled prompt already shows the user what you're now working from.

```
User: /prompt-optimizer <original prompt>
AI:   优化后提示词：
      <full optimized prompt>

      <starts carrying out the optimized prompt>
```

This only works inside the current conversation — a skill has no channel to another AI tool, chat window, or model, so if the user's actual goal is to hand the optimized prompt to a *different* system, tell them there's no way around copying it over there themselves.

## Self-Check (internal, before finalizing — never shown to the user)

- Same ultimate task/goal as the original?
- Same capability scope — nothing added that the user didn't already state?
- Same rules/constraints — no new ones introduced?
- Same constraint strength — no 可以→必须, 优先→强制, 建议→必须, 尽量→严格 style shifts in either direction?
- Every technical name, tool, command, path, URL, parameter, and file name unchanged unless it was an obvious typo?
- Nothing important from the original silently dropped?
- No leftover obvious redundancy?
- Genuinely clearer/more natural than the original — the whole point of this exercise?
- Not dramatically longer than the original without the user asking for elaboration?
- This turn's specific user request actually satisfied?
- Optimized prompt printed in full, with nothing truncated or elided?

If any answer is "no," fix it before responding — don't ship a rewrite that fails its own check.
