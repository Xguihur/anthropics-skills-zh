---
name: auto-commit
description: 自动化 Git 提交和推送工具。当用户在与 AI 协作完成功能开发、bug 修复或代码调整后，需要将改动提交到版本控制系统时使用。适用场景包括：(1) 完成一个小功能或子任务后的暂存提交；(2) 完成完整功能需求的定档提交；(3) 修复 bug 后的提交；(4) 代码重构或优化后的提交；(5) 任何需要创建 git commit 并推送到远程仓库的场景。该 skill 会智能分析代码变更内容，自动生成符合规范的 commit message，并执行提交和推送操作。
license: MIT
---

# 自动提交工具（Auto Commit）

自动化 Git 提交流程，智能生成 commit message 并推送到远程仓库。

## ⚠️ 重要使用规范

**仅在用户明确要求时才执行提交操作，绝不擅自提交代码。**

### 何时使用此 skill

**✅ 应该使用（用户有明确的提交意图）：**
- 用户说："提交代码"、"推送代码"、"commit 并 push"
- 用户说："帮我提交一下"、"把改动 commit 一下"
- 用户说："推送到仓库"、"提交到 git"
- 用户在完成功能后明确表示要提交

**❌ 不应该使用（没有明确的提交指令）：**
- 用户只是让你修改文件、添加功能、修复 bug
- 用户说"优化一下"、"改进一下"、"帮我改改"
- 你完成修改后，除非用户明确要求，否则不要自动提交
- 测试完功能后，不要主动提交

### 正确的工作流程

1. **用户请求修改功能** → 你修改文件 → 告诉用户修改完成 → **停止，等待指令**
2. **用户明确说"提交"** → 你才调用此 skill 执行提交

**原则：代码控制权在用户手中，AI 不应擅自做主。**

## 概述

在与 AI 协作开发过程中，开发者通常会将大任务拆分为小功能，逐步完成。每完成一个小功能或阶段性任务后，就需要将代码提交到版本控制系统。手动编写 commit message 和执行 git 命令虽然不复杂，但在频繁提交时会打断工作流程。

本 skill 提供自动化的代码提交方案：

- **智能分析变更**：自动检测代码变更类型、影响范围和文件操作
- **生成规范 message**：基于变更内容生成符合规范的 commit message
- **一键提交推送**：自动执行 git add、commit 和 push 操作
- **灵活配置**：支持自定义 message、仅提交不推送等选项

## 工作流程

### 标准流程

当用户表达需要提交代码时（例如"帮我提交一下代码"、"把这次的改动 commit 一下"、"推送到仓库"等），按以下步骤操作：

1. **确认用户意图**
   
   判断是否是以下场景之一：
   - 完成了一个功能点，准备暂存
   - 完成了完整需求，准备定档
   - 修复了 bug，需要提交
   - 进行了代码重构或优化
   - 需要备份当前进度

2. **执行自动提交**

   使用 `commit_and_push.py` 脚本：

   ```bash
   cd <项目目录>
   python3 scripts/commit_and_push.py
   ```

   脚本会自动：
   - 检查 git 状态
   - 暂存所有变更（如果需要）
   - 分析变更内容
   - 生成 commit message
   - 执行 commit
   - 推送到远程仓库

3. **确认结果**

   脚本执行后会显示：
   - 生成的 commit message
   - 提交结果
   - 推送结果

   确认操作成功后，告知用户提交完成。

### 自定义 Commit Message

如果用户明确指定了 commit message 或对自动生成的不满意，使用 `-m` 参数：

```bash
python3 scripts/commit_and_push.py -m "feat(api): 添加用户认证接口"
```

### 仅提交不推送

如果用户只想提交到本地仓库，不推送到远程：

```bash
python3 scripts/commit_and_push.py --no-push
```

### 手动生成 Commit Message

如果只需要生成 commit message 但不执行提交（例如用户想先查看），可以单独运行：

```bash
python3 scripts/generate_commit.py
```

这会输出生成的 commit message，用户可以查看并决定是否使用。

## Commit Message 规范

本 skill 生成的 commit message 遵循 **Gitmoji + Conventional Commits** 规范：

### 基本格式

```
<emoji> <类型>(<作用域>): <简短描述>

<详细说明>
```

### 类型（Type）与 Emoji

- `✨ feat`: 新功能
- `🐛 fix`: Bug 修复
- `♻️ refactor`: 代码重构
- `📝 docs`: 文档更新
- `🎨 style`: 代码格式调整
- `✅ test`: 测试相关
- `🔧 chore`: 日常维护、配置更改
- `⚡️ perf`: 性能优化
- `🚀 deploy`: 部署/发布
- `💄 ui`: UI/样式文件

### 作用域（Scope）

根据变更的文件自动推断：

- `docs`: Markdown、文本文件
- `test`: 测试文件
- `config`: 配置文件（JSON、YAML 等）
- `scripts`: 脚本文件
- `frontend`: 前端文件（JS、TS、CSS、HTML 等）
- `backend`: 后端文件（Python、Java、Go 等）

### 示例

**示例 1：新增功能**
```
✨ feat(api): 添加用户认证接口

- 新增 2 个文件
- 实现 JWT token 生成和验证
- 添加登录和注销端点
```

