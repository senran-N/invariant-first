# 从使用反馈提炼工程机制

本文件是维护依据，不是执行时逐条匹配的故障表。行动以 [共同判断](../RULES.md) 和当前子技能为准。论坛观察用于提出疑问，项目源码用于理解机制；二者都不能独立证明某条提示对所有模型有效。

## 已有材料怎样归并

| 共同判断 | 材料提供的线索 | 当前方法 |
| --- | --- | --- |
| 由目标决定行动 | 越界、意图误读和流程挤占目标；A7–A8 | 主路线约束交付与操作范围，专项只补判断 |
| 表示与责任 | 正确文件中仍可能选错修改层；A4、成熟实现 | 追事实与保证的归属，在责任处修改 |
| 在边界内完成变化 | 半成品、遗漏相关行为和遗留路径；A1–A2、既有现场材料 | 贯通真实入口，区分变化与保留，完成切换 |
| 保护与事实 | 包/API 假设、状态和依赖风险；A5、成熟实现 | 当前版本与真实边界决定动作，不从名称猜测 |
| 有区分力的反馈 | 自报结果、无信息循环和自评局限；A1、A4、A7、A11 | 实际执行目标逻辑，以独立预期修正实现 |
| 产品事实与接续 | 跨会话遗漏、文档膨胀及过时约束；A1、A3、A9–A10 | 短入口指向权威位置，知识按责任存放 |

原始 [现场材料](field-notes-2026-09-19.md) 与 [源码样本](source-lessons.md) 保留核查坐标；它们不是新增禁令的模板。模型、框架和故事名从执行判断中去掉，不影响真正必要的语义与风险差异。

## 本轮归纳依据 · 2026-09-19

**社区线索。** [Cursor 讨论](https://forum.cursor.com/t/why-does-cursor-ignore-rules/137219) 中用户报告规则未得到遵循；后续一位用户表示处理格式与冲突后情况改善，不能据此断言所有失效都由规则长度造成。[V2EX 讨论](https://www.v2ex.com/amp/t/1119929) 描述维护已有结构的困难，以及提示要求增多后产生额外抽象的体验。这些是个体观察，不作为发生率或对某模型的普遍结论。

**成熟机制。** Linux `v6.12` 的 [list.h](https://github.com/torvalds/linux/blob/v6.12/include/linux/list.h) 用表头自环表示空链表，添加与删除围绕相邻节点关系；同文件仍保留硬化检查。借鉴的是用表示统一操作，不是删除保护。Go `go1.23.2` 的 [io.go](https://github.com/golang/go/blob/go1.23.2/src/io/io.go) 用 Reader/Writer 契约表达复制，`copyBuffer` 可委托 WriterTo/ReaderFrom，也保留通用路径及错误处理。它仍包含具体优化；借鉴的是以共同契约组织真实差异，不是禁止特化实现。两者均为协作项目的版本样本，不将每行代码归为创始人独作。

**设计取舍。** John Ousterhout 的 [CS190 讲义](https://web.stanford.edu/~ouster/cs190-winter22/lectures/intro/) 将依赖、不一致和特殊情况列为复杂性的来源，讨论消除/隐藏复杂性与增量设计。这里只借鉴理解和修改成本的判断，不照搬课程评分取舍。

**本包推导。** 将个案合并为目标、表示、边界、反馈与知识归属的判断；同一因果关系只维护一处，专项保留独有动作。检验新规则时既换场景看迁移，也改条件看能否正确区别。收敛不能变成“永远最短”或“永远不加抽象”。这是设计选择，效果仍需 [行为对照](evaluation.md)。

## 继承材料的来源与边界

A 编号用于保留已有来源坐标，不对应新增问题条目。旧材料不是本轮重新运行的实验；本轮直接复核的网页与源码在上节。

- **A1** [Anthropic：长任务 harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)。特定系统的工程经验。
- **A2 / A11** [Anthropic：长任务应用开发](https://www.anthropic.com/engineering/harness-design-long-running-apps)。实现与评价方法，不推出每项任务都要多 Agent。
- **A3** [Anthropic：上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。按需上下文与接续方法。
- **A4** [Beyond Resolution Rates](https://arxiv.org/html/2604.02547)。特定基准的轨迹分析与小样本定性发现，不代表总体根因分布。
- **A5** [USENIX 2025：We Have a Package for You!](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen)。历史模型的包幻觉研究，不作为当前发生率。
- **A6** [Stack Overflow 2025 调查](https://survey.stackoverflow.co/2025/ai)。受访者自报告，不是输出错误率。
- **A7** [How Coding Agents Fail Their Users](https://arxiv.org/html/2605.29442v2)。公开会话和用户纠正的观察研究，有采样与遗漏限制。
- **A8** [OpenAI：GPT-5 提示指南](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide)。特定模型的提示案例，不构成普适流程。
- **A9** [OpenAI：Harness engineering](https://openai.com/index/harness-engineering/)。仓库可读性与知识组织的工程案例。
- **A10** [Anthropic：Managed Agents](https://www.anthropic.com/engineering/managed-agents)。harness 假设随能力变化的工程讨论。
