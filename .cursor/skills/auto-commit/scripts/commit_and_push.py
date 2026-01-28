#!/usr/bin/env python3
"""
自动执行 Git Commit 和 Push

执行 git commit 和 push 操作，支持自定义 commit message 或自动生成。
"""

import subprocess
import sys
import os
from typing import Tuple, List


def run_git_command(command: List[str], input_text: str = None) -> Tuple[int, str, str]:
    """执行 git 命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            input=input_text,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def check_git_repo() -> bool:
    """检查是否在 git 仓库中"""
    code, _, _ = run_git_command(['git', 'rev-parse', '--git-dir'])
    return code == 0


def has_staged_changes() -> bool:
    """检查是否有已暂存的变更"""
    code, stdout, _ = run_git_command(['git', 'diff', '--cached', '--quiet'])
    return code != 0  # 如果有变更，git diff --quiet 会返回非零


def get_current_branch() -> str:
    """获取当前分支名称"""
    code, stdout, stderr = run_git_command(['git', 'branch', '--show-current'])
    if code != 0:
        print(f"警告：无法获取当前分支\n{stderr}", file=sys.stderr)
        return "main"
    return stdout.strip() or "main"


def has_remote() -> bool:
    """检查是否配置了远程仓库"""
    code, stdout, _ = run_git_command(['git', 'remote'])
    return code == 0 and bool(stdout.strip())


def stage_all_changes() -> bool:
    """暂存所有变更"""
    print("正在暂存所有变更...")
    code, _, stderr = run_git_command(['git', 'add', '-A'])
    if code != 0:
        print(f"错误：无法暂存变更\n{stderr}", file=sys.stderr)
        return False
    print("✓ 已暂存所有变更")
    return True


def commit_changes(message: str) -> bool:
    """提交变更"""
    print("\n正在提交变更...")
    code, stdout, stderr = run_git_command(['git', 'commit', '-m', message])
    if code != 0:
        print(f"错误：提交失败\n{stderr}", file=sys.stderr)
        return False
    print(f"✓ 提交成功")
    if stdout:
        print(stdout)
    return True


def push_changes(branch: str = None) -> bool:
    """推送变更到远程仓库"""
    if not has_remote():
        print("\n提示：未配置远程仓库，跳过 push 操作")
        return True
    
    if branch is None:
        branch = get_current_branch()
    
    print(f"\n正在推送到远程仓库 (分支: {branch})...")
    
    # 首先尝试普通 push
    code, stdout, stderr = run_git_command(['git', 'push', 'origin', branch])
    
    if code != 0:
        # 如果失败，可能是因为本地分支未设置上游分支
        if 'no upstream branch' in stderr or 'has no upstream' in stderr:
            print("设置上游分支并推送...")
            code, stdout, stderr = run_git_command([
                'git', 'push', '--set-upstream', 'origin', branch
            ])
    
    if code != 0:
        print(f"错误：推送失败\n{stderr}", file=sys.stderr)
        return False
    
    print(f"✓ 推送成功")
    if stdout:
        print(stdout)
    return True


def generate_commit_message() -> str:
    """调用 generate_commit.py 生成 commit message"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    generate_script = os.path.join(script_dir, 'generate_commit.py')
    
    if not os.path.exists(generate_script):
        print("警告：找不到 generate_commit.py，使用默认消息", file=sys.stderr)
        return "chore: 更新代码"
    
    code, stdout, stderr = run_git_command(['python3', generate_script])
    
    if code != 0:
        print(f"警告：生成 commit message 失败，使用默认消息\n{stderr}", file=sys.stderr)
        return "chore: 更新代码"
    
    return stdout.strip()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='自动执行 git commit 和 push 操作'
    )
    parser.add_argument(
        '-m', '--message',
        help='自定义 commit message（如果不提供则自动生成）'
    )
    parser.add_argument(
        '--no-push',
        action='store_true',
        help='只提交不推送'
    )
    parser.add_argument(
        '--stage-all',
        action='store_true',
        help='自动暂存所有变更'
    )
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='跳过确认，直接提交（用于自动化脚本）'
    )
    
    args = parser.parse_args()
    
    # 检查是否在 git 仓库中
    if not check_git_repo():
        print("错误：当前目录不是 git 仓库", file=sys.stderr)
        return 1
    
    # 如果需要，暂存所有变更
    if args.stage_all or not has_staged_changes():
        if not stage_all_changes():
            return 1
    
    # 再次检查是否有变更
    if not has_staged_changes():
        print("提示：没有要提交的变更", file=sys.stderr)
        return 0
    
    # 获取或生成 commit message
    if args.message:
        commit_message = args.message
        print(f"\n使用自定义 commit message:\n{commit_message}\n")
    else:
        print("\n正在分析变更并生成 commit message...")
        commit_message = generate_commit_message()
        print(f"\n生成的 commit message:\n{commit_message}\n")
        
        # 交互式确认（除非指定了 --no-confirm）
        if not args.no_confirm:
            try:
                confirm = input("是否使用此 commit message？(Y/n/e-编辑): ").strip().lower()
                
                if confirm == 'n':
                    print("\n已取消提交")
                    return 0
                elif confirm == 'e' or confirm == 'edit':
                    print("\n请输入新的 commit message（可多行，输入空行结束）：")
                    lines = []
                    while True:
                        line = input()
                        if not line:
                            break
                        lines.append(line)
                    if lines:
                        commit_message = '\n'.join(lines)
                        print(f"\n使用自定义 commit message:\n{commit_message}\n")
                    else:
                        print("\n未输入内容，使用原 message")
            except (EOFError, KeyboardInterrupt):
                print("\n\n已取消提交")
                return 0
    
    # 提交变更
    if not commit_changes(commit_message):
        return 1
    
    # 推送变更（如果需要）
    if not args.no_push:
        if not push_changes():
            print("\n警告：提交成功但推送失败，请手动执行 git push", file=sys.stderr)
            return 1
    else:
        print("\n提示：已跳过 push 操作（使用了 --no-push 选项）")
    
    print("\n✓ 所有操作完成！")
    return 0


if __name__ == "__main__":
    sys.exit(main())
