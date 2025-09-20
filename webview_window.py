#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 WebView 主窗口类
=======================

这个文件包含主窗口类的实现，展示了如何将WebEngine集成到PyQt5应用程序中。
重点讲解PyQt5的窗口系统、布局管理和WebEngine的使用方法。

核心概念：
- QMainWindow: PyQt5的主窗口基类
- QWebEngineView: 用于显示Web内容的控件
- 布局管理: 控制界面元素的排列和大小
- 信号和槽: PyQt5的事件处理机制
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLineEdit, QLabel,
                             QToolBar, QStatusBar, QMenuBar, QAction,
                             QSplitter, QTextEdit, QGroupBox)
from PyQt5.QtCore import QUrl, pyqtSignal, QTimer, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont

from web_interface import WebInterface

class WebViewWindow(QMainWindow):
    """
    PyQt5 WebView 主窗口类
    ======================
    
    这个类继承自QMainWindow，是PyQt5应用程序的标准主窗口类型。
    QMainWindow提供了：
    - 菜单栏 (menuBar)
    - 工具栏 (toolBar) 
    - 状态栏 (statusBar)
    - 中央部件区域 (centralWidget)
    - 停靠部件 (dockWidgets)
    
    本类展示了如何：
    1. 创建和配置WebEngine视图
    2. 设计用户界面布局
    3. 实现Python与JavaScript的通信
    4. 处理用户交互事件
    """
    
    # 定义自定义信号
    # ===============
    # 信号是PyQt5中的重要概念，用于对象间的通信
    # 当特定事件发生时，对象可以发射信号，其他对象可以连接到这些信号
    page_loaded = pyqtSignal(str)  # 页面加载完成信号
    url_changed = pyqtSignal(QUrl)  # URL变化信号
    
    def __init__(self):
        """
        构造函数
        =========
        
        初始化主窗口的所有组件和设置。
        PyQt5的初始化遵循以下模式：
        1. 调用父类构造函数
        2. 初始化实例变量
        3. 设置窗口属性
        4. 创建用户界面
        5. 连接信号和槽
        """
        super().__init__()
        
        # 初始化实例变量
        self.web_view = None        # WebEngine视图
        self.web_interface = None   # Python-JavaScript接口
        self.url_input = None       # 地址栏输入框
        self.status_label = None    # 状态标签
        
        # 设置窗口基本属性
        self.setup_window_properties()
        
        # 创建用户界面
        self.setup_ui()
        
        # 设置WebEngine
        self.setup_webengine()
        
        # 连接信号和槽
        self.connect_signals()
        
        # 加载初始页面
        self.load_initial_page()
    
    def setup_window_properties(self):
        """
        设置窗口基本属性
        =================
        
        配置窗口的标题、大小、图标等基本属性。
        这些设置决定了窗口在桌面环境中的表现。
        """
        
        # 设置窗口标题
        self.setWindowTitle("PyQt5 WebView 示例 - 理解PyQt5与WebEngine集成")
        
        # 设置窗口大小
        # resize()方法设置窗口的初始大小
        self.resize(1200, 800)
        
        # 设置最小窗口大小，防止窗口被缩放得太小
        self.setMinimumSize(800, 600)
        
        # 设置窗口图标（如果有图标文件）
        # icon_path = os.path.join(os.path.dirname(__file__), 'static', 'icon.png')
        # if os.path.exists(icon_path):
        #     self.setWindowIcon(QIcon(icon_path))
    
    def setup_ui(self):
        """
        设置用户界面
        =============
        
        创建和布局所有的用户界面元素。
        PyQt5使用布局管理器来自动排列界面元素。
        
        布局管理器类型：
        - QVBoxLayout: 垂直布局
        - QHBoxLayout: 水平布局
        - QGridLayout: 网格布局
        - QFormLayout: 表单布局
        """
        
        # 1. 创建中央部件
        # ================
        # QMainWindow需要一个中央部件来容纳主要内容
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 2. 创建主布局
        # ==============
        # 使用垂直布局作为主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 3. 创建工具栏区域
        # ==================
        toolbar_layout = self.create_toolbar_layout()
        main_layout.addLayout(toolbar_layout)
        
        # 4. 创建内容区域
        # ================
        content_layout = self.create_content_layout()
        main_layout.addLayout(content_layout)
        
        # 5. 创建菜单栏
        # ==============
        self.create_menu_bar()
        
        # 6. 创建状态栏
        # ==============
        self.create_status_bar()
    
    def create_toolbar_layout(self):
        """
        创建工具栏布局
        ===============
        
        工具栏包含导航按钮和地址栏，提供基本的浏览器功能。
        """
        toolbar_layout = QHBoxLayout()
        
        # 创建导航按钮
        self.back_btn = QPushButton("← 后退")
        self.forward_btn = QPushButton("前进 →")
        self.refresh_btn = QPushButton("🔄 刷新")
        self.home_btn = QPushButton("🏠 首页")
        
        # 设置按钮提示文本
        self.back_btn.setToolTip("返回上一页")
        self.forward_btn.setToolTip("前往下一页")
        self.refresh_btn.setToolTip("刷新当前页面")
        self.home_btn.setToolTip("返回首页")
        
        # 创建地址栏
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入网址或文件路径...")
        
        # 创建加载按钮
        self.load_btn = QPushButton("转到")
        self.load_btn.setToolTip("加载输入的网址")
        
        # 添加到布局
        toolbar_layout.addWidget(self.back_btn)
        toolbar_layout.addWidget(self.forward_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.home_btn)
        toolbar_layout.addWidget(QLabel("地址:"))
        toolbar_layout.addWidget(self.url_input)
        toolbar_layout.addWidget(self.load_btn)
        
        return toolbar_layout
    
    def create_content_layout(self):
        """
        创建内容区域布局
        =================
        
        内容区域包含WebView和调试面板。
        使用QSplitter允许用户调整各部分的大小。
        """
        content_layout = QVBoxLayout()
        
        # 创建分割器 - 允许用户调整WebView和调试面板的大小
        splitter = QSplitter(Qt.Horizontal)
        
        # 1. 创建WebView容器
        # ===================
        webview_group = QGroupBox("Web内容显示区域")
        webview_layout = QVBoxLayout(webview_group)
        
        # 创建WebEngine视图
        self.web_view = QWebEngineView()
        webview_layout.addWidget(self.web_view)
        
        # 2. 创建调试面板
        # ================
        debug_group = QGroupBox("调试和交互面板")
        debug_layout = QVBoxLayout(debug_group)
        
        # JavaScript执行区域
        js_label = QLabel("JavaScript代码执行:")
        self.js_input = QTextEdit()
        self.js_input.setMaximumHeight(100)
        self.js_input.setPlaceholderText("在此输入JavaScript代码...")
        
        self.execute_js_btn = QPushButton("执行JavaScript")
        
        # Python函数调用区域
        python_label = QLabel("Python函数调用:")
        self.python_output = QTextEdit()
        self.python_output.setMaximumHeight(150)
        self.python_output.setReadOnly(True)
        self.python_output.setPlaceholderText("Python函数执行结果将显示在这里...")
        
        # 添加到调试布局
        debug_layout.addWidget(js_label)
        debug_layout.addWidget(self.js_input)
        debug_layout.addWidget(self.execute_js_btn)
        debug_layout.addWidget(python_label)
        debug_layout.addWidget(self.python_output)
        
        # 将组件添加到分割器
        splitter.addWidget(webview_group)
        splitter.addWidget(debug_group)
        
        # 设置分割器比例 (WebView占75%, 调试面板占25%)
        splitter.setSizes([900, 300])
        
        content_layout.addWidget(splitter)
        
        return content_layout
    
    def create_menu_bar(self):
        """
        创建菜单栏
        ===========
        
        菜单栏提供应用程序的主要功能入口。
        QMainWindow的menuBar()方法返回菜单栏对象。
        """
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        # 创建动作 (QAction)
        # QAction代表用户可以执行的动作，可以添加到菜单或工具栏
        open_action = QAction('打开文件(&O)', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('打开本地HTML文件')
        
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用程序')
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图(&V)')
        
        fullscreen_action = QAction('全屏(&F)', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        
        view_menu.addAction(fullscreen_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = QAction('关于(&A)', self)
        about_action.setStatusTip('关于此应用程序')
        
        help_menu.addAction(about_action)
    
    def create_status_bar(self):
        """
        创建状态栏
        ===========
        
        状态栏显示应用程序状态信息，如加载进度、URL等。
        """
        statusbar = self.statusBar()
        
        # 创建状态标签
        self.status_label = QLabel("就绪")
        statusbar.addWidget(self.status_label)
        
        # 创建进度显示
        self.progress_label = QLabel("")
        statusbar.addPermanentWidget(self.progress_label)
    
    def setup_webengine(self):
        """
        设置WebEngine
        ==============
        
        配置WebEngine的各种设置和选项。
        WebEngine是基于Chromium的Web渲染引擎。
        """
        
        # 获取WebEngine设置对象
        settings = self.web_view.settings()
        
        # 启用各种Web功能
        # ================
        
        # 启用JavaScript - 现代Web应用的核心
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        
        # 启用JavaScript访问剪贴板
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        
        # 启用JavaScript打开新窗口
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        
        # 启用本地存储 - Web应用数据持久化
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        
        # 启用Web安全性（默认开启，但明确设置以提高安全性）
        settings.setAttribute(QWebEngineSettings.WebSecurity, True)
        
        # 启用超链接审计（用于网页分析）
        settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, True)
        
        # 启用错误页面显示
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        
        # 启用插件（如Flash等，但现代Web很少使用）
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        
        # 设置默认字体
        # =============
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Microsoft YaHei")
        settings.setFontSize(QWebEngineSettings.DefaultFontSize, 14)
        
        # 创建Python-JavaScript接口
        # ===========================
        self.web_interface = WebInterface(self)
        
        # 将Python对象注册到JavaScript环境
        # 这允许JavaScript代码直接调用Python函数
        self.web_view.page().setWebChannel(self.web_interface.channel)
    
    def connect_signals(self):
        """
        连接信号和槽
        =============
        
        信号-槽机制是PyQt5的核心特性，用于对象间通信。
        当事件发生时，对象发射信号，连接的槽函数会被调用。
        """
        
        # WebView相关信号
        # ================
        
        # 页面加载完成
        self.web_view.loadFinished.connect(self.on_load_finished)
        
        # URL变化
        self.web_view.urlChanged.connect(self.on_url_changed)
        
        # 页面标题变化
        self.web_view.titleChanged.connect(self.setWindowTitle)
        
        # 加载进度变化
        self.web_view.loadProgress.connect(self.on_load_progress)
        
        # 导航按钮信号
        # ==============
        self.back_btn.clicked.connect(self.web_view.back)
        self.forward_btn.clicked.connect(self.web_view.forward)
        self.refresh_btn.clicked.connect(self.web_view.reload)
        self.home_btn.clicked.connect(self.load_initial_page)
        
        # 地址栏信号
        # ===========
        self.url_input.returnPressed.connect(self.load_url)
        self.load_btn.clicked.connect(self.load_url)
        
        # JavaScript执行按钮
        # ===================
        self.execute_js_btn.clicked.connect(self.execute_javascript)
        
        # 自定义信号
        # ===========
        self.page_loaded.connect(self.on_page_loaded)
        self.url_changed.connect(self.on_custom_url_changed)
    
    def load_initial_page(self):
        """
        加载初始页面
        =============
        
        应用程序启动时加载的默认页面。
        """
        # 构建本地HTML文件路径
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        index_path = os.path.join(static_dir, 'index.html')
        
        if os.path.exists(index_path):
            # 加载本地文件
            file_url = QUrl.fromLocalFile(os.path.abspath(index_path))
            self.web_view.setUrl(file_url)
            self.status_label.setText(f"加载本地文件: {index_path}")
        else:
            # 如果本地文件不存在，显示默认内容
            default_html = self.create_default_html()
            self.web_view.setHtml(default_html)
            self.status_label.setText("显示默认内容")
    
    def create_default_html(self):
        """
        创建默认HTML内容
        =================
        
        当本地HTML文件不存在时显示的默认内容。
        """
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PyQt5 WebView 示例</title>
            <style>
                body { 
                    font-family: 'Microsoft YaHei', sans-serif; 
                    margin: 40px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 10px;
                    backdrop-filter: blur(10px);
                }
                h1 { text-align: center; color: #fff; }
                .feature { 
                    background: rgba(255,255,255,0.2); 
                    padding: 20px; 
                    margin: 20px 0; 
                    border-radius: 8px;
                }
                button {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin: 5px;
                }
                button:hover { background: #45a049; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌟 PyQt5 WebView 示例应用</h1>
                
                <div class="feature">
                    <h3>📚 学习目标</h3>
                    <p>本示例展示了如何将Web技术与Python桌面应用程序相结合，重点讲解：</p>
                    <ul>
                        <li>PyQt5应用程序架构和生命周期</li>
                        <li>WebEngine的集成和配置</li>
                        <li>Python与JavaScript的双向通信</li>
                        <li>现代桌面应用开发模式</li>
                    </ul>
                </div>
                
                <div class="feature">
                    <h3>🔧 功能演示</h3>
                    <p>尝试以下功能来理解PyQt5和WebEngine的工作机制：</p>
                    <button onclick="testPythonCall()">调用Python函数</button>
                    <button onclick="showSystemInfo()">获取系统信息</button>
                    <button onclick="changeBackground()">改变背景</button>
                </div>
                
                <div class="feature">
                    <h3>💡 技术要点</h3>
                    <p>这个应用演示了现代桌面应用开发的重要概念，结合了传统桌面应用的稳定性和Web技术的灵活性。</p>
                </div>
            </div>
            
            <script>
                // JavaScript与Python通信示例
                function testPythonCall() {
                    console.log("尝试调用Python函数...");
                    alert("JavaScript运行正常！查看右侧调试面板了解Python交互。");
                }
                
                function showSystemInfo() {
                    const info = {
                        userAgent: navigator.userAgent,
                        language: navigator.language,
                        platform: navigator.platform,
                        cookieEnabled: navigator.cookieEnabled
                    };
                    alert("浏览器信息：\\n" + JSON.stringify(info, null, 2));
                }
                
                function changeBackground() {
                    const colors = [
                        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
                    ];
                    const randomColor = colors[Math.floor(Math.random() * colors.length)];
                    document.body.style.background = randomColor;
                }
                
                // 页面加载完成后的初始化
                document.addEventListener('DOMContentLoaded', function() {
                    console.log('PyQt5 WebView 示例页面加载完成');
                });
            </script>
        </body>
        </html>
        """
    
    # 槽函数 (Slot Functions)
    # =======================
    # 以下是响应信号的槽函数
    
    def on_load_finished(self, success):
        """
        页面加载完成时的处理函数
        
        参数:
            success (bool): 是否成功加载
        """
        if success:
            self.status_label.setText("页面加载完成")
            self.page_loaded.emit("页面加载成功")
        else:
            self.status_label.setText("页面加载失败")
    
    def on_url_changed(self, url):
        """
        URL变化时的处理函数
        
        参数:
            url (QUrl): 新的URL
        """
        self.url_input.setText(url.toString())
        self.url_changed.emit(url)
    
    def on_load_progress(self, progress):
        """
        加载进度变化时的处理函数
        
        参数:
            progress (int): 加载进度百分比 (0-100)
        """
        if progress < 100:
            self.progress_label.setText(f"加载中... {progress}%")
        else:
            self.progress_label.setText("")
    
    def on_page_loaded(self, message):
        """
        自定义页面加载信号的处理函数
        
        参数:
            message (str): 加载消息
        """
        print(f"页面加载事件: {message}")
    
    def on_custom_url_changed(self, url):
        """
        自定义URL变化信号的处理函数
        
        参数:
            url (QUrl): 变化的URL
        """
        print(f"URL变化事件: {url.toString()}")
    
    def load_url(self):
        """
        加载用户输入的URL
        ==================
        
        从地址栏获取URL并加载到WebView中。
        """
        url_text = self.url_input.text().strip()
        
        if not url_text:
            return
        
        # 处理不同类型的URL
        if url_text.startswith(('http://', 'https://')):
            # 网络URL
            url = QUrl(url_text)
        elif os.path.exists(url_text):
            # 本地文件路径
            url = QUrl.fromLocalFile(os.path.abspath(url_text))
        else:
            # 尝试作为搜索或补全HTTP前缀
            if '.' in url_text and not url_text.startswith('www.'):
                url = QUrl('http://' + url_text)
            else:
                url = QUrl('https://www.google.com/search?q=' + url_text)
        
        self.web_view.setUrl(url)
        self.status_label.setText(f"正在加载: {url.toString()}")
    
    def execute_javascript(self):
        """
        执行用户输入的JavaScript代码
        ==============================
        
        从输入框获取JavaScript代码并在WebView中执行。
        """
        js_code = self.js_input.toPlainText().strip()
        
        if not js_code:
            return
        
        # 在WebView中执行JavaScript
        # runJavaScript方法异步执行JavaScript代码
        self.web_view.page().runJavaScript(js_code, self.on_js_result)
        
        # 在Python输出区域显示执行的代码
        self.python_output.append(f"执行JavaScript: {js_code}")
    
    def on_js_result(self, result):
        """
        JavaScript执行结果回调函数
        ===========================
        
        参数:
            result: JavaScript执行的返回值
        """
        if result is not None:
            self.python_output.append(f"JavaScript返回结果: {result}")
        else:
            self.python_output.append("JavaScript执行完成（无返回值）")
    
    def toggle_fullscreen(self, checked):
        """
        切换全屏模式
        =============
        
        参数:
            checked (bool): 是否启用全屏
        """
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def closeEvent(self, event):
        """
        窗口关闭事件处理
        =================
        
        在窗口关闭前进行清理工作。
        这是QWidget的虚函数，当窗口即将关闭时被调用。
        
        参数:
            event (QCloseEvent): 关闭事件对象
        """
        print("应用程序正在关闭...")
        
        # 清理WebEngine资源
        if self.web_view:
            self.web_view.stop()
        
        # 接受关闭事件
        event.accept()