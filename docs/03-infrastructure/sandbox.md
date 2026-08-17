# Sandbox

**中文建议：** 沙箱 / 隔离执行环境  
**成熟度：** 🟢  
**词条状态：** ✅ Atlas-quality  
**重要程度：** ★★★★★  
**学习阶段：** 入门 → 工程实践  
**最后更新：** 2026-08-17

---

## 30 秒理解

**Sandbox 是给 Agent 一个“可以动手，但不能随便碰真实世界”的受控工作区。**

当 Agent 能运行 Shell、编辑文件、安装依赖甚至执行模型生成的代码时，直接把它放到真实宿主机上风险很高。

Sandbox 的核心目标就是：

> **让 Agent 有足够能力完成任务，同时把文件、网络、权限、凭据和系统资源限制在明确边界内。**

---

## 先建立一个直觉

想象你要让一个很聪明、但偶尔会误操作的实习生测试一段代码。

你不会直接把：

- 生产数据库密码；
- 公司主服务器 root 权限；
- 全部客户文件；

交给他。

更合理的做法是给他一个实验室：

```text
Sandbox
├── 可以看到任务需要的文件
├── 可以运行命令
├── 可以安装允许的依赖
├── 网络访问可限制
├── 凭据可隔离
└── 出问题时可以直接销毁重建
```

这就是 Sandbox 的工程直觉。

---

## 为什么 Agent 特别需要 Sandbox？

传统程序执行的是开发者提前写好的代码。

Agent 则可能在运行过程中动态产生：

```text
shell command
file edit
Python code
browser action
package install
network request
```

这些动作并不总是能被开发者在运行前完全预测。

风险包括：

- 误删文件；
- 泄露凭据；
- 访问不该访问的目录；
- 执行危险命令；
- 被 prompt injection 诱导外传数据；
- 安装恶意依赖；
- 破坏生产环境。

因此 Sandbox 是 Agent 从“能做事”走向“能安全做事”的重要基础设施。

---

## 技术定义

在 Agent Atlas 中：

> **Sandbox 是一个受控的执行边界，用于隔离 Agent 的代码、命令、文件和其他高风险操作，并限制其能够访问的资源与外部系统。**

Sandbox 可以用不同技术实现：

- 本地受控目录；
- Docker / container；
- 虚拟机；
- 云端隔离 workspace；
- 远程 provider-managed sandbox。

所以 `Sandbox` 描述的是**安全与隔离职责**，不等于某一种特定技术。

---

## 你可能是在这句话里遇到它

> “The agent runs the generated code inside a sandbox before returning the artifact.”

这句话的实际流程可能是：

```text
Model 生成代码
   ↓
Harness 判断需要执行
   ↓
Runtime 连接 Sandbox
   ↓
Sandbox 中写入文件
   ↓
运行代码
   ↓
得到 stdout / files / artifacts
   ↓
结果返回 Agent Loop
```

重点在 `inside a sandbox`：

代码确实被执行了，但执行地点和权限被限制在一个受控边界中。

---

## Sandbox 通常限制什么？

### 文件系统

```text
允许：/workspace/project
禁止：宿主机其他目录
```

### 网络

```text
允许：指定 API
禁止：任意外网访问
```

### 凭据

尽量避免把真正的 API key、SSH key、数据库密码直接暴露给模型生成的代码。

### 系统能力

例如：

- CPU / Memory 限额；
- 最大运行时间；
- 进程数量；
- package install；
- privileged operations。

### 生命周期

任务结束后可以：

```text
snapshot
archive
reset
destroy
```

---

## Sandbox ≠ Runtime

这是 Agent Atlas 核心 Concept Boundary 之一。

```text
Runtime
= 管整个 run / session 怎么执行

Sandbox
= 某些实际操作在哪个受控边界里执行
```

一个 Runtime 可以：

- 不使用 Sandbox；
- 使用一个 Sandbox；
- 为不同 Sub-agent 创建多个 Sandbox。

因此：

> **Sandbox 通常是 Runtime 可以管理的一种 execution environment，而不是 Runtime 本身。**

→ [Runtime](runtime.md)

---

## Sandbox ≠ Permission System

Sandbox 和权限控制相关，但不是同一件事。

