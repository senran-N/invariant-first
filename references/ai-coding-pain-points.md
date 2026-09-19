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

## 机制与适用前提

**把现象与解释分开。** [V2EX 作者的公开摘要](https://global.v2ex.com/t/1237708) 描述：录制任务未退出，尚未找到卡点时，Agent 已为不同猜测分别修改生命周期、取消和重试。这里只读取到检索摘要，正文访问转向登录，未复现该项目。对应的成熟机制见 Git `v2.46.0` 的 [bisect_run / verify_good](https://github.com/git/git/blob/v2.46.0/builtin/bisect.c)：无法测试的 125 状态走 skip；首次遇到可能源于执行环境的 126/127，还会在已知良好版本作对照。借鉴的是先判断信号能说明什么，再用能区分原因的反馈更新判断，不是每次修复都执行二分或重复测试。

**复用取决于前提，而非记忆有多新。** [Cursor 原始报告](https://forum.cursor.com/t/agent-with-confusion-hallucinations-and-mutiny-100-broken/168293) 描述摘要混入不同分支事实，导致重复实现和纠正后的方案摆动；这是用户归因，不是独立复现。[另一条分支显示讨论](https://forum.cursor.com/t/agents-glass-ui-reports-wrong-branch/158304) 中，支持回复将旧标签归因于存储快照与实际分支脱节，也区分了后续不同问题。SQLite `version-3.46.1` 的 [OP_Transaction](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/vdbe.c) 与 [sqlite3_step](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/vdbeapi.c) 检查 schema 条件并在对应失效时重新准备语句；仍匹配的 schema 不因一次语句失效被无条件重载。借鉴的是限定结论的适用对象和失效条件，而不是让 Agent 实现一套缓存或每轮重扫仓库。

**判断是有边界的更新。** [Ousterhout 的 CS190 讲义](https://web.stanford.edu/~ouster/cs190-winter22/lectures/intro/) 把设计视为增量过程：做一部分设计、实施、从结果中学习再调整。此前 Linux 表示与 Go 接口样本支持的共同责任仍然保留。结合这些材料，本包在已有目标、反馈和知识判断中区分要求与假设，选择会改变行动的观察，并只修订受失效前提影响的决定；明确的修复直接执行，局部纠正不自动变成全局反转。这是工程归纳，不是这些作者共同规定的方法，也没有完成模型效果实验。

**读取范围不是写入范围，恢复也需要来源。** 近期 Cursor 社区的多条报告分别描述了“读到共享工具后顺手重构”“后续 turn 覆盖用户手工修改”和“远端已有人工维护却被本地副本覆盖”等现象；这些是用户报告，不等同于统一根因或发生率。Git 的 `checkout` 在切换分支可能覆盖本地修改时默认拒绝，显式 `--merge` 才会暂存并重新应用已有修改。借鉴的是两点：为了理解可以读取更宽的依赖面，但写入范围仍由目标和责任决定；回滚或切换必须区分已有工作与本次修改的来源，而不是把当前状态当成可以重建的空白画布。

**最终内容相同，不代表修改过程等价。** Cursor 的一个近期报告中，全文件“清空再写回”触发了监听工具两次更新，并在短暂空状态下删除运行实体；另一条多文件重构报告指出整文件重写还会连带丢失注释和格式。这些案例说明某些环境会观察写入过程本身。SQLite 的原子提交机制则把中间写入视为可能被崩溃打断的真实状态：先记录可恢复信息，再在可识别的提交边界后让新状态生效。借鉴的不是让普通文本编辑实现数据库事务，而是：当 watcher、并发读者或外部系统能看到中间态时，编辑/部署方式本身属于系统行为，应利用项目已有的临时文件、锁、事务、原子替换或分阶段发布机制；没有这类观察者时，不额外制造事务框架。

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
