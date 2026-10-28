---
name: ste-writing
description: Write, review and convert technical documentation in the style of Simplified Technical English (ASD-STE100 principles, without the licensed dictionary). Use this skill whenever someone asks to make docs clearer, plainer or less ambiguous; to apply STE, ASD-STE100 or a "controlled language"; to rewrite specs, requirements, rule docs, design docs, READMEs, runbooks, procedures or agent instructions for non-native readers or for LLM agents; to check docs for long sentences, passive voice or vague "should/may" rules; or to install a writing-style rule in a repository. Use it also when a team reports that readers or agents misread a term, even if nobody names STE.
---

# STE-style writing

This skill applies the principles of ASD-STE100 (Simplified Technical English) to technical text. It uses the principles only. It does not use the licensed STE dictionary.

The style has three effects:

- A term has one meaning, so a reader or an agent cannot pick the wrong meaning.
- A rule uses "must", "can" or "cannot", so each rule is testable.
- Short sentences cost fewer tokens and less interpretation in each read.

## Select the job

| Request | Workflow |
| --- | --- |
| Write new text in this style | [A. Write](#a-write) |
| Check text and report problems, with no edits | [B. Review](#b-review) |
| Rewrite existing docs in this style | [C. Convert](#c-convert) |
| Make the style a standing rule in a repository | [D. Install the rule](#d-install-the-rule) |

If the request is not clear, ask which job the user wants. A conversion changes files. A review does not.

## The rules

Read `references/rules.md` for the reason, examples and edge cases of each rule. Read `references/word-list.md` when you select words.

**Words**

1. One word has one meaning. Define each domain term one time, in the doc that owns it. Do not use a synonym for a defined term.
2. Use the simplest common word: "use", not "utilize"; "start", not "commence".
3. Use verbs for actions, not nouns made from verbs: "the service restarts", not "a restart of the service occurs".
4. In rules, "must" is an obligation, "can" is a permission and "cannot" is a prohibition. Do not use "should", "may" or "might" in rules.
5. Do not remove "a", "the" or "that" to make a sentence shorter.

**Sentences**

6. Write one topic in each sentence.
7. A rule or a procedure step has 20 words or fewer. A descriptive sentence has 25 words or fewer.
8. Use the active voice and the present tense.
9. Put the condition first: "If X, Y."
10. Use a list, not a chain of clauses with semicolons.

**Paragraphs and lists**

11. Write one topic in each paragraph, with 6 sentences or fewer.
12. Use a numbered list for steps. Use a list for 3 or more items.

The limits in rules 7 and 11 are defaults. A team can change them in its installed rule.

## Scope

Apply the rules to technical prose: rules, specs, procedures, descriptions and agent instructions.

Do not change these items:

- Code, code blocks, inline code, identifiers, file paths, commands and log output.
- Quoted text, proper names and product names.
- User-facing UI text, marketing text and legal text. If the user asks for them, they are in scope.
- History entries: changelogs, decision logs, devlogs, meeting notes, accepted ADR decisions. A history entry records what someone wrote at that time. Do not edit it only to change its style.
- Rule numbers, IDs, anchors and headings that other docs link to.

## The checker

`scripts/ste_check.py` reads Markdown or plain text and prints observations. It does not give a pass or fail verdict, and its exit code is always 0. The script cannot see the meaning of a sentence, so a person or the model decides each fix.

```bash
python3 scripts/ste_check.py docs/rules.md design/*.md
python3 scripts/ste_check.py --rule-limit 20 --desc-limit 25 --para-limit 6 --json docs/
```

It skips front matter, code blocks, inline code and headings. It reports these codes:

| Code | Observation | Rule |
| --- | --- | --- |
| `LEN` | A sentence is longer than its limit. A sentence with "must", "cannot" or "must not", and each numbered step, uses the rule limit. | 7 |
| `PARA` | A paragraph has more sentences than the limit. | 11 |
| `MODAL` | "should", "may", "might", "could" or "would". | 4 |
| `FUTURE` | "will" or "won't". | 8 |
| `PASSIVE` | A form of "be" with a past participle. | 8 |
| `NOUN` | A noun made from a verb, with a weak verb ("perform an update", "a check occurs"). | 3 |
| `COND` | "if" or "unless" after the start of the sentence. | 9 |
| `SEMI` | A semicolon in a sentence. | 10 |
| `WORD` | A word from `references/word-list.md`, with its simple replacement. | 2 |

The script cannot find synonyms, words with two meanings, removed articles or mixed topics (rules 1, 5, 6). Check these items yourself.

Some observations are correct text. Examples:

- "May" as a month.
- A passive sentence where the actor is not known.
- A GIVEN/WHEN/THEN acceptance criterion. Apply the length limit to each clause, not to the full criterion.
- A semicolon that separates values in a table cell.

Do not make text worse only to remove an observation.

## A. Write

1. Find the term owner: the glossary or the Terms section of the doc that defines the domain. Use its terms with their defined meanings.
2. If you need a new term, define it one time, in the doc that owns it. Tell the user about the new term.
3. Write the text with the rules.
4. Run the checker on the new text. Fix each correct observation.

## B. Review

1. Run the checker on each file.
2. Read the text for rules 1, 5 and 6, because the script cannot check them.
3. Report the findings in this order:
   1. Terms with two meanings.
   2. Terms with synonyms.
   3. Rules with "should" or "may".
   4. The other observations, by count.
4. For each finding, give the line, the problem and one suggested rewrite. Do not edit the files.

## C. Convert

A conversion must keep the meaning of each rule. A clearer rule with a different meaning is a defect, because readers follow the new text and nobody decided the change.

1. Agree on the list of docs and their order with the user. Start with the docs that define terms and rules, because other docs use their terms.
2. For each doc, run the checker. Keep the counts as the baseline.
3. Make a term inventory. For each domain term, record the doc that owns it and its definition. Record each term with two meanings and each group of synonyms. Show the inventory to the user before the rewrite. The owner of the domain selects the term to keep.
4. Rewrite the doc one section at a time. Keep the structure, headings, IDs, rule numbers, links and table columns. Do not add content and do not remove content.
5. Do a meaning check on each changed rule. Compare these items in the old text and the new text:
   - The actor.
   - The condition.
   - Each number and unit.
   - The strength of the modal.
   - Each exception.
   - The order of the steps.
6. If a rewrite changes a meaning, or if you are not sure, keep the old text. Record it as a finding for the user.
7. Do not change "should" or "may" to "must" or "can" without a decision from the user. "Should" can mean an obligation or a recommendation. The text does not tell you which meaning the author had.
8. Run the checker again. Compare the counts with the baseline.
9. Show the diff and the report to the user, one doc in each review. Commit a doc only after the user approves it, and only if the repository rules permit the commit.

If a doc is longer than about 300 lines, show it in parts, one part for each review.

### Conversion report

Use this template for each doc:

```markdown
## <file path>

Checker: <before total> → <after total> observations (LEN a→b, MODAL c→d, PASSIVE e→f, ...)

Terms defined here: <term>, <term>, ...
Terms with two meanings: <term>: <meaning 1> / <meaning 2>. Kept: <selection or "decision needed">
Synonyms removed: <synonym> → <defined term>

Meaning findings (old text kept):
1. <rule ID or line>: <old text> | <proposed text> | <the possible change of meaning>

Modal decisions needed:
1. <rule ID or line>: "should" → "must" or "can"?

Not changed (out of scope): <code blocks, quotes, history entries, ...>
```

## D. Install the rule

1. Ask the user for these items:
   - The folders and file types that the rule applies to.
   - The exclusions, for example user-facing text, code or history logs.
   - The word and sentence limits. The defaults are 20, 25 and 6.
   - The location of the term owner: one glossary, or a Terms section in each doc.
2. Copy `assets/writing-style-rule.md`. Fill in the answers.
3. Put the rule where the agents and the people of the repository read it:
   - Claude Code: `.claude/rules/writing-style.md`. The `paths:` front matter loads the rule when a session reads or edits a matching file.
   - Other agents: a section in `AGENTS.md`, `CLAUDE.md` or the equivalent instruction file.
   - People: `CONTRIBUTING.md` or the docs style guide.
4. Tell the user to record the decision where the team records decisions.
5. Offer to convert the existing docs with workflow C. Apply the rule to new text and to each text that a task edits. A full conversion of old docs is a separate task.

## Frequent errors

- **Telegraphic text.** A writer removes articles to make a sentence shorter: "Check config, restart service." Write "Check the configuration. Restart the service."
- **A lost link between a condition and its result.** A split sentence must keep the condition with its result. Write "If the queue is full, the producer stops." Do not write "The queue can be full. The producer stops."
- **An unclear pronoun.** If "it" or "this" can refer to two nouns, repeat the noun.
- **A new definition.** Do not write a definition that the source does not give. Ask the owner of the domain.
- **A list with one item.** Use a sentence.
