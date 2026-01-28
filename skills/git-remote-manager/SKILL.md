---
name: git-remote-manager
description: Git 远程仓库管理工具。用于需要更换、添加或管理 Git 远程仓库的场景，包括：更新远程仓库地址、清空历史重新开始、强制推送覆盖远程仓库、添加多个远程仓库、镜像仓库等操作。当用户需要切换 GitHub/GitLab 仓库、迁移代码、或管理多个远程源时使用此技能。
---

# Git 远程仓库管理器

## 概述

此技能提供 Git 远程仓库管理的完整工作流程，帮助用户安全、高效地完成远程仓库的切换、添加和管理操作。

## 使用前检查

在执行任何操作前，先检查当前仓库状态：

```bash
# 查看当前远程仓库
git remote -v

# 查看当前分支
git branch

# 查看工作区状态
git status
```

## 场景选择

根据用户需求选择合适的操作场景：

### 场景 1：更换远程仓库（保留历史）

**适用情况：**
- 需要将代码推送到新的远程仓库
- 希望保留完整的 Git 提交历史
- 原仓库和新仓库都可访问

**操作步骤：**

1. 更新远程仓库地址：
```bash
git remote set-url origin <新仓库URL>
```

2. 验证更新：
```bash
git remote -v
```

3. 推送到新仓库：
```bash
# 首次推送，建立上游关联
git push -u origin main

# 或推送所有分支
git push -u origin --all

# 同时推送标签
git push origin --tags
```

**注意事项：**
- 如果新仓库非空且历史不同，可能需要先 `git pull origin main --allow-unrelated-histories` 或使用强制推送
- 确保有新仓库的写入权限

### 场景 2：清空历史，全新开始

**适用情况：**
- 想要一个干净的提交历史
- 不需要保留之前的提交记录
- 代码是敏感的，需要重新开始

**操作步骤：**

**方法 A：删除 .git 重新初始化**

```bash
# 1. 删除现有 Git 历史
rm -rf .git

# 2. 重新初始化仓库
git init

# 3. 添加所有文件
git add .

# 4. 创建初始提交
git commit -m "Initial commit"

# 5. 设置主分支名称（如果需要）
git branch -M main

# 6. 添加新的远程仓库
git remote add origin <新仓库URL>

# 7. 推送到远程仓库
git push -u origin main
```

**方法 B：使用 orphan 分支**

```bash
# 1. 创建一个新的孤立分支
git checkout --orphan new-main

# 2. 添加所有文件
git add .

# 3. 创建初始提交
git commit -m "Initial commit"

# 4. 删除旧的主分支
git branch -D main

# 5. 重命名新分支为 main
git branch -m main

# 6. 更新远程仓库地址（如果需要）
git remote set-url origin <新仓库URL>

# 7. 强制推送
git push -f origin main
```

**警告：** 此操作会永久删除所有历史记录，无法恢复！

### 场景 3：强制推送覆盖远程仓库

**适用情况：**
- 远程仓库已有内容，但要用本地内容完全覆盖
- 确定本地版本是正确的
- 已做好备份或确认可以丢弃远程内容

**操作步骤：**

```bash
# 1. 确认本地代码正确
git status
git log --oneline -5

# 2. 强制推送到远程
git push -f origin main

# 或者使用更安全的 --force-with-lease
git push --force-with-lease origin main
```

**安全建议：**
- 优先使用 `--force-with-lease` 而不是 `-f`，它会检查远程是否有其他人的新提交
- 在团队协作中谨慎使用强制推送
- 推送前与团队沟通
- 考虑先拉取远程更改并合并

### 场景 4：添加多个远程仓库

**适用情况：**
- 需要同时推送到多个远程仓库（如 GitHub 和 GitLab）
- 需要维护代码镜像
- 需要备份到多个位置

**操作步骤：**

**方法 A：添加多个命名远程仓库**

