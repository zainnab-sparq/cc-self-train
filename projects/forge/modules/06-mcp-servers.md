# Module 6 -- MCP Servers

<!-- progress:start -->
**Progress:** Module 6 of 10 `[██████░░░░]` 60%

**Estimated time:** ~60-75 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** MCP servers, `.mcp.json`, scopes, skills+MCP, `claude mcp add`

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

</details>

> **New term this module uses:**
> - **MCP (Model Context Protocol)** -- an open standard for connecting Claude Code to external tools (databases, APIs, filesystems). An **MCP server** is a small program that exposes tools Claude can call. You install one with `claude mcp add`. Think of MCP as the "USB port" that lets Claude plug into other systems.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 6.1 What Is MCP

MCP (Model Context Protocol) is an open standard for connecting AI tools to
external data sources and APIs. MCP servers give Claude Code access to
databases, file systems, APIs, and more.

### 6.1b MCP Transports

MCP servers talk to Claude Code over a **transport**. You will see three:

- **`stdio`** (default) -- the MCP server runs as a subprocess Claude spawns. The server reads requests from stdin and writes responses to stdout. Use this for local tools (filesystems, databases, local APIs). This is what 90% of `claude mcp add` commands use.
- **`http`** -- the MCP server is a long-running HTTP service. You give Claude a URL and it makes HTTP requests to the server. Use this when the MCP server is shared across machines or already running as a web service.
- **`sse`** (server-sent events) -- same as HTTP but the server streams events back. Use this when you want live updates (file watchers, log streams).

**Rule of thumb:** Start with `stdio`. Move to `http` if you need the server to run on a different machine. Use `sse` only if you need push-style updates from the server.

### 6.1c MCP Security Posture

Before you connect your first MCP server, three security concepts worth holding in mind.

**Untrusted servers run arbitrary code.** Adding an MCP server means Claude can call into whatever that server does. For a local `stdio` server this is "whatever command you spawned" — you're the one who typed it. For an `http` or `sse` server it's "whatever the remote service does" — you're trusting whoever operates that URL. `.mcp.json` in a cloned repo is a third-party pushing a server definition at you (see the `.mcp.json` caveat later in this module). Before connecting, ask: who wrote this server? Who's running it? What does it need to work (file access, database creds, network reach)? If any answer is "not sure," sandbox the session or skip.

**Elicitation lets servers ask you questions.** MCP servers can emit elicitation requests mid-conversation — "I need an API key to proceed" or "Confirm you want me to write to this path." Claude surfaces these for approval. There's also an auto-answer mechanism for routine prompts.

The abuse pattern: a compromised server emits an elicitation that looks routine ("retry with default parameters?") but carries a parameter change under the hood. Auto-answering elicitations from untrusted servers is the same trust decision as permanent-approving a command — fine for well-known routine interactions, risky otherwise. When in doubt, answer each elicitation manually.

**Channel scopes limit the attack surface.** MCP servers can be constrained to a subset of tools rather than the full toolbox. If a server only needs file-read, grant file-read. If it only needs database-query, grant that. Don't hand an MCP server write access to the filesystem unless it genuinely needs that to work.

The principle: every MCP server is a new principal in your trust boundary. Treat it like a service account with narrow scopes, not like you gave it root. See also [docs/SAFETY-AND-TRUST.md](../../../docs/SAFETY-AND-TRUST.md) for the cross-feature threat model.

**Verify the package exists before installing.** MCP scopes and names change. Before running any `claude mcp add ... -- npx -y <package>` command in this module, verify:

```bash
npm view <package>
```

If that returns 404, the package doesn't exist — ask Claude for the current equivalent and verify again. The commands below use packages confirmed real at the time of writing (`@modelcontextprotocol/server-filesystem` is Anthropic-published; `mcp-sqlite` is community-maintained). Treat community packages with the same scrutiny you'd give any npm dependency. See SAFETY-AND-TRUST.md §2 on hallucinated packages.

### 6.2 Add a SQLite MCP Server (illustrative — not required)

<!-- guide-only -->
**Why this step:** MCP servers give Claude new capabilities beyond reading and writing files. A SQLite server is a convenient illustration because it's concrete — Claude can run SQL queries, create tables, and inspect a database directly. We use it to demonstrate how MCP integration works; you learn the pattern, not the persistence strategy.
<!-- /guide-only -->

**You do not need to migrate your JSON storage.** Your existing file-based JSON layer is production-fine for a personal toolkit — skim this section for the MCP mechanics, then keep whichever storage fits your actual use. The command below adds a SQLite server for learning purposes; you can remove it later with `claude mcp remove forge-db` if you don't want it lingering.

On Windows, use the `cmd /c` wrapper for npx-based servers:

```
claude mcp add --transport stdio forge-db -- cmd /c npx -y mcp-sqlite --db-path forge.db
```

On macOS/Linux:

