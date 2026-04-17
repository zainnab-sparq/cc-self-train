# Module 6 -- MCP Servers

<!-- progress:start -->
**Progress:** Module 6 of 10 `[██████░░░░]` 60%

**Estimated time:** ~60-75 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** MCP servers, .mcp.json, scopes, skills+MCP, claude mcp add

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think...", "Try this and tell me..."

</details>

> **New term this module uses:**
> - **MCP (Model Context Protocol)** -- an open standard for connecting Claude Code to external tools (databases, APIs, filesystems). An **MCP server** is a small program that exposes tools Claude can call. You install one with `claude mcp add`. Think of MCP as the "USB port" that lets Claude plug into other systems.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 6.1 What is MCP

MCP (Model Context Protocol) connects Claude Code to external tools, databases, and APIs. Skills teach Claude **what to do**; MCP gives Claude **access to things**.

**Why this step:** Without MCP, Claude can only interact with your database through your application code. With an MCP server connected, Claude can directly query, inspect, and manage the database -- like giving it a database client. This is the difference between "Claude can read your code" and "Claude can read your data."

### 6.1b MCP Transports

MCP servers talk to Claude Code over a **transport**. You will see three:

- **`stdio`** (default) -- the MCP server runs as a subprocess Claude spawns. The server reads requests from stdin and writes responses to stdout. Use this for local tools (filesystems, databases, local APIs). This is what 90% of `claude mcp add` commands use.
- **`http`** -- the MCP server is a long-running HTTP service. You give Claude a URL and it makes HTTP requests to the server. Use this when the MCP server is shared across machines or already running as a web service.
- **`sse`** (server-sent events) -- same as HTTP but the server streams events back. Use this when you want live updates (file watchers, log streams).

**Rule of thumb:** Start with `stdio`. Move to `http` if you need the server to run on a different machine. Use `sse` only if you need push-style updates from the server.

### 6.2 Add the SQLite MCP Server

Connect an MCP server so Claude can directly inspect and manage the cache database:

```
# macOS / Linux
claude mcp add --transport stdio sqlite -- npx -y @anthropic-ai/mcp-sqlite --db-path ./cache.db

# Windows (requires cmd /c wrapper)
claude mcp add --transport stdio sqlite -- cmd /c npx -y @anthropic-ai/mcp-sqlite --db-path ./cache.db
```

If a SQLite MCP server is not available, ask Claude: `Help me set up an MCP server for a SQLite database at ./cache.db for my platform.`

### 6.3 Add the Filesystem MCP Server

```
# macOS / Linux
claude mcp add --transport stdio filesystem -- npx -y @anthropic-ai/mcp-filesystem --root .

# Windows
claude mcp add --transport stdio filesystem -- cmd /c npx -y @anthropic-ai/mcp-filesystem --root .
```

**STOP -- What you just did:** You connected two MCP servers that give Claude new capabilities: direct SQLite database access and filesystem operations. The `claude mcp add` command registered them, and now Claude can use their tools alongside its built-in tools. Think of MCP servers as "plugins for Claude's toolbox" -- each one adds new abilities.

**Engineering value:**
- *Entry-level:* MCP servers are like USB ports for Claude -- they let you plug in new capabilities without changing Claude itself.
- *Mid-level:* In real engineering workflows, MCP connects Claude to your actual tools -- Jira for ticket tracking, Figma for designs, Sentry for error monitoring. Claude stops being a code-only tool and becomes a full engineering assistant.
- *Senior+:* MCP is a standardized integration protocol -- like LSP (Language Server Protocol) but for AI tool access. Building on open standards means your MCP configurations work across any AI tool that supports the protocol, not just Claude.

Ready to verify your MCP connections?

### 6.4 Verify MCP Connections

Inside Claude Code, run `/mcp` to see both servers with their status. Also verify with `claude mcp list`.

**Why this step:** The `claude mcp add` command you just used stored the server config locally (just for you). A `.mcp.json` file at the project root makes the config shareable -- anyone who clones the repo gets the same MCP servers automatically. This is the difference between "works on my machine" and "works for the team."

### 6.5 Create .mcp.json for the Project

For team sharing, create a project-scoped `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-sqlite", "--db-path", "./cache.db"],
      "env": {}
    }
  }
}
```

Or use: `claude mcp add --scope project sqlite-cache -- npx -y @anthropic-ai/mcp-sqlite --db-path ./cache.db`

### 6.6 Understand MCP Scopes

| Scope | Storage Location | Shared With | Use Case |
|-------|-----------------|-------------|----------|
| local | ~/.claude.json (per-project path) | Just you | Personal servers, experiments |
| project | .mcp.json in project root | Team (via git) | Shared project servers |
| user | ~/.claude.json (global) | Just you (all projects) | Personal utilities |

**Quick check before continuing:**
- [ ] `/mcp` shows both SQLite and filesystem servers with green status
- [ ] `.mcp.json` exists at the project root
- [ ] You can explain the difference between local, project, and user scopes

**Engineering value:**
- *Entry-level:* Committing `.mcp.json` means anyone who clones your repo gets the same MCP servers -- no setup instructions to follow.
- *Mid-level:* Project-scoped MCP config is infrastructure-as-code for AI tooling. New team members clone, run `claude`, and everything just works.

### 6.7 Build the Caching Layer with MCP

