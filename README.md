# Invariant First

**选对方法，完成成果，让下一位接得住。**

跨 harness 的工程技能包：由当前交付目标选择主路线，按实际难点加载专项。共同方法是 [六项工程判断](RULES.md)，具体方法在子技能中；新场景按责任、语义与真实条件处理。

## 安装与开始

将完整 `invariant-first/` 放到当前工具支持的 Skills 目录，保留相对目录结构。升级时更新整个包，不只替换 `SKILL.md`；项目自己的规则照常保留。各宿主的发现方式见 [可移植性](references/portability.md)。

加载后直接给任务：

```text
使用 invariant-first 实现这个功能。保持现有 CLI 行为，完成代码和真实用法。
```

[总入口](SKILL.md) 读取共同判断，按目标打开对应子技能并执行。普通任务直接读取方法即可；路由脚本用于批量分派、集成或诊断。小改不需要加载整个目录。

完整包提供独立子技能入口；单入口版将子入口同源导出为 `GUIDE.md`，用于只接受一个 Skill 的导入器。两者都需要宿主能读取相对资源，自动发现并非 ZIP 本身提供的能力。

## 路线与专项

主路线覆盖定向 frame、开发 build、审查 review、发布 release、运行 operate、修复 fix、性能 optimize、演进 evolve、退役 retire 和文档 document。路线是方法选择，不是项目必须逐一经过的阶段。

handoff/recovery 在需要时恢复上下文与进展；architecture/contracts/state/dependencies/interface 分别处理结构、承诺、状态、依赖和交互。专项只补充当前目标，不扩大授权。路径、事实和加载顺序见 [技能地图](INDEX.md) 与 [分流表](MASTER-ROUTING.md)。

## 可选：运行分派器

使用已有 Python 3.10+，在本包根目录运行，无第三方依赖：

```sh
python scripts/route.py --request examples/route-request.json --format text
```

该示例的关键输出：

```text
PRIMARY -> skills/if-fix/SKILL.md
LOAD_NOW: skills/if-fix/SKILL.md, skills/if-state/SKILL.md, skills/if-contracts/SKILL.md
NEXT (requested only): release
```

完整输出见 [示例](examples/route-output.json)。选择方法后仍须执行任务；程序只读配置并打印结果，不修改项目。

也可以传入明确目标：

```sh
python scripts/route.py --task "修复重复写入问题" --intent fix --facts shared_state,external_effects,external_consumers
```

`intent` 表示调用者已判断的目标；省略时只是需核对的文本候选。`facts` 只填本次任务的已知条件。`stage` 调整实际承诺，不创建额外流程。`NEXT` 只包含显式请求的后续目标，不授予发布权限。

`LOAD_NOW` 包含当前主路线、需要的 prelude 及预算内的 domain 专项；其余在 `DEFERRED`，触及对应边界前读取。`CAPABILITIES.preferred/missing` 只描述本轮有用的能力，后续独有能力单列 `deferred`；缺少某个工具时先找等价能力，不为路由安装运行时。细节见 [路由设计](references/routing-design.md)。

## 维护本包

[AGENTS.md](AGENTS.md) 说明改进方法与修改落点：从原始反馈和成熟实现提炼因果关系，优先合并已有判断。共同规则维护一处，子技能保留独有行动；来源在 [机制归纳](references/ai-coding-pain-points.md)、[源码依据](references/source-lessons.md) 和 [文档方法](references/documentation.md)，不进入日常默认上下文。

路由配置的唯一来源是 `config/routing.json`；修改后生成视图并检查：

```sh
python scripts/catalog.py
python scripts/catalog.py --check
python -m unittest discover -s tests -v
```

这些命令维护本包，不要求用户项目采用同一流程。保持既有程序回归，模型效果则用 [迁移评估](references/evaluation.md) 单独判断；测试数量和规则数量不是效果指标。

从同一源码导出单入口目录：

```sh
python scripts/export_single.py --output ../single-entry/invariant-first
```

目标目录须不存在且位于源码树外。导出转换子入口及引用，排除版本库元数据和 Python 缓存，不修改源目录；不作为第二套手工维护源。

变更见 [CHANGELOG](CHANGELOG.md)。路由是指导而非强制执行器；执行权限、工具能力与实际加载由宿主控制。本包没有跨模型或跨 harness 效果一致性的保证。
