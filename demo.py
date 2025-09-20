#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script to check PyQt5 installation and show a simple example
演示脚本：检查PyQt5安装并显示简单示例
"""

import sys

def check_requirements():
    """检查依赖是否安装"""
    missing = []
    
    try:
        import PyQt5
        print("✅ PyQt5 已安装")
    except ImportError:
        missing.append("PyQt5")
        print("❌ PyQt5 未安装")
    
    try:
        import PyQt5.QtWebEngineWidgets
        print("✅ PyQtWebEngine 已安装")
    except ImportError:
        missing.append("PyQtWebEngine")
        print("❌ PyQtWebEngine 未安装")
    
    if missing:
        print(f"\n缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("\n🎉 所有依赖已安装，可以运行示例程序！")
    return True

def show_usage():
    """显示使用说明"""
    print("\n📖 使用说明:")
    print("基础示例:    python main.py")
    print("高级示例:    python advanced.py")
    print("检查依赖:    python demo.py")

def main():
    """主函数"""
    print("PyQt5 WebView 示例项目 - 依赖检查")
    print("=" * 40)
    
    if check_requirements():
        show_usage()
        
        # 如果依赖都安装了，可以选择运行一个简单的测试
        try:
            from PyQt5.QtWidgets import QApplication, QMessageBox
            
            app = QApplication(sys.argv)
            msg = QMessageBox()
            msg.setWindowTitle("PyQt5 测试")
            msg.setText("PyQt5 安装正常！\n\n可以运行 main.py 或 advanced.py 查看完整示例。")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            
        except Exception as e:
            print(f"PyQt5 测试失败: {e}")
    else:
        print("\n请先安装必要的依赖包。")

if __name__ == '__main__':
    main()