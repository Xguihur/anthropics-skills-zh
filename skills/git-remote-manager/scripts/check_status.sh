#!/bin/bash
# Git 仓库状态检查脚本
# 用于在执行远程仓库操作前检查当前仓库状态

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Git 仓库状态检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 1. 当前分支
echo "📍 当前分支："
current_branch=$(git branch --show-current)
echo "   $current_branch"
echo ""

# 2. 远程仓库配置
echo "🌐 远程仓库配置："
if git remote -v | grep -q .; then
    git remote -v | sed 's/^/   /'
else
    echo "   ⚠️  未配置远程仓库"
fi
echo ""

# 3. 工作区状态
echo "📝 工作区状态："
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "   ✓ 工作区干净，没有未提交的更改"
else
    echo "   ⚠️  有未提交的更改："
    git status --short | sed 's/^/      /'
fi
echo ""

# 4. 未推送的提交
echo "📤 未推送的提交："
unpushed=$(git log @{u}.. --oneline 2>/dev/null || echo "")
if [ -z "$unpushed" ]; then
    echo "   ✓ 没有未推送的提交"
else
    echo "   ⚠️  有 $(echo "$unpushed" | wc -l | xargs) 个未推送的提交："
    echo "$unpushed" | head -5 | sed 's/^/      /'
    if [ $(echo "$unpushed" | wc -l) -gt 5 ]; then
        echo "      ... (还有更多)"
    fi
fi
echo ""

# 5. 最近的提交
echo "📜 最近的提交（最多 5 条）："
git log --oneline -5 | sed 's/^/   /'
echo ""

# 6. 所有分支
echo "🌿 本地分支："
git branch | sed 's/^/   /'
echo ""

# 7. 标签
echo "🏷️  标签："
tag_count=$(git tag | wc -l | xargs)
if [ "$tag_count" -eq 0 ]; then
    echo "   无标签"
else
    echo "   共 $tag_count 个标签"
    if [ "$tag_count" -le 10 ]; then
        git tag | sed 's/^/   /'
    else
        git tag | head -5 | sed 's/^/   /'
        echo "   ... (还有 $((tag_count - 5)) 个)"
    fi
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  检查完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

