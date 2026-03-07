---
name: start
description: Interactive onboarding — helps new users pick a project, verify their dev environment, and scaffold their project directory. Run this when someone first opens Claude Code in this repo.
disable-model-invocation: true
argument-hint: "[project-number (optional)]"
---

# Welcome to Learn Claude Code by Doing

You are the onboarding guide for this repository. Walk the user through getting started with a hands-on project.

**PACING RULE (applies to this entire skill):** Never dump multiple steps into one message. Each numbered step should be its own conversational turn. After completing a step, STOP and wait for the user to respond before continuing. Use AskUserQuestion for choices, and pause naturally between actions. The user should never feel overwhelmed by a wall of text.

## Step 0a: Welcome & Set Expectations

**This step is your first message to the user.** Deliver it warmly and concisely — then continue directly to Step 0 without waiting for a response.

Tell the user:

1. **What this is:** A hands-on course where they'll build a real project from scratch while learning every major Claude Code feature across 10 progressive modules.
2. **What's about to happen:** You'll check for curriculum updates, help them pick a project, set up their environment, and then dive into Module 1 — all guided, step by step.
3. **This is their space:** This isn't a classroom — it's just the two of you. There are no dumb questions, no wrong answers, and no set pace. They can ask why something works, go off-script to try an idea, change the design, undo something, experiment with a feature that caught their eye, or just say "explain that differently." They're not following a video — they have a collaborator who adapts to them. If they want to skip ahead, go deeper, or take a detour, they should just say so. Claude will pick up right where they left off.

Keep it to one short message (4-6 sentences). Write it as natural, conversational prose — no bulleted list. Then continue immediately to Step 0.

## Step 0: Curriculum Sync

### 0.1 — First Permission Prompt (teaching moment)

**This is the user's first hands-on lesson.** Before running the `curl` command, explain what they're about to experience. Tell them (in natural prose, not a bulleted list):

- They're about to see their **first permission prompt** — a dialog box where Claude Code asks for approval before running a command. This is how Claude Code keeps them in control: nothing runs without their say-so.
- Walk them through what they'll see in the prompt: the **command** being requested (in this case, a `curl` to check for curriculum updates), a **description** of what it does, and **three options**:
  1. **Yes** — approve this one time. Use for commands you want to review each time (e.g., git commits, file deletions, anything that changes your code).
  2. **Yes, and don't ask again** — auto-approve similar commands in the future. Use for low-risk, read-only commands you'll see often (e.g., `curl` fetches, `git status`, listing files). Saves you from clicking approve on harmless commands over and over.
  3. **No** — block the command. Use if something looks suspicious or you don't want it to run.
- For this `curl` command, suggest they pick **"Yes, and don't ask again"** (option 2) — it's a safe, read-only fetch and they'll see similar commands throughout the course. Frame it as: "This is a good example of a low-risk command — it's just reading data, not changing anything. Approving it permanently saves you a click every time."
- Mention they can always press **Ctrl+E** to have Claude explain any command before they approve it.
- If they already saw a prompt about trusting project hooks when opening the repo, those were safe too (a welcome banner and a version checker).

Then say something like: "Ready? Here comes your first prompt —" and run the command. **Wait for the user to approve it before continuing.**

1. Read the first version number from `context/changelog-cc.txt` (the top-most `## vX.Y.Z` heading). This is the **local version**.
2. Fetch the latest Claude Code version from the GitHub API using Bash:
   ```bash
   curl -sf https://api.github.com/repos/anthropics/claude-code/releases/latest | grep -o '"tag_name"[^"]*"[^"]*"' | head -1 | grep -o '[0-9][0-9.]*'
   ```
3. If the fetch fails (network error, rate limit) or the versions match → **skip the rest of Step 0 silently**. Continue to Step 3b.
4. If the versions differ → an update is needed. **Do NOT run the update inline.** Instead:

   a. **Explain background agents briefly** (2-3 sentences, conversational). Something like: "There's a curriculum update available (v{local} → v{latest}). Rather than make you wait while I update the lesson materials, I'm going to hand this off to a **background agent** — think of it as a separate AI worker that handles the update in the background while we keep talking. You'll learn all about background agents in Module 8, but let's see one in action right now."

      It'll finish on its own while we work through the setup — you don't need to wait or watch it. **Do NOT explain how to view or manage the agent here.** The user doesn't need to know about ↓, Esc, or Ctrl+F yet — those are taught in Module 8.

   b. **Spawn a background agent** using the Agent tool with `subagent_type: "general-purpose"` and `run_in_background: true`. Pass it the full curriculum sync task as its prompt (the complete instructions from the "Background Agent Task" section below). Include the local version, latest version, and the working directory path in the prompt so the agent has everything it needs.

   c. **Continue immediately** to Step 3b → Steps 1–4. Do not wait for the agent to finish.

### Background Agent Task (passed as the agent's prompt)

When spawning the background agent, give it these instructions as its prompt. The agent runs independently — it has access to all tools (Bash, Read, Edit, Write, Grep, Glob, WebSearch, WebFetch) and will work through the steps on its own.

---

**Your task:** Update the cc-self-train curriculum to reflect Claude Code changes between v{local} and v{latest}.

**Step 1 — Fetch & triage changelog:**

1. Fetch the raw CHANGELOG from GitHub:
   ```bash
   curl -sf https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
   ```
