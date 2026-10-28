# ste-writing

An agent skill that writes, reviews and converts technical documentation in the style of Simplified Technical English (ASD-STE100).

The skill uses the writing principles of ASD-STE100. It does not include the licensed STE dictionary.

## What the style does

- A term has one meaning, so a reader or an agent cannot pick the wrong meaning.
- A rule uses "must", "can" or "cannot", so each rule is testable.
- Short sentences cost fewer tokens and less interpretation in each read.

## What the skill does

| Job | Result |
| --- | --- |
| Write | New text that follows the 12 rules and uses the defined terms of the project. |
| Review | A list of findings with a suggested rewrite for each. The files do not change. |
| Convert | A rewrite of existing docs, one doc in each review. Each rule keeps its meaning. If a rewrite changes a meaning, the old text stays and the skill reports a finding. |
| Install the rule | A writing-style rule file for your repository: `.claude/rules/`, `AGENTS.md`, `CLAUDE.md` or `CONTRIBUTING.md`. |

The skill includes `ste_check.py`. This script reads Markdown or plain text and reports observations:

- Long sentences and long paragraphs.
- "should", "may", "might" and "will".
- The passive voice.
- Nouns made from verbs.
- Conditions after the start of a sentence.
- Semicolons.
- Complex words, with a simple replacement.

The script gives observations, not a verdict. Its exit code is 0.

```bash
python3 plugins/ste-writing/skills/ste-writing/scripts/ste_check.py docs/
```

## Install

### Claude Code

```bash
claude plugin marketplace add amgolubev/ste-writing
claude plugin install ste-writing@ste-writing
```

In a session, run `/ste-writing:ste-writing`, or ask Claude to "rewrite this doc in STE style".

### Claude.ai

1. Download `ste-writing.skill` from [`dist/`](dist/ste-writing.skill).
2. In Claude.ai, open the settings for skills and upload the file.

### Other agents, or a manual install

Copy the folder `plugins/ste-writing/skills/ste-writing/` to the skills folder of your agent. For Claude Code, the folders are `~/.claude/skills/` for one user and `.claude/skills/` for one project.

## Contents

```
plugins/ste-writing/skills/ste-writing/
├── SKILL.md                      # rules, scope, workflows, report template
├── references/rules.md           # the reason, examples and edge cases of each rule
├── references/word-list.md       # complex word → simple word; the checker reads it
├── assets/writing-style-rule.md  # a rule file with blanks for your repository
└── scripts/ste_check.py          # the checker
```

## Contribute

To add a pair of words, add a row to `references/word-list.md`. To report a false observation of the checker, open an issue with the sentence.

## Disclaimer

This project is not affiliated with ASD (AeroSpace and Defence Industries Association of Europe). ASD-STE100 is the specification of ASD. To get the full specification and its dictionary, apply to ASD at https://www.asd-ste100.org/.

## License

[MIT](LICENSE)