**示例 2：修复 Bug**
```
🐛 fix(reports): 修复日期显示错误

- 修改 1 个文件
- 修正时区转换逻辑
```

**示例 3：文档更新**
```
📝 docs: 更新 API 使用文档

- 修改 1 个文件
- 添加新接口的说明和示例
```

**示例 4：代码重构**
```
♻️ refactor(database): 优化查询性能

- 修改 3 个文件
- 重构数据库查询逻辑
- 添加索引提升性能
```

更多示例和详细规范见 [commit-guidelines.md](references/commit-guidelines.md)。

## 使用场景

### 场景 1：完成小功能后暂存

**用户说**："这个功能做完了，帮我提交一下"

**操作**：
```bash
cd <项目目录>
python3 scripts/commit_and_push.py
```

### 场景 2：功能完成后定档

**用户说**："整个用户管理模块做完了，推送到仓库吧"

**操作**：
```bash
cd <项目目录>
python3 scripts/commit_and_push.py
```

### 场景 3：修复 Bug

**用户说**："bug 修好了，commit 一下"

**操作**：
```bash
cd <项目目录>
python3 scripts/commit_and_push.py
```

### 场景 4：代码重构或优化

**用户说**："代码优化完了，提交一下"

**操作**：
```bash
cd <项目目录>
python3 scripts/commit_and_push.py
```

### 场景 5：中途备份进度

**用户说**："先保存一下进度，待会继续"

**操作**：
```bash
cd <项目目录>
python3 scripts/commit_and_push.py
```

### 场景 6：用户指定 Commit Message

**用户说**："帮我提交，commit message 写'修复登录页面的样式问题'"

**操作**：
```bash
cd <项目目录>
python3 scripts/commit_and_push.py -m "fix(ui): 修复登录页面的样式问题"
```

注意：如果用户提供了 message 但没有包含类型前缀，可以根据内容自动补充。

## 错误处理

### 不在 Git 仓库中

如果当前目录不是 git 仓库，脚本会报错。需要先进入正确的项目目录。

### 没有变更

如果没有任何代码变更，脚本会提示"没有要提交的变更"。这是正常的，告知用户即可。

### 推送失败

常见原因：
- 网络问题
- 远程仓库未配置
- 没有推送权限
- 需要先拉取远程更新

如果推送失败，脚本会显示错误信息。根据错误提示，可能需要：
- 检查网络连接
- 执行 `git pull` 合并远程更新
- 检查远程仓库配置

### 冲突处理

如果远程仓库有新的提交，可能需要先拉取更新：

```bash
git pull --rebase
# 解决冲突（如果有）
python3 scripts/commit_and_push.py
```

## 脚本说明

### generate_commit.py

**功能**：分析代码变更并生成 commit message

**工作原理**：
1. 检查 git 状态，获取已暂存的文件列表
2. 获取变更内容（git diff）
3. 分析变更类型（新增、修改、删除）
4. 根据文件类型推断作用域
5. 根据变更内容和关键词判断提交类型
6. 生成结构化的 commit message

**使用**：
```bash
python3 scripts/generate_commit.py
```

### commit_and_push.py

**功能**：执行完整的提交和推送流程

**参数**：
- `-m, --message <msg>`: 自定义 commit message
- `--no-push`: 只提交不推送
- `--stage-all`: 自动暂存所有变更

**使用**：
```bash
# 自动生成 message 并提交推送
python3 scripts/commit_and_push.py

# 使用自定义 message
python3 scripts/commit_and_push.py -m "feat: 添加新功能"

# 只提交不推送
python3 scripts/commit_and_push.py --no-push

# 暂存所有变更并提交
python3 scripts/commit_and_push.py --stage-all
```

**工作流程**：
1. 检查是否在 git 仓库中
2. 检查是否有已暂存的变更，没有则自动暂存
3. 生成或使用提供的 commit message
4. 执行 git commit
5. 如果未禁用，执行 git push

## 最佳实践

1. **小步提交**：每完成一个小功能就提交，保持提交粒度适中

2. **清晰描述**：虽然会自动生成 message，但如果自动生成的不够准确，可以手动指定

3. **及时推送**：除非有特殊原因，建议每次提交后都推送到远程，避免积累过多本地提交

4. **查看变更**：在提交前，可以先让 AI 总结一下本次做了哪些改动，确认无误后再提交

5. **处理冲突**：如果遇到推送冲突，先拉取远程更新并解决冲突，再重新提交

6. **统一规范**：团队协作时，确保 commit message 格式统一，可以根据团队规范调整脚本

## 扩展功能

如果需要更高级的功能，可以考虑扩展脚本：

- **交互式确认**：在提交前显示 message 并询问用户是否确认
- **自动版本号**：根据提交类型自动更新版本号（语义化版本）
- **变更日志**：自动生成 CHANGELOG.md
- **提交模板**：支持自定义不同场景的 message 模板
- **多语言支持**：支持中英文切换
- **Git hooks 集成**：作为 pre-commit 或 commit-msg hook 使用

## 相关资源

- **详细规范**：[commit-guidelines.md](references/commit-guidelines.md) - Commit message 完整规范和示例
- **脚本源码**：
  - `scripts/generate_commit.py` - Message 生成脚本
  - `scripts/commit_and_push.py` - 提交和推送脚本
