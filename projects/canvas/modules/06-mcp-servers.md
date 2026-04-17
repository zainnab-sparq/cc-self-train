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

### 6.2 Add a Filesystem MCP Server

For enhanced file operations on your site files:

On Windows:

```
claude mcp add --transport stdio canvas-fs -- cmd /c npx -y @anthropic-ai/mcp-filesystem --root .
```

On macOS/Linux:

```
claude mcp add --transport stdio canvas-fs -- npx -y @anthropic-ai/mcp-filesystem --root .
```

After adding, check the status:

```
/mcp
```

You should see `canvas-fs` listed and connected.

**STOP -- What you just did:** You connected your first MCP server and verified it with `/mcp`. The filesystem MCP server gives Claude enhanced file operations beyond the built-in Read/Write tools. The key command pattern is `claude mcp add --transport stdio <name> -- <command>`. You will use this same pattern to add any MCP server.

**Engineering value:**
- *Entry-level:* MCP servers are like USB ports for Claude — they let you plug in new capabilities without changing Claude itself.
- *Mid-level:* In real engineering workflows, MCP connects Claude to your actual tools — Jira for ticket tracking, Figma for designs, Sentry for error monitoring. Claude stops being a code-only tool and becomes a full engineering assistant.
- *Senior+:* MCP is a standardized integration protocol — like LSP (Language Server Protocol) but for AI tool access. Building on open standards means your MCP configurations work across any AI tool that supports the protocol, not just Claude.

Shall we add a Fetch server to pull in real web content?

### 6.3 Add a Fetch MCP Server

The Fetch MCP server lets Claude pull in real content from the web -- perfect
for populating your portfolio with real data.

On Windows:

```
claude mcp add --transport stdio canvas-fetch -- cmd /c npx -y @anthropic-ai/mcp-fetch
```

On macOS/Linux:

```
claude mcp add --transport stdio canvas-fetch -- npx -y @anthropic-ai/mcp-fetch
```

Now try it out. Ask Claude to use the Fetch server to pull in real content for your portfolio. For example:

```
Using the canvas-fetch MCP server, fetch my GitHub profile and use the data to populate the projects page with real project cards.
```

Or if you do not have public repos, give Claude any URL and ask it to pull content from there:

```
Use the fetch server to grab content from [your URL] and convert it to an HTML entry for the site.
```

### 6.4 Check MCP Status

```
/mcp
```

This shows all connected servers, their status, and available tools. You
should see both `canvas-fs` and `canvas-fetch`.

**STOP -- What you just did:** You used the Fetch MCP server to pull real data from the web into your portfolio. This is a powerful pattern: instead of manually copying content, Claude can fetch, parse, and integrate external data directly. You used a natural language prompt ("fetch my GitHub profile") and Claude handled the MCP tool calls behind the scenes.

**Quick check before continuing:**
- [ ] `/mcp` shows both `canvas-fs` and `canvas-fetch` as connected
- [ ] You used the Fetch server to pull real content into your site
- [ ] The content rendered correctly in your browser

### 6.5 Create .mcp.json for Team Sharing

To share MCP configuration with your team, use the project scope:

```
claude mcp add --transport stdio canvas-fs --scope project -- npx -y @anthropic-ai/mcp-filesystem --root .
```

This creates a `.mcp.json` file at your project root:

```json
{
  "mcpServers": {
    "canvas-fs": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem", "--root", "."],
      "env": {}
    }
  }
}
```

Commit this file so teammates get the same MCP setup.

### 6.6 Understand MCP Scopes

| Scope | Where Stored | Who Sees It |
|-------|-------------|------------|
| **local** (default) | `~/.claude.json` under project path | Only you, this project |
| **project** | `.mcp.json` in project root | Everyone (via version control) |
| **user** | `~/.claude.json` | Only you, all projects |

**Why this step:** The three scopes (local, project, user) control who sees an MCP configuration. The `project` scope creates `.mcp.json` which gets committed to git -- every teammate who clones the repo gets the same MCP servers automatically. This is how you standardize a team's tool setup.

**Engineering value:**
- *Entry-level:* Committing `.mcp.json` means anyone who clones your repo gets the same MCP servers — no setup instructions to follow.
- *Mid-level:* Project-scoped MCP config is infrastructure-as-code for AI tooling. New team members clone, run `claude`, and everything just works.

### 6.7 Create a Skill That Orchestrates MCP Tools

Create a "publish" skill that combines MCP tools with built-in tools to validate and package your site for deployment. Describe the workflow to Claude:

```
Create a 'publish' skill that validates the site, generates a sitemap.xml, copies everything into a dist/ directory, minifies the CSS, and shows a deployment summary. Set disable-model-invocation to true and include mcp__canvas-fs__* in the allowed-tools so it can use the filesystem MCP server.
```

Discuss the publish steps with Claude -- you might want different minification, or maybe you want to skip certain files. This is your deployment workflow.

Test it: `/publish`

**STOP -- What you just did:** You created a skill that combines MCP tools with built-in tools into a single workflow. The `allowed-tools` frontmatter field (`mcp__canvas-fs__*`) grants the skill access to MCP server tools using the naming pattern `mcp__<server-name>__<tool-name>`. This is the Skills + MCP integration pattern -- your most powerful automation combines custom skills with external data sources.

### 6.8 Connect a Tool You Actually Use

The MCP servers you added above are local utilities -- filesystem and fetch. But MCP also connects to cloud tools you already use.

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

After adding, run `/mcp` to authenticate and verify the connection. Then try it out:

```
Using the Figma MCP server, look at my recent files and suggest which design tokens I should add to my portfolio's CSS custom properties.
```

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

- [ ] Filesystem MCP server is connected (`/mcp` shows it active)
- [ ] Fetch MCP server is connected
- [ ] You used Fetch to pull real data into the site
- [ ] `.mcp.json` exists for team sharing
- [ ] You understand the three MCP scopes (local, project, user)
- [ ] Publish skill orchestrates MCP tools to validate and package the site
- [ ] `dist/` directory contains a deployable version of the site
- [ ] Understand MCP elicitation and channels
- [ ] (Optional) You connected an MCP server for a tool you actually use
