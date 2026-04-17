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

**Why this step:** Until now, Claude Code has only worked with local files and shell commands. MCP (Model Context Protocol) servers extend Claude's reach to external systems -- file servers, web APIs, databases, and more. This is what turns Claude Code from a code assistant into an integration platform.

MCP (Model Context Protocol) is an open standard for connecting AI tools to
external data sources and APIs. MCP servers give Claude Code access to
databases, file systems, APIs, and more.

### 6.1b MCP Transports

MCP servers talk to Claude Code over a **transport**. You will see three:

- **`stdio`** (default) -- the MCP server runs as a subprocess Claude spawns. The server reads requests from stdin and writes responses to stdout. Use this for local tools (filesystems, databases, local APIs). This is what 90% of `claude mcp add` commands use.
- **`http`** -- the MCP server is a long-running HTTP service. You give Claude a URL and it makes HTTP requests to the server. Use this when the MCP server is shared across machines or already running as a web service.
- **`sse`** (server-sent events) -- same as HTTP but the server streams events back. Use this when you want live updates (file watchers, log streams).

**Rule of thumb:** Start with `stdio`. Move to `http` if you need the server to run on a different machine. Use `sse` only if you need push-style updates from the server.

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
claude mcp add --transport stdio project-fs -- cmd /c npx -y @anthropic-ai/mcp-filesystem --root .
```

On macOS/Linux:

```
claude mcp add --transport stdio project-fs -- npx -y @anthropic-ai/mcp-filesystem --root .
```

For Fetch (web projects, API projects):

On Windows:

```
claude mcp add --transport stdio project-fetch -- cmd /c npx -y @anthropic-ai/mcp-fetch
```

On macOS/Linux:

```
claude mcp add --transport stdio project-fetch -- npx -y @anthropic-ai/mcp-fetch
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
claude mcp add --transport stdio project-fs --scope project -- npx -y @anthropic-ai/mcp-filesystem --root .
```

This creates a `.mcp.json` file at your project root:

```json
{
  "mcpServers": {
    "project-fs": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem", "--root", "."],
      "env": {}
    }
  }
}
```

Commit this file so teammates get the same MCP setup. If your server requires secrets (API keys, database URLs), those should go in environment variables -- never in `.mcp.json`.

### 6.6 Understand MCP Scopes

| Scope | Where Stored | Who Sees It |
|-------|-------------|------------|
| **local** (default) | `~/.claude.json` under project path | Only you, this project |
| **project** | `.mcp.json` in project root | Everyone (via version control) |
| **user** | `~/.claude.json` | Only you, all projects |

**Why this step:** The three scopes (local, project, user) control who sees an MCP configuration. The `project` scope creates `.mcp.json` which gets committed to git -- every teammate who clones the repo gets the same MCP servers automatically. This is how you standardize a team's tool setup.

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

### Checkpoint

Claude Code now reaches beyond your local files. MCP servers give it access to databases, APIs, and tools you already use -- that's a big expansion of what's possible.

- [ ] At least one MCP server is connected (`/mcp` shows it active)
- [ ] You used the MCP server for a real task in your project
- [ ] `.mcp.json` exists for team sharing
- [ ] You understand the three MCP scopes (local, project, user)
- [ ] A skill orchestrates MCP tools with built-in tools for a multi-step workflow
- [ ] Understand MCP elicitation and channels
- [ ] (Optional) You connected an MCP server for a cloud tool you actually use
