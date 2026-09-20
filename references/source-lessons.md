# 源码依据与适用边界

资料包含前版保留的 S/D 系列研究与本次新增的 R 系列生命周期依据；R1–R4、开放格式及 D1/D4 于 2026-09-19 核查。采用可定位的历史版本，不把样本冒充最新实现或完整仓库审计。区分项目事实、规则归纳与适用限制；项目是协作成果，创始人姓名不是每行代码的作者归属。所有规则均为本 Skill 的工程提炼，并非这些项目共同发布的方法论。

目录：[探索](#explore) · [交付](#deliver) · [演进](#evolve) · [归纳边界](#limits) · [文档](#documentation) · [可移植性](#portability) · [生命周期补充与路由映射](#lifecycle)

<a id="explore"></a>
## 探索：对齐价值，保留真实闭环

### S1 · Andrej Karpathy / micrograd：小实现也要有独立判据

**样本：** `karpathy/micrograd`，短提交标识 `c911406`。

- [README](https://github.com/karpathy/micrograd/blob/c911406/README.md)：项目明确定位为小型、标量级自动微分与教育用途，提供神经网络训练演示。
- [micrograd/engine.py](https://github.com/karpathy/micrograd/blob/c911406/micrograd/engine.py)：`Value` 保存值、梯度与计算图关系；`backward` 按拓扑顺序反向传播。
- [test/test_engine.py](https://github.com/karpathy/micrograd/blob/c911406/test/test_engine.py)：`test_sanity_check`、`test_more_ops` 对同一运算分别运行 micrograd 和 PyTorch，比较前向结果与梯度。

**提炼：** 缩小一次实验的规模，不删掉要验证的核心能力；用参考实现或已知性质判断是否真的做对。实验回答核心是否成立，不因此重写用户要求的完整交付范围；探索验收不是层次漂亮的脚手架。

**边界：** 这是教育仓库，不是生产服务成熟度模板；不能据此取消输入安全、数值约束或必要资源管理，也不能推断所有作者都采用同一开发顺序。

### S2 · Linus Torvalds / Git 初始提交：明确表示，直接贯通

**样本：** `git/git`，提交 `e83c5163316f89bfbde7d9ab23ca2e25604af290`。

- [README](https://github.com/git/git/blob/e83c5163316f89bfbde7d9ab23ca2e25604af290/README)：先解释内容寻址对象、树、历史关系及当前目录缓存，明确不同表示承担什么工作。
- [write-tree.c](https://github.com/git/git/blob/e83c5163316f89bfbde7d9ab23ca2e25604af290/write-tree.c)：`main` 读取缓存条目，检查引用对象可读，构造树内容并写入对象存储。

**提炼：** 先让清楚的数据模型支撑核心路径；不要先搭一个无实际消费者的通用平台。允许为真实不变量封装，不把“最小”误解为完全没有设计。

**边界：** 只借鉴目标与表示的收敛方式，不复刻早期实现的缺陷、历史存储格式或安全假设。初始提交不能证明兼容在所有新项目中都不重要；“没有旧消费者才不建兼容层”是我们的适用条件。

<a id="value-and-intent"></a>
### 目标与意向：对齐决定，分别验证价值与底线

**Matt Pocock 的版本化方法：** `mattpocock/skills` 的 `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` 中，[grilling](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grilling/SKILL.md) 按决定的依赖关系组织问题，给出建议，并把可调查的事实与用户作出的决定分开；[to-spec](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/to-spec/SKILL.md) 从已有讨论综合规格，而非重新进行整轮访谈。借鉴回答会改变下游选择、已有决定应延续；不移植其穷尽式提问、所有决定都交给用户、强制子代理或固定发布流程。作者[关于过度访谈的说明](https://www.aihero.dev/things-people-get-wrong-with-grill-me-and-grill-with-docs)（2026-05-25 更新）还区分能讨论的取舍与需通过原型理解的体验；这里不采用其中未验证的统一上下文阈值或吞吐推断。

**不同协作方法的取舍：** [Superpowers 的 brainstorming](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/brainstorming/SKILL.md) 在 `5bf4e780` 中先辨认用途、使用者和成功标准，再将共同理解带入方案；但也要求按工作类别逐阶段批准，并且一次只问一个问题。上述 Matt Pocock 版本则把前提已确定的问题放在同一轮，尚依赖未决答案的问题留到后面。两种组织方式不同，不能仅凭名气选一种为所有任务的默认流程。本包借鉴问题与决定的依赖、回答进入方案，而不移植固定提问节奏、穷尽访谈或对每个已授权内部步骤重新审批。这里比较的是实际指令，不是运行这些 Skill 后的效果排名。

**OpenSpiel 的可核查区分：** `google-deepmind/open_spiel` 的 `48401890ee9857e611678302371378175a8e4c6b` 中，[Kuhn 游戏实现](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/games/kuhn_poker/kuhn_poker.cc) 分别定义合法动作、可观察信息与收益；[策略评价测试](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/python/algorithms/exploitability_test.py) 对始终选择首个合法动作、均匀随机策略和均衡策略使用不同的 NashConv 预期。合法性约束不等于策略目标；策略也不能使用决策者实际看不到的信息。NashConv 衡量单方偏离可获得的改善，不等于对指定对手的胜率；选哪种评价仍取决于用户目标，不能用一个指标重新替用户定重点。源码测试的存在不是本包已执行该项目的证明。

此前用标准库分数运算写了独立的双人 Kuhn 枚举器，遍历六种发牌及每位玩家的 64 个纯策略响应；三组策略均满足合法动作分布，NashConv 分别为 2、11/12、0，与上述测试的预期吻合。它只验证这个有限游戏的指标区分，不是运行 OpenSpiel、复现用户的 Mod、评估意图推断或验证本 Skill 的模型效果。

**提炼与边界：** 对齐用户为何需要成果，再把关键能力分配到产生该价值的机制与可观察结果。必要底线约束方案，不能冒充目标；已明确要求策略质量时，稳定执行只是其支撑。用户只要执行器可靠性时，稳定性又可以是当前目标，不擅自扩大为策略研究。问题不清就用会改变取舍的问题澄清；明确后自主解决实现。分阶段保留总体承诺，删减另行协商；不复制某个访谈模板、评分公式或游戏算法成为通用流程。

<a id="mechanism-walkthrough"></a>
### 设计机制：用场景走通决定

**作者方法与反例：** Beck 与 Cunningham 的 [1989 年 CRC 原文](https://c2.com/doc/oopsla89/paper.html) 用执行场景暴露尚无承担者的责任，按需要调整协作；同时记录过收件人脱离讨论后无法理解成品卡片的反例。因此借鉴的是沿场景发现缺口、在交付物中留下必要关系，不是要求画卡片、采用面向对象或输出整段演练过程。

**不同实现怎样落实选择：** [NetworkX `networkx-3.6.1` 的 A*](https://github.com/networkx/networkx/blob/networkx-3.6.1/networkx/algorithms/shortest_paths/astar.py) 由边权表达成本，权重函数可排除边，启发函数与 cutoff 影响搜索；[对应测试](https://github.com/networkx/networkx/blob/networkx-3.6.1/networkx/algorithms/shortest_paths/tests/test_astar.py) 区分成本变化、隐藏边及过高启发估计。没有指定成本字段时，默认缺失权重按 1 处理；算法名不能替调用者决定目标。相比之下，[OR-Tools `v9.11` 的最小作业车间示例](https://github.com/google/or-tools/blob/v9.11/ortools/sat/samples/minimal_jobshop_sat.py) 用区间变量表达任务，分别写出机器不重叠、任务先后约束与最小化最终完工时间的目标。前者扩展相邻路径，后者求解区间约束；实现形态不同，都把目标与可行条件落成了数据和运算。这里只阅读 OR-Tools 示例，未运行该求解器。

本地以 NetworkX 3.6.1 做六组小图对照，安装的 A* 文件 Git blob 与上述源码一致：遗漏成本字段选到耗时 9 的路径，指定耗时后为 2，禁止收费路段后为 6；过高启发估计又选到 9。成本上界为 1 时没有返回路径，上界为 2 时成功，独立穷举确认图上一直存在耗时 2 的路径。它说明目标、限制与算法前提会改变结果，也说明有限搜索没有结果不等于原问题无解；这不是性能基准、用户项目复现或模型评估。

**提炼与边界：** 关键场景走到某一步还需要临时发明决定性规则，方案就在该处缺少机制。补足会改变行为的判据、责任与条件，未知参数给出来源或校准办法，既不编数值制造确定性，也不展开所有局部实现。现有库已承担完整机制时说明采用的契约即可；算法实验验证其性质，不能单独确定用户偏好。落实于 frame 与文档方法，不新增通用评分框架或强制实验阶段。

<a id="deliver"></a>
## 交付：保护真实承诺和真实风险

### S3 · Go 团队：兼容需要范围和具体机制

- [Go 1 兼容承诺](https://go.dev/doc/go1compat)：明确源代码兼容范围，以及安全、未指定行为、实现缺陷等例外。
- [GODEBUG 兼容说明](https://go.dev/doc/godebug)：解释改变默认行为与降低旧程序升级影响之间的取舍。
- [`go1.23.2` / src/net/http/servemux121.go](https://github.com/golang/go/blob/go1.23.2/src/net/http/servemux121.go)：文件头要求冻结旧 ServeMux 行为；`httpmuxgo121` 在初始化时决定是否启用，`serveMux121` 用锁保护内部状态。
- [同版本 server.go](https://github.com/golang/go/blob/go1.23.2/src/net/http/server.go)：`ServeHTTP`、`Handle`、`HandleFunc` 在明确位置选择新旧实现，而非让所有业务代码猜测版本。

**提炼：** 兼容服务真实使用者，集中于清楚的边界；先讲明保证什么，再测试它。内部实现可以变。安全问题不能以“用户依赖”为由原样保留。

**边界：** 不把所有已有行为都永久冻结；也不机械要求每个兼容开关限期删除。是否保留由项目承诺与使用证据决定。迁移、发布与恢复的具体操作要求是本 Skill 的工程归纳，并非 Go 对所有项目的规定。

### S4 · Richard Hipp 与 SQLite 团队：失败后的状态才是可靠性的一部分

- [测试方法](https://sqlite.org/testing.html)：说明内存不足、I/O 错误及崩溃模拟，检查异常后的数据库状态和事务结果。
- [安全边界](https://sqlite.org/security.html)：讨论不可信 SQL、数据库输入及相应限制；保护取决于威胁入口，而非产品版本名称。
- [`version-3.46.1` / src/pager.c](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/pager.c)：`Pager.eState` 的状态图、`assert_pager_state`、`pager_error` 使锁、日志、错误与合法迁移的关系可核查。
- [同版本 test/ioerr.test](https://github.com/sqlite/sqlite/blob/version-3.46.1/test/ioerr.test)：`do_ioerr_test` 覆盖多文件提交、日志恢复及其他 I/O 失败路径。

**提炼：** 遇到重要持久状态或外部写入，检查中途失败留下什么；用对应故障验证清理、一致性和恢复，而不是再加一个吞错分支。

**边界：** 不要求每个小项目复刻 SQLite 的测试体系；断言也不等于发布环境的安全检查。一条失败测试不足以证明所有崩溃一致性，代码回滚更不保证数据能够回滚。

### S5 · Rich Hickey / Clojure：可重复的计算，不等于可重复的副作用

- [Atoms 文档](https://clojure.org/reference/atoms)：更新函数可能因竞争重新执行，因而必须避免副作用；Atom 面向独立状态。
- [`clojure-1.11.1` / src/jvm/clojure/lang/Atom.java](https://github.com/clojure/clojure/blob/clojure-1.11.1/src/jvm/clojure/lang/Atom.java)：`swap` 读取值、调用函数、验证、尝试 CAS；失败则循环，成功路径才通知观察者。

**提炼：** 先明确共享状态的所有者和原子边界。把可重算部分与不可重复动作分离，不能靠“出错再试一次”保证正确。

**边界：** 单个 Atom 不给多个状态或外部服务提供事务；CAS 循环也不是业务网络重试的模板。本 Skill 对网络重试期限、取消和重复效果的要求是额外适配，不是要求改写 Clojure 同步算法。

### 传输重试对照：操作身份、恢复责任与保证范围

**Go `go1.23.2`：** [`transport.go`](https://github.com/golang/go/blob/go1.23.2/src/net/http/transport.go) 的 `shouldRetryRequest` 区分未写出请求、连接是否复用、错误类别与可重放性；`rewindBody` 处理请求体能否重建。[`request.go`](https://github.com/golang/go/blob/go1.23.2/src/net/http/request.go) 的 `isReplayable` 识别特定方法或幂等键声明，但这不是服务端已经去重的证明。借鉴的是根据失败位置和协议选择恢复，不把所有连接错误统一转成重试。

**Stripe Python `v15.6.1`：** [`_api_requestor.py`](https://github.com/stripe/stripe-python/blob/v15.6.1/stripe/_api_requestor.py) 在进入重试前构造请求头，接受调用者提供的幂等键；[`_http_client.py`](https://github.com/stripe/stripe-python/blob/v15.6.1/stripe/_http_client.py) 在同一重试循环复用请求参数，按次数、底层错误可重试标志及服务端提示决定是否继续。由此可见，一次 SDK 调用内部的重试和 Agent 再次调用 API 是不同边界：后者若重新生成键，不能指望前一次身份自动延续。[API 文档](https://docs.stripe.com/api/idempotent_requests) 还限定参数一致性与记录保留期，并说明同键可能重放失败响应；不能把幂等误作必然成功。

**作者说明与反例：** [Stripe 的 Brandur Leach](https://stripe.com/blog/idempotency) 区分连接前失败、处理中失败、已成功却丢失响应；[AWS 的 Malcolm Featonby](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) 区分同一次请求重传与用户有意创建两个相同资源，并讨论同键异参、晚到请求和保存期限。[Google SRE](https://sre.google/sre-book/handling-overload/) 将重试限制在适当责任层，并用预算避免多层放大。

**提炼与边界：** 原操作的等待、查询和重放不是同一个动作；可能重复产生效果的重放既要保持意图，也要有接收方仍有效的保证；已确认未执行则按实际失败条件恢复。客户端日志或包装无法单独填补远端提交后的确认缺口，状态查询也要考虑可见性。优先使用现有协议、句柄和恢复机制，不从这些样本推出每项任务都需去重平台、统一超时或固定重试次数；源码阅读不是端到端故障实验，更不是模型效果证据。

<a id="evolve"></a>
## 演进：改变要有范围，效果要有证据

### S6 · Git 维护实践：逻辑上独立的改动应可独立审查

**样本：** `git/git`，版本 `v2.46.0`。

- [Documentation/SubmittingPatches](https://github.com/git/git/blob/v2.46.0/Documentation/SubmittingPatches)：要求分开逻辑独立的变更、说明问题与理由，并为修复和新行为添加相应测试。
- [t/t6030-bisect-porcelain.sh](https://github.com/git/git/blob/v2.46.0/t/t6030-bisect-porcelain.sh)：测试正常二分，也测试无法确定坏提交、缺失测试脚本、脚本不可执行等情形；脚本环境错误不能被直接包装成成功找到了坏提交。

**提炼：** 区分行为证据与测试环境故障，保留可审查的改动单元。回归测试应识别目标缺陷；重构不能夹带未经声明的行为改变。

**边界：** 不声称所有 Git 贡献者都严格先写测试。当前 Skill 保留针对性复现与用户工作区保护，但不要求每次重建完整红绿历史，也不要求 Agent 擅自提交代码。

### S7 · SQLite 性能工程：测量同一工作负载，同时保留正确性

- [性能测量说明](https://sqlite.org/cpu.html)：讨论固定负载、Cachegrind 对比和微优化，也列出编译器、平台、应用负载与 I/O 等局限。
- [`version-3.46.1` / test/speedtest1.c](https://github.com/sqlite/sqlite/blob/version-3.46.1/test/speedtest1.c)：维护测试负载、时间记录和 `--verify` 路径；`speedtest1_final` 输出总耗时及验证摘要。

**提炼：** 先选实际目标指标和可重复负载，定位后再优化；只在观测支持的范围内宣称收益，并保留正确性判据。不要把“加缓存”“上并发”当优化任务的固定答案。

**边界：** 该样本的验证摘要不包含浮点结果的具体值，不能作为全部正确性的替代；CPU 指令类指标也不等于端到端延迟。性能说明在 2026-01-06 注明新脚本 `speedtest.tcl` 已替代旧 `speed-check.sh`；这里阅读历史样本，不要求用户照跑旧命令。

<a id="limits"></a>
## 归纳边界

本版的十条主路线及两类专题是为任务分派而设计，不是对作者私人思考过程的复原。前版按探索、交付、演进归档的研究仍作为依据；实际执行以当前 SKILL.md 的路由和交付目标为准，不能把来源说明中的历史分类再次变成前置流程。

“按修改边界分类”“维护贯穿各阶段”“风险早于版本标签”“先验证转向再迁移”等是我们据此提出的工作规则。它们允许合理取舍，不是对每个仓库新增同一套框架。没有对真实 Agent 做对照评估前，不宣称本 Skill 已降低回归率或达到某位工程师的能力。

<a id="documentation"></a>
## 文档：让用户能行动，让维护者能定位

### D1 · ripgrep：先给真实行为与可运行路径

- README: https://github.com/BurntSushi/ripgrep/blob/14.1.1/README.md
- Guide: https://github.com/BurntSushi/ripgrep/blob/14.1.1/GUIDE.md

**提炼：** README 先说用途、关键默认行为和最快开始；示例交代前提、操作和可辨认结果，不用宣传词替代行为描述。

### D2 · Django：按读者任务分离教程、指南、参考与说明

- Documentation contribution guide: https://github.com/django/django/blob/5.2/docs/internals/contributing/writing-documentation.txt
- Tutorial: https://github.com/django/django/blob/5.2/docs/intro/tutorial01.txt

**提炼：** 文档信息架构围绕读者要完成的任务，不围绕作者写代码的顺序；教程让人做成，参考让人查准。

### D3 · Rust 标准库：写类型签名表达不了的语义

- `std::env`: https://github.com/rust-lang/rust/blob/1.81.0/library/std/src/env.rs

**提炼：** 接口文档优先说明错误、平台差异、时机、副作用和限制，而不是复述函数名与类型。

### D4 · rust-analyzer：架构文档记录边界及刻意不存在的依赖

- Architecture: https://github.com/rust-lang/rust-analyzer/blob/2024-09-16/docs/dev/architecture.md

**提炼：** 架构说明应告诉维护者主路径、责任、依赖方向和有意保持的隔离，使新会话知道“该改哪里”以及“什么不该被补进去”。

<a id="portability"></a>
## Skill 可移植性：格式标准化，行为去平台化

- Agent Skills specification: https://agentskills.io/specification

**提炼：** `SKILL.md` 使用最小标准 frontmatter、相对引用和渐进加载；核心行为以语义动作描述，不绑定特定 harness 的工具名或命令。平台安装路径与 UI 元数据是适配层，不是 Skill 的工程逻辑。
<a id="lifecycle"></a>
## 生命周期补充：按目标选择，不把流程叠满

### R1 · Django：发布的是用户能安装的实际产物

- 历史样本 `5.2`：[docs/internals/howto-release-django.txt](https://github.com/django/django/blob/5.2/docs/internals/howto-release-django.txt)
- 本次读取的原文：https://raw.githubusercontent.com/django/django/5.2/docs/internals/howto-release-django.txt

**项目事实：** 发布指南将创建产物、检查安装与最小功能、发布与用户公告分开；也要求更新版本与说明，并清理已走完弃用周期的功能。

**提炼：** release 关注最终交付物，而非仅有工作目录；准备发布与实际外部发布分开，完成用户可操作的升级说明。

**限制：** 不照搬其 PyPI、签名、时间安排、人员角色与全部检查。项目自己的发布约定优先，简单项目不建发布平台。

### R2 · Google SRE：先恢复用户，再做根因改进

- 官方原始实践：https://sre.google/sre-book/managing-incidents/

**项目事实：** 事件管理实践强调停止扩大损失、恢复服务、保留根因分析的证据，并避免未协调的独立生产变更。

**提炼：** operate 和 fix 分开；正在损害用户且请求处置时先恢复，稳定后再完成授权范围内的根因修复。

**限制：** 这是 Google 的运行实践，不是一个开源仓库源码样本。不把其完整人员编组移植到单人 Agent，也不把事件处置授权扩展成任意生产操作许可。

### R3 · Kubernetes：弃用提示包含移除与替代信息

- 当前政策（本次核查）：https://kubernetes.io/docs/reference/deprecation-policy/
- 历史代码 `v1.31.0`：[deprecation.go](https://github.com/kubernetes/kubernetes/blob/v1.31.0/staging/src/k8s.io/apiserver/pkg/endpoints/deprecation/deprecation.go)
- 本次读取的原文：https://raw.githubusercontent.com/kubernetes/kubernetes/v1.31.0/staging/src/k8s.io/apiserver/pkg/endpoints/deprecation/deprecation.go

**项目事实：** `WarningMessage` 根据对象声明组合弃用版本、可选移除版本与替代类型；政策按稳定级别区分支持规则，而非简单把所有旧东西永久保留。

**提炼：** retire 需要让消费者知道去哪里、何时变化与需要做什么；没有真实消费者的实验可直接清理，有承诺的能力有明确退出过程。

**限制：** 不照搬 Kubernetes 的年限或版本数量；服务下线、数据导出和资源收尾是本包的适配，不是上述单个函数提供的保证。

<a id="review-evidence"></a>
### R4 · Google、Go 与 curl：结论由证据和适用条件承担

[Google 审查标准](https://google.github.io/eng-practices/review/reviewer/standard.html) 区分实质问题与非阻塞修饰，允许整体质量改善的变更推进；[审查内容指南](https://google.github.io/eng-practices/review/reviewer/looking-for.html) 要求阅读相关上下文、关注用户行为与测试有效性。借鉴的是让发现能推动正确修改，不按评论数量或个人偏好判断审查价值。

**Go `go1.23.2`：** [`lostcancel.go`](https://github.com/golang/go/blob/go1.23.2/src/cmd/vendor/golang.org/x/tools/go/analysis/passes/lostcancel/lostcancel.go) 在控制流图中寻找取消函数未被使用就返回的路径，并关联定义处与返回处；它将任意变量引用计为使用，也对超出函数作用域的变量作保守假设。因此诊断提供的是其分析模型内的线索，沉默不是取消动作一定发生的证明。本地以同版本分析器做了四个小对照：分支遗漏被告警且行为检查失败；仅补变量引用后告警消失而行为仍失败；正确释放时两者通过；明确转交取消责任时，调用方检查通过且没有告警。这是工具机制试验，不是完整分析器评估或模型实验。

**curl 的反例：** [`curl-8_16_0/lib/hostip.c`](https://github.com/curl/curl/blob/curl-8_16_0/lib/hostip.c) 将 `Curl_resolv` 的输出参数注释为可选；在 [`curl-8_17_0` 的同文件](https://github.com/curl/curl/blob/curl-8_17_0/lib/hostip.c) 中，该说法被移除，实现仍要求有效输出参数。结合[维护者对该报告的说明](https://daniel.haxx.se/blog/2025/10/10/a-new-breed-of-analyzers/)，这支持把问题定位为错误的接口说明，而不是见到解引用就增加一层判空。这里只比较该注释与用法，不声称两个版本之间只有此项变化，也未编译审计全部 curl。

**提炼与边界：** 可疑形状先成为候选；用输入、真实调用、现有保证与后果建立可核查关系，复现与明确推导均可提供证据。再判断应修改实现、文档还是调用者。真实对外承诺允许空值时仍须修实现，不能照抄 curl 的结论；其他受支持配置未在本机运行，也不等于缺陷不存在。复核须证实原关系不再成立或原判断有误，不能从评论关闭、未再告警推断修复。只读与修改的授权边界仍由用户决定。

## 修改过程：保护已有工作与可观察中间态

### Git：切换状态时不把本地修改当成可覆盖缓存

- 文档：https://git-scm.com/docs/git-checkout

**项目事实：** 分支切换会覆盖本地修改时，`git checkout` 默认拒绝；显式 `--merge` 才暂存这些修改、切换后重新应用。Git 因此区分目标树状态与工作区中尚未归入目标树的现有工作。

**提炼：** Agent 可以为了理解读取宽范围，但不能把“被读到”当成写权限。恢复、回滚和切换方向时，先区分本次产生的修改与会话前已存在的人类或其他执行者工作；只能安全归因的部分才默认可撤销。

**限制：** 不要求每个任务都 commit/stash，也不把 Git 当成所有远端、数据库或编辑器状态的唯一事实源；具体恢复方式仍由当前系统决定。

### SQLite：中间状态可见时，修改方式属于正确性

- 官方说明：https://www.sqlite.org/atomiccommit.html

**项目事实：** SQLite 在修改数据库页前先建立 rollback journal，使崩溃发生在提交过程的任意中间点时仍能判定并恢复到一致状态；提交边界不是“最终字节碰巧正确”，而是经过可恢复的状态转移。

**提炼：** 当 watcher、并发读者、热重载或外部系统能观察写入过程时，最终内容之外还要保护中间状态；优先复用已有事务、临时文件、锁、原子替换或分阶段发布机制。若不存在可观察中间态，就不为普通编辑增加事务架构。

**限制：** 这是状态转移原则，不是让代码 Agent 模拟 SQLite 日志协议；工具原子性和文件系统保证必须以实际环境为准。

### Git 测试框架：测试安全来自隔离资源，不来自“测试”名称

- 源码：`t/test-lib.sh`、`t/t4139-apply-escape.sh`（v2.46.0）

**项目事实：** Git 的测试框架明确在 `trash directory` 子目录运行测试；路径逃逸测试还会额外下沉一层，避免失败用例真的写出 trash directory。

**提炼：** 测试、预览和 dry-run 是否安全，要看它最终触及的资源身份和副作用。具有清空、覆盖、迁移等能力的测试应把可丢弃资源显式作为输入，而不是默认复用项目真实数据位置。

**限制：** 不要求所有测试都创建独立进程或容器；只在副作用可能碰到真实状态时建立相称隔离。

### Git lockfile + Kubernetes resourceVersion：发布既要互斥，也要防止旧结果覆盖新状态

- Git 源码：`lockfile.h`（v2.46.0）
- Kubernetes API 概念：https://kubernetes.io/docs/reference/using-api/api-concepts/

**项目事实：** Git lockfile 用独占 `.lock` 文件和最终 rename 提供写者互斥与原子替换；Kubernetes 的对象更新带 `resourceVersion`，客户端基于已过期版本提交 PUT 时服务端返回冲突，避免 lost update。

**提炼：** 并行或后台结果如果可能晚于更新后的目标到达，不能只保证“同一时刻只有一个写者”，还要判断结果是否仍新鲜。优先复用项目已有的锁、版本、generation、ETag、前置条件或隔离产物；目标在工作期间已经变化，就重新读取/合并或丢弃旧结果，而不是凭完成顺序覆盖。

**限制：** 不为单线程、无共享目标的普通修改新增锁或版本系统；具体机制由现有存储和协议决定。

## 路由到依据的映射

| 路线 / 公共原则 | 主要依据 | 本包新增判断 |
| --- | --- | --- |
| frame、build | S1–S2、D4 | 可逆选择自定；设计与实施按交付物分开 |
| review | R4、S6 | 审查不等于修改授权 |
| release | R1、S3–S4 | 准备、发布、回退按实际责任区分 |
| operate | R2、S4–S5 | 先恢复，再进入授权范围内的修复 |
| fix | S4、S6 | 目标复现服务根因修复，不重演流程 |
| optimize | S7 | 只声明负载与观测支持的收益 |
| evolve | S2–S6、D4 | 完成切换与旧路径收尾 |
| retire | R3、R1 | 消费者、数据、服务与资源分别处理 |
| document | D1–D4 | 文档交付正文，按读者任务组织 |
| 契约与状态专题 | S3–S5、R3 | 根据触及的责任加载，不按项目版本堆要求 |
| 轻入口、相对模块 | Agent Skills 规范 | 单主路线与冲突优先级属于本包设计 |

路线并非对这些项目质量的排名，也不是它们共同采用的十步生命周期。未运行模型与真实项目对照前，不宣称该路由能保证更高完成率、更低回归率或所有 harness 行为一致。

<a id="router-v2"></a>
## 可执行路由与 AI 编码痛点补充

本次升级保留上述工程和文档依据，不再要求按表人工维护十份平行流程。参考用户指定的 reverse-skill 的独立入口、配置驱动 PRIMARY、ACTION 衔接和经验回流，新增离线分派器与按事实加载的专项技能；详细读过的文件、借鉴和有意不照搬的部分见[路由设计](routing-design.md)。本包未执行上游脚本或复制其渗透测试内容。

[AI 编码痛点研究](ai-coding-pain-points.md)给出 2025 开发者调查、2025–2026 官方工程案例、USENIX 论文及 2026 预印本的原始来源、样本边界和对应行为。architecture、dependencies、interface、recovery、handoff 分别针对责任层、依赖幻觉、未接通的交互、无信息循环和接续丢失；contracts 与 state 延续真实承诺和实际边界规则。它们是工程上的干预设计，不是已证实的效果量。

路由规则的权威来源是 config/routing.json；本文件只记录设计依据，不维护第二份优先级、路径或能力登记。
