---
name: jeese-writing
description: Draft, restructure, or revise durable long-form Simplified Chinese learning notes, technical articles, retrospectives, and personal Markdown documents in Jeese's writing style. Use when source material or an existing draft should become a coherent document that can be saved, maintained, or published. For formal proposals, specifications, or PRDs, apply this skill's reasoning, organization, and voice while preserving the structure established by the task and destination project. Do not use for conversational explanations, code-only tasks, short chat replies, marketing copy, or fiction.
---

# Jeese Writing

Write clear Chinese prose in Jeese's preferred voice without mechanically copying the interview-question structure identified in `references/corpus-observations.md`.

## Load the right guidance

1. Read [references/core-style.md](references/core-style.md) for every task.
2. For learning notes, concept explanations, technical retrospectives, or personal technical articles, also read [references/learning-notes.md](references/learning-notes.md).
3. When creating or restructuring a Markdown document, also read [references/markdown-format.md](references/markdown-format.md).
4. When editing an existing document, read [references/document-maintenance.md](references/document-maintenance.md).
5. When explicitly merging multiple documents into one, read [references/document-merging.md](references/document-merging.md).
6. When drafting or substantially rewriting prose, read [references/examples-and-counterexamples.md](references/examples-and-counterexamples.md).
7. For writing about real-world probability, behavior, social or historical patterns, empirical risk, or competing explanations of actual events, also read [references/reality-judgment.md](references/reality-judgment.md).
8. Read [references/corpus-observations.md](references/corpus-observations.md) only when auditing, extending, or recalibrating this skill. Do not load it for ordinary writing.

For proposals, specifications, design documents, PRDs, incident reports, or other structured artifacts, apply the stable reasoning, organization, and voice preferences in `references/core-style.md` throughout. Determine the genre-specific structure, required sections, metadata, and heading hierarchy first from the current task and explicit destination-repository rules, then from an existing document that the user or project designates as a reference, or from stable patterns repeated across relevant documents of the same genre and audience. A single existing document establishes a convention only when the user or project identifies it as a reference; otherwise distinguish repeated practice from an author's incidental choice. If the routing list above selects a task-specific reference, use that file for the remaining task-specific defaults. An explicitly required template is part of the current task; otherwise treat a standalone blank or semi-blank template as a fallback when the stronger sources above do not establish the structure. If no applicable structure is established, organize the document around its actual content. When an applicable project structure conflicts with a default in `references/markdown-format.md`, follow the project structure while preserving all compatible rules from `references/core-style.md`.

## Establish the writing task

Before drafting, determine:

- what the reader should understand or be able to do afterward;
- what the reader already knows and which missing premise blocks understanding;
- which claims come from sources, which are the author's judgment, and which remain uncertain;
- whether the destination already has heading, metadata, citation, or formatting conventions.

Complete the necessary analysis and material synthesis before drafting. Write the most stable current understanding rather than reproducing the chronology of tentative classifications, abandoned structures, or conversational self-correction.

Inspect relevant source material and nearby destination documents when available. Use the bundled style rules, observations, and examples as writing evidence, not technical authority. Do not assume the original calibration corpus exists outside this skill. Verify factual claims from appropriate sources rather than inheriting old notes uncritically.

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
- Keep established judgments and their confidence stable unless the evidence changes. When correcting a prior claim, state what changed and why instead of presenting the correction as another angle.
- During revision, remove repeated conclusions, delayed qualifications, empty transitions, decorative headings, and fragmented bullets.
- If rewriting existing prose, preserve the author's claims and intent unless the user asked for factual correction or restructuring.

## Confirm what belongs in a technical proposal

This applies only when turning prior discussion into a technical proposal for an established project, or when revising such a proposal. Put designs that have been discussed and confirmed into the document. Keep approaches raised during discussion but not yet accepted outside the document, and ask whether to continue discussing or incorporate them. While organizing material, drafting, or performing a review explicitly requested by the user, if you naturally discover a contradiction or gap in the current design, or a candidate approach that directly serves the current goal, can reuse an existing implementation or has low adoption cost, and would materially improve correctness, feasibility, or maintenance cost, raise it separately from the document and let the user decide whether to adjust the proposal.

## Deliver the result

For file work, modify only the requested artifact and preserve unrelated local changes. If the task is an analysis rather than an edit, return the observed patterns and actionable recommendations without changing files.

Before finishing, verify that the article:

- has one stable organizing logic rather than the chronology of the conversation that produced it;
- makes actors and causal relationships explicit;
- uses conversational phrasing deliberately rather than performing a persona;
- contains no repeated summary disguised as a new angle;
- uses Markdown because it improves comprehension, not because a template demands it;
- distinguishes sourced fact, author judgment, and uncertainty where that distinction matters.
