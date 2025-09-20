#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 WebView 示例启动器
Example Launcher for PyQt5 WebView
"""

import sys
import os

def show_banner():
    """显示项目横幅"""
    print("=" * 60)
    print("🚀 PyQt5 WebView 桌面应用程序示例")
    print("   Desktop Application Examples with PyQt5 WebView")
    print("=" * 60)
    print()

def check_dependencies():
    """检查依赖并给出建议"""
    try:
        import PyQt5
        import PyQt5.QtWebEngineWidgets
        return True
    except ImportError:
        print("❌ 缺少必要依赖!")
        print("请运行以下命令安装:")
        print("pip install -r requirements.txt")
        print()
        return False

def show_menu():
    """显示选择菜单"""
    print("请选择要运行的示例:")
    print()
    print("1. 基础示例 (Basic Example)")
    print("   - PyQt5 WebView 基本集成")
    print("   - 菜单栏和界面演示")
    print("   - HTML/CSS/JavaScript 支持")
    print()
    print("2. 高级示例 (Advanced Example)")
    print("   - Python-JavaScript 双向通信")
    print("   - 数据库集成和文件操作")
    print("   - 桌面通知和系统集成")
    print()
    print("3. 依赖检查 (Dependency Check)")
    print("   - 检查PyQt5安装状态")
    print("   - 显示使用说明")
    print()
    print("0. 退出 (Exit)")
    print()

def run_example(choice):
    """运行选择的示例"""
    if choice == '1':
        print("🚀 启动基础示例...")
        try:
            os.system(f"{sys.executable} main.py")
        except Exception as e:
            print(f"启动失败: {e}")
            
    elif choice == '2':
        print("🚀 启动高级示例...")
        try:
            os.system(f"{sys.executable} advanced.py")
        except Exception as e:
            print(f"启动失败: {e}")
            
    elif choice == '3':
        print("🔍 运行依赖检查...")
        try:
            os.system(f"{sys.executable} demo.py")
        except Exception as e:
            print(f"检查失败: {e}")
            
    elif choice == '0':
        print("👋 再见!")
        return False
        
    else:
        print("❌ 无效选择，请重新输入")
        
    return True

def main():
    """主函数"""
    show_banner()
    
    # 检查依赖
    if not check_dependencies():
        input("按回车键退出...")
        return
    
    print("✅ 依赖检查通过!")
    print()
    
    while True:
        show_menu()
        try:
            choice = input("请输入选择 (0-3): ").strip()
            print()
            
            if not run_example(choice):
                break
                
            if choice in ['1', '2', '3']:
                print()
                input("按回车键返回主菜单...")
                print()
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出程序")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            break

if __name__ == '__main__':
    main()