```text
Permission / Approval
= 这件事“可不可以做”

Sandbox
= 这件事“在哪里、以什么边界做”
```

例如：

用户批准 Agent 执行：

```text
npm install
```

仍然可以要求它只在隔离容器中执行。

这两个机制应该叠加，而不是二选一。

---

## Sandbox ≠ Security 的全部

把 Agent 放进 Docker 并不意味着系统自动安全。

Sandbox 仍然可能：

- 允许危险网络出口；
- 挂载敏感目录；
- 注入真实凭据；
- 暴露过高权限；
- 把恶意工具输出重新送回模型。

因此完整安全体系还需要：

```text
Sandbox
+ Permissions
+ Credential isolation
+ Network policy
+ Tool policy
+ Prompt-injection defenses
+ Logging / Tracing
```

---

## 为什么现在强调 “Harness 和 Compute 分离”？

OpenAI 2026 年的 Agents SDK 演进明确强调：

```text
Harness / Brain
       ↓ controls
Sandbox / Compute
```

可以分离运行。

这样做的好处之一是：

> **模型生成的代码所在环境不需要直接持有 orchestration credentials。**

如果 Sandbox 崩溃或过期，只要 Agent State 被保存在外部，Runtime 还可以新建 Sandbox、恢复 snapshot 并继续任务。

这使 Sandbox 不再只是“安全小盒子”，还成为长时间 Agent 的**可替换计算工作区**。

---

## 一个现代 Sandbox Agent 心智模型

```text
Agent Definition
├── instructions
├── tools
├── handoffs
└── capabilities
        ↓
Runner / Runtime
        ↓
Sandbox Session
├── workspace files
├── shell
├── dependencies
├── mounts
└── snapshot
```

OpenAI Agents SDK 当前就把 `SandboxAgent` 的定义和每次 run 使用的 `SandboxRunConfig / client / live session` 分开。

这说明：

> **“Agent 是谁”与“这一次 Agent 在哪里工作”是两个不同问题。**

---

## Concept Graph Relations

```text
Harness ─manages────────→ Runtime

Runtime ─connects────────→ Sandbox

Sandbox ─isolates────────→ Code Execution
Sandbox ─isolates────────→ Shell
Sandbox ─contains────────→ Workspace

State ─can-reference─────→ Snapshot
Snapshot ─restores───────→ Sandbox

Permissions ─gates───────→ Actions
```

---

## 常见误解

### ❌ Sandbox = Docker

Docker 是一种常见实现，但 Sandbox 是更广的安全边界概念。

### ❌ 有 Sandbox 就绝对安全

不是。网络、凭据、挂载和权限配置仍然可能造成风险。

### ❌ Sandbox 就是 Agent 的 Memory

不是。Sandbox 文件可以被用作 memory，但 Memory 是“信息如何被保存和再次利用”的更广机制。

### ❌ Sandbox 必须每轮销毁

不一定。现代长时间 Agent 经常使用持久 session、snapshot 和 resume。

---

## Terminology Observatory

**成熟度：🟢 稳定概念。**

Sandbox 是计算机安全与软件工程中的成熟术语。

Agent 时代的新变化不是“发明了 Sandbox”，而是 Sandbox 开始成为 Coding Agent、Computer-use Agent 和长时间 Agent 的核心运行组件，并与 Agent State、Snapshot、Harness 分离等架构更紧密地结合。

---

## 下一步应该学什么？

1. [Runtime](runtime.md) —— 谁创建和管理 Sandbox；
2. [Harness](harness.md) —— 更上层的运行控制系统；
3. [Tool Calling](../04-tools/tool-calling.md) —— 什么动作可能被送进 Sandbox 执行；
4. [State](state.md) —— Sandbox 消失后任务如何恢复；
5. Memory —— 文件型 memory 和持久 workspace 有什么关系。

---

## 一手资料

- OpenAI, The next evolution of the Agents SDK: https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- OpenAI Agents SDK, Sandbox concepts: https://openai.github.io/openai-agents-python/sandbox/guide/
- OpenAI Agents SDK, Sandbox clients: https://openai.github.io/openai-agents-python/sandbox/clients/
- OpenAI Agents SDK, Sandbox quickstart: https://openai.github.io/openai-agents-python/sandbox_agents/
