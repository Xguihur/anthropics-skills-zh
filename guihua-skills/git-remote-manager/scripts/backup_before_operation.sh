#!/bin/bash
# Git 仓库备份脚本
# 在执行危险操作前创建仓库备份

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Git 仓库备份工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 获取仓库根目录
repo_root=$(git rev-parse --show-toplevel)
repo_name=$(basename "$repo_root")

# 生成备份目录名称
timestamp=$(date +"%Y%m%d_%H%M%S")
backup_name="${repo_name}_backup_${timestamp}"

# 获取备份位置
echo "当前仓库：$repo_root"
echo ""
echo "选择备份位置："
echo "  1) 与仓库同级目录（推荐）"
echo "  2) 自定义位置"
read -p "请选择 (1-2): " location_choice

case $location_choice in
    1)
        backup_dir="$(dirname "$repo_root")/$backup_name"
        ;;
    2)
        read -p "请输入备份目录路径: " custom_path
        if [ -z "$custom_path" ]; then
            echo "❌ 错误：路径不能为空"
            exit 1
        fi
        backup_dir="$custom_path/$backup_name"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

# 确认备份
echo ""
echo "备份信息："
echo "  源目录：$repo_root"
echo "  备份到：$backup_dir"
echo ""

# 计算仓库大小
repo_size=$(du -sh "$repo_root" | cut -f1)
echo "  仓库大小：$repo_size"
echo ""

read -p "确认开始备份？(y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "操作已取消"
    exit 0
fi

# 创建备份
echo ""
echo "🔄 正在创建备份..."
echo ""

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "⚠️  警告：检测到未提交的更改"
    read -p "是否在备份前创建临时提交？(y/N): " stash_confirm
    if [[ "$stash_confirm" =~ ^[Yy]$ ]]; then
        git stash push -m "Backup stash ${timestamp}"
        echo "✓ 已暂存未提交的更改"
    fi
fi

# 使用 git clone 创建完整备份
if git clone --mirror "$repo_root" "$backup_dir/.git"; then
    cd "$backup_dir"
    git config --bool core.bare false
    git reset --hard
    cd - > /dev/null
    
    echo ""
    echo "✅ 备份创建成功！"
    echo ""
    echo "备份位置：$backup_dir"
    
    # 创建备份信息文件
    cat > "$backup_dir/BACKUP_INFO.txt" << EOF
Git 仓库备份信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

备份时间：$(date)
原始仓库：$repo_root
备份位置：$backup_dir

当前分支：$(git -C "$repo_root" branch --show-current)
最后提交：$(git -C "$repo_root" log -1 --oneline)

远程仓库配置：
$(git -C "$repo_root" remote -v)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

恢复方法：
1. 如需恢复，可将备份目录内容复制回原位置
2. 或使用：git clone $backup_dir 恢复的仓库名

删除备份：
rm -rf "$backup_dir"
EOF
    
    echo ""
    echo "备份信息已保存到：$backup_dir/BACKUP_INFO.txt"
    echo ""
    
    # 询问是否打开备份目录
    if command -v open &> /dev/null; then
        read -p "是否在 Finder 中打开备份目录？(y/N): " open_confirm
        if [[ "$open_confirm" =~ ^[Yy]$ ]]; then
            open "$backup_dir"
        fi
    fi
else
    echo ""
    echo "❌ 备份失败"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  备份完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

