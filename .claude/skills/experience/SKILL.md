---
name: experience
description: Change your curriculum experience level (beginner / intermediate / advanced) mid-course. Takes effect immediately.
disable-model-invocation: true
---

# /experience — Adjust Your Teaching Level

The learner picked an experience level during `/start` onboarding. This skill lets them adjust it mid-course without restarting. Level changes are normal — treat them as a calibration, not a confession of difficulty. Do NOT say "no shame in either direction" or similar framing to the user; the skill should just make the change and confirm it.

## Steps

1. **Read `CLAUDE.local.md` from the cc-self-train root.** Find the `Experience Level` line (e.g., `Experience Level: beginner`). If the file doesn't exist, say: "I don't see an active project yet. Run `/start` first — it collects your experience level as part of onboarding."

2. **Ask using `AskUserQuestion`:**

   - **Question:** "Where are you now?"
   - **Options** (three):
     - `New` — "Bootcamp grad, student, or first dev tools. We'll explain every concept and pace slowly."
     - `Some experience` — "1-3 years professional. We'll skip git basics and setup, move faster."
     - `Experienced` — "3+ years, comfortable with terminals/git/package managers. Straight to CC-specific depth."

3. **Map the choice to a level:**
   - `New` → `beginner`
   - `Some experience` → `intermediate`
   - `Experienced` → `advanced`

4. **Update `CLAUDE.local.md`.** Rewrite the `Experience Level:` line with the new value. If the file contains an `Effective Level:` line, rewrite that to match too — the adaptive system may re-adjust Effective Level on the next module boundary based on engagement patterns, and that's fine. This just resets the baseline.

5. **Print ONE short confirmation line:**

   > "Got it — I'll teach at the **<new level>** level from here. Change again anytime with `/experience`."

   Where `<new level>` is `beginner`, `intermediate`, or `advanced` (lowercase).

## Tone rules

- One-line confirmation. No preamble ("Great choice!"), no trailing explanation ("This means...").
- Treat the change as routine. Don't congratulate them for leveling up; don't reassure them for leveling down.
- If the new level equals the current level, just say: "Already at **<level>** — nothing changed." Don't rewrite the file unnecessarily.
