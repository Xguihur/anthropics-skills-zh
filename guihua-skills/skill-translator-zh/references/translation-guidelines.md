# Skill翻译完整指南

本文档提供详细的翻译指南、常见术语对照表和最佳实践。

## 目录

- [通用翻译原则](#通用翻译原则)
- [常见技术术语对照表](#常见技术术语对照表)
- [特定内容类型翻译指南](#特定内容类型翻译指南)
- [翻译质量标准](#翻译质量标准)

## 通用翻译原则

### 准确性优先

- 确保技术准确性，不要为了流畅而牺牲准确性
- 如果不确定某个术语的标准译法，保持英文
- 保持代码和配置的完整性

### 可读性与自然度

- 译文应该读起来像原创的中文内容，而不是翻译痕迹明显
- 避免生硬的直译
- 使用符合中文习惯的表达方式

### 一致性

- 同一个术语在整个文档中保持相同的翻译
- 与其他已翻译skill保持术语一致性
- 命名风格保持一致

## 常见技术术语对照表

### 编程相关

| 英文 | 中文 | 使用建议 |
|------|------|----------|
| function | 函数 | 翻译 |
| method | 方法 | 翻译 |
| class | 类 | 翻译 |
| variable | 变量 | 翻译 |
| parameter | 参数 | 翻译 |
| argument | 参数/实参 | 翻译 |
| return value | 返回值 | 翻译 |
| import | 导入 | 翻译描述，保留代码 |
| export | 导出 | 翻译描述，保留代码 |
| module | 模块 | 翻译 |
| package | 包 | 翻译 |
| library | 库 | 翻译 |
| framework | 框架 | 翻译 |
| frontend | 前端 | 翻译 |
| backend | 后端 | 翻译 |
| database | 数据库 | 翻译 |
| query | 查询 | 翻译 |
| API | API | 保持英文 |
| endpoint | 端点 | 翻译 |
| request | 请求 | 翻译 |
| response | 响应 | 翻译 |
| callback | 回调 | 翻译 |
| async/asynchronous | 异步 | 翻译 |
| sync/synchronous | 同步 | 翻译 |

### 文档处理相关

| 英文 | 中文 | 使用建议 |
|------|------|----------|
| document | 文档 | 翻译 |
| template | 模板 | 翻译 |
| format | 格式 | 翻译 |
| style | 样式 | 翻译 |
| paragraph | 段落 | 翻译 |
| heading | 标题 | 翻译 |
| table | 表格 | 翻译 |
| cell | 单元格 | 翻译 |
| row | 行 | 翻译 |
| column | 列 | 翻译 |
| page | 页面 | 翻译 |
| layout | 布局 | 翻译 |
| PDF | PDF | 保持英文 |
| DOCX | DOCX | 保持英文 |
| PPTX | PPTX | 保持英文 |
| XLSX | XLSX | 保持英文 |
| Markdown | Markdown | 保持英文 |

### 文件和路径相关

| 英文 | 中文 | 使用建议 |
|------|------|----------|
| file | 文件 | 翻译 |
| folder/directory | 文件夹/目录 | 翻译 |
| path | 路径 | 翻译 |
| filename | 文件名 | 翻译 |
| extension | 扩展名 | 翻译 |
| root | 根目录 | 翻译 |
| parent | 父目录 | 翻译 |
| subdirectory | 子目录 | 翻译 |

### 工作流相关

| 英文 | 中文 | 使用建议 |
|------|------|----------|
| workflow | 工作流程 | 翻译 |
| step | 步骤 | 翻译 |
| process | 流程/处理 | 翻译 |
| procedure | 过程/步骤 | 翻译 |
| task | 任务 | 翻译 |
| operation | 操作 | 翻译 |
| create | 创建 | 翻译 |
| read | 读取 | 翻译 |
| update | 更新 | 翻译 |
| delete | 删除 | 翻译 |
| edit | 编辑 | 翻译 |
| modify | 修改 | 翻译 |
| generate | 生成 | 翻译 |
| build | 构建 | 翻译 |
| deploy | 部署 | 翻译 |
| validate | 验证 | 翻译 |
| test | 测试 | 翻译 |

### Skill特定术语

| 英文 | 中文 | 使用建议 |
|------|------|----------|
| skill | skill/技能 | 上下文决定 |
| SKILL.md | SKILL.md | 保持英文（文件名） |
| frontmatter | frontmatter/前置元数据 | 首次使用混合 |
| description | 描述 | 翻译 |
| bundled resources | 打包资源 | 翻译 |
| scripts | scripts/脚本 | 保持目录名，翻译描述 |
| references | references/参考文档 | 保持目录名，翻译描述 |
| assets | assets/资源文件 | 保持目录名，翻译描述 |

### 工具和框架名称

| 名称 | 处理方式 |
|------|----------|
| Python | 保持英文 |
| JavaScript | 保持英文 |
| TypeScript | 保持英文 |
| React | 保持英文 |
| Vue | 保持英文 |
| Node.js | 保持英文 |
| Django | 保持英文 |
| Flask | 保持英文 |
| Git | 保持英文 |
| GitHub | 保持英文 |
| Docker | 保持英文 |
| Kubernetes | 保持英文 |

## 特定内容类型翻译指南

### Frontmatter翻译

**原则：**
- 保持YAML格式不变
- 完整翻译description字段
- name字段根据需要决定是否添加-zh后缀

**示例：**

原文：
```yaml
---
name: pdf-editor
description: Comprehensive PDF manipulation including form filling, text extraction, and page operations. Use when working with PDF files for editing, analysis, or data extraction tasks.
---
```

译文：
```yaml
---
name: pdf-editor-zh
description: 全面的PDF处理功能，包括表单填写、文本提取和页面操作。当需要编辑、分析PDF文件或提取数据时使用此skill。
---
```

### 代码块翻译

**原则：**
- 代码本身保持不变
- 翻译代码前后的说明文字
- 可翻译代码注释

**示例：**

原文：
```markdown
Extract text from a PDF using pdfplumber:

```python
import pdfplumber

# Open the PDF file
with pdfplumber.open('document.pdf') as pdf:
    # Extract text from first page
    text = pdf.pages[0].extract_text()
    print(text)
```
```

译文：
```markdown
使用pdfplumber从PDF中提取文本：

```python
import pdfplumber

# 打开PDF文件
with pdfplumber.open('document.pdf') as pdf:
    # 从第一页提取文本
    text = pdf.pages[0].extract_text()
    print(text)
```
```

### 列表和步骤翻译

**原则：**
- 保持列表结构和缩进
- 翻译所有说明文字
- 保持代码和文件名不变

**示例：**

原文：
```markdown
## Workflow

1. Read the existing document
2. Identify the sections to modify
3. Make changes using the appropriate method
4. Save the updated document
```

译文：
```markdown
## 工作流程

1. 读取现有文档
2. 识别需要修改的部分
3. 使用适当的方法进行更改
4. 保存更新后的文档
```

### 表格翻译

**原则：**
- 保持表格结构
- 翻译表头和说明
- 技术术语根据对照表处理

**示例：**

原文：
```markdown
| Method | Description | Use Case |
|--------|-------------|----------|
| extract_text() | Extracts plain text | Simple text extraction |
| extract_tables() | Extracts table data | Data analysis |
```

译文：
```markdown
| 方法 | 描述 | 使用场景 |
|--------|-------------|----------|
| extract_text() | 提取纯文本 | 简单的文本提取 |
| extract_tables() | 提取表格数据 | 数据分析 |
```

### 命令行指令翻译

**原则：**
- 命令本身保持不变
- 翻译命令前后的说明
- 保持文件路径和参数

**示例：**

原文：
```markdown
Run the script with the following command:

```bash
python scripts/process.py --input data.pdf --output result.txt
```
```

译文：
```markdown
使用以下命令运行脚本：

```bash
python scripts/process.py --input data.pdf --output result.txt
```
```

### 链接和引用翻译

**原则：**
- 保持链接URL不变
- 翻译链接文字
- 更新内部文档引用（如果文件名改变）

**示例：**

原文：
```markdown
See [API Reference](references/api.md) for detailed documentation.
```

译文（如果保持原文件名）：
```markdown
详细文档请参见[API参考](references/api.md)。
```

译文（如果改变文件名）：
```markdown
详细文档请参见[API参考](references/api-zh.md)。
```

## 翻译质量标准

### 优秀翻译的特征

1. **准确性**
   - 技术信息准确无误
   - 代码和配置完整可用
   - 术语使用正确

2. **可读性**
   - 中文表达自然流畅
   - 逻辑清晰易懂
   - 符合中文阅读习惯

3. **一致性**
   - 术语翻译统一
   - 格式风格一致
   - 结构保持完整

4. **完整性**
   - 所有需要翻译的内容都已翻译
   - 没有遗漏的章节或段落
   - 链接和引用完整有效

### 常见错误避免

❌ **错误示例：**

1. 破坏代码：
```python
# 错误：翻译了函数名
def 提取文本(文件路径):
    pass
```

2. 破坏文件路径：
```markdown
# 错误：翻译了路径
请参见 `脚本/处理.py`
```

3. 过度翻译技术术语：
```markdown
# 错误：过度翻译
使用应用程序编程接口终点来获取数据
```

4. 不一致的术语：
```markdown
# 错误：同一概念使用不同翻译
第一段：使用API获取数据
第二段：通过应用程序接口获取信息
```

✅ **正确示例：**

1. 保持代码不变：
```python
# 正确：只翻译注释
def extract_text(file_path):
    """从文件中提取文本"""
    pass
```

2. 保持路径不变：
```markdown
# 正确
请参见 `scripts/process.py`
```

3. 适度翻译：
```markdown
# 正确
使用API端点获取数据
```

4. 保持一致性：
```markdown
# 正确
第一段：使用API获取数据
第二段：通过API获取信息
```

## 翻译检查清单

完成翻译后，使用此清单进行质量检查：

### 内容完整性
- [ ] 所有章节都已翻译
- [ ] 所有说明文字都已翻译
- [ ] 没有遗漏的段落

### 技术准确性
- [ ] 所有代码保持原样
- [ ] 所有文件路径正确
- [ ] 所有命令可执行
- [ ] 所有配置文件完整

### 格式正确性
- [ ] Markdown格式正确
- [ ] 代码块正确渲染
- [ ] 表格对齐正确
- [ ] 列表缩进正确

### 语言质量
- [ ] 中文表达自然流畅
- [ ] 术语使用一致
- [ ] 没有明显的翻译腔
- [ ] 专业术语准确

### 链接和引用
- [ ] 所有内部链接有效
- [ ] 所有外部链接正确
- [ ] 文件引用路径正确

### Frontmatter
- [ ] YAML格式正确
- [ ] description完整准确
- [ ] name字段符合规范

## 特殊场景处理

### 处理专有名词

对于公司名、产品名、品牌名等专有名词：
- 保持原文
- 首次出现时可添加中文说明
- 后续使用保持一致

示例：
```markdown
使用Anthropic的Claude模型...
```

### 处理缩写词

对于缩写词：
- 保持英文缩写
- 首次出现时可添加中文全称
- 后续使用缩写即可

示例：
```markdown
使用API (Application Programming Interface, 应用程序编程接口) 进行数据交互...
后续可以直接使用API...
```

### 处理版本号和日期

- 保持版本号格式不变
- 日期格式根据中文习惯调整（可选）

示例：
```markdown
版本 1.0.0
发布日期：2024年1月28日（或2024-01-28）
```

### 处理示例和占位符

- 翻译示例的说明文字
- 保持示例代码和数据
- 翻译占位符描述

示例：

原文：
```markdown
Example:
```python
process_file('<your-file-name>')
```
```

译文：
```markdown
示例：
```python
process_file('<你的文件名>')
```
```

## 总结

成功的skill翻译需要平衡三个关键要素：

1. **技术准确性** - 确保所有技术信息正确无误
2. **语言自然度** - 让中文读者感到流畅易懂
3. **保持一致性** - 在整个文档中统一风格和术语

遵循本指南，可以创建高质量的中文skill翻译版本。

