#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 WebView 高级示例
Advanced example of PyQt5 WebView with Python-JavaScript communication
"""

import sys
import os
import json
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QMenuBar, QAction, QMessageBox, QFileDialog,
                           QStatusBar, QToolBar, QPushButton, QLineEdit, QLabel)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QFont


class PythonBridge(QObject):
    """Python与JavaScript通信的桥梁类"""
    
    # 定义信号，用于从Python向JavaScript发送数据
    dataChanged = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_database()
        
    def init_database(self):
        """初始化SQLite数据库"""
        self.db_path = os.path.join(os.path.dirname(__file__), 'app_data.db')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    @pyqtSlot(str, result=str)
    def get_system_info(self, request_type):
        """获取系统信息"""
        try:
            if request_type == "basic":
                info = {
                    "python_version": sys.version,
                    "platform": sys.platform,
                    "current_time": datetime.now().isoformat(),
                    "working_directory": os.getcwd()
                }
            elif request_type == "database":
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM user_data")
                user_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM logs")
                log_count = cursor.fetchone()[0]
                conn.close()
                
                info = {
                    "database_path": self.db_path,
                    "user_records": user_count,
                    "log_records": log_count,
                    "database_size": os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                }
            else:
                info = {"error": "Unknown request type"}
                
            return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @pyqtSlot(str, str, result=str)
    def save_data(self, name, value):
        """保存数据到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_data (name, value) VALUES (?, ?)", (name, value))
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            # 记录日志
            self.log_action("INFO", f"Data saved: {name} = {value}")
            
            return json.dumps({"success": True, "id": record_id}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)
    
    @pyqtSlot(result=str)
    def get_all_data(self):
        """获取所有保存的数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, value, timestamp FROM user_data ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            conn.close()
            
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "name": row[1],
                    "value": row[2],
                    "timestamp": row[3]
                })
            
            return json.dumps(data, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @pyqtSlot(int, result=str)
    def delete_data(self, record_id):
        """删除指定的数据记录"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_data WHERE id = ?", (record_id,))
            affected_rows = cursor.rowcount
            conn.commit()
            conn.close()
            
            if affected_rows > 0:
                self.log_action("INFO", f"Data deleted: ID {record_id}")
                return json.dumps({"success": True}, ensure_ascii=False)
            else:
                return json.dumps({"success": False, "error": "Record not found"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)
    
    @pyqtSlot(str)
    def log_action(self, level, message):
        """记录操作日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (level, message) VALUES (?, ?)", (level, message))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to log action: {e}")
    
    @pyqtSlot(str)
    def show_notification(self, message):
        """显示桌面通知"""
        QMessageBox.information(None, "来自网页的消息", message)
    
    @pyqtSlot(result=str)
    def select_file(self):
        """打开文件选择对话框"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                None, "选择文件", "", "所有文件 (*);;文本文件 (*.txt);;图片文件 (*.png *.jpg *.jpeg)")
            
            if file_path:
                file_info = {
                    "path": file_path,
                    "name": os.path.basename(file_path),
                    "size": os.path.getsize(file_path),
                    "exists": os.path.exists(file_path)
                }
                return json.dumps(file_info, ensure_ascii=False)
            else:
                return json.dumps({"cancelled": True}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)


class AdvancedWebView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bridge = PythonBridge()
        self.init_ui()
        self.setup_web_channel()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('PyQt5 WebView 高级示例 - Python与JavaScript交互')
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建工具栏
        self.create_toolbar(main_layout)
        
        # 创建WebEngineView
        self.browser = QWebEngineView()
        main_layout.addWidget(self.browser)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 加载高级页面
        self.load_advanced_page()
        
    def create_toolbar(self, layout):
        """创建工具栏"""
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar_widget.setLayout(toolbar_layout)
        
        # URL输入框
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入URL或文件路径...")
        self.url_input.returnPressed.connect(self.load_url)
        toolbar_layout.addWidget(QLabel("地址:"))
        toolbar_layout.addWidget(self.url_input)
        
        # 导航按钮
        back_btn = QPushButton("后退")
        back_btn.clicked.connect(self.browser.back)
        toolbar_layout.addWidget(back_btn)
        
        forward_btn = QPushButton("前进")
        forward_btn.clicked.connect(self.browser.forward)
        toolbar_layout.addWidget(forward_btn)
        
        reload_btn = QPushButton("刷新")
        reload_btn.clicked.connect(self.browser.reload)
        toolbar_layout.addWidget(reload_btn)
        
        home_btn = QPushButton("主页")
        home_btn.clicked.connect(self.load_advanced_page)
        toolbar_layout.addWidget(home_btn)
        
        layout.addWidget(toolbar_widget)
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 加载本地文件
        load_file_action = QAction('加载本地HTML文件', self)
        load_file_action.triggered.connect(self.load_local_file)
        file_menu.addAction(load_file_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 开发菜单
        dev_menu = menubar.addMenu('开发')
        
        # 开发者工具
        dev_tools_action = QAction('开发者工具', self)
        dev_tools_action.triggered.connect(self.open_dev_tools)
        dev_menu.addAction(dev_tools_action)
        
        # 清除数据
        clear_data_action = QAction('清除应用数据', self)
        clear_data_action.triggered.connect(self.clear_app_data)
        dev_menu.addAction(clear_data_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        # 关于
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪 - 高级WebView示例已加载")
        
        # 连接页面加载信号
        self.browser.loadStarted.connect(lambda: self.status_bar.showMessage("正在加载..."))
        self.browser.loadFinished.connect(lambda ok: self.status_bar.showMessage("加载完成" if ok else "加载失败"))
        
    def setup_web_channel(self):
        """设置Web通道以便Python与JavaScript通信"""
        self.channel = QWebChannel()
        self.channel.registerObject('pythonBridge', self.bridge)
        self.browser.page().setWebChannel(self.channel)
        
    def load_advanced_page(self):
        """加载高级示例页面"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, 'advanced_content.html')
        
        if os.path.exists(html_path):
            self.browser.setUrl(QUrl.fromLocalFile(html_path))
            self.url_input.setText(html_path)
        else:
            # 创建一个简单的高级示例页面
            self.create_advanced_html()
            self.load_advanced_page()
    
    def create_advanced_html(self):
        """如果高级HTML文件不存在，则创建一个"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, 'advanced_content.html')
        
        # 这里会在后续创建advanced_content.html文件
        pass
        
    def load_url(self):
        """加载用户输入的URL"""
        url_text = self.url_input.text().strip()
        if url_text:
            if url_text.startswith('http://') or url_text.startswith('https://'):
                self.browser.setUrl(QUrl(url_text))
            elif os.path.exists(url_text):
                self.browser.setUrl(QUrl.fromLocalFile(url_text))
            else:
                self.status_bar.showMessage("无效的URL或文件路径")
                
    def load_local_file(self):
        """加载本地HTML文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择HTML文件", "", "HTML文件 (*.html *.htm);;所有文件 (*)")
        
        if file_path:
            self.browser.setUrl(QUrl.fromLocalFile(file_path))
            self.url_input.setText(file_path)
            
    def open_dev_tools(self):
        """打开开发者工具"""
        # 注意：这需要在编译时启用开发者工具支持
        try:
            page = self.browser.page()
            page.setDevToolsPage(page)
        except:
            QMessageBox.information(self, "提示", "开发者工具在此版本中不可用")
            
    def clear_app_data(self):
        """清除应用数据"""
        reply = QMessageBox.question(self, "确认", "确定要清除所有应用数据吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                db_path = self.bridge.db_path
                if os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM user_data")
                    cursor.execute("DELETE FROM logs")
                    conn.commit()
                    conn.close()
                    
                QMessageBox.information(self, "成功", "应用数据已清除")
                self.browser.reload()  # 重新加载页面以更新显示
            except Exception as e:
                QMessageBox.critical(self, "错误", f"清除数据失败: {str(e)}")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, '关于', 
                         'PyQt5 WebView 高级示例\n\n'
                         '功能特色：\n'
                         '• Python与JavaScript双向通信\n'
                         '• SQLite数据库集成\n'
                         '• 文件操作和对话框\n'
                         '• 桌面通知功能\n'
                         '• 完整的工具栏和菜单\n\n'
                         '版本: 2.0')


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName('PyQt5 WebView 高级示例')
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    
    # 创建主窗口
    window = AdvancedWebView()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()