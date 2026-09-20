# 从使用反馈提炼工程机制

本文件是维护依据，不是执行时逐条匹配的故障表。行动以 [共同判断](../RULES.md) 和当前子技能为准。论坛观察用于提出疑问，项目源码用于理解机制；二者都不能独立证明某条提示对所有模型有效。

## 已有材料怎样归并

| 共同判断 | 材料提供的线索 | 当前方法 |
| --- | --- | --- |
| 由目标决定行动 | 越界、意图误读和流程挤占目标；A7–A8 | 用户价值决定重点与承诺，主路线选方法，专项只补判断 |
| 表示与责任 | 正确文件中仍可能选错修改层；A4、成熟实现 | 追事实与保证的归属，在责任处修改 |
| 在边界内完成变化 | 半成品、遗漏相关行为和遗留路径；A1–A2、既有现场材料 | 贯通真实入口，区分变化与保留，完成切换 |
| 保护与事实 | 包/API 假设、状态和依赖风险；A5、成熟实现 | 当前版本与真实边界决定动作，不从名称猜测 |
| 有区分力的反馈 | 自报结果、无信息循环和自评局限；A1、A4、A7、A11 | 实际执行目标逻辑，以独立预期修正实现 |
| 产品事实与接续 | 跨会话遗漏、文档膨胀及过时约束；A1、A3、A9–A10 | 短入口指向权威位置，知识按责任存放 |

原始 [现场材料](field-notes-2026-09-19.md) 与 [源码样本](source-lessons.md) 保留核查坐标；它们不是新增禁令的模板。模型、框架和故事名从执行判断中去掉，不影响真正必要的语义与风险差异。

## 机制与适用前提

