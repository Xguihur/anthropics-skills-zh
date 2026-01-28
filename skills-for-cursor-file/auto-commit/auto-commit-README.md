# Auto-Commit Skill 使用说明

## 概述

Auto-Commit 是一个自动化 Git 提交和推送的 skill，专为与 AI 协作开发的工作流程设计。

## 主要功能

1. **智能分析代码变更**
   - 自动检测文件的增删改操作
   - 识别变更的文件类型和影响范围
   - 分析代码 diff 内容

2. **自动生成 Commit Message**
   - 符合业界规范的格式（类型 + 作用域 + 描述）
   - 根据变更内容智能判断提交类型（feat/fix/refactor/docs 等）
   - 自动推断作用域（frontend/backend/docs/test 等）
   - 生成详细的变更说明

3. **一键提交推送**
   - 自动暂存变更
   - 执行 git commit
   - 推送到远程仓库
   - 处理上游分支设置

## 使用场景

- ✅ 完成小功能后的暂存提交
- ✅ 完成完整需求的定档提交
- ✅ Bug 修复后的提交
- ✅ 代码重构或优化后的提交
- ✅ 中途备份进度
- ✅ 任何需要提交代码的时刻

## 快速开始

### 基本用法

当你完成一个功能或需要提交代码时，只需告诉 AI：

```
"帮我提交一下代码"
"把这次的改动 commit 一下"
"推送到仓库"
"commit 并 push"
```

AI 会自动：
1. 进入你的项目目录
2. 运行 `python3 scripts/commit_and_push.py`
3. 显示生成的 commit message
4. 确认提交和推送结果

### 自定义 Commit Message

如果你想指定 commit message：

```
"帮我提交，message 写'修复登录页面的样式问题'"
```

### 只提交不推送

如果只想提交到本地：

```
"只提交到本地，不要 push"
```

## Commit Message 格式

生成的 commit message 遵循以下规范：

```
<类型>(<作用域>): <简短描述>

<详细说明>
```

### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 代码重构
- `docs`: 文档更新
- `style`: 代码格式调整
- `test`: 测试相关
- `chore`: 日常维护

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

```
docs: 更新 API 使用文档

- 修改 1 个文件
- 添加新接口的说明
```

## 脚本说明

### generate_commit.py

生成 commit message 的脚本。

**功能**：
- 分析 git 状态和变更内容
- 识别文件操作类型
- 推断提交类型和作用域
- 生成结构化的 message

**直接使用**（只生成 message，不提交）：
```bash
python3 scripts/generate_commit.py
```

### commit_and_push.py

执行完整提交流程的脚本。

**参数**：
- `-m, --message <msg>`: 自定义 commit message
- `--no-push`: 只提交不推送
- `--stage-all`: 自动暂存所有变更

**示例**：
```bash
# 自动生成 message 并提交推送
python3 scripts/commit_and_push.py

# 使用自定义 message
python3 scripts/commit_and_push.py -m "feat: 添加新功能"

# 只提交不推送
python3 scripts/commit_and_push.py --no-push
```

## 常见问题

### Q: 如何修改生成的 commit message？

A: 有两种方式：
1. 告诉 AI 你想要的 message，它会使用 `-m` 参数
2. 手动运行时指定：`python3 scripts/commit_and_push.py -m "你的消息"`

### Q: 如果推送失败怎么办？

A: 常见原因和解决方法：
- 网络问题：检查网络连接
- 需要先拉取：执行 `git pull` 合并远程更新
- 未配置远程仓库：执行 `git remote add origin <url>`
- 权限问题：检查 SSH 密钥或访问令牌

### Q: 可以只生成 message 但不提交吗？

A: 可以，运行 `python3 scripts/generate_commit.py` 只会输出生成的 message。

### Q: 支持哪些提交类型？

A: 支持标准的 7 种类型：feat, fix, refactor, docs, style, test, chore。
脚本会根据变更内容自动判断，也可以手动指定。

### Q: 如何自定义规范？

A: 可以修改 `scripts/generate_commit.py` 中的逻辑：
- `analyze_changes()`: 修改类型判断逻辑
- `generate_commit_message()`: 修改 message 生成格式

## 文件结构

```
auto-commit/
├── SKILL.md                          # 主文档
├── LICENSE.txt                        # MIT 许可证
├── scripts/
│   ├── generate_commit.py            # Message 生成脚本
│   └── commit_and_push.py            # 提交推送脚本
└── references/
    └── commit-guidelines.md          # 详细规范和示例
```

## 最佳实践

1. **小步提交**：每完成一个小功能就提交，保持提交粒度适中
2. **清晰描述**：如果自动生成的 message 不够准确，手动指定更好的
3. **及时推送**：避免积累过多本地提交
4. **查看变更**：提交前先确认改动内容
5. **处理冲突**：遇到冲突时先拉取并解决，再重新提交

## 与 AI 协作的典型流程

```
1. 你：实现用户登录功能
   AI：[实现功能...]
   
2. 你：测试一下
   AI：[测试功能...]
   
3. 你：没问题，提交一下
   AI：[运行 auto-commit]
   生成的 commit message:
   feat(auth): 实现用户登录功能
   - 新增 3 个文件
   - 实现 JWT 认证
   - 添加登录接口和中间件
   
   ✓ 提交成功
   ✓ 推送成功
```

## 依赖要求

- Python 3.6+
- Git 2.0+
- 已配置 git 用户信息（`git config user.name` 和 `user.email`）

## 许可证

MIT License - 详见 LICENSE.txt

## 参考资源

- 详细规范：`references/commit-guidelines.md`
- 脚本源码：`scripts/` 目录

