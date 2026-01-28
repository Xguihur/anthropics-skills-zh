---
name: auto-commit
description: 自动化 Git 提交和推送工具。智能分析代码变更，生成符合规范的 commit message，并执行提交和推送操作。当用户需要提交代码、推送改动、创建 git commit 时使用。适用于完成功能开发、修复 bug、代码重构、中途备份等场景。
---

# 自动提交工具（Auto Commit）

自动化 Git 提交流程，智能生成 commit message 并推送到远程仓库。

## 快速开始

当用户表达需要提交代码时（例如"帮我提交一下代码"、"把这次的改动 commit 一下"、"推送到仓库"等），执行：

```bash
cd <项目目录>
python3 scripts/commit_and_push.py
```

脚本会自动：
- 检查 git 状态并暂存变更
- 分析变更内容生成 commit message
- 执行 commit 和 push

## 工作流程

### 标准提交流程

1. **确认用户意图**：判断是否需要提交代码
2. **执行脚本**：运行 `python3 scripts/commit_and_push.py`
3. **确认结果**：检查提交和推送是否成功

### 自定义 Commit Message

如果用户指定了 message：

```bash
python3 scripts/commit_and_push.py -m "feat(api): 添加用户认证接口"
```

### 仅提交不推送

如果用户只想提交到本地：

```bash
python3 scripts/commit_and_push.py --no-push
```

### 只生成 Message

如果只需要查看生成的 message：

```bash
python3 scripts/generate_commit.py
```

## Commit Message 规范

生成的 message 遵循格式：`<类型>(<作用域>): <简短描述>`

### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 代码重构
- `docs`: 文档更新
- `style`: 代码格式调整
- `test`: 测试相关
- `chore`: 日常维护

### 作用域

根据文件类型自动推断：`docs`, `test`, `config`, `scripts`, `frontend`, `backend`

### 示例

```
feat(api): 添加用户认证接口

- 新增 2 个文件
- 实现 JWT token 生成和验证
- 添加登录和注销端点
```

```
fix(ui): 修复登录页面样式问题

- 修改 1 个文件
- 调整按钮对齐方式
```

更多示例和详细规范见 [commit-guidelines.md](references/commit-guidelines.md)。

## 使用场景

### 场景 1：完成功能后提交
**用户说**："这个功能做完了，帮我提交一下"  
**操作**：`python3 scripts/commit_and_push.py`

### 场景 2：修复 Bug
**用户说**："bug 修好了，commit 一下"  
**操作**：`python3 scripts/commit_and_push.py`

### 场景 3：指定 Message
**用户说**："帮我提交，message 写'修复登录页面的样式问题'"  
**操作**：`python3 scripts/commit_and_push.py -m "fix(ui): 修复登录页面的样式问题"`

### 场景 4：只提交不推送
**用户说**："先提交到本地，不要 push"  
**操作**：`python3 scripts/commit_and_push.py --no-push`

## 脚本说明

### generate_commit.py

分析代码变更并生成 commit message。

**功能**：
- 检查 git 状态，获取已暂存的文件列表
- 获取变更内容（git diff）
- 分析变更类型（新增、修改、删除）
- 根据文件类型推断作用域
- 根据变更内容和关键词判断提交类型
- 生成结构化的 commit message

**使用**：
```bash
python3 scripts/generate_commit.py
```

### commit_and_push.py

执行完整的提交和推送流程。

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
```

**工作流程**：
1. 检查是否在 git 仓库中
2. 检查是否有已暂存的变更，没有则自动暂存
3. 生成或使用提供的 commit message
4. 执行 git commit
5. 如果未禁用，执行 git push

## 错误处理

### 不在 Git 仓库中
脚本会报错，需要先进入正确的项目目录。

### 没有变更
脚本会提示"没有要提交的变更"，这是正常的。

### 推送失败
常见原因：网络问题、远程仓库未配置、需要先拉取更新。

如果推送失败，可能需要：
- 检查网络连接
- 执行 `git pull` 合并远程更新
- 检查远程仓库配置

### 冲突处理
如果远程仓库有新的提交：

```bash
git pull --rebase
# 解决冲突（如果有）
python3 scripts/commit_and_push.py
```

## 最佳实践

1. **小步提交**：每完成一个小功能就提交，保持提交粒度适中
2. **清晰描述**：如果自动生成的不够准确，可以手动指定
3. **及时推送**：建议每次提交后都推送到远程
4. **查看变更**：提交前可以先让 AI 总结一下改动内容
5. **处理冲突**：遇到推送冲突时，先拉取远程更新并解决冲突

## 相关资源

- **详细规范**：[commit-guidelines.md](references/commit-guidelines.md) - Commit message 完整规范和示例
- **脚本源码**：
  - `scripts/generate_commit.py` - Message 生成脚本
  - `scripts/commit_and_push.py` - 提交和推送脚本
