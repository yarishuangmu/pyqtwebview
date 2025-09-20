#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 WebView 示例应用测试脚本
==============================

这个脚本用于验证代码结构和语法正确性，而无需实际运行PyQt5 GUI。
在没有PyQt5环境的情况下，可以用来检查代码质量。
"""

import os
import sys
import ast
import importlib.util

def check_file_syntax(filepath):
    """
    检查Python文件的语法正确性
    
    参数:
        filepath (str): 文件路径
        
    返回:
        tuple: (是否成功, 错误信息)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查语法
        ast.parse(content)
        return True, None
        
    except SyntaxError as e:
        return False, f"语法错误: {e}"
    except Exception as e:
        return False, f"其他错误: {e}"

def check_project_structure():
    """
    检查项目文件结构
    
    返回:
        dict: 检查结果
    """
    expected_files = {
        'main.py': '主程序入口',
        'webview_window.py': '主窗口类',
        'web_interface.py': 'Python-JavaScript接口',
        'requirements.txt': '依赖列表',
        'README.md': '项目文档',
        'static/index.html': '主页面',
        'static/style.css': '样式表',
        'static/app.js': 'JavaScript交互层'
    }
    
    results = {}
    
    for file_path, description in expected_files.items():
        abs_path = os.path.abspath(file_path)
        exists = os.path.exists(abs_path)
        
        if exists:
            size = os.path.getsize(abs_path)
            results[file_path] = {
                'exists': True,
                'description': description,
                'size': size,
                'status': '✓ 存在'
            }
        else:
            results[file_path] = {
                'exists': False,
                'description': description,
                'size': 0,
                'status': '✗ 缺失'
            }
    
    return results

def check_python_files():
    """
    检查Python文件的语法
    
    返回:
        dict: 检查结果
    """
    python_files = ['main.py', 'webview_window.py', 'web_interface.py']
    results = {}
    
    for file_path in python_files:
        if os.path.exists(file_path):
            success, error = check_file_syntax(file_path)
            results[file_path] = {
                'syntax_ok': success,
                'error': error,
                'status': '✓ 语法正确' if success else f'✗ {error}'
            }
        else:
            results[file_path] = {
                'syntax_ok': False,
                'error': '文件不存在',
                'status': '✗ 文件不存在'
            }
    
    return results

def check_web_files():
    """
    检查Web文件的基本内容
    
    返回:
        dict: 检查结果
    """
    web_files = {
        'static/index.html': ['<!DOCTYPE html>', '<html', '</html>'],
        'static/style.css': ['body', '{', '}'],
        'static/app.js': ['function', 'QWebChannel', 'bridge']
    }
    
    results = {}
    
    for file_path, required_content in web_files.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                missing_content = []
                for required in required_content:
                    if required not in content:
                        missing_content.append(required)
                
                if not missing_content:
                    results[file_path] = {
                        'content_ok': True,
                        'missing': [],
                        'status': '✓ 内容完整'
                    }
                else:
                    results[file_path] = {
                        'content_ok': False,
                        'missing': missing_content,
                        'status': f'✗ 缺少内容: {", ".join(missing_content)}'
                    }
                    
            except Exception as e:
                results[file_path] = {
                    'content_ok': False,
                    'missing': [],
                    'status': f'✗ 读取错误: {e}'
                }
        else:
            results[file_path] = {
                'content_ok': False,
                'missing': [],
                'status': '✗ 文件不存在'
            }
    
    return results

def print_results():
    """
    打印所有检查结果
    """
    print("=" * 50)
    print("PyQt5 WebView 示例应用 - 代码质量检查报告")
    print("=" * 50)
    print()
    
    # 检查项目结构
    print("📁 项目文件结构检查:")
    print("-" * 30)
    structure_results = check_project_structure()
    
    for file_path, result in structure_results.items():
        size_info = f" ({result['size']} 字节)" if result['exists'] else ""
        print(f"{result['status']} {file_path}{size_info}")
        print(f"   描述: {result['description']}")
        print()
    
    # 检查Python文件语法
    print("🐍 Python文件语法检查:")
    print("-" * 30)
    python_results = check_python_files()
    
    for file_path, result in python_results.items():
        print(f"{result['status']} {file_path}")
        if result['error']:
            print(f"   错误: {result['error']}")
        print()
    
    # 检查Web文件内容
    print("🌐 Web文件内容检查:")
    print("-" * 30)
    web_results = check_web_files()
    
    for file_path, result in web_results.items():
        print(f"{result['status']} {file_path}")
        if result['missing']:
            print(f"   缺少内容: {', '.join(result['missing'])}")
        print()
    
    # 总结
    all_python_ok = all(r['syntax_ok'] for r in python_results.values())
    all_web_ok = all(r['content_ok'] for r in web_results.values())
    all_files_exist = all(r['exists'] for r in structure_results.values())
    
    print("📊 总结:")
    print("-" * 30)
    print(f"文件结构完整: {'✓ 是' if all_files_exist else '✗ 否'}")
    print(f"Python语法正确: {'✓ 是' if all_python_ok else '✗ 否'}")
    print(f"Web文件内容完整: {'✓ 是' if all_web_ok else '✗ 否'}")
    print()
    
    if all_python_ok and all_web_ok and all_files_exist:
        print("🎉 恭喜！所有检查都通过了。")
        print("📝 项目已准备就绪，可以在有PyQt5环境的系统上运行。")
    else:
        print("⚠️  存在一些问题需要修复。")
    
    print()
    print("📖 使用说明:")
    print("   1. 安装依赖: pip install -r requirements.txt")
    print("   2. 运行应用: python main.py")
    print("   3. 如果遇到问题，请参考README.md中的故障排除部分")

def check_imports():
    """
    检查代码中的导入语句是否合理
    """
    print("📦 导入检查:")
    print("-" * 30)
    
    python_files = ['main.py', 'webview_window.py', 'web_interface.py']
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析AST查找导入
                tree = ast.parse(content)
                imports = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            imports.append(name.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ''
                        for name in node.names:
                            imports.append(f"{module}.{name.name}")
                
                print(f"✓ {file_path}:")
                for imp in imports[:5]:  # 只显示前5个导入
                    print(f"   - {imp}")
                if len(imports) > 5:
                    print(f"   - ... 还有 {len(imports) - 5} 个导入")
                print()
                
            except Exception as e:
                print(f"✗ {file_path}: 解析错误 - {e}")
                print()

if __name__ == '__main__':
    try:
        print_results()
        print()
        check_imports()
        
    except KeyboardInterrupt:
        print("\n\n用户中断了检查过程。")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)