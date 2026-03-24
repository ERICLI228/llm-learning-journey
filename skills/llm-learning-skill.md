# 🎓 LLM 学习助手 - OpenClaw Skill

## 功能说明

此技能用于辅助 3 个月大模型转型计划，提供以下能力：

### 模型调用命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `/llm-model <model>` | 切换当前使用的模型 | `/llm-model gemini` |
| `/llm-compare` | 对比多个模型的响应 | `/llm-compare 今天天气如何` |
| `/llm-explain <concept>` | 用简单语言解释大模型概念 | `/llm-explain Attention 机制` |
| `/llm-prompt <task>` | 生成提示工程模板 | `/llm-prompt TK 选品分析` |

### 学习追踪命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `/llm-progress` | 查看当前学习进度 | `/llm-progress` |
| `/llm-log <note>` | 记录今日学习日志 | `/llm-log 今天学习了 Transformer` |
| `/llm-review` | 回顾本周学习内容 | `/llm-review` |

### 项目命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `/llm-rag <query>` | 检索知识库回答问题 | `/llm-rag 选品标准` |
| `/llm-agent <task>` | 触发多智能体工作流 | `/llm-agent 选品` |
| `/llm-finetune` | 启动微调实验 | `/llm-finetune` |

---

## 模型配置

```yaml
models:
  daily:
    - google/gemini-2.5-pro      # 日常主力（无限量）
    - aliyun/qwen3.5-plus        # 代码/低成本任务
  premium:
    - github-copilot/claude-sonnet-4.5  # 复杂推理
    - github-copilot/claude-opus-4.5    # 关键任务
  local:
    - ollama/qwen2.5:7b          # 离线测试
```

---

## 学习资源链接

### 课程
- [Generative AI with LLMs - DeepLearning.AI](https://www.deeplearning.ai/courses/generative-ai-with-llms/)
- [Prompt Engineering for Developers - DeepLearning.AI](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)

### 论文
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685)

### 工具文档
- [LangChain Docs](https://python.langchain.com/)
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [Unsloth Docs](https://docs.unsloth.ai/)

---

## 验收检查清单

### 阶段 1 验收
- [ ] 能用自己的话解释 Attention 机制
- [ ] NotebookLM 中有 Transformer 知识卡片
- [ ] 掌握零样本、少样本、思维链提示技巧
- [ ] 能写出 TK 选品分析提示模板
- [ ] Ollama 本地模型正常响应
- [ ] OpenClaw 能调用 Gemini/Qwen/Copilot
- [ ] 智能客服原型在飞书群正常工作
- [ ] Notion 学习数据库建立完成

### 阶段 2 验收
- [ ] RAG 系统能回答内部文档问题
- [ ] `/rag` 命令在飞书群正常工作
- [ ] 微调数据集格式正确（50+ 条）
- [ ] LoRA 微调实验完成
- [ ] 多智能体系统能协作工作
- [ ] OpenClaw 技能封装完成
- [ ] 技术总结笔记完成

### 阶段 3 验收
- [ ] 系统架构图完成
- [ ] GitHub 仓库有完整代码和 README
- [ ] 微调模型部署为 API，响应<3 秒
- [ ] 端到端测试通过
- [ ] 成本优化报告完成（降低 30%+）
- [ ] 技术博客发布（阅读>500）
- [ ] 学习成果集可分享

---

*创建日期：2026-03-24*
