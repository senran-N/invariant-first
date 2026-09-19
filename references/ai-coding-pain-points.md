# AI 编码痛点 → 可执行纠偏

研究核查：2026-09-19。下列证据来自第一方开发者调查、官方工程案例与研究论文，不把网络吐槽当发生率。纠偏规则是本包的设计选择，不是已经完成的模型效果实验；调查是自报告，预印本和观察研究不建立普遍因果结论。

## P1 · 看起来快完成，核心路径却没接通

**观察。** Stack Overflow 2025 调查的 AI 困扰题（31,476 份回答，多选）中，66% 选择“答案接近正确但仍不对”，45% 选择调试 AI 代码更费时 [A6]。这是受访者体验，不是所有 AI 输出的错误率。Anthropic 的长任务案例也报告过提前宣布完成、界面存在但关键交互没有实现的问题 [A1–A2]。

**动作。** build 接通真实入口，interface 完成用户动作，release 检查真正分发的产物。结果区分实现、运行、集成和发布；不额外设置空洞的“完成检查报告”。

## P2 · 找对文件，改错责任层

**观察。** 2026 年预印本《Beyond Resolution Rates》分析 9,374 条轨迹、19 个 Agent、500 个 SWE-bench Verified 任务；其对 12 个简单补丁却始终未解出的任务做的定性分析中，10 个表现为架构层级判断问题 [A4]。例如在显示后端修改症状，而非在序列化处修正不应持久化的值。这是特定 Python 基准和小型子样本，不代表所有失败都属于此类。

**动作。** architecture 追踪数据生产、转换与消费责任；fix 修最早失真的事实，不让每个消费者添加 fallback。结构改动围绕同一根因，不能因此重写无关系统。

## P3 · 上下文越长越乱，换会话又重新猜

**观察。** Anthropic 官方案例讨论了跨上下文会话的半成品、重复定位与过早结束；上下文工程文章说明应按需取信息并留下稳定接续材料 [A1、A3]。这些是特定系统中的工程经验，不证明某个固定日志模板对所有模型最优。

**动作。** 路由仅加载当前 PRIMARY 和实际需要的 SUPPORT。handoff 核对当前文件，保留目标、真实进度、关键决定、最近反馈与下一动作；稳定事实回到代码或文档，不复制整段聊天，不强制每次小改记日志。

## P4 · 虚构包、API 或当前版本不支持的用法

**观察。** USENIX Security 2025 的包幻觉研究在 16 个模型、576,000 个 Python/JavaScript 代码样本上观察到不存在的包名及其供应链风险 [A5]。不要把研究中的历史模型比例当成 2026 年所有模型的实时水平。

**动作。** dependencies 先看锁文件、已装版本的类型/源码和真实同类调用；新增包还核对官方来源与登记身份。不能因为某包名现在能搜到，就把它当成原本想使用的可信项目。环境受阻走 runtime，不删除锁文件反复重装。

## P5 · 擅自扩大范围、忽略明确约束、过度防御

**观察。** 2026 年预印本《How Coding Agents Fail Their Users》观察了来自 1,639 个仓库的 20,574 场会话，用开发者的纠正识别失配；它区分了约束违反、意图误读、越界和代码错误，并记录了对已验证数据继续叠加检查的实例 [A7]。公开日志不含所有背景，依赖开发者反馈的识别也会遗漏未被指出的问题。

**动作。** 先确定交付物和授权；read-only review、document 与实际部署分开。自主决定可逆内部选择不等于扩张需求。共同规则要求 guard 有责任和实际失败依据，contracts 只为真实消费者加载。

## P6 · 工具用错、反复失败，却没有新信息

**观察。** 上述会话研究包括路径、环境与目标选择错误 [A7]；轨迹研究显示动作顺序与结果有关，也强调长轨迹不能简单等同于失败，任务难度和模型是混杂因素 [A4]。

**动作。** recovery 不按固定尝试次数强行放弃，而是在反馈重复、没有新信息时换观测；确认实际目录、目标与版本，缩小复现，追事实生产处。它保留原 PRIMARY，不重启整个任务、不回滚用户工作。

## P7 · 过度搜索、流程堆叠与提示冲突

**观察。** OpenAI 的 GPT-5 提示指南描述过过强上下文搜集要求导致重复搜索，以及互相冲突的指令妨碍任务推进的案例 [A8]。这支持避免矛盾和无边界调查，但不是取消必要阅读、测量或检查的证据。

**动作。** 明确目标、一个 PRIMARY、有限即时加载、其余按边界读取。找到足以行动的信息就实现；继续调查必须能改变决定。没有默认 plan/review Agent、阶段数据库、全仓审计或强制红绿重演。

## P8 · 自报完成不可靠，文档与事实逐渐分叉

**观察。** 会话研究把不准确自报单独分类，包含把部分实现和未证实状态说成完成 [A7]；官方长任务案例同样指出完成判断问题 [A1]。文档漂移和测试弱化在本包中作为工程风险处理，不据此捏造其总体发生率。

**动作。** DONE 是具体成果，不是写了报告。一个规则一个权威位置，调用和文档同改。禁止删除预期、把替身当集成、把未运行当通过；经验回流只写有条件、有依据、可失效的教训。

## 来源

- **A1** Anthropic, Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **A2** Anthropic, Harness design for long-running application development: https://www.anthropic.com/engineering/harness-design-long-running-apps
- **A3** Anthropic, Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **A4** Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure，2026 年预印本：https://arxiv.org/html/2604.02547
- **A5** Spracklen et al., We Have a Package for You!, USENIX Security 2025: https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen
- **A6** Stack Overflow 2025 Developer Survey, AI section: https://survey.stackoverflow.co/2025/ai
- **A7** How Coding Agents Fail Their Users，2026 年预印本 v2：https://arxiv.org/html/2605.29442v2
- **A8** OpenAI, GPT-5 prompting guide: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide

没有在真实项目上用同一模型和相同预算做对照前，不宣称这些规则已降低回归率、提升开发速度，或让所有 harness 产生相同效果。路由器的结构测试只能证明分派实现符合本包定义。
