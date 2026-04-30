# Module 6 -- MCP Servers

<!-- progress:start -->
**Progress:** Module 6 of 10 `[██████░░░░]` 60%

**Estimated time:** ~60-75 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** MCP servers, `.mcp.json`, scopes, skills+MCP, `claude mcp add`

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think...", "Try this and tell me..."

</details>

> **New term this module uses:**
> - **MCP (Model Context Protocol)** -- an open standard for connecting Claude Code to external tools (databases, APIs, filesystems). An **MCP server** is a small program that exposes tools Claude can call. You install one with `claude mcp add`. Think of MCP as the "USB port" that lets Claude plug into other systems.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 6.1 What Is MCP

<!-- guide-only -->
**Why this step:** Until now, Claude Code has only worked with local files and shell commands. MCP (Model Context Protocol) servers extend Claude's reach to external systems -- file servers, web APIs, databases, and more. This is what turns Claude Code from a code assistant into an integration platform.
<!-- /guide-only -->

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

If that returns 404, the package doesn't exist — ask Claude for the current equivalent and verify again. The commands below use packages confirmed real at the time of writing (`@modelcontextprotocol/server-filesystem` is Anthropic-published; `mcp-fetch-server` is community-maintained). Treat community packages with the same scrutiny you'd give any npm dependency. See SAFETY-AND-TRUST.md §2 on hallucinated packages.

### 6.2 Add an MCP Server Relevant to Your Stack

Pick the MCP server that best fits your project. Here are common choices by project type:

| Project Type | Recommended MCP Server | What It Gives You |
|-------------|----------------------|-------------------|
| Any project | Filesystem | Enhanced file operations beyond built-in Read/Write |
| Web app with DB | Database (Postgres, SQLite) | Query and inspect your database from Claude |
| Web frontend | Fetch | Pull in real content, APIs, design references |
| API project | Fetch | Test external endpoints, pull API specs |
| Data project | Filesystem + Fetch | Access data files and remote data sources |

Add the one that fits your project best. For filesystem (works for any project):

On Windows:

```
claude mcp add --transport stdio project-fs -- cmd /c npx -y @modelcontextprotocol/server-filesystem --root .
```

On macOS/Linux:

```
claude mcp add --transport stdio project-fs -- npx -y @modelcontextprotocol/server-filesystem --root .
```

For Fetch (web projects, API projects):

On Windows:

```
claude mcp add --transport stdio project-fetch -- cmd /c npx -y mcp-fetch-server
```

On macOS/Linux:

```
claude mcp add --transport stdio project-fetch -- npx -y mcp-fetch-server
```

If your project uses a database, check `context/mcp.txt` for database-specific MCP servers (Postgres, SQLite, etc.).

**STOP -- What you just did:** You connected your first MCP server and it's one that actually fits your project's stack. The key command pattern is `claude mcp add --transport stdio <name> -- <command>`. You will use this same pattern to add any MCP server.

**Engineering value:**
- *Entry-level:* MCP servers are like USB ports for Claude -- they let you plug in new capabilities without changing Claude itself.
- *Mid-level:* In real engineering workflows, MCP connects Claude to your actual tools -- Jira for ticket tracking, Figma for designs, Sentry for error monitoring. Claude stops being a code-only tool and becomes a full engineering assistant.
- *Senior+:* MCP is a standardized integration protocol -- like LSP (Language Server Protocol) but for AI tool access. Building on open standards means your MCP configurations work across any AI tool that supports the protocol, not just Claude.

### 6.3 Try Your MCP Server

Use the MCP server you just added for a real task in your project. The task depends on which server you added:

**Filesystem server:** Ask Claude to use the MCP filesystem tools to analyze your project structure, find large files, or reorganize a directory.

```
Using the filesystem MCP server, analyze my project's directory structure and suggest which files could be better organized.
```

**Fetch server:** Ask Claude to pull in real data relevant to your project -- an API response, documentation, or a dependency's changelog.

```
Using the fetch MCP server, pull the latest changelog for [your main dependency] and summarize what changed in the most recent version.
```

**Database server:** Ask Claude to inspect your schema or run a diagnostic query.

```
Using the database MCP server, show me the current schema and flag any tables missing indexes on foreign keys.
```

### 6.4 Check MCP Status

```
/mcp
```

This shows all connected servers, their status, and available tools. You should see your MCP server listed and connected.

**STOP -- What you just did:** You used an MCP server for a real task in your project -- not a toy example, but something that actually helped. This is the key insight: MCP servers are most valuable when they connect Claude to the tools and data sources your project actually depends on.

**Quick check before continuing:**
- [ ] `/mcp` shows your MCP server as connected
- [ ] You used the MCP server for a real task in your project
- [ ] The result was useful (not just a demo)

### 6.5 Create .mcp.json for Team Sharing

To share MCP configuration with your team (or your future self on another machine), use the project scope:

```
claude mcp add --transport stdio project-fs --scope project -- npx -y @modelcontextprotocol/server-filesystem --root .
```

This creates a `.mcp.json` file at your project root:

```json
{
  "mcpServers": {
    "project-fs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "--root", "."],
      "env": {}
    }
  }
}
```

Commit this file so teammates get the same MCP setup. If your server requires secrets (API keys, database URLs), those should go in environment variables -- never in `.mcp.json`.