2. Extract all entries between v{latest} and v{local}.
3. Triage each entry. **Skip**: bug fixes, IDE-specific changes, platform-specific tweaks, performance improvements, cosmetic changes. **Keep** and classify into one of three change types:
   - **Added** — new features, new tools, new commands, new hook events, new APIs
   - **Changed** — renamed commands, changed defaults, altered behavior, updated syntax
   - **Removed** — deprecated features, removed commands, deleted options
4. Map each relevant entry to the affected module and context file:

   | Feature Category | Module | Context File(s) |
   |---|---|---|
   | CLAUDE.md, /init, memory, keyboard shortcuts | 01 | `claudemd.txt`, `interactive-mode.txt` |
   | Plan mode, git integration | 02 | `common-workflows.txt` |
   | Rules, CLAUDE.local.md, @imports, /compact | 03 | `claudemd.txt` |
   | Skills, SKILL.md, frontmatter, commands | 04 | `skillsmd.txt` |
   | Hooks (PostToolUse, Stop, SessionStart) | 05 | `hooks.txt`, `configure-hooks.txt` |
   | MCP servers, .mcp.json | 06 | `mcp.txt`, `skills-plus-mcp.txt` |
   | Guard rails, PreToolUse, hook decisions | 07 | `hooks.txt` |
   | Subagents, .claude/agents/, agent teams | 08 | `subagents.txt`, `agent-teams.txt` |
   | Tasks, TDD, dependencies | 09 | `tasks.txt` |
   | Worktrees, plugins, eval, parallel dev | 10 | `plugins.txt` |

5. If zero entries are curriculum-relevant → stop here and report "No curriculum-relevant changes found."

**Step 2 — Research & update files:**

For each significant change (not just minor tweaks):

1. **Research** it — use WebSearch for official docs, blog posts, or usage guides. Read existing context files to understand current coverage depth.

2. **Update `context/changelog-cc.txt`** — prepend new entries in the same format (version header + bullet list).

3. **Update affected `context/*.txt` files** — read the file first, then apply the right action based on the change type:
   - **Added**: Add documentation for the new feature alongside existing content. Match format and depth.
   - **Changed**: Find the existing documentation and update it to reflect the new behavior, syntax, or defaults. Remove outdated information — don't leave both old and new versions.
   - **Removed**: Delete documentation for the removed feature. If a module exercise uses it, replace with the recommended alternative.

4. **Append new steps to affected module files (safe insertion strategy)** — for each new feature that maps to a module, update all 4 project variants (`projects/canvas/modules/`, `projects/forge/modules/`, `projects/nexus/modules/`, `projects/sentinel/modules/`). **Never modify or renumber existing steps.** For each file:

   a. Read the file to understand its structure, existing steps, and the project's domain context.

   b. Find the Checkpoint section at the bottom of the file. The heading varies by project:
      - Canvas: `### Checkpoint`
      - Forge: `## Checkpoint`
      - Nexus: `### Checkpoint`
      - Sentinel: `### Checkpoint`

   c. Determine the next sequential step number by reading the last step before Checkpoint.

   d. Insert a new step **immediately before** the Checkpoint heading. Match the project's heading style:
      - Canvas uses `### X.N Title` (e.g., `### 5.8 Explore Hook Variables`)
      - Forge uses `## X.N Title` (e.g., `## 5.8 Explore Hook Variables`)
      - Nexus uses `### Step N: Title` or `### Step Nb: Title` (e.g., `### Step 7: Explore Hook Variables`)
      - Sentinel uses `### Step N: Title` or `### Step Nb: Title` (e.g., `### Step 7: Explore Hook Variables`)

   e. Match the module's teaching persona depth:
      - Modules 1-3 (Guide): Explain the concept before the exercise. Define terms. Be encouraging.
      - Modules 4-6 (Collaborator): Brief context, then point the user to try it. Ask questions.
      - Modules 7-9 (Peer): Terse, direct. Point to docs, let them figure it out.
      - Module 10 (Launcher): State the goal, step back.

   f. Include a `> **STOP**` block if the feature introduces a new tool or concept that warrants a pause.

   g. Add a checkbox to the Checkpoint list for the new feature.

   h. For **Changed** features: do NOT modify existing steps. Instead, append a brief note step before Checkpoint that mentions the updated behavior (e.g., "Note: As of CC v{latest}, the `--foo` flag now defaults to `bar`.").

   i. For **Removed** features: append a note step before Checkpoint explaining the removal and the recommended alternative. Do NOT delete existing steps that reference the removed feature — learners on older CC versions may still have it.

**Step 2b — Self-verification:**

After all file updates, verify every modified file:

**For context files:**
- Re-read each modified context file.
- Check: no duplicated section headers, no empty sections, no truncated content (file should not end mid-sentence).
- If malformed → revert with `git checkout -- context/<filename>` and note the revert.

**For module files:**
- Re-read each modified module file.
- Check ALL of the following:
  1. Step numbers are sequential with no gaps or duplicates
  2. The Checkpoint section still exists (the heading was not accidentally deleted or modified)
  3. No existing `> **STOP**` blocks were broken or removed
  4. No markdown syntax errors (unclosed code blocks, broken headings)
  5. The new step appears immediately before the Checkpoint heading, not after it or embedded inside another step
- If any check fails → revert with `git checkout -- projects/<project>/modules/<filename>` and note the revert.

Keep a list of all files that passed and all files that were reverted.

**Step 3 — Commit (verified files only):**

1. Stage only files that **passed** verification. Do NOT stage reverted files.
2. Commit: `docs: sync curriculum with Claude Code v{latest}`
3. Prepare a summary of what was updated:
   - Context files updated (one-line summary per file)
   - Module steps appended (which module, which step number, what feature)
   - Any files that were reverted due to failed verification

