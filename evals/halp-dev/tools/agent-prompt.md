You are the subject of a skill evaluation. Follow these steps exactly.

1. Read the skill at /Users/thomasestep/Developer/skills/skills/halp/SKILL.md. Its script is at /Users/thomasestep/Developer/skills/skills/halp/scripts/collect-evidence.sh. Use the skill exactly as you would if the user typed `/halp` in a real session.
2. Read the scenario at {RUN}/prompt.md. It describes your session so far and the user's message. Your repository is {RUN}/repo.
3. When you run shell commands, put {RUN}/bin first on PATH (`PATH={RUN}/bin:$PATH`): it holds the `gh` available in this environment. Do not read anything outside {RUN}/ and the skill directory above.
4. Act as the coding agent in that session and answer the user's message.
5. Write your reply to the user, exactly as the user would see it and nothing else, to {RUN}/outputs/response.md (harness bookkeeping, outside the repository), then return the same text as your final message.

The conversation may continue: the user may send further messages, and each later message is addressed to you as the same coding agent in the same session. Respond to those as you naturally would; you need not write later replies to a file.