**`.mcp.json` is shipped with your repo.**

The `.mcp.json` file is a shared trust surface — everyone who clones the repo gets the same MCP servers configured. That's the whole point for team setup, but it's also the risk: a PR that adds a new MCP server to `.mcp.json` is a supply-chain event. The added server can point at any URL, any command. On first use Claude Code prompts for permission, but learners trained to approve prompts fast will approve it without reading.

Treat `.mcp.json` diffs in PRs with the same review bar as CI config changes or GitHub Actions workflow changes. Ask: what command or URL is being added, who controls it, what data does it see once connected.

### 6.6 Understand MCP Scopes

| Scope | Where Stored | Who Sees It |
|-------|-------------|------------|
| **local** (default) | `~/.claude.json` under project path | Only you, this project |
| **project** | `.mcp.json` in project root | Everyone (via version control) |
| **user** | `~/.claude.json` | Only you, all projects |

<!-- guide-only -->
**Why this step:** The three scopes (local, project, user) control who sees an MCP configuration. The `project` scope creates `.mcp.json` which gets committed to git -- every teammate who clones the repo gets the same MCP servers automatically. This is how you standardize a team's tool setup.
<!-- /guide-only -->

**Engineering value:**
- *Entry-level:* Committing `.mcp.json` means anyone who clones your repo gets the same MCP servers -- no setup instructions to follow.
- *Mid-level:* Project-scoped MCP config is infrastructure-as-code for AI tooling. New team members clone, run `claude`, and everything just works.

### 6.7 Create a Skill That Orchestrates MCP Tools

Create a skill that combines MCP tools with built-in tools into a workflow that matters for your project. Think about what multi-step process you'd automate:

- **Build and validate:** lint, test, build, then summarize results
- **Deploy prep:** run checks, generate changelog, package artifacts
- **Database refresh:** pull schema, run migrations, verify integrity
- **Dependency audit:** fetch latest versions, check for vulnerabilities, update lockfile

Describe the workflow to Claude:

```
Create a skill that [describe your multi-step workflow]. Set disable-model-invocation to true and include mcp__project-fs__* in the allowed-tools so it can use the filesystem MCP server. Also include any other MCP tools it needs.
```

Replace `project-fs` with whatever you named your MCP server. Discuss the steps with Claude -- you might want different ordering or additional checks.

Test it by invoking the skill.

**STOP -- What you just did:** You created a skill that combines MCP tools with built-in tools into a single workflow. The `allowed-tools` frontmatter field (`mcp__project-fs__*`) grants the skill access to MCP server tools using the naming pattern `mcp__<server-name>__<tool-name>`. This is the Skills + MCP integration pattern -- your most powerful automation combines custom skills with external data sources.

### 6.8 Connect a Tool You Actually Use

The MCP servers you added above are local utilities. But MCP also connects to cloud tools you already use.

**What tools do you use day-to-day?** Think about your design tools (Figma, Canva), deployment platforms (Netlify, Cloudflare), and project management (Jira, Linear). Many of these have MCP servers you can connect to Claude Code. Pick one from the table below, or browse `context/mcp.txt` for the full list:

| Tool | What it gives you | Command |
|------|------------------|---------|
| Figma | Read design files, extract colors and specs | `claude mcp add --transport http figma-remote-mcp https://mcp.figma.com/mcp` |
| Canva | Search and export Canva designs | `claude mcp add --transport http canva https://mcp.canva.com/mcp` |
| Netlify | Deploy and manage your site from Claude | `claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp` |
| Jira / Confluence | Track issues, search docs from inside Claude | `claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse` |

Notice the `--transport http` flag -- that is how you connect to remote cloud servers (as opposed to `--transport stdio` for local servers like the filesystem MCP).

If you want the server available across all your projects, add `--scope user`:

```
claude mcp add --transport http figma-remote-mcp --scope user https://mcp.figma.com/mcp
```

After adding, run `/mcp` to authenticate and verify the connection. Then try it out with a real task in your project.

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
    "myserver": {
      "command": "python",
      "args": ["-m", "myserver"],
      "alwaysLoad": true
    }
  }
}
```

Use it for small, frequently-needed servers in your workflow (a project-specific lint runner, a database connector) where the lazy-load round-trip is wasted overhead. Avoid it for servers with dozens of tools -- the tool descriptions count against your context window even when unused.

> **STOP** -- Pick one of your MCP servers, add `"alwaysLoad": true` to it in `.mcp.json`, restart Claude Code, and confirm via `/mcp` that its tools are loaded immediately.

### Checkpoint

Claude Code now reaches beyond your local files. MCP servers give it access to databases, APIs, and tools you already use -- that's a big expansion of what's possible.

- [ ] At least one MCP server is connected (`/mcp` shows it active)
- [ ] You used the MCP server for a real task in your project
- [ ] `.mcp.json` exists for team sharing
- [ ] You understand the three MCP scopes (local, project, user)
- [ ] A skill orchestrates MCP tools with built-in tools for a multi-step workflow
- [ ] Understand MCP elicitation and channels
- [ ] (Optional) You connected an MCP server for a cloud tool you actually use
- [ ] Set `"alwaysLoad": true` on at least one server in `.mcp.json`
