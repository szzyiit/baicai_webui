# Obsidian 格式支持说明

## 概述

本项目已经添加了对 Obsidian 特有格式的完整支持，使得 Obsidian 创建的 Markdown 文件可以在 Streamlit Web 应用中优雅地显示。

## 支持的格式

### 1. Callouts (提示框)

Obsidian 的 callout 格式会被转换为美观的 HTML 样式框：

```markdown
> [!info] 信息提示
> 这是一个信息提示框

> [!warning] 警告
> 这是一个警告提示框

> [!question] 思考问题
> 请思考以下问题

> [!todo] 待办事项
> 需要完成的任务
```

**支持的类型：**

- `info` - 信息提示 (蓝色)
- `note` - 笔记 (绿色)
- `warning` - 警告 (橙色)
- `error` - 错误 (红色)
- `success` - 成功 (绿色)
- `question` - 问题 (紫色)
- `todo` - 待办 (绿色)
- `tip` - 提示 (蓝色)
- `abstract` - 摘要 (黄色)
- `quote` - 引用 (灰色)
- `example` - 示例 (紫色)

### 2. Frontmatter (文件元数据)

Obsidian 文件头部的 YAML 元数据会被解析并显示为信息卡片：

```yaml
---
Date created: 2025-04-21
Date edited: 2025-04-22
Source: AI入门教材
Description: 人工智能基础知识
tags:
  - AI/basic_book
  - tutorial
Important: true
Rating: 5
imageNameKey: AI_first
---
```

**支持的字段：**

- 创建日期、编辑日期
- 来源、描述
- 标签 (会显示为彩色标签)
- 重要性、评分
- 图片键名

### 3. Markmap (思维导图)

Obsidian 的 markmap 代码块会被转换为层级化的 HTML 结构：

````markdown
```markmap
---
markmap:
  height: 407
---
# 人工智能
## 基本认识
### 理解人工智能的定义
### 认识人工智能的现实意义
```
````

### 4. Timeline (时间线)

Obsidian 的 `[list2timeline]` 格式会被转换为时间线显示：

```markdown
[list2timeline]
- 1943 | 麦卡洛克和皮茨提出了神经元的数学模型
- 1956 | 约翰·麦卡锡等科学家举办达特矛斯会议
- 1957 | 罗森布拉特提出感知机
```

### 5. 内部链接

Obsidian 的内部链接格式会被转换为可点击的链接：

```markdown
[[第2章 人工智能创作：生成式人工智能]]
[[第3章 人工智能自主行动力：智能体|智能体章节]]
```

### 6. 外部链接

外部链接会添加图标和样式：

```markdown
[OpenAI官网](https://openai.com)
```

### 7. 表格

Markdown 表格会被转换为美观的 HTML 表格，支持：

- 表头样式
- 交替行背景色
- 响应式设计
- 边框和圆角

## 技术实现

### 处理流程

1. **Frontmatter 处理** - 解析文件头部元数据
2. **图片处理** - 处理相对路径图片，转换为 base64 编码
3. **Callout 处理** - 转换 Obsidian callout 为 HTML
4. **特殊格式处理** - 处理 markmap、timeline 等
5. **链接处理** - 处理内部和外部链接
6. **表格处理** - 美化表格显示

### CSS 样式

所有样式都通过 CSS 类实现，确保：

- 一致的视觉风格
- 响应式设计
- 良好的可读性
- 现代化的 UI 体验

## 使用方法

在 `book.py` 中，所有 Obsidian 格式会自动被处理。你只需要：

1. 将 Obsidian 创建的 `.md` 文件放入 `AI_intro_book` 文件夹
2. 启动 Streamlit 应用
3. 选择要阅读的章节
4. 所有 Obsidian 格式会自动转换为美观的 HTML 显示

## 自定义样式

如果需要修改样式，可以编辑 `get_callout_css()` 函数中的 CSS 代码。

## 注意事项

1. 确保图片文件存在于 `attachments/` 文件夹中
2. 内部链接指向的文件应该存在于同一文件夹中
3. 某些复杂的 Obsidian 插件功能可能无法完全支持
4. 建议使用标准的 Markdown 语法作为备选

## 示例效果

处理后的 Obsidian 文件会显示：

- 顶部的文档信息卡片
- 美观的 callout 提示框
- 结构化的思维导图
- 时间线显示
- 美化的表格
- 可点击的内部链接
- 带图标的外部链接

这样就能在保持 Obsidian 编辑体验的同时，在 Web 应用中提供优秀的阅读体验。