```
claude mcp add --transport stdio forge-db -- npx -y mcp-sqlite --db-path forge.db
```

After adding, check the status:

```
/mcp
```

You should see `forge-db` listed and connected.

Now ask Claude to set up a demo schema using the MCP server. This is where you see MCP tools in action — you're not committing to SQLite as your real storage, just exercising the pattern.

"Using the forge-db MCP server, create demo tables for my four data types. If you want to try populating them, copy a few rows from my JSON — but keep the JSON as my source of truth. I want to see the MCP tools work, not replace my storage."

Claude may ask about column types or indexes. Answer however you like — the point is watching Claude drive the database through MCP, not landing a production schema.

**STOP -- What you just did:** You connected an external tool to Claude Code using MCP. Claude can now create tables, insert data, and run queries on a SQLite database -- all through natural language. The `/mcp` command is your dashboard for checking which servers are connected and healthy. Whether you adopt SQLite as real storage is your call; this module's job is teaching MCP integration, not prescribing a persistence layer.

**Engineering value:**
- *Entry-level:* MCP servers are like USB ports for Claude — they let you plug in new capabilities without changing Claude itself.
- *Mid-level:* In real engineering workflows, MCP connects Claude to your actual tools — Jira for ticket tracking, Figma for designs, Sentry for error monitoring. Claude stops being a code-only tool and becomes a full engineering assistant.
- *Senior+:* MCP is a standardized integration protocol — like LSP (Language Server Protocol) but for AI tool access. Building on open standards means your MCP configurations work across any AI tool that supports the protocol, not just Claude.

Shall we add a filesystem MCP server too?

### 6.3 Add a Filesystem MCP Server

For enhanced file operations:

On Windows:

```
claude mcp add --transport stdio forge-fs -- cmd /c npx -y @modelcontextprotocol/server-filesystem --root .
```

On macOS/Linux:

```
claude mcp add --transport stdio forge-fs -- npx -y @modelcontextprotocol/server-filesystem --root .
```

### 6.4 Check MCP Status

```
/mcp
```

This shows all connected servers, their status, and available tools. You
should see both `forge-db` and `forge-fs`.

**Quick check before continuing:**
- [ ] `/mcp` shows both `forge-db` and `forge-fs` as connected
- [ ] You can ask Claude to query the SQLite database and get results
- [ ] (Optional) demo tables exist in SQLite — you can revert to JSON-only anytime

### 6.5 Create .mcp.json for Team Sharing

<!-- guide-only -->
**Why this step:** MCP servers you add with `claude mcp add` are stored locally by default -- only you can see them. By using the `--scope project` flag, the configuration goes into `.mcp.json` at your project root, which you can commit to version control. This means any teammate who clones your repo gets the same MCP setup automatically.
<!-- /guide-only -->

To share MCP configuration with your team, use the project scope:

```
claude mcp add --transport stdio forge-db --scope project -- npx -y mcp-sqlite --db-path forge.db
```

This creates a `.mcp.json` file at your project root:

```json
{
  "mcpServers": {
    "forge-db": {
      "command": "npx",
      "args": ["-y", "mcp-sqlite", "--db-path", "forge.db"],
      "env": {}
    }
  }
}
```

Commit this file so teammates get the same MCP setup.

**`.mcp.json` is shipped with your repo.**

The `.mcp.json` file is a shared trust surface — everyone who clones the repo gets the same MCP servers configured. That's the whole point for team setup, but it's also the risk: a PR that adds a new MCP server to `.mcp.json` is a supply-chain event. The added server can point at any URL, any command. On first use Claude Code prompts for permission, but learners trained to approve prompts fast will approve it without reading.

Treat `.mcp.json` diffs in PRs with the same review bar as CI config changes or GitHub Actions workflow changes. Ask: what command or URL is being added, who controls it, what data does it see once connected.

### 6.6 Understand MCP Scopes

| Scope | Where Stored | Who Sees It |
|-------|-------------|------------|
| **local** (default) | `~/.claude.json` under project path | Only you, this project |
| **project** | `.mcp.json` in project root | Everyone (via version control) |
| **user** | `~/.claude.json` | Only you, all projects |

**STOP -- What you just did:** You learned the three MCP scopes and how they control visibility. Local scope is for personal experimentation, project scope is for team sharing, and user scope is for tools you want everywhere. Understanding scopes prevents the common mistake of adding MCP servers that only work on your machine while your teammates get errors.

**Engineering value:**
- *Entry-level:* Committing `.mcp.json` means anyone who clones your repo gets the same MCP servers — no setup instructions to follow.
- *Mid-level:* Project-scoped MCP config is infrastructure-as-code for AI tooling. New team members clone, run `claude`, and everything just works.

How about we combine skills with MCP servers?

### 6.7 Create a Skill That Orchestrates MCP Tools

Now combine skills and MCP by creating a backup skill. Describe the workflow to Claude -- exporting data from the database, writing it to a dated backup directory, and logging the backup.