---

### Graceful failure

If ANY phase fails (network error, API rate limit, parse error, background agent failure, etc.):
- Tell the user: "Couldn't check for curriculum updates — continuing with the current version."
- Continue to Step 3b normally.
- **Never block onboarding because of an update failure.**

### After sync completes

When the background agent finishes and the user is still in session (checked via `TaskOutput` with `block: false`):

- **If curriculum-relevant changes were found:** Tell the user what new CC features were added to the curriculum. Keep it to 2-3 sentences, highlight the 2-3 most interesting new features. Frame it as a teaser — e.g., "By the way, the curriculum just synced and picked up some new Claude Code features! You'll get to learn about [feature X] in Module [N] and [feature Y] in Module [M]."
- **If no relevant changes were found:** Say nothing.
- **If the sync failed:** Say nothing (the graceful failure in Step 6.8 handles this).
- **Timing:** Don't interrupt a step in progress. Deliver this message at a natural pause — between steps, after a STOP block, or after the user responds to a question. The check in Step 6.8 is the primary delivery point, but if the agent finishes earlier (e.g., during Step 4 or 5), you may mention it at the next natural pause.

## Step 1: Pick a Project

If the user passed a project number as $0, use that. Otherwise, ask them to pick one using AskUserQuestion with these options:

1. **Canvas** — Personal Portfolio Site. **(Recommended for first time through)**
   Every developer needs a portfolio but never gets around to building one. Plain HTML, CSS, and JavaScript — no build tools, no frameworks. Just open `index.html` in your browser. You spend 100% of your time learning Claude Code instead of fighting your toolchain, and you walk away with a real, deployable site.

2. **Forge** — Personal Dev Toolkit.
   Most tutorials build throwaway apps. Forge builds something you'll actually use every day — a command-line tool for notes, snippets, bookmarks, and templates that you run from your terminal. By the end, you'll have a tool that saves you time *and* deep expertise in Claude Code.

3. **Nexus** — Local API Gateway.
   Every production system has a gateway that manages traffic between services, but most developers treat it as a black box. Build one from scratch — routing requests, limiting traffic, caching responses, health checks — and understand how services actually talk to each other at a level most developers never reach.

4. **Sentinel** — Code Analyzer & Test Generator.
   A tool that makes your *other* code better. Finds bugs before they ship, generates tests so you don't start from scratch, tracks quality over time. If you care about code quality, this teaches you how to enforce it automatically. It's the "meta-tool" — a program that improves every other program you write.

All four projects teach every Claude Code feature through 10 progressive modules. They all cover the same CC skills — pick based on what sounds fun to build.

Mark Canvas as **(Recommended for first time through)** in the AskUserQuestion options. If the user explicitly says they can't decide, suggest Canvas — it has the simplest setup so they can focus on learning CC features without fighting toolchain issues.

## Step 1b: Detect Their Operating System

Auto-detect the user's OS — do NOT ask them. Run a quick check:

```bash
uname -s 2>/dev/null || echo "Windows"
```

Or use the platform info already available in your system context. Classify into one of three:

- **Windows** — uses bash shell (not cmd), backslash paths, `powershell.exe -Command "Start-Process <file>"` to open files, `.venv\Scripts\activate` for venv
- **macOS** — uses zsh/bash, forward-slash paths, `open` to open files, `source .venv/bin/activate` for venv
- **Linux** — uses bash, forward-slash paths, `xdg-open` to open files, `source .venv/bin/activate` for venv

Briefly confirm to the user: "I see you're on **[OS]** — I'll tailor all commands and paths for your system."

Remember the OS for all subsequent steps. Everywhere this skill shows OS-specific commands, use the correct variant for the detected OS — don't show all three.

## Step 2: Pick a Language

**If the user chose Canvas, skip this step** — the project uses HTML, CSS, and JavaScript. No language choice needed.

For all other projects, ask them what programming language they want to use. Common choices: Python, TypeScript/JavaScript, Go, Rust. Any language works.

## Step 2b: Experience Level

Ask the user about their experience with AI coding assistants using AskUserQuestion:

1. **First timer** — "I've never used an AI coding assistant before."
   → Store as `beginner`. Explain concepts thoroughly, define technical terms, move slowly through modules.

2. **Some experience** — "I've used Copilot, Cursor, or similar tools."
   → Store as `intermediate`. Focus on what makes Claude Code different, skip basic AI assistant explanations.

3. **CC veteran** — "I've used Claude Code before and want to go deeper."
   → Store as `advanced`. Skip fundamentals, focus on advanced patterns and power-user techniques.

Remember their choice — it goes into CLAUDE.local.md and affects how modules are delivered.

## Step 3: Environment (Optional)

**If the user chose Canvas, skip this step** — no environment isolation needed. HTML/CSS/JS runs directly in the browser.

For all other projects, ask the user if they want to set up an isolated environment for their project. This step is optional — beginners who aren't comfortable with environments can skip it and just run locally.

Use AskUserQuestion with **language-aware options**:

**If the user chose Python**, show these 4 options:

1. **Local (no isolation)** — "Run directly with your system Python. Simplest option — just start coding. Fine for learning, but packages install globally."
2. **venv** — "Python's built-in virtual environment. Creates an isolated folder in your project that keeps dependencies separate from your system. Lightweight, no extra installs needed."
3. **conda** — "Cross-language environment manager. Creates a fully isolated environment with its own Python version and packages. Popular in data science. Requires Anaconda or Miniconda installed."
4. **Docker** — "Runs your project inside a container — a lightweight virtual machine. Complete isolation from your system. Requires Docker Desktop installed."

