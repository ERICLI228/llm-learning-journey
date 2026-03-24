# ⚙️ OpenClaw 学习配置指南

## 模型配置

### 推荐配置

在 OpenClaw 配置文件中添加以下模型配置：

```yaml
models:
  # 日常主力模型（无限量/高额度）
  daily:
    - id: gemini-daily
      model: google/gemini-2.5-pro
      description: "日常学习主力，用于 RAG 问答、概念解释"
      
    - id: qwen-code
      model: aliyun/qwen3.5-plus
      description: "代码生成、低成本任务"
  
  # 高级模型（有限额度，谨慎使用）
  premium:
    - id: claude-sonnet
      model: github-copilot/claude-sonnet-4.5
      description: "复杂推理、代码审查"
      
    - id: claude-opus
      model: github-copilot/claude-opus-4.5
      description: "关键任务、最终审核"
  
  # 本地模型（离线、隐私）
  local:
    - id: ollama-qwen
      model: ollama/qwen2.5:7b
      description: "本地测试、隐私任务"
```

---

## 智能体配置

### 学习助手智能体

创建一个新的智能体配置：

```yaml
agents:
  - id: llm-tutor
    name: "🎓 LLM 学习助手"
    model: google/gemini-2.5-pro
    description: "辅助大模型学习，解答概念问题"
    systemPrompt: |
      你是一位专业的大模型学习助手，正在帮助用户完成 3 个月的大模型转型计划。
      
      你的职责：
      1. 用简单易懂的语言解释大模型相关概念
      2. 提供实践建议和代码示例
      3. 帮助用户理解论文和文档
      4. 生成学习测验和复习材料
      
      回答风格：
      - 简洁清晰，避免过度学术化
      - 多用类比和实例
      - 鼓励用户动手实践
      - 适时提问检查理解程度
```

### 提示工程助手

```yaml
agents:
  - id: prompt-engineer
    name: "✍️ 提示工程助手"
    model: aliyun/qwen3.5-plus
    description: "优化提示词，生成模板"
    systemPrompt: |
      你是提示工程专家，帮助用户优化提示词。
      
      你的职责：
      1. 分析用户提示词的问题
      2. 提供优化建议
      3. 生成改进版本
      4. 解释优化原因
      
      优化方向：
      - 清晰度：确保指令明确
      - 上下文：提供必要背景
      - 示例：添加 few-shot 示例
      - 格式：指定输出格式
```

### 代码助手

```yaml
agents:
  - id: code-helper
    name: "💻 代码助手"
    model: github-copilot/claude-sonnet-4.5
    description: "辅助代码编写、审查、调试"
    systemPrompt: |
      你是编程助手，帮助用户完成大模型相关的代码任务。
      
      你的职责：
      1. 编写 LangChain/LlamaIndex 代码
      2. 调试模型调用代码
      3. 代码审查和优化建议
      4. 解释代码原理
      
      注意：
      - 优先使用开源库
      - 添加详细注释
      - 考虑性能和成本
      - 提供测试建议
```

---

## 快捷命令配置

### 学习相关命令

在 OpenClaw 配置中添加：

```yaml
commands:
  - name: llm-progress
    description: "查看学习进度"
    handler: |
      读取 ~/.openclaw/workspace/learning/llm-transformation/WBS-MASTER.md
      提取当前周次和完成状态
      生成进度报告

  - name: llm-log
    description: "记录学习日志"
    handler: |
      追加内容到 ~/.openclaw/workspace/learning/llm-transformation/logs/YYYY-MM-DD.md
      同时更新 Notion（如果配置了集成）

  - name: llm-review
    description: "周复习"
    handler: |
      读取本周所有学习日志
      生成复习大纲
      列出需要重点复习的概念
```

---

## 飞书集成

### 飞书群命令配置

在飞书群中可以使用的命令：

| 命令 | 功能 | 示例 |
|------|------|------|
| `/model <name>` | 切换模型 | `/model gemini` |
| `/compare <prompt>` | 对比模型响应 | `/compare 解释 Attention` |
| `/explain <concept>` | 解释概念 | `/explain Transformer` |
| `/prompt <task>` | 生成提示模板 | `/prompt TK 选品` |
| `/progress` | 查看学习进度 | `/progress` |
| `/log <note>` | 记录日志 | `/log 今天学习了 RAG` |

---

## 技能开发（阶段 2-3）

### RAG 技能模板

```python
# skills/llm-rag/SKILL.md
# 阶段 2 开发

def rag_query(query, collection="llm-learning"):
    """
    检索学习笔记知识库
    
    Args:
        query: 用户问题
        collection: 知识库集合名
    
    Returns:
        检索结果 + 模型生成的答案
    """
    # 使用 LangChain + Chroma 实现
    pass
```

### Agent 技能模板

```python
# skills/llm-agent/SKILL.md
# 阶段 2-3 开发

def multi_agent_workflow(task):
    """
    多智能体协作工作流
    
    Args:
        task: 用户任务（如"选品并生成视频脚本"）
    
    Returns:
        各智能体的输出汇总
    """
    # 使用 LangGraph 实现
    # 1. 选品 Agent
    # 2. 内容 Agent
    # 3. 广告 Agent
    pass
```

---

## 成本追踪

### 模型用量统计

配置 OpenClaw 记录每次调用的成本：

```yaml
usage:
  track: true
  logFile: ~/.openclaw/workspace/learning/llm-transformation/usage-log.json
  dailyLimit:
    gemini: unlimited
    qwen: $5
    claude: $2
```

### 每周成本报告

使用以下命令查看本周成本：

```bash
openclaw usage --weekly --project llm-learning
```

---

## 故障排查

### 常见问题

**Q: 模型调用失败**
```bash
# 检查配置
openclaw config get models

# 测试连接
openclaw model test google/gemini-2.5-pro
```

**Q: Ollama 无法启动**
```bash
# 检查服务状态
ollama list

# 重新启动
ollama serve
```

**Q: 飞书命令无响应**
```bash
# 检查飞书集成
openclaw channels status feishu

# 重新授权
openclaw channels auth feishu
```

---

## 下一步

1. **立即执行**：
   - [ ] 检查当前 OpenClaw 配置
   - [ ] 添加学习助手智能体
   - [ ] 测试模型调用

2. **本周完成**：
   - [ ] 配置所有推荐模型
   - [ ] 测试飞书命令
   - [ ] 创建使用文档

3. **阶段 2 开发**：
   - [ ] RAG 技能
   - [ ] Agent 技能
   - [ ] 微调集成

---

*创建日期：2026-03-24*
