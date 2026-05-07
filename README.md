# Commit Classifier Agent

> 基于 DeepSeek API 的 Git Commit 智能分类工具

自动将 `git log` 输出的 commit 消息分类为 feat、fix、docs、perf、refactor、test、chore、breaking 等类别，大幅提升 Changelog 整理效率。

## ✨ 功能特点

- 🚀 自动解析 `git log --oneline` 输出
- 🤖 调用 DeepSeek Chat API 进行智能分类
- 📊 输出各类别统计和详细分类结果
- 🔒 支持环境变量配置 API Key，安全可靠
- 💰 低成本：单次任务仅消耗约 1200 tokens

## 📋 分类类别

| 类别 | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更 |
| perf | 性能优化 |
| refactor | 代码重构 |
| test | 测试相关 |
| chore | 构建/依赖/工具变更 |
| breaking | 破坏性变更 |

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openai