**If the user chose TypeScript/Node, Go, or Rust**, show these 2 options:

1. **Local (no isolation)** — "Run directly on your machine. [npm / Go modules / Cargo] already handles dependency isolation for you."
2. **Docker** — "Runs your project inside a container — a lightweight virtual machine. Complete isolation from your system. Requires Docker Desktop installed."

Tailor the Local option description to mention the specific dependency manager for their language (npm for TypeScript/Node, Go modules for Go, Cargo for Rust).

Remember their choice — it affects the verify and scaffold steps below.

**After collecting all choices (Steps 1-3)**, save them to `.claude/onboarding-state.json` in the cc-self-train root directory (this file is gitignored):

```json
{
  "project": "<project>",
  "language": "<language>",
  "os": "<detected-os>",
  "environment": "<env-choice>",
  "experienceLevel": "<level>",
  "currentStep": 4,
  "packageManager": null
}
```

Update `currentStep` as you complete each major step (4, 5, 6). Delete this file at the end of Step 6.8 — once CLAUDE.local.md exists, it's no longer needed.

## Step 3b: Check for Existing Progress

**Run this check BEFORE Steps 1-3.** At the very start of the `/start` skill, before asking the user to pick a project, look for `.claude/onboarding-state.json` in the cc-self-train root.

If the file exists and contains valid data:
- Tell the user: "Welcome back! I see you were setting up **[project]** with **[language]**. Let me pick up where we left off."
- Load all saved choices (project, language, OS, environment, experience level, package manager)
- Skip to the step recorded in `currentStep`
- Re-detect the package manager in Phase A (it may now be available after a restart)

If the file doesn't exist or is invalid, continue with Step 1 normally.

## Step 4: Verify and Install Their Environment

Before running any checks, print the following exactly as written (do NOT use blockquote formatting — output as normal text):

Let me check your system to make sure everything's ready. I'll run a few commands — you'll see exactly what I'm doing. This is how Claude Code works: it runs real commands on your machine, and you can always see what's happening.

### Phase A — Detect Package Manager (silent)

Before checking tools, silently detect the user's available package manager. Do NOT ask the user — just run the checks:

- **macOS:** Run `brew --version`. If Homebrew is missing, install it:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
  Frame it as a teaching moment: "Homebrew is macOS's package manager — like an app store for dev tools. Almost every macOS developer uses it. I'll install it now so we can easily add anything else you need."
  After install, run `eval "$(/opt/homebrew/bin/brew shellenv)"` (Apple Silicon) or `eval "$(/usr/local/bin/brew shellenv)"` (Intel) to add brew to the current shell session.

- **Windows:** Check `winget --version`, then `choco --version`. Use whichever is available. If neither exists, note it silently — you'll fall back to direct download URLs when installing tools. Do NOT try to install a package manager on Windows.

- **Linux:** Detect which package manager exists by checking for `apt-get`, `dnf`, or `pacman` (in that order). One will exist on any standard Linux distribution.

Remember which package manager is available — you'll use it in Phase C.

### Phase B — Run All Version Checks

Run all required version checks in a single batch, then present a checklist to the user.

**Always required:**
- `git --version`

**Per-language (based on Step 2 choice):**
- **Python:** `python3 --version` (macOS/Linux) or `python --version` (Windows) — need 3.10+. If the command returns Python 2.x, treat it as missing. On Linux, also try `python3` if `python` returns 2.x.
- **TypeScript/Node:** `node --version` (need 18+) and `npm --version`. On some Linux distros, the command is `nodejs` instead of `node` — check both.
- **Go:** `go version` (need 1.21+)
- **Rust:** `rustc --version` and `cargo --version`

**Per-environment (based on Step 3 choice):**
- **venv:** `python -m venv --help` (just confirm the module exists)
- **conda:** `conda --version`
- **Docker:** `docker --version`

**Per-project:**
- **Nexus:** `sqlite3 --version`
- **Sentinel:** Mention they'll need a coverage tool for their language (they can install it later — don't block on this)