```bash
# 1. 查看现有远程仓库
git remote -v

# 2. 添加第二个远程仓库（使用不同名称）
git remote add backup <备份仓库URL>
git remote add gitlab <GitLab仓库URL>

# 3. 推送到不同的远程仓库
git push origin main
git push backup main
git push gitlab main

# 4. 查看所有远程仓库
git remote -v
```

**方法 B：为 origin 添加多个推送地址**

```bash
# 1. 添加额外的推送 URL
git remote set-url --add --push origin <第一个仓库URL>
git remote set-url --add --push origin <第二个仓库URL>

# 2. 验证配置
git remote -v

# 3. 一次推送到所有远程仓库
git push origin main
```

**注意：** 方法 B 中，`git pull` 仍然只从第一个 URL 拉取。

### 场景 5：仓库迁移（保留所有分支和标签）

**适用情况：**
- 完整迁移项目到新的远程仓库
- 需要保留所有分支、标签和历史
- 从一个托管平台迁移到另一个

**操作步骤：**

```bash
# 1. 克隆原仓库（镜像模式）
git clone --mirror <原仓库URL> repo-mirror
cd repo-mirror

# 2. 添加新的远程仓库
git remote set-url origin <新仓库URL>

# 3. 推送所有内容到新仓库
git push --mirror

# 4. 清理（可选）
cd ..
rm -rf repo-mirror
```

**或者在现有仓库中：**

```bash
# 1. 更新所有远程分支
git fetch --all

# 2. 更换远程仓库地址
git remote set-url origin <新仓库URL>

# 3. 推送所有分支
git push origin --all

# 4. 推送所有标签
git push origin --tags
```

## 常见问题处理

### 问题 1：推送时提示 "non-fast-forward"

**原因：** 远程仓库有本地没有的提交。

**解决方案：**

```bash
# 选项 A：拉取并合并
git pull origin main --rebase
git push origin main

# 选项 B：强制推送（谨慎使用）
git push -f origin main
```

### 问题 2：推送被拒绝（权限问题）

**检查清单：**
- 确认有仓库的写入权限
- 检查 SSH 密钥或 HTTPS 凭据配置
- 验证仓库 URL 是否正确

**解决方案：**

```bash
# 检查 SSH 连接
ssh -T git@github.com

# 或切换到 HTTPS
git remote set-url origin https://github.com/用户名/仓库名.git
```

### 问题 3：远程仓库名称冲突

**解决方案：**

```bash
# 删除现有远程仓库配置
git remote remove origin

# 重新添加
git remote add origin <新仓库URL>
```

### 问题 4：需要保留多个远程源

**解决方案：**

```bash
# 将 origin 重命名为 upstream
git remote rename origin upstream

# 添加新的 origin
git remote add origin <新仓库URL>

# 查看配置
git remote -v
```

## 工作流程决策树

```
用户需求
├── 只是更换远程地址？
│   ├── 保留历史 → 场景 1
│   └── 不保留历史 → 场景 2
├── 需要覆盖远程内容？ → 场景 3
├── 需要多个远程仓库？ → 场景 4
└── 完整迁移项目？ → 场景 5
```

## 安全建议

1. **操作前备份：** 在执行破坏性操作前，确保有代码备份
2. **团队沟通：** 涉及强制推送时，提前与团队成员沟通
3. **测试验证：** 在测试仓库先验证流程，再应用到生产仓库
4. **权限检查：** 确认对新仓库有适当的访问权限
5. **使用 --force-with-lease：** 比 -f 更安全，能检测他人的更改

## 执行流程

1. **理解用户需求：** 询问用户具体要实现什么目标
2. **确认场景：** 根据需求匹配对应的场景
3. **检查当前状态：** 运行检查命令了解仓库当前状态
4. **提供操作方案：** 展示具体的命令序列
5. **执行操作：** 逐步执行命令，确认每步结果
6. **验证结果：** 检查操作是否成功完成

## 脚本支持

此技能包含辅助脚本以提高操作效率和安全性：

- `scripts/check_status.sh` - 检查仓库状态的完整脚本
- `scripts/switch_remote.sh` - 交互式远程仓库切换工具
- `scripts/backup_before_operation.sh` - 操作前自动备份脚本
