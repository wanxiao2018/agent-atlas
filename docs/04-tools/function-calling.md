# Function Calling

**中文建议：** 函数调用  
**成熟度：** 🟢  
**重要程度：** ★★★★☆

## 一句话解释

模型按照预定义 schema 生成函数名和参数，由宿主程序解析并执行对应函数。

## 为什么需要它？

它把“模型想使用外部能力”转换为结构化、可验证的机器接口，减少依赖自由文本解析。

## 在 Agent 系统中的位置

Function Calling 常用于实现 Tool Calling，但不同平台可能使用不同术语和接口形式。

## 最容易混淆

模型通常**不会亲自执行函数**。它生成调用请求；Harness / Runtime / 应用代码负责真正执行，再把结果返回模型。

## 相关概念

- [Tool Calling](tool-calling.md)
- [MCP](mcp.md)
- [Harness](../03-infrastructure/harness.md)
