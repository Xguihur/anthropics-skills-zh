#!/bin/bash
# 交互式远程仓库切换工具
# 提供友好的界面来切换 Git 远程仓库

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Git 远程仓库切换工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 显示当前配置
echo "📍 当前远程仓库配置："
if git remote -v | grep -q .; then
    git remote -v | grep "(push)" | sed 's/^/   /'
else
    echo "   未配置远程仓库"
fi
echo ""

# 获取新的远程仓库 URL
echo "请输入新的远程仓库 URL："
read -p "URL: " new_url

if [ -z "$new_url" ]; then
    echo "❌ 错误：URL 不能为空"
    exit 1
fi

# 验证 URL 格式
if [[ ! "$new_url" =~ ^(https://|git@) ]]; then
    echo "⚠️  警告：URL 格式可能不正确"
    read -p "是否继续？(y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "操作已取消"
        exit 0
    fi
fi

# 获取远程仓库名称（默认 origin）
echo ""
read -p "远程仓库名称 (默认: origin): " remote_name
remote_name=${remote_name:-origin}

# 检查远程仓库是否存在
if git remote | grep -q "^${remote_name}$"; then
    echo ""
    echo "远程仓库 '$remote_name' 已存在"
    echo "选择操作："
    echo "  1) 更新现有远程仓库 URL"
    echo "  2) 删除后重新添加"
    echo "  3) 取消操作"
    read -p "请选择 (1-3): " choice
    
    case $choice in
        1)
            echo ""
            echo "🔄 更新远程仓库 URL..."
            git remote set-url "$remote_name" "$new_url"
            ;;
        2)
            echo ""
            echo "🔄 删除并重新添加远程仓库..."
            git remote remove "$remote_name"
            git remote add "$remote_name" "$new_url"
            ;;
        3)
            echo "操作已取消"
            exit 0
            ;;
        *)
            echo "❌ 无效选择"
            exit 1
            ;;
    esac
else
    echo ""
    echo "🔄 添加新的远程仓库..."
    git remote add "$remote_name" "$new_url"
fi

# 验证配置
echo ""
echo "✅ 远程仓库配置已更新："
git remote -v | grep "^${remote_name}" | sed 's/^/   /'
echo ""

# 询问是否推送
read -p "是否立即推送到新的远程仓库？(y/N): " push_confirm
if [[ "$push_confirm" =~ ^[Yy]$ ]]; then
    current_branch=$(git branch --show-current)
    echo ""
    echo "推送选项："
    echo "  1) 推送当前分支 ($current_branch)"
    echo "  2) 推送所有分支"
    echo "  3) 推送所有分支和标签"
    echo "  4) 强制推送当前分支（谨慎）"
    echo "  5) 跳过推送"
    read -p "请选择 (1-5): " push_choice
    
    case $push_choice in
        1)
            echo ""
            echo "📤 推送当前分支..."
            git push -u "$remote_name" "$current_branch"
            ;;
        2)
            echo ""
            echo "📤 推送所有分支..."
            git push -u "$remote_name" --all
            ;;
        3)
            echo ""
            echo "📤 推送所有分支和标签..."
            git push -u "$remote_name" --all
            git push "$remote_name" --tags
            ;;
        4)
            echo ""
            echo "⚠️  警告：即将执行强制推送！"
            read -p "确定要强制推送吗？(yes/NO): " force_confirm
            if [ "$force_confirm" = "yes" ]; then
                echo "📤 强制推送当前分支..."
                git push -f "$remote_name" "$current_branch"
            else
                echo "强制推送已取消"
            fi
            ;;
        5)
            echo "跳过推送"
            ;;
        *)
            echo "❌ 无效选择，跳过推送"
            ;;
    esac
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  操作完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

