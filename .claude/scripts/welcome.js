// SessionStart hook — outputs JSON so the welcome message is shown to the user
// and injected into Claude's context. No dependencies beyond Node (which CC requires).

const message = `
========================================
  Hey! Welcome to Learn CC by Doing
========================================

  You're about to build something real
  and pick up every Claude Code feature
  along the way — no lectures, just doing.

  4 projects. Your language. Let's go.

  Type /start and I'll walk you through it.

========================================`;

process.stdout.write(JSON.stringify({ systemMessage: message }));