"Create a backup skill that exports all tables from the SQLite database to JSON files in a backups/YYYY-MM-DD/ directory, logs the backup in a backup_log table, and shows a summary with counts and file sizes. Make it manual-only and give it access to both MCP servers plus Bash, Read, and Write."

Claude will wire up the `mcp__forge-db__*` and `mcp__forge-fs__*` tool patterns in the `allowed-tools` frontmatter. This is the skills+MCP pattern in action.

Test it: `/backup`

**STOP -- What you just did:** You combined two Claude Code features -- skills and MCP -- into something more powerful than either one alone. The backup skill uses `allowed-tools` to access MCP tools (`mcp__forge-db__*`) alongside regular tools. This is the skills+MCP pattern: a skill defines the workflow, MCP servers provide the data access. You will use this pattern whenever you need a repeatable workflow that touches external data sources.

### 6.8 Connect a Tool You Actually Use

The MCP servers you added above are local utilities -- SQLite and filesystem. But MCP also connects to cloud tools you already use.

**What tools do you use day-to-day?** Think about your project management (Jira, Linear), notes and docs (Notion, Confluence), and communication (Slack). Many of these have MCP servers you can connect to Claude Code. Pick one from the table below, or browse `context/mcp.txt` for the full list:

| Tool | What it gives you | Command |
|------|------------------|---------|
| Notion | Search and update notes from inside Claude | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| Linear | Manage issues for your toolkit | `claude mcp add --transport http linear https://mcp.linear.app/mcp` |
| Slack | Send messages and fetch channel data | `claude mcp add slack --transport http https://mcp.slack.com/mcp` |
| Jira / Confluence | Track issues, search docs from inside Claude | `claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse` |

Notice the `--transport http` flag -- that is how you connect to remote cloud servers (as opposed to `--transport stdio` for local servers like SQLite).

If you want the server available across all your projects, add `--scope user`:

```
claude mcp add --transport http notion --scope user https://mcp.notion.com/mcp
```

After adding, run `/mcp` to authenticate and verify the connection. Then try it out:

"Using the Notion MCP server, find my most recently edited pages and suggest which ones I should link from the forge toolkit's help output."

This section is optional -- if you do not use any of these tools, skip ahead to the checkpoint.

### 6.9 MCP Elicitation & Channels

Two major MCP capabilities have landed. How might you use them?

**Elicitation** (v2.1.76) — MCP servers can now request structured input from you mid-task. When a server needs information it can't get on its own, Claude Code displays an interactive dialog (form fields or browser URL). No configuration needed on your side — dialogs appear automatically. Use the `Elicitation` hook to auto-respond programmatically.

**Channels** (v2.1.80, research preview) — MCP servers can push messages directly into your session. A server declares `claude/channel` capability, and you opt in with `--channels` at startup. Use cases: reacting to Telegram messages, Discord chats, CI results, or monitoring alerts while you work.

**OAuth discovery** (v2.1.69) — MCP servers can now set `oauth.authServerMetadataUrl` for custom OAuth metadata discovery when standard discovery fails.

What kind of MCP server would benefit most from elicitation in your workflow? Think about servers that need credentials or configuration mid-task.

> **STOP** — Consider how elicitation and channels could enhance your MCP setup.

### 6.10 Skip tool-search deferral with `alwaysLoad` (v2.1.121)

By default, MCP tools are lazy-loaded through tool-search to keep your context lean -- Claude only sees a server's tools after asking for them. As of v2.1.121, you can opt a server out of that deferral with `"alwaysLoad": true` in `.mcp.json`:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "forge.db"],
      "alwaysLoad": true
    }
  }
}
```

Use it for small, frequently-needed servers (the toolkit's SQLite store, a project-specific lint runner) where the lazy-load round-trip is wasted overhead. Avoid it for servers with dozens of tools -- the tool descriptions count against your context window even when unused.

> **STOP** -- Pick one of your MCP servers, add `"alwaysLoad": true` to it in `.mcp.json`, restart Claude Code, and confirm via `/mcp` that its tools are loaded immediately.

### Checkpoint

Your toolkit just got a real database. MCP servers let Claude reach beyond local files into databases, APIs, and tools you already use.

- [ ] SQLite MCP server is connected (`/mcp` shows it active)
- [ ] Filesystem MCP server is connected
- [ ] You can query the SQLite database through Claude
- [ ] `.mcp.json` exists for team sharing
- [ ] You understand the three MCP scopes (local, project, user)
- [ ] Backup skill orchestrates MCP tools to export and archive data
- [ ] (Optional) SQLite demo schema exists; JSON storage can remain your source of truth
- [ ] Understand MCP elicitation and channels
- [ ] (Optional) You connected an MCP server for a tool you actually use
- [ ] Set `"alwaysLoad": true` on at least one server in `.mcp.json`
