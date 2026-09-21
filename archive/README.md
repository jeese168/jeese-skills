# Skill 归档记录

这里保存退役 Skill 与重构前的冻结版本，便于追溯原有规则与迁移原因。日常维护和平台发现使用 `skills/` 下的现役源码；归档内容不作为现役 Skill 的运行依赖。

## jeese-change-review

- 归档日期：2026-09-19。
- 存档：[jeese-change-review/](jeese-change-review/)，从原 `skills/jeese-change-review/` 原样移动，保留归档时的入口、references 和平台元数据。
- 原因：原有审查与修改讲解能力，与 `jeese-engineers` 中用户实际使用的协作方式重叠。将仍适用的规则按职责迁入新 Skill，统一维护和调用入口。

| 原有内容 | 现役位置与用途 |
| --- | --- |
| 按对象和项目环境选择审查标准、证据要求、逐项组织发现 | [审查判断与发现要求](../skills/jeese-engineers/references/review-findings.md)，由情况二按任务写入[完整送审指令](../skills/jeese-engineers/references/review-brief.md) |
| 独立审查指定技术文档 | [情况三：独立文档核查](../skills/jeese-engineers/references/document-review.md)，收窄为明确触发的文档一致性核查 |
| 解释已完成的修改、前后证据和精确修改示例 | [情况五：讲解改动](../skills/jeese-engineers/references/explain-changes.md)及[精确修改示例](../skills/jeese-engineers/references/precise-edits.md) |

迁移按用户确认的使用场景整理，没有保留旧版泛用的独立代码、配置审查入口。当前工程任务通过情况二生成审查指令，审查窗口直接执行；低频的已有文档核查由新的情况三处理。旧版的归档元数据仅保留历史，不代表仍推荐安装或调用。

## jeese-explaining-preview

- 归档日期：2026-09-21。
- 存档：[jeese-explaining-preview/](jeese-explaining-preview/)，完整复制普通版重构前的 `skills/jeese-explaining/`，仅调整副本的 Skill 名称、入口标题和平台显示、调用名称。
- 原因：在普通版重构前保留现有讲解规则，作为预览版归档供后续对照。
- 现役源码仍位于 `skills/jeese-explaining/`，已按五种情况重构为普通版；归档副本保持冻结，不作为另一份维护源码或现役 Skill 的运行依赖。
