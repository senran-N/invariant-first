# Invariant First

**选对方法，完成成果，让下一位接得住。**

跨 harness 的工程技能包：把优秀工程师识别条件、作出取舍、用反馈校正的判断压缩成可调用的方法，而不是积累错误禁令。由当前交付目标选择主路线，按实际难点加载专项；共同方法是 [六项工程判断](RULES.md)。

## 安装与开始

运行时安装优先使用 **single-entry 导出**：整个目录仍完整保留，但只有根 `SKILL.md` 可被宿主发现，子方法是按需读取的 `GUIDE.md` 资源。升级时先替换整个 Skill 目录，不只覆盖 `SKILL.md`，再让宿主重新加载资源；项目自己的规则照常保留。源码仓库中的多 `SKILL.md` 结构用于维护和受控寻址，不应直接交给会递归发现嵌套 Skill 的宿主。各宿主的发现方式见 [可移植性](references/portability.md)。

加载后直接给任务：

```text
使用 invariant-first 实现这个功能。保持现有 CLI 行为，完成代码和真实用法。
```

[总入口](SKILL.md) 内置从清单生成的方法地图：按目标选方法，按登记链接打开真实文件。路径相对于安装的根入口，不是项目工作目录。普通任务不必运行路由脚本，也不必先读完整分流表。

源码包保留独立子技能入口，便于维护、测试与需要显式寻址的宿主；**默认运行时分发使用单入口版**，把子入口同源导出为 `GUIDE.md`，避免递归扫描器绕过根路由或保留已删除子技能的发现记录。两种形态都需要宿主能读取相对资源。

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

[AGENTS.md](AGENTS.md) 规定改进方法与修改落点：先搜论坛与作者博客的真实痛点，再对照成熟仓库的版本化源码与不同取舍，提炼可迁移判断并检验条件变化；优先替换已有表述，不一事一禁令。共同规则维护一处，子技能保留独有行动；来源在 [机制归纳](references/ai-coding-pain-points.md)、[源码依据](references/source-lessons.md) 和 [文档方法](references/documentation.md)，不进入日常默认上下文。

路由配置只在 `config/routing.json` 维护；修改后生成根入口的方法地图、MASTER-ROUTING 与 INDEX：

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

目标目录须不存在且位于源码树外，同一目标串行导出。转换在目标父目录下的临时目录完成，资源与入口检查通过后再移到正式位置；正常异常会清理本次临时内容，修正原因后可重用原目标路径。多个方法映射到同一文件，或转换会覆盖已有资源时，导出报错并保留源文件。

导出仍会转换子入口及引用、排除版本库元数据和 Python 缓存，不修改源目录，也不形成第二套手工维护源。强制终止或系统故障可能留下临时目录，此机制不提供断电恢复或多写者协调。

变更见 [CHANGELOG](CHANGELOG.md)。路由是指导而非强制执行器；执行权限、工具能力与实际加载由宿主控制。本包没有跨模型或跨 harness 效果一致性的保证。
