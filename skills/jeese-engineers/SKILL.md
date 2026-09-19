---
name: jeese-engineers
description: >-
  Handle Jeese's dual-window engineering handoff when explicitly invoked as
  jeese-engineers: list absolute paths of files actually written to disk
  (this-round incremental or feature-related full), generate an objective
  review brief, write review findings from user-assembled materials,
  independently verify another agent's review into three dispositions, or
  explain a completed change at the asked scope. Use only when the user
  explicitly invokes this skill or names jeese-engineers. Do not use for
  ordinary conversation, long-form writing, OpenSpec planning, or as a
  substitute for jeese-explaining, jeese-writing, or jeese-change-review.
---

# Jeese Engineers

这是执行窗口和审查窗口之间的交接协议。用户自己搬运材料，各窗口只交本轮指定的那一种产物。用户点名本 Skill 之后才按下面的情况工作。

先判断**这一轮要交的产物是哪一种**。五种情况互斥：一次只走一条。用户指定了产物，就按指定走；没指定时，按这条消息里贴来的材料认；材料和指定都没有，再停下来问，或按当前窗口进度给一个推荐。对照少样本：[指定了就按指定、有材料就按材料](references/examples-and-counterexamples.md#指定了就按指定有材料就按材料)、[只有点名时询问或按进度推荐](references/examples-and-counterexamples.md#只有点名时询问或按进度推荐)。

**用户指定了。** 这句话里已经点明要路径、审查指令、审查发现、三类核实，或只讲某一个改动点：按指定进入对应情况。用户偷懒只写了 `/jeese-engineers`，但同一条消息里已经带了材料的，仍先看材料，不把「没写要干什么」当成空调用。

**没指定，但材料对得上。** 靠材料形状就能分开、不必再问的，主要是这两种：

- 贴来的是给审查窗口用的那一包：审查指令，加上被审的方案原文，或落盘文件的绝对路径和路径说明 → 情况三，写发现。
- 贴来的是审查窗口已经写好的发现：按条列出对象、问题、建议，要执行窗口消化 → 情况四，核实成三类。

审查指令加被审对象，和「已经写好的审查发现」，不是同一类材料。前一种是送去审的；后一种是审完送回来的。情况一、二、五主要靠你指定要路径、要审查指令、或要讲某一个改动；空调用时用下面的询问或推荐。五种情况不必拆成五个 Skill。

**只有点名。** 用户就是发了 `/jeese-engineers` 或同等点名，同一条里没有指定、也没有上面那些材料：停下来问这一轮要交什么。问法跟着当前窗口走，可以给一个推荐，例如刚改完代码、路径还没交，推荐先做情况一；路径已经有了、审查指令还没有，推荐情况二。推荐之后等用户应一声再做。五种产物做成固定选择题、每轮都点一遍，不是这一步要的问法。

认准后再读取对应 reference，只读这一条，并按该文件指出的少样本标题对照。

用户说「全量」或「存量」时，都按全量处理：收齐和当前功能、需求相关的已落盘文件。用户说「增量」时，只收这一轮实际落盘的文件。

## 情况一：列出实际落盘文件的绝对路径

在下面任一时机进入：

- 用户让执行窗口开始写方案、写代码、写文档、改 Skill 或改配置，并顺带点名本 Skill，要求做完后交出落盘路径；
- 正事已经做完，用户单独点名，只要路径和路径说明，不再另写提示词。

先确认这一轮是增量还是全量。用户在当前这句话、或同一任务里已经说过，就按已说的执行。当前也没说、前面也没说时：只问这一句，问清之前停在提问。正事还没开始的，确认范围后再开始改文件。

确认之后：若用户是在开始干活时顺带点名的，先完成用户要的正事，等实际落盘结束，再交路径。若用户只是单独来要路径，只交路径。

产物是已经写到磁盘上的绝对路径，并说明每个路径在本任务里是什么。范围包括代码、文档、Skill、配置。

读 [references/landed-paths.md](references/landed-paths.md)。

## 情况二：生成给审查窗口用的指令

时机是改完、输出完，也包括情况一的路径已经整理完之后，用户再点名，要求生成审查指令。

产物是直接打在对话里的一份审查指令。这份指令足够让另一个窗口按材料审查，并且对执行窗口自己保持客观。

读 [references/review-brief.md](references/review-brief.md)。

用户会自己把原始材料或路径包起来，再拼上这份指令，贴到审查窗口。拼接是用户的工作。

## 情况三：审查窗口根据用户拼好的材料写发现

用户贴来的是拼接好的送审包：被审的技术方案原文，或落盘文件的绝对路径及说明，外加给审查窗口用的指令。用户点了要审查、找问题，或只在材料首尾加了本 Skill 的点名，都走这里。

产物是直接打在对话里的审查发现。按条写问题：对象是什么、为什么成立、建议怎么改。这一窗口只报告发现。

读 [references/review-findings.md](references/review-findings.md)。

同一审查窗口里，第一轮之后用户只用很短的话再审一轮时，仍按情况三，沿用已经加载的规则。

## 情况四：执行窗口把审查结论核实成三类

用户把审查窗口写好的发现丢回执行窗口。用户点了核实、分类、整理成三类，或只在这份发现的首尾加了本 Skill 的点名，都走这里。

先对着方案、用户给出的路径或磁盘上的实际文件自己查，再划分：

1. **认可**：执行窗口确认这项成立，可以采纳；
2. **不采纳**：审查方信息不全、指令没把上下文说清、或判断错误；
3. **争议、待用户判断**：和审查有分歧，或两边都认为该改、但还要用户自己判断或去问产品、leader、客户端。这一类写清争议点，并给出参考意见和推荐选项。

产物是这三类的整理说明。这一轮只整理。

读 [references/review-disposition.md](references/review-disposition.md)。

## 情况五：讲已经改了什么

在中间或更晚，用户要求讲清楚已经发生的改动时进入。再看用户要的是哪一种深度：

- 用户只问某一个点、某一处行为、某一个文件为什么这样改：只答这一点，让用户能接着读代码或接着问下一句。
- 用户要拿去做笔记、归纳、沉淀，或明确要求把相关改动讲全：按磁盘上的实际改动把该讲的部分讲完整。

读 [references/explain-changes.md](references/explain-changes.md)。

## 少样本

正例和反例在 [references/examples-and-counterexamples.md](references/examples-and-counterexamples.md)。各情况的 reference 会指向需要对照的标题。进入某一情况时读那些标题，不必整份通读。
