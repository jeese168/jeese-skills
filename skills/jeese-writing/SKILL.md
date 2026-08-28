---
name: jeese-writing
description: Draft, restructure, or revise long-form Simplified Chinese learning notes, technical explainers, and personal technical articles in Jeese's writing style. Use for Chinese Markdown prose that should be direct, causally connected, naturally structured, mildly conversational, and free of repetitive AI framing. For formal proposals, specifications, or PRDs, use this skill only as the voice layer and preserve the document's own required structure. Do not use for code-only tasks, short chat replies, marketing copy, or fiction.
---

# Jeese Writing

Write clear Chinese prose in Jeese's preferred voice without copying the interview-question format of the source corpus.

## Load the right guidance

1. Read [references/core-style.md](references/core-style.md) for every task.
2. For learning notes, concept explanations, technical retrospectives, or personal technical articles, also read [references/learning-notes.md](references/learning-notes.md).
3. When creating or restructuring a Markdown document, also read [references/markdown-format.md](references/markdown-format.md).
4. When drafting or substantially rewriting prose, read [references/examples-and-counterexamples.md](references/examples-and-counterexamples.md).
5. Read [references/corpus-observations.md](references/corpus-observations.md) only when auditing, extending, or recalibrating this skill. Do not load it for ordinary writing.

Do not invent a genre profile. For proposals, specifications, design documents, PRDs, incident reports, or other structured artifacts, follow the user's template and the destination repository's conventions first. Apply only the shared voice rules from `core-style.md` unless a dedicated profile is later added.

## Establish the writing task

Before drafting, determine:

- what the reader should understand or be able to do afterward;
- what the reader already knows and which missing premise blocks understanding;
- which claims come from sources, which are the author's judgment, and which remain uncertain;
- whether the destination already has heading, metadata, citation, or formatting conventions.

Inspect relevant source material and nearby destination documents when available. Treat the interview-note corpus as style evidence, not technical authority. Verify factual claims from appropriate sources rather than inheriting old notes uncritically.

## Build the article around its subject

Find the subject's natural structure before choosing Markdown. Group tightly related facts, causes, mechanisms, examples, and consequences into one coherent explanation. Separate modules only when they answer genuinely independent reader questions.

For a concept or mechanism, the usual cognitive order is:

1. state what it is or give the decisive conclusion;
2. explain why it exists or which problem creates the need;
3. show the actors, objects, mechanism, or sequence;
4. use a concrete example when abstraction remains high;
5. explain the result, cost, boundary, or selection condition.

This is a reasoning order, not a mandatory five-section template. Omit steps that add no information. Do not turn every item into a heading.

When explaining a collaborative system, permission model, workflow, or UI operation, explicitly identify **who acts, on what object, where the action occurs, what state changes, and who is affected**. Never hide the actor behind vague second-person wording such as “你点击后就会……”.

## Draft and revise

- Write the first complete explanation before polishing individual sentences.
- Explain each concept sufficiently at its first occurrence; do not scatter missing premises across distant sections.
- Let paragraphs carry connected thought. Use lists, tables, code, diagrams, or quotes only when the information itself has that structure.
- Preserve useful uncertainty. Do not convert inference or preference into fact.
- During revision, remove repeated conclusions, delayed qualifications, empty transitions, decorative headings, and fragmented bullets.
- If rewriting existing prose, preserve the author's claims and intent unless the user asked for factual correction or restructuring.

## Deliver the result

For file work, modify only the requested artifact and preserve unrelated local changes. If the task is an analysis rather than an edit, return the observed patterns and actionable recommendations without changing files.

Before finishing, verify that the article:

- has one stable organizing logic rather than the chronology of the conversation that produced it;
- makes actors and causal relationships explicit;
- uses conversational phrasing deliberately rather than performing a persona;
- contains no repeated summary disguised as a new angle;
- uses Markdown because it improves comprehension, not because a template demands it;
- distinguishes sourced fact, author judgment, and uncertainty where that distinction matters.
