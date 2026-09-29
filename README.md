# prompt-optimizer

An [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) that optimizes and polishes an **existing** AI/LLM prompt — without changing what it asks for.

> **Optimize, don't recreate. Improve expression, don't expand scope. Tidy structure, don't redesign it.**

## What it does

Point it at a prompt you've already written and ask to optimize / refine / polish / simplify / restructure / make more professional. It fixes wording, grammar, redundancy, and structure, while strictly preserving:

- the original goal, role, and scope
- the capability list (it will not add tools/technologies you didn't mention)
- constraint strength (可以/can → 建议/suggest → 优先/prefer → 尽量/try to → 应该/should → 必须/must → 禁止/forbidden → 严禁/strictly forbidden — it will not silently strengthen or soften these)
- every technical detail verbatim: commands, paths, URLs, parameters, file names, code blocks, model/tool names (only an unmistakable typo in a well-known command or tool gets fixed)
- the original language (Chinese stays Chinese, English stays English, mixed stays mixed)

When you invoke it with `/prompt-optimizer`, it prints the optimized prompt and then carries it out (see [Usage](#usage)). When it is triggered by an ordinary "optimize this prompt" request instead, it outputs **only the optimized prompt**. Either way it doesn't explain its edits, show a before/after or add analysis unless you ask for one, and the prompt is always printed in full, never truncated or shortened with "(rest unchanged)", so you can see exactly what it became.

It deliberately does **not** trigger for: writing a new prompt from scratch, merely running a prompt you provide without asking to optimize it, polishing ordinary prose (emails/articles), optimizing source code, or explaining prompt-engineering theory. See the "When Not to Use" section in `SKILL.md` for the full boundary.

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

**Codex / other Agent Skills-compatible tools:** put `SKILL.md` at `<skills-dir>/prompt-optimizer/SKILL.md` in whatever skills directory that tool discovers — the file itself is platform-neutral.

**No install (any chat AI):** paste the full content of `SKILL.md` into the chat together with the prompt you want optimized (no "帮我优化" needed). It then behaves the same as `/prompt-optimizer` below.

## Usage

Invoke the skill with `/prompt-optimizer` followed by your prompt — no need to add "帮我优化" / "optimize this". Claude optimizes the prompt, prints it as `优化后提示词：<full optimized prompt>` (or `Optimized prompt:` for an English prompt), and then carries it out. If the prompt leaves open something where a wrong guess would be costly (which files to change, whether to delete something, which approach to use), Claude asks you about it before starting. Add "只优化，不用执行" (just optimize it) if you only want the text back.

```
You: /prompt-optimizer 你是一名专业提示词优化大师，熟悉各种提示词优化，书写，你主要任务是协助用户完成提示词优化工作

Claude: 优化后提示词：
你是一名专业的提示词优化大师，熟悉各类提示词的优化与撰写，主要任务是协助用户完成提示词优化工作。

（随后按这个角色回应你的下一条消息）
```

Remarks addressed to the AI rather than part of the prompt — "只优化，不用执行", "帮我优化一下", "以上是我的想法，交给你执行" — are followed, not optimized into the result:

```
You: /prompt-optimizer 你是一名资深运维工程师，帮我检查服务器上nginx的配置有没有问题，有问题就告诉我怎么改。以上是我的想法，具体执行交给你做

Claude: 优化后提示词：
你是一名资深运维工程师。请检查服务器上的 nginx 配置是否存在问题；如有问题，请告诉我应如何修改。

（接着开始检查 nginx 配置）
```

When a wrong guess would be costly, Claude asks first and waits for your answer:

```
You: /prompt-optimizer 给我的网站项目加一个用户登陆功能，要好看一点

Claude: 优化后提示词：
为我的网站项目添加用户登录功能，要美观一些。

开始之前，有几点需要先确认。如果我猜错了，返工的成本会比较高：

1. 登录方式：用账号（用户名或邮箱）加密码，还是用手机验证码，或者用第三方登录（如微信、GitHub、Google）？
2. 功能范围：只做登录，还是连注册、找回密码、退出登录一起做？
3. 后端认证：项目里已经有用户系统或登录接口了吗？如果没有，要我一并实现后端吗？还是先只做前端页面？

You: 账号密码登录，连注册一起做，后端也要

Claude: （先查看项目的技术栈和现有代码结构，再按你的回答开始实现）
```

```
You (without invoking the skill): Optimize this prompt: "you are helpful assistant that help user write code and also fix bug and also explain things good"

Claude: You are a helpful assistant that helps users write code, fix bugs, and explain things clearly.
```

Constraint strength and technical details stay exactly as written — "优先" stays "优先", "尽量" stays "尽量", "禁止" stays "禁止". An unmistakable typo in a well-known command is fixed (`npm isntall` → `npm install`), but file names, paths and identifiers are never "corrected" (`recieve_handler.js` is kept as is, since that may be its real name):

```
You: 帮我优化这个提示词：你是前端工程师，熟悉vue和react，写代码时优先使用第三方组件库，尽量不要自己造轮子，禁止使用jquery

Claude: 你是一名前端工程师，熟悉 vue 和 react。编写代码时，优先使用第三方组件库，尽量不要自己造轮子；禁止使用 jquery。
```

```
You: 帮我优化这个提示词：你是部署助手，先执行 npm isntall 安装依赖，然后读取 src/utils/recieve_handler.js 里的配置，把服务部署到 http://localhost:3000

Claude: 你是一名部署助手。请先执行 `npm install` 安装依赖，然后读取 `src/utils/recieve_handler.js` 中的配置，并将服务部署到 `http://localhost:3000`。
```

Shortening only removes repetition and filler — every condition, exception, fallback and example survives:

```
You: 帮我精简一下这个提示词：你是一个写周报的助手，你的任务就是帮我写周报，就是把我每天做的事情整理成周报。如果我没有提供某天的内容，就直接跳过那天，不要自己编。除非我特别说明，否则周报都用中文写。写的时候按照 周一 到 周五 的顺序排。例如：周一：完成登录模块联调。不确定的地方先问我。

Claude: 你是一个周报写作助手，负责把我每天做的事情整理成周报。

- 如果我没有提供某天的内容，直接跳过那天，不要自己编造。
- 除非我特别说明，否则周报一律用中文写。
- 按周一到周五的顺序排列，例如：周一：完成登录模块联调。
- 遇到不确定的地方，先问我。
```

A prompt that is already clean comes back (nearly) unchanged rather than rewritten for its own sake.

Want to know what changed? Just ask: "tell me what you changed" or "give me a before/after comparison" — by default the skill stays silent about its edits and just returns the result.

When the skill is triggered by an ordinary "optimize this prompt" request instead of `/prompt-optimizer`, you get the optimized text back and decide what to do with it. If you want to skip the copy-paste round trip and have Claude immediately start operating under the optimized prompt in the same conversation (it works the same as `/prompt-optimizer`), say so explicitly — e.g. "优化完直接用" / "apply it directly, don't make me paste it back". This only works within the current conversation; a skill has no way to push text into a different chat window or model.

## Design principles

This skill was built to solve a specific failure mode of naive "prompt optimization": an LLM asked to "optimize" a prompt tends to *expand* it — adding capabilities, softening or hardening constraints, inventing process steps, and turning a three-line prompt into a ten-section template. That's prompt *creation* wearing the costume of prompt *editing*, and it quietly changes what the user is committing their AI to do.

`SKILL.md` counters this with an explicit preservation boundary (goal / capability scope / constraint strength / technical content / language) and a self-check the model runs before returning output, rather than relying on the model to intuit restraint on its own.

See `SKILL.md` for the full ruleset — it's the single source of truth and is meant to be read directly.

## License

MIT — see [LICENSE](LICENSE).
