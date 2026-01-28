#!/usr/bin/env python3
"""
自动生成 Git Commit Message

分析当前的代码变更，基于变更内容和类型智能生成符合规范的 commit message。
"""

import subprocess
import sys
import os
from typing import Tuple, List, Dict
import re


def run_git_command(command: List[str]) -> Tuple[int, str, str]:
    """执行 git 命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def get_git_status() -> Dict[str, List[str]]:
    """获取 git 状态信息"""
    code, stdout, stderr = run_git_command(['git', 'status', '--short'])
    
    if code != 0:
        print(f"错误：无法获取 git 状态\n{stderr}", file=sys.stderr)
        sys.exit(1)
    
    status = {
        'staged': [],
        'unstaged': [],
        'untracked': []
    }
    
    for line in stdout.strip().split('\n'):
        if not line:
            continue
        
        status_code = line[:2]
        filename = line[3:].strip()
        
        if status_code[0] in ['M', 'A', 'D', 'R', 'C']:
            status['staged'].append((status_code[0], filename))
        elif status_code[1] in ['M', 'D']:
            status['unstaged'].append((status_code[1], filename))
        elif status_code == '??':
            status['untracked'].append(filename)
    
    return status


def get_staged_diff() -> str:
    """获取已暂存的变更内容"""
    code, stdout, stderr = run_git_command(['git', 'diff', '--cached'])
    
    if code != 0:
        print(f"警告：无法获取 diff 信息\n{stderr}", file=sys.stderr)
        return ""
    
    return stdout


def analyze_changes(status: Dict[str, List[str]], diff: str) -> Dict[str, any]:
    """分析变更内容并提取关键信息"""
    analysis = {
        'type': 'chore',  # feat, fix, refactor, docs, style, test, chore
        'scope': '',
        'files_count': len(status['staged']),
        'files': [f[1] if isinstance(f, tuple) else f for f in status['staged']],
        'operations': {
            'added': 0,
            'modified': 0,
            'deleted': 0
        },
        'diff_content': diff  # 保存 diff 内容供后续分析
    }
    
    # 统计操作类型
    for item in status['staged']:
        if isinstance(item, tuple):
            op_type, _ = item
            if op_type == 'A':
                analysis['operations']['added'] += 1
            elif op_type == 'M':
                analysis['operations']['modified'] += 1
            elif op_type == 'D':
                analysis['operations']['deleted'] += 1
    
    # 分析文件类型来推断 scope
    file_patterns = {
        'docs': [r'\.md$', r'\.txt$', r'README', r'CHANGELOG'],
        'test': [r'test_.*\.py$', r'.*_test\.py$', r'\.test\.', r'\.spec\.'],
        'config': [r'\.json$', r'\.yaml$', r'\.yml$', r'\.toml$', r'\.ini$', r'\.conf$'],
        'scripts': [r'scripts/', r'\.sh$', r'\.bash$'],
        'frontend': [r'\.jsx?$', r'\.tsx?$', r'\.vue$', r'\.css$', r'\.scss$', r'\.html$'],
        'backend': [r'\.py$', r'\.java$', r'\.go$', r'\.rb$', r'\.php$'],
    }
    
    for file_info in status['staged']:
        filename = file_info[1] if isinstance(file_info, tuple) else file_info
        for scope, patterns in file_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    if not analysis['scope']:
                        analysis['scope'] = scope
                    break
    
    # 分析变更类型（通过关键词）
    if diff:
        diff_lower = diff.lower()
        
        # 检查是否是新功能
        if any(keyword in diff_lower for keyword in ['add', 'new', 'feature', 'implement']):
            if analysis['operations']['added'] > 0:
                analysis['type'] = 'feat'
        
        # 检查是否是 bug 修复
        elif any(keyword in diff_lower for keyword in ['fix', 'bug', 'issue', 'error', 'correct']):
            analysis['type'] = 'fix'
        
        # 检查是否是重构
        elif any(keyword in diff_lower for keyword in ['refactor', 'restructure', 'reorganize']):
            analysis['type'] = 'refactor'
        
        # 检查是否是文档更新
        elif analysis['scope'] == 'docs':
            analysis['type'] = 'docs'
        
        # 检查是否是样式调整
        elif any(keyword in diff_lower for keyword in ['style', 'format', 'lint']):
            analysis['type'] = 'style'
        
        # 检查是否是测试相关
        elif analysis['scope'] == 'test':
            analysis['type'] = 'test'
    
    return analysis


def generate_commit_message(analysis: Dict[str, any]) -> str:
    """根据分析结果生成 commit message"""
    
    # 构建 commit 类型和作用域
    commit_type = analysis['type']
    scope = analysis['scope']
    
    type_line = f"{commit_type}"
    if scope:
        type_line += f"({scope})"
    
    # 生成简短描述
    files = analysis['files']
    ops = analysis['operations']
    diff_content = analysis.get('diff_content', '').lower()
    
    # 构建描述
    if len(files) == 1:
        filename = os.path.basename(files[0])
        if ops['added'] > 0:
            summary = f"添加 {filename}"
        elif ops['deleted'] > 0:
            summary = f"删除 {filename}"
        else:
            summary = f"更新 {filename}"
    else:
        # 多文件时，尝试根据文件名、路径和 diff 内容推断功能
        file_keywords = ' '.join(files).lower()
        
        # 分析 diff 内容获取更多上下文
        diff_keywords = {
            'improve': '改进', 'enhance': '增强', 'optimize': '优化',
            'confirm': '确认', 'interactive': '交互式', 'validation': '验证',
            'message': 'commit message', 'better': '更好',
            'add.*confirm': '添加确认', 'add.*interaction': '添加交互'
        }
        
        improvement_hint = ""
        for keyword, hint in diff_keywords.items():
            if re.search(keyword, diff_content):
                improvement_hint = hint
                break
        
        if commit_type == 'feat':
            # 尝试根据文件名推断功能
            if 'skill' in file_keywords or 'SKILL.md' in str(files):
                if ops['added'] > ops['modified']:
                    summary = "创建 auto-commit skill 实现自动化代码提交"
                else:
                    if improvement_hint:
                        summary = f"改进 auto-commit skill 功能（{improvement_hint}）"
                    else:
                        summary = "增强 auto-commit skill 功能"
            elif 'auth' in file_keywords or 'login' in file_keywords:
                summary = "实现用户认证功能"
            elif 'api' in file_keywords:
                summary = "添加新的 API 接口"
            elif 'ui' in file_keywords or 'component' in file_keywords:
                summary = "添加新的 UI 组件"
            else:
                summary = "添加新功能模块"
        elif commit_type == 'fix':
            if 'test' in file_keywords:
                summary = "修复测试相关问题"
            else:
                summary = "修复功能缺陷"
        elif commit_type == 'refactor':
            summary = "重构代码结构"
        elif commit_type == 'docs':
            if 'readme' in file_keywords.lower():
                summary = "更新 README 文档"
            elif 'api' in file_keywords:
                summary = "更新 API 文档"
            elif 'skill' in file_keywords:
                if improvement_hint:
                    summary = f"改进 skill 文档（添加{improvement_hint}说明）"
                else:
                    summary = "更新 skill 文档"
            else:
                summary = "更新项目文档"
        elif commit_type == 'style':
            summary = "调整代码格式"
        elif commit_type == 'test':
            summary = "添加或更新测试用例"
        elif commit_type == 'chore':
            # chore 类型也尝试提供更多上下文
            if 'script' in file_keywords and improvement_hint:
                summary = f"改进脚本功能（{improvement_hint}）"
            else:
                summary = "更新项目代码"
        else:
            summary = "更新项目代码"
    
    # 构建详细说明
    details = []
    
    if ops['added'] > 0:
        details.append(f"- 新增 {ops['added']} 个文件")
    if ops['modified'] > 0:
        details.append(f"- 修改 {ops['modified']} 个文件")
    if ops['deleted'] > 0:
        details.append(f"- 删除 {ops['deleted']} 个文件")
    
    # 列出主要文件（最多5个）
    if len(files) > 1:
        details.append("\n主要文件：")
        for f in files[:5]:
            details.append(f"- {f}")
        if len(files) > 5:
            details.append(f"- ... 及其他 {len(files) - 5} 个文件")
    
    # 组装完整的 commit message
    message = f"{type_line}: {summary}"
    
    if details:
        message += "\n\n" + "\n".join(details)
    
    return message


def main():
    """主函数"""
    # 检查是否在 git 仓库中
    code, _, _ = run_git_command(['git', 'rev-parse', '--git-dir'])
    if code != 0:
        print("错误：当前目录不是 git 仓库", file=sys.stderr)
        sys.exit(1)
    
    # 获取 git 状态
    status = get_git_status()
    
    # 检查是否有已暂存的变更
    if not status['staged']:
        print("提示：没有已暂存的变更，正在暂存所有变更...", file=sys.stderr)
        # 暂存所有变更
        code, _, stderr = run_git_command(['git', 'add', '-A'])
        if code != 0:
            print(f"错误：无法暂存变更\n{stderr}", file=sys.stderr)
            sys.exit(1)
        # 重新获取状态
        status = get_git_status()
        
        if not status['staged']:
            print("错误：没有要提交的变更", file=sys.stderr)
            sys.exit(1)
    
    # 获取变更内容
    diff = get_staged_diff()
    
    # 分析变更
    analysis = analyze_changes(status, diff)
    
    # 生成 commit message
    message = generate_commit_message(analysis)
    
    # 输出生成的 message
    print(message)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
