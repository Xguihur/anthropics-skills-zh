# Auto-Commit Skill 总结

## 创建目的

为与 AI 协作开发的工作流程提供自动化的代码提交解决方案。在逐步完成小功能、修复 bug 或进行代码调整后，能够快速、规范地提交代码到版本控制系统。

## 核心价值

### 1. 提升工作流程效率

在与 AI 协作时，开发者通常会：
- 将大任务拆分为小功能
- 逐步实现和测试
- 频繁提交代码以保存进度

手动编写 commit message 和执行 git 命令会打断思维流程。Auto-Commit 通过自动化这些操作，让开发者专注于功能实现。

### 2. 保证提交规范性

自动生成的 commit message 遵循业界标准：
- 结构化格式：`类型(作用域): 描述`
- 清晰的提交类型：feat/fix/refactor/docs/style/test/chore
- 详细的变更说明

即使在快节奏的开发中，也能保持高质量的提交历史。

### 3. 智能分析变更

脚本会：
- 自动识别文件操作类型（新增/修改/删除）
- 根据文件类型推断作用域
- 分析 diff 内容判断提交类型
- 生成包含关键信息的描述

## 技术实现

### 架构设计

```
auto-commit/
├── scripts/
│   ├── generate_commit.py      # 核心：分析变更并生成 message
│   └── commit_and_push.py      # 执行：完整的提交推送流程
└── references/
    └── commit-guidelines.md    # 规范：详细的最佳实践指南
```

### generate_commit.py - 智能分析引擎

**功能模块**：

1. **Git 状态获取**
   ```python
   def get_git_status() -> Dict[str, List[str]]
   ```
   - 检测已暂存、未暂存、未跟踪的文件
   - 识别文件操作类型（A=新增, M=修改, D=删除）

2. **Diff 内容分析**
   ```python
   def get_staged_diff() -> str
   ```
   - 获取已暂存变更的详细内容
   - 用于关键词分析

3. **智能推断**
   ```python
   def analyze_changes(status, diff) -> Dict
   ```
   - **作用域推断**：根据文件扩展名和路径
     - `.md`, `.txt` → docs
     - `test_*.py`, `*.test.js` → test
     - `.json`, `.yaml` → config
     - `.py`, `.java`, `.go` → backend
     - `.js`, `.ts`, `.css` → frontend
   
   - **类型推断**：根据 diff 内容关键词
     - "add", "new", "feature", "implement" → feat
     - "fix", "bug", "issue", "error" → fix
     - "refactor", "restructure" → refactor
     - "style", "format", "lint" → style

4. **Message 生成**
   ```python
   def generate_commit_message(analysis) -> str
   ```
   - 构建标准格式
   - 生成简短描述
   - 添加详细说明（文件列表、操作统计）

### commit_and_push.py - 执行引擎

**工作流程**：

1. **环境检查**
   - 验证 git 仓库
   - 检查是否有变更
   - 获取当前分支

2. **变更暂存**
   - 自动暂存所有变更（如果需要）
   - 或使用已有的暂存

3. **Message 处理**
   - 使用自定义 message（如果提供）
   - 或调用 generate_commit.py 自动生成

4. **提交执行**
   - 执行 `git commit -m "message"`
   - 显示提交结果

5. **推送远程**
   - 检查远程仓库配置
   - 执行 `git push origin <branch>`
   - 处理上游分支设置（首次推送）
   - 显示推送结果

**参数支持**：
- `-m, --message`: 自定义 commit message
- `--no-push`: 只提交不推送
- `--stage-all`: 强制暂存所有变更

### 错误处理机制

1. **优雅降级**
   - 如果 generate_commit.py 失败，使用默认 message
   - 如果没有远程仓库，跳过 push
   - 如果需要设置上游分支，自动处理

2. **清晰的错误提示**
   - 所有错误信息输出到 stderr
   - 包含具体的失败原因
   - 提供解决建议

## 使用场景示例

### 场景 1：功能开发完成

