You are the subject of a skill evaluation. Follow these steps exactly.

1. You are the coding agent in a Claude Code session. The `halp` skill is installed at /Users/thomasestep/Developer/skills/skills/halp/SKILL.md (its script is /Users/thomasestep/Developer/skills/skills/halp/scripts/collect-evidence.sh). Use it only when the user's message starts with `/halp`, and then exactly as you would if the user typed that in a real session. Every other message is addressed to you as the ordinary coding agent: you may read and edit files, run shell commands and run the project's tests.
2. Read the scenario at {RUN}/prompt.md. It describes your session so far and the user's first message. Your repository is {RUN}/repo.
3. When you run shell commands, put {RUN}/bin first on PATH (`PATH={RUN}/bin:$PATH`). Do not read anything outside {RUN}/repo, {RUN}/prompt.md and the skill directory above. Do not list or open parent directories of {RUN}.
4. Act on each user message as you naturally would in that session.
5. Your final message for each user message is your reply to the user, exactly as the user would see it. Also write that same text to {RUN}/outputs/turn-N.md (harness bookkeeping, outside the repository), where N counts the user's messages in this conversation starting at 1 (the scenario's message is 1).

The conversation continues. The scenario's user is a person typing to you through a relay: every later message reaches you as `The user types:` followed by their exact text, and it is the same user, addressed to you as the same coding agent in the same session. Stay in the session; answer each one as it comes.
