# mediahal_01201201 功能分析 Prompt 列表
本指南提供了一套标准化的指令模板，旨在辅助开发者为任意项目快速生成高质量的架构分析与调试文档。

**使用说明：**
请在 Prompt 中将以下变量替换为实际值：
*   `mediahal_01201201`: 项目名称（例如 `AmNuPlayer`）
*   `/home/bj17300-049u/work/mediahal_wraper/media_hal`: 源码根目录绝对路径（例如 `/home/code/AmNuPlayer`）
## 1. 初始化与目录结构 (Initialization)

**目标**：建立文档存储目录，并获取源码结构全貌。

**Prompt 指令：**
> 我正在分析一个名为 `mediahal_01201201` 的播放器项目，源码位于 `/home/bj17300-049u/work/mediahal_wraper/media_hal`。
> 请执行以下操作：
> 1.  创建一个名为 `debug_mediahal_01201201` 的文件夹，后续所有生成的文档都存放在此目录中。
> 2.  查看目录结构树文件 ，将分析结果整理并写入`debug_mediahal_01201201/mediahal_01201201_tree.txt`，不限制深度（`tree -P "*.c|*.cpp|*.h|*.java"`）。

---

## 2. 架构功能分析 (Architecture Analysis)
### 2.1 架构功能分析 (Architecture Analysis)
**目标**：理解代码组织结构，明确各模块职责。

**Prompt 指令：**
> 基于生成的 `mediahal_01201201_tree.txt` 目录结构，请逐一分析 `/home/bj17300-049u/work/mediahal_wraper/media_hal` 下每个主要目录及核心子目录的功能。
> 将分析结果整理并写入 `debug_mediahal_01201201/mediahal_01201201_Architecture.md`。
> 使用中文输出

### 2.2 架构图绘制 (Architecture Diagram)

**目标**：可视化模块交互与层次关系。

**Prompt 指令：**
> 根据 `mediahal_01201201_Architecture.md` 的分析，请使用 **Mermaid 8.14.0** 语法绘制 `mediahal_01201201` 的整体架构图。
> 请将 Mermaid 代码和简要说明写入 `debug_mediahal_01201201/mediahal_01201201_Architecture_Diagram.md`。

## 3. 列出核心功能 (Core Features)
### 3.1 列出核心功能 (Core Features)
**目标**：识别 `mediahal_01201201` 中最核心的功能模块。

**Prompt 指令：**
> 基于 `mediahal_01201201_Architecture.md` 架构，`mediahal_01201201_tree.txt` 目录结构和源码 `/home/bj17300-049u/work/mediahal_wraper/media_hal`分析，列出 `mediahal_01201201` 中生命周期管理、控制的功能模块。
> 将结果整理并写入 `debug_mediahal_01201201/mediahal_01201201_Core_Features.md`。
> 使用中文输出

### 3.2 核心功能名称替换
**目标**：将参考内容中的功能名称与核心功能模块的名称替换。

**Prompt 指令：**
> 基于 `mediahal_01201201_Core_Features.md` 中列出的核心功能模块，参考以下的格式替换功能名称。
> 将结果整理并写入 `debug_mediahal_01201201/mediahal_01201201_Core_Features_Prompts.md`。
> **禁止修改<PROJECT> <SOURCE_PATH> 内的内容，只替换功能名称即可**
> 使用中文输出
```markdown
## 4. 核心流程分析
### 4.1 功能流程 (功能)

**Prompt 指令：**

> 结合 `<PROJECT>_Architecture.md `架构图、目录结构树文件 `<PROJECT>_tree.txt`和源码 `<SOURCE_PATH>`，请深入分析播放器的**起播流程**。

> 1.  **核心调用链追踪**：梳理完整的函数调用路径。

> 2.  **关键日志**：核心调用中的关键日志，标识出排查功能失败（如 Open Failed, Prepare Timeout, Format Unsupported）时的关键函数入口和 Log 打印。

> 3.  将内容写入 `debug_<PROJECT>/<PROJECT>_功能_Flow.md`。

> 使用中文输出

#### 4.1.1 功能程架构图

**目标**：可视化模块交互与层次关系。

**Prompt 指令：**

> 根据 `<PROJECT>_功能_Flow.md` 的分析，请使用 **Mermaid 8.14.0** 语法绘制起播流程架构图。

> 请将 Mermaid 代码和简要说明写入 `debug_<PROJECT>/<PROJECT>_功能_Flow_Diagram.md`。
```