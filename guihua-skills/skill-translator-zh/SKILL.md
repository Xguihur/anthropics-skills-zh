---
name: skill-translator-zh
description: 将英文编写的skill翻译成中文版本。当用户需要将现有的英文skill（包括SKILL.md和相关文档）翻译成中文，同时保持核心内容、代码、路径、技术细节不变时使用此skill。适用于创建skill的中文本地化版本。
---

# Skill Translator (中文翻译)

## 概述

此skill用于将英文编写的skill翻译成中文版本，确保中文版本保持原有skill的结构、功能和技术准确性。

## 翻译工作流程

### 1. 理解原始Skill

首先阅读并理解待翻译的skill：

- 阅读SKILL.md的frontmatter和body
- 了解skill的目的、工作流程和核心功能
- 查看所有bundled resources（scripts/、references/、assets/）
- 识别哪些内容需要翻译，哪些需要保持原样

### 2. 创建翻译后的Skill目录

使用skill-creator的init_skill.py创建新的skill目录：

```bash
python3 skills/skill-creator/scripts/init_skill.py <原skill名>-zh --path skills
```

例如，翻译`pdf`skill时：

```bash
python3 skills/skill-creator/scripts/init_skill.py pdf-zh --path skills
```

### 3. 翻译SKILL.md

按照以下原则翻译SKILL.md：

**Frontmatter翻译：**
- `name`: 保持原样或添加`-zh`后缀
- `description`: 完整翻译成中文，确保保留所有触发条件和使用场景

**Body翻译：**
- 标题和说明文字翻译成中文
- 保持markdown结构和格式不变
- 技术术语根据上下文决定是否翻译（参见下方"翻译原则"）

### 4. 处理Bundled Resources

根据文件类型采取不同策略：

**scripts/ 目录：**
- 代码文件（.py, .sh, .js等）：保持代码不变
- 可翻译代码注释和docstring为中文
- 文件名通常保持英文

**references/ 目录：**
- Markdown文档：翻译所有说明性文字
- 保持代码示例、配置文件、JSON/YAML示例不变
- 保持文件名或添加`-zh`后缀

**assets/ 目录：**
- 通常不需要翻译
- 如包含文本模板，根据需要翻译

### 5. 验证和打包

翻译完成后：

1. 检查所有链接和引用是否正确
2. 确保代码示例可运行
3. 验证markdown格式
4. 使用package_skill.py打包：

```bash
python3 skills/skill-creator/scripts/package_skill.py skills/<skill名>-zh
```

## 翻译原则

### 需要翻译的内容

✅ **必须翻译：**
- 标题、章节名称
- 说明性文字、描述、解释
- 工作流程步骤
- 用户指南和教程
- 注释和文档字符串

### 保持原样的内容

❌ **不要翻译：**
- 代码（Python, JavaScript, Bash等）
- 文件路径和文件名
- 命令行指令
- 变量名、函数名、类名
- API端点和URL
- 正则表达式
- 配置文件内容（JSON, YAML, XML等）
- 包名和导入语句

### 技术术语处理

⚖️ **根据情况处理：**

**保持英文的术语：**
- 广泛使用的技术术语：API, JSON, XML, PDF, DOCX, HTML, CSS, Git
- 编程概念：frontend, backend, middleware, webhook
- 工具和框架名：React, Vue, Django, Flask
- 文件格式：.md, .py, .json, .yaml

**可以翻译的术语：**
- 一般概念：文档(document)、表格(table)、文件(file)
- 操作动词：创建(create)、编辑(edit)、删除(delete)
- 通用术语：用户(user)、数据(data)、配置(configuration)

**混合使用（推荐）：**
- 首次提及时使用"中文(English)"格式
- 后续使用中文或英文，保持一致性
- 示例："前端(frontend)"、"应用程序接口(API)"

### 格式和结构保持

- 保持原有的markdown结构
- 保持代码块的缩进和格式
- 保持列表、表格的对齐
- 保持链接引用的正确性
- 保持frontmatter的YAML格式

### 语言风格

- 使用简洁、专业的中文
- 避免过度直译，注重可读性
- 保持技术准确性
- 使用祈使句（命令式）描述步骤
- 保持与原文相同的语气（正式/非正式）

## 翻译示例

### 示例1：标题和描述

**原文：**
```markdown
## Quick Start

To extract text from a PDF, use pdfplumber:
```

**译文：**
```markdown
## 快速开始

要从PDF中提取文本，使用pdfplumber：
```

### 示例2：代码和注释

**原文：**
```python
# Extract text from PDF
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    text = pdf.pages[0].extract_text()
```

**译文：**
```python
# 从PDF中提取文本
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    text = pdf.pages[0].extract_text()
```

### 示例3：技术术语混合

**原文：**
```markdown
Use the API endpoint to fetch user data from the database.
```

**译文：**
```markdown
使用API端点从数据库中获取用户数据。
```

或

```markdown
使用API端点(API endpoint)从数据库中获取用户数据。
```

## 质量检查清单

翻译完成后，检查以下项目：

- [ ] frontmatter的description完整且准确
- [ ] 所有章节标题已翻译
- [ ] 说明性文字已翻译成自然的中文
- [ ] 代码保持原样，可正常运行
- [ ] 文件路径和命令未被破坏
- [ ] 链接和引用仍然有效
- [ ] markdown格式正确渲染
- [ ] 技术术语使用一致
- [ ] 保持了原文的结构和逻辑流程
- [ ] 中文表达自然、专业

## 参考资源

详细的翻译指南和示例请参见：

- `references/translation-guidelines.md` - 完整的翻译指南和常见术语对照表
