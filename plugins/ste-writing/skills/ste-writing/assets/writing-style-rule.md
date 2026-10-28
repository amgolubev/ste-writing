---
paths:
  - "<docs folder>/**"
  - "<specs folder>/**"
  - "**/*.md"
---

# Writing Style

<!-- Fill in each <...> item. Delete the `paths:` front matter if the agent does not support it. -->

Write the docs in <folders> with the principles of ASD-STE100 (Simplified Technical English). Use the principles only. The licensed dictionary is not used.

## Words

1. One word has one meaning. Define each domain term one time, in <the glossary at path | the Terms section of the doc that owns it>. Do not use a synonym for a defined term.
2. Use the simplest common word: "use", not "utilize"; "start", not "commence".
3. Use verbs for actions, not nouns made from verbs: "the service restarts", not "a restart of the service occurs".
4. In rules, "must" is an obligation, "can" is a permission and "cannot" is a prohibition. Do not use "should", "may" or "might" in rules.
5. Do not remove "a", "the" or "that" to make a sentence shorter.

## Sentences

6. Write one topic in each sentence.
7. A rule or a procedure step has <20> words or fewer. A descriptive sentence has <25> words or fewer.
8. Use the active voice and the present tense.
9. Put the condition first: "If X, Y."
10. Use a list, not a chain of clauses with semicolons.

## Paragraphs and lists

11. Write one topic in each paragraph, with <6> sentences or fewer.
12. Use a numbered list for steps. Use a list for 3 or more items.

## Scope

- Apply these rules to new text and to each text that a task edits.
- Do not edit history entries (<changelog, decision log, meeting notes>) only to change their style.
- <User-facing text>, code, code blocks and quoted text are out of scope.
- A rewrite must keep the meaning of each rule. If a rewrite changes a meaning, keep the old text and ask <the owner>.