Now use the SQLite MCP server to build the caching layer. Describe the caching behavior you want and let Claude design the schema and implementation. Tell Claude to use MCP to inspect the database as it builds.

```
I want to add response caching to the gateway using SQLite. Cache GET request responses with a configurable TTL per route. If a cached response exists and hasn't expired, return it without hitting the upstream. I also want CLI commands for cache stats and cache clear. Use the SQLite MCP tools to inspect the database as you build this.
```

Claude will design the cache table schema, implement the caching logic, and add the CLI commands. It may ask you about cache key strategy, what happens on TTL expiry, and whether you want cache size limits. Answer based on your preferences.

After building, ask Claude to query the live database:

```
Use the SQLite MCP server to show me what's in the cache. How many hits and misses have there been?
```

**STOP -- What you just did:** You built a real caching layer and then used MCP to inspect it from inside Claude Code. This is a major shift: instead of writing one-off SQL queries or print statements to debug your cache, you asked Claude to query the live database directly. MCP turns Claude from a code assistant into a system operator that can see your running application's state.

Want to see how skills and MCP work together?

### 6.8 Create a Skill That Uses MCP

**Why this step:** This step combines two features you have already learned -- skills (Module 4) and MCP (this module). The skill provides the *workflow* ("check stats, find expired entries, format a table"), while MCP provides the *capability* ("query SQLite"). This skills+MCP pattern is how you build sophisticated developer tools inside Claude Code.

Ask Claude to create a skill that orchestrates MCP tools for cache inspection. Describe the kind of report you want -- totals, hit rates, top keys, expired entries.

```
Create a cache-inspect skill that uses the SQLite MCP tools to query cache.db and generate a report. I want to see total entries, size, oldest and newest entries, hit/miss ratio, top 5 most-accessed keys, and any expired entries that haven't been cleaned up. If I pass a path argument, filter to matching entries. This one can be auto-invoked by Claude.
```

This demonstrates the skills+MCP pattern: the skill provides the workflow logic ("what to do"), while MCP provides the tool access ("ability to query SQLite").

### 6.9 Connect a Tool You Actually Use

The MCP servers you added above are local utilities -- SQLite and filesystem. But MCP also connects to cloud tools you already use.

**What tools do you use day-to-day?** Think about your monitoring (Sentry, Honeycomb), infrastructure (Cloudflare), project management (Jira, Linear), and code hosting (GitHub). Many of these have MCP servers you can connect to Claude Code. Pick one from the table below, or browse `context/mcp.txt` for the full list:

| Tool | What it gives you | Command |
|------|------------------|---------|
| Sentry | Query real errors hitting your gateway | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| Honeycomb | Query observability data and SLOs | `claude mcp add --transport http honeycomb https://mcp.honeycomb.io/mcp` |
| GitHub | Manage issues for the gateway project | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` |
| Cloudflare | Inspect deployed app state | `claude mcp add --transport http cloudflare https://bindings.mcp.cloudflare.com/mcp` |
| Jira / Confluence | Track issues, search docs from inside Claude | `claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse` |

Notice the `--transport http` flag -- that is how you connect to remote cloud servers (as opposed to `--transport stdio` for local servers like SQLite).

If you want the server available across all your projects, add `--scope user`:

```
claude mcp add --transport http sentry --scope user https://mcp.sentry.dev/mcp
```

After adding, run `/mcp` to authenticate and verify the connection. Then try it out:

```
Using the Sentry MCP server, what are the most common errors in the last 24 hours?
```

This section is optional -- if you do not use any of these tools, skip ahead to the checkpoint.

### 6.10 MCP Elicitation & Channels

Two major MCP capabilities have landed. How might you use them?

**Elicitation** (v2.1.76) — MCP servers can now request structured input from you mid-task. When a server needs information it can't get on its own, Claude Code displays an interactive dialog (form fields or browser URL). No configuration needed on your side — dialogs appear automatically. Use the `Elicitation` hook to auto-respond programmatically.

**Channels** (v2.1.80, research preview) — MCP servers can push messages directly into your session. A server declares `claude/channel` capability, and you opt in with `--channels` at startup. Use cases: reacting to Telegram messages, Discord chats, CI results, or monitoring alerts while you work.

**OAuth discovery** (v2.1.69) — MCP servers can now set `oauth.authServerMetadataUrl` for custom OAuth metadata discovery when standard discovery fails.

What kind of MCP server would benefit most from elicitation in your workflow? Think about servers that need credentials or configuration mid-task.

> **STOP** — Consider how elicitation and channels could enhance your MCP setup.

### Checkpoint

Your gateway now has persistent storage and Claude can query it directly. MCP servers bridge the gap between Claude and the external tools your project depends on.

- [ ] SQLite MCP server is connected (`/mcp` shows it)
- [ ] Filesystem MCP server is connected
- [ ] `.mcp.json` exists at the project root
- [ ] You can explain the three MCP scopes (local, project, user)
- [ ] The caching layer works: GET requests are cached in SQLite
- [ ] `nexus cache stats` and `nexus cache clear` work
- [ ] The `/cache-inspect` skill queries the SQLite MCP server
- [ ] Claude can directly query cache.db through MCP tools
- [ ] Changes committed to git
- [ ] Understand MCP elicitation and channels
- [ ] (Optional) You connected an MCP server for a tool you actually use