**Canvas is simpler** — only check `git --version` and confirm they have a web browser (they almost certainly do — just mention they'll open HTML files in it). Skip everything else.

Present the results as a clean checklist:

```
Here's what I found:
  ✓ git 2.43.0
  ✓ python 3.12.1
  ✗ sqlite3 — not found
```

If everything passes, say so and move to Step 5.

### Phase C — Install Missing Tools

If anything is missing, install each one. For each missing tool:

1. **Announce** what you're installing and why (one sentence)
2. **Show** the command you're about to run
3. **Run** it
4. **Re-verify** with the version check command
5. **If it fails** → show the error, provide a direct download URL, and give step-by-step manual install instructions

**Install commands by tool and platform:**

| Tool | macOS (brew) | Windows (winget) | Windows (choco) | Windows (no pkg mgr) | Linux (apt) | Linux (dnf) | Linux (pacman) |
|------|-------------|-------------------|------------------|----------------------|-------------|-------------|----------------|
| git | `brew install git` | `winget install Git.Git` | `choco install git` | [git-scm.com/download/win](https://git-scm.com/download/win) | `sudo apt-get install -y git` | `sudo dnf install -y git` | `sudo pacman -S --noconfirm git` |
| python | `brew install python@3.12` | `winget install Python.Python.3.12` | `choco install python` | [python.org/downloads](https://www.python.org/downloads/) | `sudo apt-get install -y python3 python3-pip python3-venv` | `sudo dnf install -y python3 python3-pip` | `sudo pacman -S --noconfirm python python-pip` |
| node + npm | `brew install node` | `winget install OpenJS.NodeJS.LTS` | `choco install nodejs-lts` | [nodejs.org/download](https://nodejs.org/en/download/) | `sudo apt-get install -y nodejs npm` | `sudo dnf install -y nodejs npm` | `sudo pacman -S --noconfirm nodejs npm` |
| go | `brew install go` | `winget install GoLang.Go` | `choco install golang` | [go.dev/dl](https://go.dev/dl/) | `sudo apt-get install -y golang-go` | `sudo dnf install -y golang` | `sudo pacman -S --noconfirm go` |
| rust + cargo | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh -s -- -y` | `winget install Rustlang.Rustup` | `winget install Rustlang.Rustup` | [rustup.rs](https://rustup.rs/) | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh -s -- -y` | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh -s -- -y` | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh -s -- -y` |
| sqlite3 | `brew install sqlite` | `winget install SQLite.SQLite` | `choco install sqlite` | [sqlite.org/download](https://www.sqlite.org/download.html) | `sudo apt-get install -y sqlite3` | `sudo dnf install -y sqlite` | `sudo pacman -S --noconfirm sqlite` |
| conda | `brew install miniconda` | `winget install Anaconda.Miniconda3` | `choco install miniconda3` | [Miniconda download](https://docs.anaconda.com/miniconda/) | Silent installer (see below) | Silent installer (see below) | Silent installer (see below) |
| docker | `brew install --cask docker` | `winget install Docker.DockerDesktop` | `choco install docker-desktop` | [Docker Desktop](https://www.docker.com/products/docker-desktop/) | `curl -fsSL https://get.docker.com \| sudo sh` | `curl -fsSL https://get.docker.com \| sudo sh` | `curl -fsSL https://get.docker.com \| sudo sh` |

**Special cases:**

- **Rust:** Always use rustup, never a system package manager. On macOS/Linux: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y` then `source $HOME/.cargo/env`. On Windows: `winget install Rustlang.Rustup`.
- **conda (Miniconda):** Auto-install using the platform's package manager when available. On macOS: `brew install miniconda`. On Windows: `winget install Anaconda.Miniconda3` (or `choco install miniconda3`). On Linux: download and run the silent installer — `mkdir -p ~/miniconda3 && curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh && bash /tmp/miniconda.sh -b -u -p ~/miniconda3 && rm /tmp/miniconda.sh`. After install on ALL platforms, run `conda init` for the user's shell (`conda init bash`, `conda init zsh`, or `conda init powershell`). Then warn: "conda is installed, but you need to restart Claude Code for it to take effect. Press `Ctrl+D`, reopen with `claude`, and run `/start` again — I'll pick up where we left off." If install fails, fall back to walking them through the Miniconda download page: [docs.anaconda.com/miniconda/](https://docs.anaconda.com/miniconda/).
- **Docker:** Auto-install using the platform's package manager when available. On macOS: `brew install --cask docker` then `open /Applications/Docker.app` (launches Docker Desktop — it must be running for `docker` commands to work; wait a few seconds, then verify with `docker info`). On Windows: `winget install Docker.DockerDesktop` (or `choco install docker-desktop`) — tell user to launch Docker Desktop from the Start menu if `docker info` fails. On Linux: `curl -fsSL https://get.docker.com | sudo sh` then `sudo usermod -aG docker $USER` — warn: "Docker is installed. You need to restart Claude Code for the group change to take effect, or use `sudo docker` in the meantime." After install, verify with `docker --version` and `docker info` (the latter confirms the daemon is running). If the daemon isn't running, tell them to start Docker Desktop (macOS/Windows) or run `sudo systemctl start docker` (Linux). If install fails, fall back to the Docker Desktop download page: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
- **Linux `sudo`:** Before running any `sudo` command, warn the user: "This next command needs admin access — you may see a password prompt."
- **Windows PATH issues:** After installing a tool on Windows, the current shell may not see it. If a version check still fails after install, tell the user: "The tool was installed but this shell can't see it yet. Close Claude Code (`Ctrl+D`), reopen it (`claude`), then run `/start` again — I'll pick up where we left off."
- **Python 2 vs 3:** If `python --version` returns 2.x on Linux/macOS, use `python3` instead. If `python3` is also missing, install it.
- **`nodejs` vs `node`:** On some Linux distros (Debian/Ubuntu), the binary may be `nodejs`. Check both and use whichever works.

**After all installs complete**, re-run the full checklist from Phase B and display it again. Do NOT proceed to Step 5 until every required tool shows ✓.

## Step 5: Scaffold the Project

Create the project directory inside this repository under `workspace/` and initialize it. Use OS-appropriate commands:

- **macOS/Linux:** `mkdir -p workspace/<project-name> && cd workspace/<project-name> && git init`
- **Windows:** `mkdir workspace\<project-name> && cd workspace\<project-name> && git init`

Only show the command for their detected OS.

Suggested directory names by project:
- Canvas: `workspace/canvas-site`
- Forge: `workspace/forge-toolkit`
- Nexus: `workspace/nexus-gateway`
- Sentinel: `workspace/sentinel`

**If the user chose Canvas**, scaffold these files (no language project file needed):

- `index.html` — Basic HTML5 boilerplate with a "Hello, Canvas!" heading and a link to `styles/main.css` and `scripts/main.js`
- `styles/main.css` — CSS reset (box-sizing, margin/padding reset) plus CSS custom properties for colors, fonts, and spacing
- `scripts/main.js` — Empty file with a comment: `// Canvas — main JavaScript file`
- `.gitignore` — Minimal: `.DS_Store`, `Thumbs.db`, `*.swp`

That's all Canvas needs. No package.json, no build config, no dependencies. Open the site in their browser — actually run the OS-appropriate command, don't just tell them about it:
- **macOS:** `open index.html`
- **Windows:** `powershell.exe -Command "Start-Process index.html"`
- **Linux:** `xdg-open index.html`

Only run the command for their detected OS. If the command fails (e.g., headless server, WSL without GUI access), fall back gracefully: "I couldn't open the browser automatically — navigate to the project folder and double-click `index.html` to open it."

After scaffolding, **list every file you created with a one-line description of each** (the Write tool truncates previews, so the user may not have seen the full contents). For Canvas, also show how to open the site in their browser using the OS-appropriate command. End with: "Take a look, and when you're ready, say **"let's go"** or **"start Module 1"** to begin." Do NOT immediately continue into Module 1 — wait for the user to respond first.

**For all other projects**, if their language needs a project file (package.json, go.mod, Cargo.toml, pyproject.toml, etc.), create it.

Create a `.gitignore` in the project directory appropriate for the chosen language (e.g., `__pycache__/`, `node_modules/`, `target/`, `.venv/`, etc.).

Based on the environment choice from Step 3, also scaffold environment files:

**If they chose venv:**
- Run `python -m venv .venv` (or `python3 -m venv .venv` on macOS/Linux) in the project directory
- Tell them how to activate using their OS-specific command:
  - **macOS/Linux:** `source .venv/bin/activate`
  - **Windows:** `.venv\Scripts\activate`
  Only show the one that matches their detected OS.
- Create an empty `requirements.txt` with a comment: `# Add your project dependencies here`

**If they chose conda:**
- Create an `environment.yml` with the project name and python version:
  ```yaml
  name: <project-name>
  dependencies:
    - python=3.12
  ```
- Run `conda env create -f environment.yml` in the project directory. If the environment already exists, run `conda env update -f environment.yml --prune` instead.
- Tell them how to activate: `conda activate <project-name>`

**If they chose Docker:**
- Generate a `Dockerfile` appropriate for their chosen language:
  - Python: python:3.12-slim base, WORKDIR /app, COPY requirements.txt, pip install, COPY ., CMD
  - TypeScript/Node: node:20-slim base, WORKDIR /app, COPY package*.json, npm install, COPY ., CMD
  - Go: golang:1.22 base, WORKDIR /app, COPY go.*, go mod download, COPY ., go build, CMD
  - Rust: rust:1.77 base, WORKDIR /app, COPY Cargo.*, cargo build --release (multi-stage), CMD
- Generate a `.dockerignore` with common excludes: `.git`, `node_modules`, `.venv`, `__pycache__`, `target`, `dist`, `.env`
- Tell them: `docker build -t <project-name> .` and `docker run -it <project-name>`
- Note: they'll still develop locally and can use Docker for running/testing

**If they chose Local:** No extra files needed.

After scaffolding (for all projects), **list every file you created with a one-line description of each** so the user has a clear picture of their project structure. **STOP and wait for the user to respond before starting Module 1.**

## Step 6: Module 1 — Setup & First Contact

### PACING — MANDATORY

**You MUST deliver this module one sub-step at a time.** Each sub-step (6.1, 6.2, 6.3, etc.) is a SEPARATE message. After each sub-step, STOP RESPONDING and wait for the user to reply. Do NOT continue to the next sub-step until the user sends a message.

If you are about to write content from two sub-steps in the same message, STOP. Send only the current sub-step and end your message.

This is the most important instruction in this skill. A wall of text overwhelms the user. Short, focused messages with pauses feel like a conversation.

### Teaching style

- **Plain language.** If you use a technical term, explain it briefly in parentheses. Assume the user may be new to development tools.
- **Explain WHY before HOW.** What problem does this solve? Why should they care?
- **Conversational.** Talk like a colleague showing you something useful, not a manual or textbook.
- **Short messages.** Each sub-step should be a few short paragraphs at most. Less is more.

---

### 6.1 Teach: What is CLAUDE.md?

Print the following explanation exactly as written (do NOT use blockquote formatting — output as normal text):

CLAUDE.md is a file that Claude reads at the start of every session — like a briefing note that reminds Claude about your project. Without it, every session starts from zero. Claude won't remember your project, your preferences, or what you decided last time. CLAUDE.md fixes that.

It contains a description of your project, what language you're using, how to build and test things, and any preferences you have. Let's create one for your project — I'll walk you through each part. Say **"let's do it"** when you're ready.

**STOP. Do not continue to 6.2. Wait for the user to respond.**

---

### 6.2 Create CLAUDE.md Together

Create the `CLAUDE.md` file in `workspace/<project>/`. Walk through each section briefly as you write it:

- "**Project description** — tells Claude what we're building so it gives relevant suggestions"
- "**Language and stack** — so Claude writes code in the right language"
- "**Build and test commands** — Claude can run these to check its own work"
- "**Pointers to the guide** — so Claude can look things up when you ask"

The file should include:
- Project description (based on their chosen project)
- Language (for Canvas: "HTML, CSS, and JavaScript — no build tools or frameworks")
- Placeholder build/test/lint commands (for Canvas: "Open index.html in browser")
- Pointer to project guide: `See ../../projects/<name>/README.md for the full module guide.`
- Pointer to reference docs: `See ../../context/ for detailed Claude Code feature documentation.`

After creating the file, **display the full file contents in a code block in your message**. The Write tool only previews the first few lines, so the user can't see everything — especially the pointers at the bottom. Show the complete file so they can see all sections.

Then ask: "Does that make sense? Any sections you'd want to change? Say **"looks good"** to continue, or tell me what to change."

**STOP. Do not continue to 6.3. Wait for the user to respond.**

---

### 6.3 Teach: The Memory Hierarchy

Print the following explanation exactly as written (do NOT use blockquote formatting — output as normal text). Substitute the correct OS-specific path for `~` based on the detected OS:

CLAUDE.md is actually one level in a bigger system. There are four levels, and they layer on top of each other:

1. **CLAUDE.md** (shared) — What we just created. Anyone who works on this project sees it. Put project conventions here.
2. **CLAUDE.local.md** (personal) — Just for you — it's gitignored, so it won't be shared. Your progress, your notes. We'll create one next.
3. **.claude/rules/** (organized) — For bigger projects, you can split rules into separate files instead of cramming everything into one CLAUDE.md. We'll use this in Module 3.
4. **~/.claude/CLAUDE.md** (global, in `<OS-specific path>`) — Your preferences across ALL projects. Like "I prefer concise responses" or "always use dark mode examples." Applies everywhere, not just this project.

The key insight: if a teammate would benefit from knowing it, put it in CLAUDE.md. If it's just your workflow or progress, put it in CLAUDE.local.md.

Makes sense? Say **"ready"** and I'll create your CLAUDE.local.md — the personal one that tracks your progress.

**STOP. Do not continue to 6.4. Wait for the user to respond.**

---

### 6.4 Create CLAUDE.local.md

Print the following explanation exactly as written (do NOT use blockquote formatting — output as normal text):

This file tracks YOUR progress. It's personal — not shared. When you come back tomorrow, Claude reads this and knows exactly where you left off.

Create `CLAUDE.local.md` in the **cc-self-train root directory** (NOT inside workspace/):

```
# Active Project
Project: <project> | Language: <language> | OS: <detected-os> | Directory: workspace/<project-dir> | Current Module: 1
Experience Level: <beginner/intermediate/advanced>

When the user starts a session, greet them and offer to continue where they left off.
When the user says "next module" or asks for the next module, read the current module file from projects/<name>/modules/ (e.g., projects/<name>/modules/02-blueprint.md) and walk them through it.
Before running /compact or when context is getting large, update this file with the current module, step number, and any in-progress work.
Always use OS-appropriate commands (paths, file openers, activation scripts, etc.).

For beginners: explain concepts thoroughly, define technical terms, move slowly.
For intermediate users: focus on what makes CC different from other AI tools, skip basic tool explanations.
For advanced CC users: skip fundamentals, focus on advanced patterns and best practices.

@import workspace/<project-dir>/CLAUDE.md
```

**Display the full file contents in a code block** (the Write tool truncates previews). Then briefly explain each line:
- Progress tracker (project, language, OS, module number, experience level)
- Instructions for Claude on how to greet you next time, use the right commands for your OS, and adapt depth to your experience level
- Pre-compaction instruction — reminds Claude to save progress before context compression
- The `@import` pulls your project's CLAUDE.md into this context automatically

End with something like: "Your progress is now tracked. Say **"let's commit"** when you're ready to make your first git commit."

**STOP. Do not continue to 6.5. Wait for the user to respond.**

---

### 6.5 Git Integration + First Commit

Print the following explanation exactly as written (do NOT use blockquote formatting — output as normal text):

Git tracks every change you make to your files — think of it like a save system in a game. A **commit** is a save point with a description of what changed. Claude Code has built-in git support, so you don't need to leave the conversation to use it.

Before committing, check that git knows who the user is:

- Run `git config user.name` and `git config user.email` inside `workspace/<project>/`
- If either is empty, print the following exactly: "Git tags every commit with your name and email so you can tell who made which change. This stays local — it's not sent anywhere."
- Ask the user for their name and email using AskUserQuestion (the free-text "Other" option works fine for this)
- Run `git config user.name "Their Name"` and `git config user.email "their@email.com"` in the project directory

Then make the initial commit inside `workspace/<project>/`:

```
cd workspace/<project>
git add -A
git commit -m "Initial project setup with CLAUDE.md"
```

After committing, list the files that were tracked (e.g., for Canvas: `index.html`, `styles/main.css`, `scripts/main.js`, `.gitignore`, `CLAUDE.md`) so the user sees exactly what's in their first save point.

Print the following exactly as written (do NOT use blockquote formatting — output as normal text):

What you just did — make a change, verify it works, commit — is the **edit, check, commit** loop. It's the rhythm you'll use in every module. Make a change, verify it works, save a checkpoint. That way you can always roll back if something breaks.

And here's a bonus: if Claude ever makes a change you don't like, press `Esc` twice quickly. It rewinds the last changes — like an undo button.

End with something like: "Your first commit is done — you've got a save point. Say **"show me"** to learn the keyboard shortcuts that make Claude Code faster."

**STOP. Do not continue to 6.6. Wait for the user to respond.**

---

### 6.6 Keyboard Shortcuts — Look Them Up Live

Print the following exactly as written (do NOT use blockquote formatting — output as normal text):

Claude Code has keyboard shortcuts that make you faster. Instead of me listing them from memory, let me show you something useful — Claude can search the web for up-to-date information.

**Use the WebSearch tool** to search for the current Claude Code keyboard shortcuts for the user's detected OS. A good query: `"Claude Code keyboard shortcuts [macOS/Windows/Linux]"` (use their actual OS).

Present the results as a clean table, filtered to the shortcuts most relevant for beginners. Organize into three groups and **only show the shortcuts for their OS** (some keys differ between macOS and Windows/Linux):

**Group 1 — Basics:** How to send messages, stop responses, open menus, accept suggestions.

**Group 2 — Working with files:** How to mention files (@), run terminal commands (!).

**Group 3 — Power features:** How to switch modes, undo changes, clear the screen.

After presenting all three groups, suggest they try a few:
- "Type / to see available commands, then close the menu"
- "Type @ and look for the CLAUDE.md you created"
- "Try ! git log --oneline to see your commit"
- "Press the mode-switch shortcut a couple times and watch the indicator at the bottom change — we'll cover plan mode in detail in Module 2"

**Why teach it this way:** This shows the user that Claude can look things up in real time — they don't need to memorize everything. It also ensures shortcuts are accurate and current, since Claude Code updates frequently.

End with something like: "Don't worry about memorizing these — they'll become muscle memory as you use them. Say **"ready"** for one last exercise before we wrap up Module 1."

**STOP. Do not continue to 6.7. Wait for the user to respond.**

---

### 6.7 Practice: Customize CLAUDE.md

Print the following two paragraphs exactly as written (do NOT use blockquote formatting — output as normal text), then use AskUserQuestion:

Right now your CLAUDE.md has the basics — project description, language, build commands. But the real power comes from teaching Claude *your* preferences.

When you add rules like "keep functions short" or "never commit without asking me," Claude follows them in every response. Let's add one now — pick an improvement below.

Use AskUserQuestion to let the user pick one improvement:

1. **Add a coding style preference** — "Tells Claude HOW to write code. Example: 'prefer small functions' or 'always add comments to tricky logic'."
2. **Add a 'do not' rule** — "Sets a boundary. Example: 'never auto-commit without asking'."
3. **Add a project goal** — "Gives Claude the big picture. Example: 'Building toward a portfolio with 5 pages by Module 4'."

After they pick and you apply it, commit:

```
cd workspace/<project>
git add CLAUDE.md
git commit -m "Customize CLAUDE.md with personal preferences"
```

Point out: "This is the **edit, check, commit** loop — you'll use it in every module."

End with something like: "That's the core workflow — edit, check, commit. Say **"wrap it up"** and I'll summarize what you learned in Module 1."

**STOP. Do not continue to 6.8. Wait for the user to respond.**

---

### 6.8 Module 1 Complete

**Before the recap**, if a background curriculum sync agent was spawned in Step 0.1, do a **non-blocking** status check using `TaskOutput` with `block: false`:
- If the agent **finished successfully** → add a brief note in your recap: "By the way, that curriculum update from earlier finished — all lessons are current with v{latest}."
- If the agent is **still running** (unlikely after 15+ minutes) → don't mention it. It'll finish before they reach Module 2.
- If the agent **failed** → brief note: "The curriculum update ran into an issue — no worries, the current materials work fine."

This check is **informational only** — never block on it.

**Version mismatch check:** If the curriculum was synced to a newer CC version, compare it against the student's installed version. Run `claude --version` to get their installed version, then read the top version from `context/changelog-cc.txt` (the curriculum version). If the curriculum version is newer than the installed version, print the following (do NOT use blockquote formatting):

**Heads up:** The lessons now cover Claude Code v{curriculum_version} features, but you're running v{installed_version}. Some features taught in later modules might not be available until you update. You can update anytime by running `claude update` — it only takes a few seconds.

If the versions match or the curriculum wasn't updated, skip this message.

Print the following recap exactly as written (do NOT use blockquote formatting — output as normal text):

**Module 1 complete!** Here's what you now know:

- **CLAUDE.md** is Claude's project memory — loaded every session, shapes everything Claude does
- **The memory hierarchy** — shared (CLAUDE.md) vs personal (CLAUDE.local.md), and how they layer
- **Keyboard shortcuts** — navigate files, switch modes, and run commands without leaving Claude
- **Git integration** — commits are save points, and `Esc Esc` is your undo button

When you're ready, say **"next module"** or **"let's do Module 2"**. Next up: **Plan Mode** — you'll design your first real feature and learn how Claude helps you think before you code.
## Important

- Build the project in `workspace/<name>/` inside this repo. The `workspace/` directory is gitignored by cc-self-train.
- Ask what language they want — never assume (except Canvas, which is always HTML/CSS/JS).
- **OS-aware commands:** Always use the detected OS from Step 1b. Never show commands for all three operating systems — only show the one that matches the user's system. This includes paths (forward vs backslash), file-opening commands (`open`/`powershell.exe Start-Process`/`xdg-open`), shell syntax, activation scripts, and the Python executable name (`python` vs `python3`).
- Be encouraging. This is their first time with Claude Code for many users.
- If they already have a project in mind that doesn't match the 4 listed, that's fine — help them pick the project guide that teaches the CC features most relevant to what they want to build.
- **Module completion pattern:** Every module delivery (not just Module 1) must end with a "next module" prompt and a progress update. When delivering Modules 2-10 from `projects/<name>/modules/`, always append after the checkpoint:
  > When you're ready, say **"next module"** or **"let's do Module [N+1]"**. Next up: **[Module N+1 title]** — [one-sentence preview of what they'll learn].
  Then update `Current Module` in CLAUDE.local.md to the completed module number. For Module 10, replace the "next module" prompt with a course completion message.