```
用户：这个登录功能做完了，帮我提交一下

AI 执行：
cd /path/to/project
python3 scripts/commit_and_push.py

输出：
正在分析变更并生成 commit message...

生成的 commit message:
feat(auth): 实现用户登录功能

- 新增 3 个文件
- 实现 JWT 认证逻辑
- 添加登录接口

主要文件：
- src/auth/jwt.py
- src/routes/auth.py
- tests/test_auth.py

正在提交变更...
✓ 提交成功

正在推送到远程仓库 (分支: feature/login)...
✓ 推送成功

✓ 所有操作完成！
```

### 场景 2：Bug 修复

```
用户：bug 修好了，commit 一下

AI 执行：
python3 scripts/commit_and_push.py

输出：
fix(ui): 修复按钮对齐问题

- 修改 1 个文件
- 调整 CSS 样式

✓ 提交成功
✓ 推送成功
```

### 场景 3：自定义 Message

```
用户：提交一下，message 写"优化数据库查询性能"

AI 执行：
python3 scripts/commit_and_push.py -m "perf(db): 优化数据库查询性能"

输出：
使用自定义 commit message:
perf(db): 优化数据库查询性能

✓ 提交成功
✓ 推送成功
```

### 场景 4：只提交不推送

```
用户：先提交到本地，不要 push

AI 执行：
python3 scripts/commit_and_push.py --no-push

输出：
chore: 更新配置文件

✓ 提交成功
提示：已跳过 push 操作（使用了 --no-push 选项）
```

## 设计亮点

### 1. 渐进式加载（Progressive Disclosure）

遵循 skill 设计原则，信息分层：

- **Level 1 - Metadata**（总是加载）
  - name: auto-commit
  - description: 详细说明使用场景和时机

- **Level 2 - SKILL.md**（skill 触发后加载）
  - 工作流程说明
  - 快速参考
  - 常见场景示例

- **Level 3 - References**（按需加载）
  - commit-guidelines.md: 完整的规范和最佳实践

### 2. 低自由度设计

代码提交是一个相对固定的流程，不适合高自由度的文本指导。使用脚本确保：
- 操作的一致性
- 格式的规范性
- 流程的可靠性

### 3. 智能推断 + 人工干预

- **默认自动**：大多数情况下自动分析就够用
- **支持覆盖**：关键场景可以手动指定
- **平衡效率与质量**：既快速又不失准确

### 4. 用户友好的输出

- 使用 emoji 和符号（✓, ✗）增强可读性
- 清晰的阶段提示（"正在..."）
- 详细的结果反馈

## 扩展可能

虽然当前版本已经满足基本需求，但未来可以考虑：

### 1. 交互式模式

```python
# 生成 message 后询问用户
print(f"生成的 commit message:\n{message}\n")
confirm = input("是否使用此 message？[Y/n]: ")
if confirm.lower() == 'n':
    custom_message = input("请输入自定义 message: ")
```

### 2. 模板系统

支持为不同类型的提交定义模板：

```python
templates = {
    'feat': '{scope}: 实现{feature}\n\n- 新增功能点1\n- 新增功能点2',
    'fix': '{scope}: 修复{issue}\n\n原因：...\n解决方案：...',
    'refactor': '{scope}: 重构{component}\n\n目标：...\n效果：...'
}
```

### 3. AI 增强

调用 LLM API 生成更智能的 commit message：

```python
def generate_ai_message(diff: str) -> str:
    prompt = f"分析以下代码变更，生成简洁的 commit message:\n{diff}"
    return call_llm_api(prompt)
```

### 4. 版本管理集成

根据提交类型自动更新版本号（语义化版本）：

```python
# feat → minor version +1
# fix → patch version +1
# feat + BREAKING CHANGE → major version +1
```

### 5. 变更日志生成

自动维护 CHANGELOG.md：

```python
def update_changelog(commit_type, message):
    changelog = read_changelog()
    changelog.add_entry(commit_type, message)
    changelog.save()
```

