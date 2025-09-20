#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 WebView 基础示例
A basic example of PyQt5 WebView integration
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar, QAction, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon


class BasicWebView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('PyQt5 WebView 基础示例')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 创建WebEngineView
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 加载默认页面
        self.load_default_page()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 首页动作
        home_action = QAction('首页', self)
        home_action.triggered.connect(self.load_default_page)
        file_menu.addAction(home_action)
        
        # 重新加载动作
        reload_action = QAction('重新加载', self)
        reload_action.triggered.connect(self.browser.reload)
        file_menu.addAction(reload_action)
        
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        # 关于动作
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def load_default_page(self):
        """加载默认页面"""
        # 获取HTML文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, 'basic_content.html')
        
        if os.path.exists(html_path):
            self.browser.setUrl(QUrl.fromLocalFile(html_path))
        else:
            # 如果HTML文件不存在，显示一个简单的内容
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>PyQt5 WebView 基础示例</title>
                <meta charset="UTF-8">
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                        background: rgba(255, 255, 255, 0.1);
                        padding: 30px;
                        border-radius: 10px;
                        backdrop-filter: blur(10px);
                    }
                    h1 {
                        text-align: center;
                        margin-bottom: 30px;
                    }
                    .feature {
                        margin: 20px 0;
                        padding: 15px;
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 5px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>PyQt5 WebView 基础示例</h1>
                    <div class="feature">
                        <h3>✨ 功能特点</h3>
                        <ul>
                            <li>集成PyQt5与WebEngine</li>
                            <li>支持现代HTML5和CSS3</li>
                            <li>响应式设计界面</li>
                            <li>菜单栏集成</li>
                        </ul>
                    </div>
                    <div class="feature">
                        <h3>🚀 快速开始</h3>
                        <p>这是一个展示如何在PyQt5应用程序中嵌入WebView的基础示例。</p>
                        <p>您可以在这里显示任何HTML内容，包括本地文件或网页。</p>
                    </div>
                    <div class="feature">
                        <h3>📚 学习资源</h3>
                        <p>查看源代码了解如何实现：</p>
                        <ul>
                            <li>WebEngineView的基本用法</li>
                            <li>菜单栏集成</li>
                            <li>HTML内容加载</li>
                        </ul>
                    </div>
                </div>
            </body>
            </html>
            """
            self.browser.setHtml(html_content)
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, '关于', 
                         'PyQt5 WebView 基础示例\n\n'
                         '这是一个展示如何使用PyQt5和WebEngine\n'
                         '创建桌面应用程序的示例。\n\n'
                         '版本: 1.0')


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName('PyQt5 WebView 基础示例')
    
    # 创建主窗口
    window = BasicWebView()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()