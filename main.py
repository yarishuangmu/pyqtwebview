#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 WebView 桌面应用程序主入口
==========================================

这是一个完整的PyQt5 WebView应用程序示例，展示了如何将Web技术与Python桌面应用程序相结合。
本文件是应用程序的主入口点，负责初始化PyQt5应用程序环境并启动主窗口。

作者: yarishuangmu
用途: 教育示例 - 帮助理解PyQt5和WebEngine的工作机制
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from webview_window import WebViewWindow

def main():
    """
    应用程序主函数
    ================
    
    这个函数负责：
    1. 创建QApplication实例 - PyQt5应用程序的核心对象
    2. 设置应用程序属性和配置
    3. 创建并显示主窗口
    4. 启动事件循环
    
    PyQt5应用程序的基本结构：
    - QApplication: 管理应用程序的主要设置和控制流程
    - QWidget/QMainWindow: 应用程序的窗口容器
    - 事件循环: 处理用户交互和系统事件
    """
    
    # 1. 创建QApplication实例
    # ========================
    # QApplication是PyQt5应用程序的核心，负责：
    # - 初始化GUI系统
    # - 管理应用程序的主事件循环
    # - 处理命令行参数
    # - 管理应用程序级别的设置
    app = QApplication(sys.argv)
    
    # 2. 设置应用程序属性
    # ====================
    # 这些设置会影响整个应用程序的行为
    
    # 设置应用程序名称 - 显示在任务栏和窗口标题中
    app.setApplicationName("PyQt5 WebView 示例")
    
    # 设置应用程序版本
    app.setApplicationVersion("1.0.0")
    
    # 设置组织信息 - 用于配置文件存储路径
    app.setOrganizationName("yarishuangmu")
    app.setOrganizationDomain("github.com/yarishuangmu")
    
    # 3. 启用高DPI缩放支持
    # =====================
    # 在高分辨率显示器上保证界面清晰度
    # 这对现代桌面应用程序非常重要
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # 4. WebEngine特定设置
    # ====================
    # WebEngine需要一些特殊的属性设置
    
    # 启用软件OpenGL渲染 - 提高兼容性
    app.setAttribute(Qt.AA_UseSoftwareOpenGL, True)
    
    # 5. 创建主窗口实例
    # ==================
    # WebViewWindow是我们自定义的主窗口类，继承自QMainWindow
    # 它包含了WebEngine视图和所有的界面逻辑
    main_window = WebViewWindow()
    
    # 6. 显示主窗口
    # ==============
    # show()方法会：
    # - 渲染窗口内容
    # - 将窗口添加到桌面窗口管理器
    # - 使窗口可见
    main_window.show()
    
    # 7. 启动应用程序事件循环
    # ========================
    # exec_()方法启动Qt的主事件循环，这是PyQt5应用程序的核心机制：
    # 
    # 事件循环的工作原理：
    # - 持续监听系统事件（鼠标、键盘、定时器等）
    # - 将事件分发给相应的窗口部件
    # - 处理绘制和更新请求
    # - 管理应用程序状态
    #
    # 事件循环会一直运行直到：
    # - 用户关闭所有窗口
    # - 调用QApplication.quit()
    # - 系统要求应用程序退出
    exit_code = app.exec_()
    
    # 8. 应用程序退出
    # ================
    # 当事件循环结束时，返回退出代码
    # 0 表示正常退出，非0表示异常退出
    return exit_code

def setup_application_environment():
    """
    设置应用程序运行环境
    =====================
    
    这个函数处理应用程序启动前的环境配置，包括：
    - 路径设置
    - 环境变量配置
    - 资源文件检查
    """
    
    # 获取应用程序目录
    # 这对于查找资源文件（如HTML、CSS、JS）很重要
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置资源文件路径
    static_dir = os.path.join(app_dir, 'static')
    if not os.path.exists(static_dir):
        # 如果static目录不存在，创建它
        os.makedirs(static_dir)
        print(f"创建资源目录: {static_dir}")
    
    # 返回重要路径信息
    return {
        'app_dir': app_dir,
        'static_dir': static_dir
    }

if __name__ == '__main__':
    """
    程序入口点
    ===========
    
    这个代码块只在直接运行此文件时执行，而不是在被导入时执行。
    这是Python的标准做法，确保模块既可以作为脚本运行，也可以被其他模块导入。
    """
    
    # 设置应用程序环境
    env_info = setup_application_environment()
    print("PyQt5 WebView 应用程序启动中...")
    print(f"应用程序目录: {env_info['app_dir']}")
    print(f"静态资源目录: {env_info['static_dir']}")
    
    try:
        # 启动应用程序
        exit_code = main()
        print(f"应用程序退出，退出代码: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        # 捕获并处理未预期的异常
        print(f"应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)