### 6. Git Hooks 集成

作为 commit-msg hook，在提交时自动验证或生成 message：

```bash
#!/bin/bash
# .git/hooks/commit-msg

python3 scripts/generate_commit.py > "$1"
```

## 与其他 Skills 的协同

### git-remote-manager

- **auto-commit**: 处理日常提交
- **git-remote-manager**: 管理远程仓库切换

协同场景：
```
1. 使用 git-remote-manager 切换到 GitHub
2. 使用 auto-commit 提交代码
3. 使用 git-remote-manager 切换到 Gitee
4. 使用 auto-commit 再次推送
```

### skill-creator

本 skill 就是使用 skill-creator 创建的，展示了完整的创建流程：
1. 理解需求
2. 规划内容（脚本 + 参考文档）
3. 初始化结构
4. 实现脚本和文档
5. 验证和打包

## 最佳实践建议

### 1. 提交频率

- ✅ 每完成一个独立的小功能就提交
- ✅ 修复一个 bug 后立即提交
- ✅ 重构一个模块后提交
- ❌ 不要积累太多变更一次提交
- ❌ 不要混合多个不相关的改动

### 2. Message 质量

- ✅ 使用自动生成作为起点
- ✅ 对重要提交手动优化 message
- ✅ 确保描述准确反映变更内容
- ❌ 不要使用过于简单的描述（如"更新"）
- ❌ 不要包含敏感信息

### 3. 工作流集成

```
开发阶段 → 测试验证 → 确认无误 → auto-commit → 继续下一个功能
         ↑                                              ↓
         └──────────────── 需要修改则回退 ───────────────┘
```

### 4. 团队协作

- 与团队统一 commit 规范
- 定期 pull 保持同步
- 重要提交前与团队沟通
- 遵守分支管理策略

## 技术细节

### Python 版本要求

- Python 3.6+（使用了 f-string 和类型提示）
- 标准库依赖：subprocess, sys, os, re, typing, argparse
- 无需安装额外的第三方包

### Git 版本要求

- Git 2.0+
- 需要配置 user.name 和 user.email
- 需要配置 SSH 密钥或 HTTPS 认证（用于 push）

### 兼容性

- ✅ macOS
- ✅ Linux
- ✅ Windows（需要 Git Bash 或 WSL）

### 性能

- 分析速度：< 1 秒（大多数项目）
- 提交速度：取决于文件数量和大小
- 推送速度：取决于网络和远程仓库

## 总结

Auto-Commit Skill 通过自动化和智能化的方式，优化了与 AI 协作开发的代码提交流程：

✅ **节省时间**：从手动编写 message 到一键完成
✅ **保证质量**：符合规范的提交历史
✅ **专注开发**：减少流程打断，保持专注
✅ **易于使用**：自然语言触发，无需记忆命令
✅ **灵活配置**：支持自定义和多种模式

它体现了 skill 设计的核心理念：**将重复的、程式化的操作封装为可靠的工具，让 AI 和人类都能更高效地协作**。

## 文件清单

### Skill 包内容

```
auto-commit.skill (zip 文件)
├── SKILL.md                          # 主文档（357 行）
├── LICENSE.txt                        # MIT 许可证
├── scripts/
│   ├── generate_commit.py            # 生成脚本（295 行）
│   └── commit_and_push.py            # 执行脚本（195 行）
└── references/
    └── commit-guidelines.md          # 规范文档（228 行）
```

### 辅助文档

```
skills-for-cursor-file/auto-commit/
├── auto-commit.skill                 # 打包后的 skill 文件
├── auto-commit-README.md             # 使用说明
└── auto-commit-总结.md               # 本文档
```

## 制作信息

- **创建时间**：2026-01-28
- **制作工具**：skill-creator
- **Python 版本**：3.6+
- **Git 版本**：2.0+
- **许可证**：MIT License
- **语言**：中文

---

*本 skill 专为与 AI 协作的开发者设计，让代码提交变得简单、快速、规范。*

