# 路由设计：借鉴 reverse-skill，而不搬它的业务流程

核查日期：2026-09-19。本次实际读取了上游 README、skills/SKILL.md、MASTER-ROUTING.md、config/routing.json、routing.md、master-route.sh / .ps1、test-routing.sh 和 field-journal 模板。读取的是当时 main 分支页面，不声明已取得不可变提交快照，也没有执行上游安装或安全操作脚本。

## 学的是什么

| reverse-skill 中的机制 | 本包对应实现 | 为一般编码做的调整 |
| --- | --- | --- |
| 全局入口与共同约束 | SKILL.md + RULES.md | 以完成授权成果为中心，不给每次修改建案件档案 |
| routing.json 单一事实源 | config/routing.json | 主路线、专项触发、优先级和能力都集中登记 |
| PRIMARY 快路径与独立 SKILL | scripts/route.py + skills/if-*/SKILL.md | 选出目标后立即执行 ACTION，不止于“已路由” |
| 脚本计分与冲突优先级 | 文本候选 + 显式 intent | 文本只推荐；真实交付目标优先，不用关键词推断授权 |
| 工具索引与按需自举 | CAPABILITIES + runtime.md | 使用宿主现有语义能力；不强制安装工具或注册服务 |
| 多场景衔接 | 显式 sequence / NEXT | 只保留用户已请求的后续目标，不擅自启动下一阶段 |
| field-journal | experience/README.md + handoff | 只沉淀有依据的项目教训，不每任务写流水账或改全局规则 |
| 路由测试和一致性检查 | tests/route-cases.json + catalog.py --check | 测路由和导出语义，不把路由通过冒充模型开发质量 |

这是原创的通用工程实现，未复制或分发上游脚本、渗透技能或工具链。引入的是模块组织方式和契约思路，不是给普通项目强加安全作业平台。

## 实际执行链

```text
用户当前目标 + 仓库事实 + 真实授权
    ↓
SKILL.md / RULES.md
    ↓
route.py（或同源 MASTER-ROUTING）
    ↓
PRIMARY + 已确认事实命中的 SUPPORT
    ↓
读取目标技能 → 执行 ACTION → 形成真实成果
    ↘ 卡住：recovery → 新观测 → 回到原目标
    ↘ 换会话：handoff → 仓库当前事实 → 继续
    ↓
完成当前范围；只有显式请求才衔接 NEXT
    ↓
非显然可复用经验 → 项目权威位置，不自动改全局包
```

## 单一事实源与职责

`routing.json` 保存路径、条件、优先级、目标和能力清单；`route.py` 只解释它并打印结果，不维护第二张路由表。`catalog.py` 生成 MASTER-ROUTING 和 INDEX，`--check` 检测漂移。每个子技能只定义自己的操作，不重新全局分类。

原始文本规则使用命中规则的最高权重，并按 priority 解并列；返回候选与 `needs_intent_check`，不输出伪装成概率的置信度。明确 intent 和 sequence 优先，sequence 必须以当前 intent 开始。真实工程语义仍由调用 Agent 理解，脚本不声称解决任意语言或复杂否定的语义解析。

SUPPORT 只由显式确认的布尔 facts 激活；文字线索仅进入 SUGGESTED_SUPPORT。一次默认加载最多两个专项，其余仍在 DEFERRED，触及对应边界前加载，不能当作免除。stage 只调整承诺倾向，不自动把成熟仓库的隔离实验变成兼容项目。

CAPABILITIES 仅表示任务需要和环境可用能力的差额；未知不等于不存在。路由程序不执行目标工具，因此也不构成权限防火墙。它不安装、不部署、不写工作目录、不改变模型设置、不创建后台任务。

## 跨 harness 分发

规范入口与语义能力保持中立；原生客户端是否递归发现子技能各不相同，所以路由器直接读取所选路径，不依赖子 Agent 或跨 Skill 调用 API。

canonical 包有一个总入口和独立子技能入口；single-entry 导出由同一源码自动将子入口转换为 GUIDE.md 并重写引用，适合只接受一个 SKILL.md 的导入器。两个版本不能手工分叉维护。

## 上游对应文件

- https://github.com/zhaoxuya520/reverse-skill
- https://github.com/zhaoxuya520/reverse-skill/blob/main/skills/MASTER-ROUTING.md
- https://github.com/zhaoxuya520/reverse-skill/blob/main/skills/config/routing.json
- https://github.com/zhaoxuya520/reverse-skill/blob/main/skills/scripts/master-route.sh
- https://github.com/zhaoxuya520/reverse-skill/blob/main/skills/scripts/master-route.ps1
- https://github.com/zhaoxuya520/reverse-skill/blob/main/skills/scripts/test-routing.sh
- https://github.com/zhaoxuya520/reverse-skill/blob/main/skills/field-journal/_template.md

格式规范：https://agentskills.io/specification 。这些来源说明借鉴关系，不代表上游认可本包，也不构成所有宿主的实机兼容证明。
