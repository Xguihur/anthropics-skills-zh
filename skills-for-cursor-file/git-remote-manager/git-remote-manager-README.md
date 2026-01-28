# Git 远程仓库管理器 (Git Remote Manager)

## 📖 简介

`git-remote-manager` 是一个专门用于管理 Git 远程仓库的 Claude skill，帮助你轻松完成远程仓库的切换、添加和管理操作。

## ✨ 功能特性

### 支持的操作场景

1. **更换远程仓库（保留历史）**
   - 保留完整的提交历史
   - 安全地切换到新的远程仓库

2. **清空历史，全新开始**
   - 删除所有提交历史
   - 创建一个干净的新仓库

3. **强制推送覆盖远程仓库**
   - 用本地内容覆盖远程仓库
   - 支持安全的 `--force-with-lease` 选项

4. **添加多个远程仓库**
   - 同时推送到多个远程仓库
   - 维护代码镜像和备份

5. **仓库完整迁移**
   - 保留所有分支、标签和历史
   - 从一个托管平台迁移到另一个

### 辅助工具脚本

- **check_status.sh** - 检查当前仓库状态
- **switch_remote.sh** - 交互式远程仓库切换工具
- **backup_before_operation.sh** - 操作前自动备份

## 📦 安装

将 `git-remote-manager.skill` 文件导入到 Cursor 中：

1. 打开 Cursor
2. 进入 Settings → Features → Skills
3. 点击 "Import Skill"
4. 选择 `git-remote-manager.skill` 文件

## 🚀 使用方法

安装后，直接向 Claude 提出 Git 远程仓库相关的需求，skill 会自动触发。

### 示例对话

**场景 1：更换远程仓库**
```
用户：我想把这个项目推送到我的 GitHub 仓库 https://github.com/myname/my-repo.git
Claude：[使用 git-remote-manager skill 提供步骤指导]
```

**场景 2：清空历史**
```
用户：我想清空所有 git 历史记录，重新开始
Claude：[提供清空历史的安全方案]
```

**场景 3：添加镜像仓库**
```
用户：我想同时推送到 GitHub 和 GitLab
Claude：[配置多个远程仓库]
```

## 🛠️ 手动使用脚本

skill 包含的脚本也可以单独使用：

```bash
# 检查仓库状态
bash check_status.sh

# 交互式切换远程仓库
bash switch_remote.sh

# 创建备份
bash backup_before_operation.sh
```

## ⚠️ 安全建议

1. **操作前备份** - 在执行破坏性操作前，建议先运行 `backup_before_operation.sh`
2. **团队沟通** - 涉及强制推送时，提前与团队成员沟通
3. **使用 --force-with-lease** - 比 `-f` 更安全，能检测他人的更改
4. **权限检查** - 确认对新仓库有适当的访问权限

## 📋 技能触发条件

当你提出以下类型的需求时，此 skill 会自动启用：

- 更换 Git 远程仓库地址
- 切换到新的 GitHub/GitLab 仓库
- 清空 Git 历史记录
- 添加多个远程仓库
- 强制推送到远程仓库
- 迁移代码到新平台
- 管理多个远程源

## 🔧 支持的 Git 操作

- `git remote add/set-url/remove`
- `git push --all/--tags/-f/--force-with-lease`
- `git init` / `git clone --mirror`
- 分支管理和历史清理
- 多远程仓库配置

## 📄 许可证

Apache License 2.0

## 🤝 反馈与建议

如有问题或建议，欢迎反馈！

---

**创建日期：** 2026-01-28  
**版本：** 1.0.0  
**作者：** 基于 Anthropic Skills 框架创建