**对齐用户价值，不把实施便利当成缩减目标的授权。** [Cursor 的原始报告](https://forum.cursor.com/t/agent-ignores-ambiguous-impossible-instructions-instead-of-asking/171061)（2026-09-08）描述 Agent 对一个有歧义的前置要求自行解释，得知无法执行后又直接略过。报告未给出完整版本，后续支持回复还对 IDE/CLI 作了不同假设；这里不认定统一根因，也不采用“遇到任何未知就停掉所有工作”的建议。相反，[逐次审批的讨论](https://forum.cursor.com/t/cursor-agent-asking-for-approval-at-each-code-change/148476)（2026-01）说明过密的操作确认同样有成本；它涉及工具权限体验，不能当成所有澄清问题都有害的证据，更不据此关闭安全机制。[Ambig-SWE v3](https://arxiv.org/html/2502.13069v3)（2026-02-21）把识别欠明确、取得有效信息和利用回答分开研究；其主要实验使用人为删减的问题与模型扮演的用户，不能外推为真实用户的通用改善幅度。

[作者方法与 OpenSpiel 的源码对照](source-lessons.md#value-and-intent) 支持两项区分：事实由调查取得，意向分歧由有建议的交流澄清；操作合法、链路稳定与策略或结果质量分别评价。本包旧表述把提问收窄到冲突/高影响操作，又让设计默认列非目标，容易为擅自定重点和缩范围留出解释空间；这只是指令审查发现，不是已证实的模型因果解释。现替换为价值、能力与成功标准先对齐，按决定依赖提问，简化实现但不擅自删减承诺。明确的局部任务仍直接做；需要体验才能判断的取舍用适当样例或原型，不把交流变成穷尽问卷。

**把现象与解释分开。** [V2EX 作者的公开摘要](https://global.v2ex.com/t/1237708) 描述：录制任务未退出，尚未找到卡点时，Agent 已为不同猜测分别修改生命周期、取消和重试。这里只读取到检索摘要，正文访问转向登录，未复现该项目。对应的成熟机制见 Git `v2.46.0` 的 [bisect_run / verify_good](https://github.com/git/git/blob/v2.46.0/builtin/bisect.c)：无法测试的 125 状态走 skip；首次遇到可能源于执行环境的 126/127，还会在已知良好版本作对照。借鉴的是先判断信号能说明什么，再用能区分原因的反馈更新判断，不是每次修复都执行二分或重复测试。

**复用取决于前提，而非记忆有多新。** [Cursor 原始报告](https://forum.cursor.com/t/agent-with-confusion-hallucinations-and-mutiny-100-broken/168293) 描述摘要混入不同分支事实，导致重复实现和纠正后的方案摆动；这是用户归因，不是独立复现。[另一条分支显示讨论](https://forum.cursor.com/t/agents-glass-ui-reports-wrong-branch/158304) 中，支持回复将旧标签归因于存储快照与实际分支脱节，也区分了后续不同问题。SQLite `version-3.46.1` 的 [OP_Transaction](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/vdbe.c) 与 [sqlite3_step](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/vdbeapi.c) 检查 schema 条件并在对应失效时重新准备语句；仍匹配的 schema 不因一次语句失效被无条件重载。借鉴的是限定结论的适用对象和失效条件，而不是让 Agent 实现一套缓存或每轮重扫仓库。

**判断是有边界的更新。** [Ousterhout 的 CS190 讲义](https://web.stanford.edu/~ouster/cs190-winter22/lectures/intro/) 把设计视为增量过程：做一部分设计、实施、从结果中学习再调整。此前 Linux 表示与 Go 接口样本支持的共同责任仍然保留。结合这些材料，本包在已有目标、反馈和知识判断中区分要求与假设，选择会改变行动的观察，并只修订受失效前提影响的决定；明确的修复直接执行，局部纠正不自动变成全局反转。这是工程归纳，不是这些作者共同规定的方法，也没有完成模型效果实验。

**读取范围不是写入范围，恢复也需要来源。** 近期 Cursor 社区的多条报告分别描述了“读到共享工具后顺手重构”“后续 turn 覆盖用户手工修改”和“远端已有人工维护却被本地副本覆盖”等现象；这些是用户报告，不等同于统一根因或发生率。Git 的 `checkout` 在切换分支可能覆盖本地修改时默认拒绝，显式 `--merge` 才会暂存并重新应用已有修改。借鉴的是两点：为了理解可以读取更宽的依赖面，但写入范围仍由目标和责任决定；回滚或切换必须区分已有工作与本次修改的来源，而不是把当前状态当成可以重建的空白画布。

**最终内容相同，不代表修改过程等价。** Cursor 的一个近期报告中，全文件“清空再写回”触发了监听工具两次更新，并在短暂空状态下删除运行实体；另一条多文件重构报告指出整文件重写还会连带丢失注释和格式。这些案例说明某些环境会观察写入过程本身。SQLite 的原子提交机制则把中间写入视为可能被崩溃打断的真实状态：先记录可恢复信息，再在可识别的提交边界后让新状态生效。借鉴的不是让普通文本编辑实现数据库事务，而是：当 watcher、并发读者或外部系统能看到中间态时，编辑/部署方式本身属于系统行为，应利用项目已有的临时文件、锁、事务、原子替换或分阶段发布机制；没有这类观察者时，不额外制造事务框架。

**副作用看资源身份，异步结果看发布时前提。** [Cursor 的数据丢失报告](https://forum.cursor.com/t/include-gitignore-ed-files-in-checkpoint/165652/5) 中，Agent 写出的集成测试把测试服务指向真实运行数据目录，测试框架的 reset 语义因此删除了真实数据；风险来自资源身份与副作用，而不是 `test` 命令本身。[Claude Code 的后台任务报告](https://github.com/anthropics/claude-code/issues/79354) 则描述了后台任务在 Agent 已继续编辑后晚到，把较新的文件状态覆盖掉。两个案例都只是用户报告。Git 的测试框架把测试运行在独立 trash directory，并有专门用例确保路径写入不能逃出工作树；Kubernetes 用 `resourceVersion` 让基于过期对象的更新返回冲突。借鉴的是：有破坏性的测试先隔离真实资源；异步/并发结果发布前确认它仍基于当前状态。锁只能解决同时写入，若“晚到但已过期”也有风险，还需要版本、前置条件、隔离产物后比较或重新读取；不存在这些风险时，不加额外协调层。

**简单性要减少需要共同理解的知识，不只减少代码量。** [V2EX 的“AI 编程后，我更累了”](https://edge.v2ex.com/t/1192730) 中，作者及部分评论描述生成提速之后理解、裁剪与审查负担增加；也有评论将疲劳归因于任务增加，不能把讨论当成统一因果结论。[Armin Ronacher 的 The Final Bottleneck](https://lucumr.pocoo.org/2026/2/13/the-final-bottleneck/) 讨论生成与审查吞吐失衡，[Simon Willison 的亲身体验](https://simonwillison.net/2026/Feb/15/cognitive-debt/) 则描述跳过实现阅读后失去项目心智模型。共同线索是维护者需要理解的关系没有随生成成本下降，而不是“AI 代码一律冗长”。

对照 `karpathy/micrograd` 的 `c911406` 与 Go `go1.23.2`：前者将教育目标收在紧凑计算图内，并在 [test_engine.py](https://github.com/karpathy/micrograd/blob/c911406/test/test_engine.py) 用 PyTorch 比较前向值和梯度；后者的 [strings.Builder](https://github.com/golang/go/blob/go1.23.2/src/strings/builder.go) 将缓冲区保持私有，以 `copyCheck` 检测非零 Builder 的值复制，`Reset` 丢弃底层缓冲区引用。两者不是同一种文件规模或抽象形状，借鉴的是用表示与所有权收住知识，并让调用者少承担隐含步骤；不照搬 unsafe 实现、教育项目的风险假设或历史编译器 workaround。落实到 RULES、architecture 与知识交接：沿真实调用和变化比较理解成本，而非设行数上限、统一禁止抽象或增加解释文档来掩盖耦合。

**验证的价值是分辨对错，不是产出绿色信号。** [Jesse Vincent 的测试删除回忆](https://blog.fsck.com/2026/04/30/that-time-it-tried-to-delete-all-my-tests/) 描述 Agent 为消除失败而删除断言和测试；作者没有保留会话日志，模型事后给出的解释也不能证明心理状态或训练原因。该经验提示需要审视“字面达标却没有完成目标”的空间，但不采用“测试数量或覆盖率只能增长”的通则。

对照 [SQLite 测试说明的 mutation testing](https://sqlite.org/testing.html#mutation_testing) 与 `version-3.46.1` 的 [malloc_common.tcl](https://github.com/sqlite/sqlite/blob/version-3.46.1/test/malloc_common.tcl)：前者区分执行过分支与能够发现分支行为被改变，并说明仅影响速度的分支可能造成误判；后者将故障注入的执行与后续检查分开，提供完整性检查。结合 micrograd 的独立参考，提炼为“目标错误仍在时，这个观测会不会揭露它”。这是按风险选择复现、独立预期或隔离对照的判断，不是让每次小改都跑变异测试、禁止替身、禁止删除过时测试或复刻数据库测试平台。指令变化尚未接受模型对照评估。

**恢复应接续原操作，不把通信尝试当成业务意图。** [Cursor 的自动恢复请求](https://forum.cursor.com/t/agent-should-auto-abort-and-retry-when-stalled-30s-not-hang-until-manual-stop/161234)（2026-05-21）描述流式连接停滞，主张约 30 秒无进展便中止并重试；6 月回复称已有流监测而 UI 仍可能滞留。这是报告与回复，不是本包复现。相反，[长命令超时讨论](https://forum.cursor.com/t/timeout-setting-on-terminal-shell-agent-tool/148885)（2026-01-14）描述正常测试需要 20 分钟乃至更久。两者等待的对象不同，不能归纳成统一的静默阈值。[Claude Code #54086](https://github.com/anthropics/claude-code/issues/54086)（2026-04-27）则报告：本想醒来查看后台测试，却把完整审查命令再次执行。此处借鉴操作身份与观察/执行的区分，不采纳其按命令前缀封禁的具体建议；未独立复现，也不据 issue 关闭状态推断已修复。

[Everett Quebral 的 Idempotency for AI Agents](https://www.everettquebral.com/blog/artificial-intelligence/idempotency-for-ai-agents)（2026-08-03）用退款超时的说明性例子讨论已完成、仍在执行和结果未知，强调稳定的操作身份。这不是提供运行日志的事故统计。与 [Brandur Leach 的 Stripe 工程说明](https://stripe.com/blog/idempotency)、[AWS 的幂等 API 设计](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) 及 [Go / Stripe 版本化实现](source-lessons.md#deliver) 对照后，落点是：先分清操作是否还在运行、结果是否已存在，安全重试保持同一意图，新的独立意图不被错误去重。接收方不支持去重时，仅在客户端包一层或生成键不能消除提交与确认之间的不确定性；去重有效期、参数和作用范围都是条件，不是“一次加键永久安全”。

现有 recovery 中“重复只为新信息”的表述不足以涵盖安全重试对暂时故障的恢复作用，现区分诊断循环与操作重试：前者需要有区分力的观察，后者需要有效恢复契约和预算。等待、续取结果与重放分别决定动作；handoff 保留未决操作的定位信息。按 [Google SRE 的重试责任与预算](https://sre.google/sre-book/handling-overload/) 防止各层重复放大工作，不固定次数、时长或要求新建调度平台。上述归纳尚未经过模型对照评估。

**审查结论随行为证据更新，不随报告数量和显示状态更新。** [Cursor 的多轮审查讨论](https://forum.cursor.com/t/bugbot-doesnt-catch-all-issues-on-first-pass-multiple-review-cycles-needed/151367)（2026-02 至 04）描述同一变更需多轮才陆续出现问题；[另一条报告与支持回复](https://forum.cursor.com/t/bugbot-appears-to-resolve-prior-inline-findings-after-an-unrelated-commit/154401)（2026-03-11）则描述旧问题未修却被判为已解决。它们提示发现集合与问题状态不是同一件事，不证明本包能让模型一次找全所有问题，也不代表这些工具当前仍有同样表现。未独立复现这些会话。[Hacker News 的使用者讨论](https://news.ycombinator.com/item?id=45449348) 中，也有人描述审查只重复已有 FIXME 或泛泛称赞，并希望得到有价值的可疑位置；这是个人体验，不是对当前模型的能力测量。

Daniel Stenberg 的 [2025-07 维护经历](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/) 描述核查低质量报告的负担；他的 [2025-10 反例](https://daniel.haxx.se/blog/2025/10/10/a-new-breed-of-analyzers/) 又展示有效的 AI 辅助发现，其中一处正确修复是改错注释而不是实现新容错行为。[2026-04 的后续](https://daniel.haxx.se/blog/2026/04/22/high-quality-chaos/) 描述报告质量改善后仍存在的处理压力。因此不按 AI 来源接受或排斥报告，也不把降低报告数当目标。对照 [R4 的 Go 控制流诊断与 curl 历史修正](source-lessons.md#review-evidence)，提炼为：沿真实条件确认违背了什么保证，区分问题成立与修法成立，再以原条件复核是否修好。高后果的未知需要交代，不因缺少可运行环境就排除；显示关闭、重新扫描未提及或局部检查通过，都不能扩大证据的结论范围。落实在 review 与 fix，不另建事故目录或审批流程。

**按读者任务保留信息。** [Tildes 的原始讨论](https://tildes.net/~comp/1g6h/slop_is_the_new_name_for_unwanted_ai_generated_content)（2024-05-08）中，审查者描述 AI 生成的 PR 长篇逐文件复述且影响说明不准，阅读成本落到接收者身上；[Simon Willison 的作者说明](https://simonwillison.net/2024/May/8/slop/) 将发布责任放在使用工具的人，而非反对一切 AI 写作。反向线索是 [Cursor 的注释删除报告](https://forum.cursor.com/t/unintended-code-alterations-in-agent-mode-removal-translation-of-comments-and-console-logs/93881)（2025-05-20）：未经要求的精简或翻译也会损害协作者与调试用途。这些是作者经验与用户报告，不是模型行为统计。

对照 [Git `v2.46.0` 的 SubmittingPatches](https://github.com/git/git/blob/v2.46.0/Documentation/SubmittingPatches)：维护理由进入提交正文，补丁轮次的沟通放在分隔线后；它也要求解释有实际意义的排除条件。[rust-analyzer `2024-09-16` 的架构说明](https://github.com/rust-lang/rust-analyzer/blob/2024-09-16/docs/dev/architecture.md) 保留解析器和语法层刻意隔离的依赖，并给出原因。两者支持按信息职责编辑，而非按否定词或字数删除：纠正要改变成稿事实，必要的修订回应留在对话；真实边界、未决事项和设计理由仍就近可查。本次用户提供的方案片段暴露了修订回应与正文混写，现收紧共同判断及 frame/document 的输出边界，具体写法见 [文档方法](documentation.md)。未作独立模型对照，不把上述源码阅读当成效果证明。

## 继承材料的来源与边界

A 编号用于保留已有来源坐标，不对应新增问题条目，也不表示每轮都重新读取或复现实验；各机制段落分别说明报告、作者解释与源码依据的限制。

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
