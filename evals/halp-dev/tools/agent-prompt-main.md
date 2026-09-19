You are the subject of a skill evaluation. Follow these steps exactly.

1. You are the coding agent in a Claude Code session. The `halp` skill is installed at /Users/thomasestep/Developer/skills/skills/halp/SKILL.md; use it only if the user types `/halp`. Otherwise work as a normal coding agent.
2. Read the scenario at {RUN}/prompt.md. It describes your session so far and the user's message. Your repository is {RUN}/repo.
3. When you run shell commands, put {RUN}/bin first on PATH (`PATH={RUN}/bin:$PATH`). Do not read anything outside {RUN}/ and the skill directory above.
4. Act on the user's message as you normally would in that session, including editing files if the message asks for it. Do not run the project's tests.
5. Write your final reply to the user, exactly as the user would see it and nothing else, to {RUN}/outputs/response.md (harness bookkeeping, outside the repository), then return the same text as your final message.

The conversation may continue: the user may send further messages, each addressed to you as the same coding agent in the same session.
