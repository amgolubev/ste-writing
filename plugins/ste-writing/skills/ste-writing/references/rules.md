# The rules: reasons, examples and edge cases

Contents:

- [Words: rules 1–5](#words)
- [Sentences: rules 6–10](#sentences)
- [Paragraphs and lists: rules 11–12](#paragraphs-and-lists)
- [Source](#source)

## Words

### 1. One word has one meaning

**Reason.** Most misreadings come from a term with two meanings, or from two terms for one thing. A reader who sees "job" and "task" in one doc must guess whether they are the same. An agent guesses too, and its guess is not visible.

**Procedure.**

1. Find the doc that owns the term: a glossary, or the Terms section of the system that defines it.
2. Define the term there, one time.
3. In each other doc, use the term with that meaning only. If the doc format permits links, link to the definition.

| Before | After |
| --- | --- |
| "The user can cancel the job. If a task is cancelled, the worker frees the slot." (Is a task a job?) | "The user can cancel the job. If a job is cancelled, the worker frees the slot." |
| "The customer submits an order. Order the results by date." (Is "order" a purchase or a sort?) | "Order: a request from a customer to buy items." "Sort the results by date." |

**Edge cases.**

- If the doc does not define a general English word, the word keeps its general meaning. If the doc defines the word, the general meaning is not available in that doc.
- If two teams own one term with two meanings, do not select a meaning. Report the conflict.

### 2. Use the simplest common word

**Reason.** Simple words are known to more readers, and they have fewer meanings. See `word-list.md`.

| Before | After |
| --- | --- |
| "Utilize the CLI in order to commence the migration." | "Use the CLI to start the migration." |
| "Prior to deployment, ascertain that the flag is enabled." | "Before you deploy, make sure that the flag is enabled." |

**Edge case.** A technical term is not a complex word. If the domain uses "idempotent", "mutex" or "checksum", keep the term. Define them per rule 1.

### 3. Use verbs for actions

**Reason.** A noun made from a verb hides the actor and adds words.

| Before | After |
| --- | --- |
| "Validation of the input is performed by the parser." | "The parser validates the input." |
| "Synchronization of the replicas occurs after the commit." | "The replicas synchronize after the commit." |

### 4. "must", "can", "cannot" in rules

**Reason.** "Should" can be an obligation or a recommendation. "May" can be a permission or a possibility. A test cannot check a rule with two possible meanings.

| Word | Meaning | Test |
| --- | --- | --- |
| must | Obligation | A failure is a defect. |
| must not, cannot | Prohibition | The action is a defect. |
| can | Permission or capability | Both outcomes are correct. |

| Before | After |
| --- | --- |
| "The API should return 404 for a missing ID." | "The API must return 404 for a missing ID." (If the author decides that it is an obligation.) |
| "Users may skip the onboarding." | "The user can skip the onboarding." |
| "The cache might be stale after a deploy." | "After a deploy, the cache can be stale." (Description of a possibility.) |

**Edge case.** In a conversion, a change from "should" to "must" or "can" changes the meaning. Ask the owner. Do not select one yourself.

**Edge case.** A recommendation that is not a rule can stay as a recommendation, but write it as one: "We recommend X, because Y."

### 5. Keep "a", "the" and "that"

**Reason.** Without articles, a reader cannot tell a noun from a verb. "Update record" is an instruction or a name. "Update the record" is an instruction.

| Before | After |
| --- | --- |
| "Check value is valid before save." | "Make sure that the value is valid before you save it." |

## Sentences

### 6. One topic in each sentence

**Reason.** A sentence with two topics has two places for an error, and a review finds only one of them.

| Before | After |
| --- | --- |
| "The worker reads the queue and, because the queue can be empty, it waits 5 s, which also lets the scheduler run." | "The worker reads the queue. If the queue is empty, the worker waits 5 s. During the wait, the scheduler can run." |

### 7. Sentence length: 20 words for a rule or step, 25 for a description

**Reason.** Long sentences hide conditions and exceptions. The limits come from ASD-STE100.

**How to count.** A word is a group of characters between spaces. A number is a word. A hyphenated word is one word. Inline code is one word.

**Edge case.** A list in prose can make a sentence long: "The actor is the user, an administrator, a service account or the scheduler." If it has 3 or more items and the items are long, use a list (rule 12).

### 8. Active voice and present tense

**Reason.** The active voice names the actor. The present tense describes what the system does. The future tense ("will") adds a word and makes a rule sound like a plan.

| Before | After |
| --- | --- |
| "The file will be deleted after 30 days." | "The system deletes the file after 30 days." |
| "An error is raised." | "The parser raises an error." |

**Edge case.** If the actor is not known or not important, the passive voice is correct: "The data is encrypted at rest."

### 9. The condition first

**Reason.** The reader must know the condition before the action. If the action comes first, a reader can start the action before the reader reads the condition.

| Before | After |
| --- | --- |
| "Restart the service if the health check fails." | "If the health check fails, restart the service." |
| "The job retries unless it is cancelled." | "If the job is not cancelled, it retries." |

### 10. A list, not a chain of clauses

| Before | After |
| --- | --- |
| "The build fails if the lint fails; the tests fail; or the bundle is larger than 2 MB." | "The build fails if one of these occurs:<br>- The lint fails.<br>- A test fails.<br>- The bundle is larger than 2 MB." |

## Paragraphs and lists

### 11. One topic in each paragraph, 6 sentences or fewer

**Reason.** A reader finds a topic by its paragraph. An agent that reads one part of a doc gets the full topic.

### 12. Numbered lists for steps, lists for 3 or more items

**Reason.** A numbered step can be referred to ("step 3"), and a reader can do the steps in order. A list shows that items are parallel.

- If the order is important, use a numbered list.
- If the order is not important, use a bulleted list.
- Each item in a list has the same grammar: all items are sentences, or all items are noun phrases.
- A list with one or two items can be a sentence.

## Source

- ASD-STE100, Simplified Technical English, issue 8 (2021) or later. Part 1 contains the writing rules. The standard and its dictionary are available from ASD on application: https://www.asd-ste100.org/
- This skill uses a subset of the writing rules. It does not reproduce the dictionary of approved words.
