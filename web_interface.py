#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python与JavaScript交互接口
============================

这个文件展示了如何在PyQt5 WebEngine中实现Python和JavaScript的双向通信。
重点讲解QWebChannel的使用和PyQt5的对象暴露机制。

核心概念：
- QWebChannel: PyQt5提供的Web通信通道
- pyqtSlot: 将Python方法暴露给JavaScript的装饰器
- 对象序列化和反序列化
- 异步通信模式
"""

import json
import platform
import sys
import os
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QWebChannel
from PyQt5.QtWidgets import QMessageBox

class WebInterface(QObject):
    """
    Python与JavaScript交互接口类
    ===============================
    
    这个类通过QWebChannel暴露Python方法给JavaScript调用。
    QWebChannel是PyQt5提供的强大机制，允许：
    
    1. JavaScript调用Python方法
    2. Python向JavaScript发送数据
    3. 双向异步通信
    4. 类型自动转换
    
    工作原理：
    - 使用pyqtSlot装饰器标记可被JavaScript调用的方法
    - QWebChannel自动处理数据序列化/反序列化
    - 支持Python基本类型、列表、字典等的自动转换
    """
    
    # 定义信号用于向JavaScript发送数据
    # ==================================
    # 这些信号可以被JavaScript监听，实现Python主动向前端发送消息
    message_to_js = pyqtSignal(str)          # 发送消息到JavaScript
    data_updated = pyqtSignal('QVariant')    # 发送数据更新
    system_event = pyqtSignal(str, str)      # 发送系统事件
    
    def __init__(self, parent=None):
        """
        构造函数
        =========
        
        初始化Web接口，设置通信通道。
        
        参数:
            parent: 父对象，通常是主窗口
        """
        super().__init__(parent)
        
        # 保存父窗口引用
        self.parent_window = parent
        
        # 创建Web通道
        # ============
        # QWebChannel是实现Python-JavaScript通信的核心组件
        self.channel = QWebChannel()
        
        # 将当前对象注册到通道
        # 注册名称"bridge"，JavaScript可以通过这个名称访问Python对象
        self.channel.registerObject("bridge", self)
        
        # 初始化数据存储
        self.user_data = {}
        self.system_info = self.get_system_info()
        
        print("Python-JavaScript接口初始化完成")
    
    # ========================
    # 系统信息相关方法
    # ========================
    
    @pyqtSlot(result=str)
    def get_system_info(self):
        """
        获取系统信息
        =============
        
        返回当前系统的详细信息，包括操作系统、Python版本等。
        这个方法展示了如何将复杂的Python数据结构传递给JavaScript。
        
        装饰器说明：
        - @pyqtSlot: 标记此方法可被JavaScript调用
        - result=str: 指定返回值类型为字符串
        
        返回:
            str: JSON格式的系统信息
        """
        info = {
            "操作系统": platform.system(),
            "系统版本": platform.version(),
            "处理器架构": platform.machine(),
            "处理器类型": platform.processor(),
            "Python版本": sys.version,
            "PyQt5版本": "5.x",  # 可以通过PyQt5.QtCore.PYQT_VERSION_STR获取
            "当前时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "工作目录": os.getcwd(),
            "环境变量数量": len(os.environ),
            "可用编码": sys.getdefaultencoding()
        }
        
        # 将字典转换为JSON字符串
        # JavaScript可以使用JSON.parse()解析
        return json.dumps(info, ensure_ascii=False, indent=2)
    
    @pyqtSlot(result=str)
    def get_python_version(self):
        """
        获取Python版本信息
        ===================
        
        简单的示例方法，展示最基本的Python-JavaScript交互。
        
        返回:
            str: Python版本字符串
        """
        return f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # ========================
    # 消息和通信方法
    # ========================
    
    @pyqtSlot(str)
    def show_message(self, message):
        """
        显示消息对话框
        ===============
        
        JavaScript可以调用此方法显示桌面消息对话框。
        这展示了JavaScript如何调用系统级功能。
        
        参数:
            message (str): 要显示的消息内容
        """
        print(f"JavaScript请求显示消息: {message}")
        
        # 创建消息对话框
        msg_box = QMessageBox(self.parent_window)
        msg_box.setWindowTitle("来自JavaScript的消息")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
        
        # 将消息记录到父窗口的Python输出区域
        if hasattr(self.parent_window, 'python_output'):
            self.parent_window.python_output.append(f"[消息对话框] {message}")
    
    @pyqtSlot(str, str)
    def log_message(self, level, message):
        """
        记录日志消息
        =============
        
        JavaScript可以调用此方法将消息记录到Python端。
        展示了多参数方法的调用。
        
        参数:
            level (str): 日志级别 (info, warning, error)
            message (str): 日志消息
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        
        print(log_entry)
        
        # 记录到父窗口的输出区域
        if hasattr(self.parent_window, 'python_output'):
            self.parent_window.python_output.append(log_entry)
    
    @pyqtSlot(str, result=str)
    def echo_message(self, message):
        """
        回显消息
        =========
        
        简单的回显功能，JavaScript发送消息，Python处理后返回。
        展示了同步调用和返回值处理。
        
        参数:
            message (str): 输入消息
            
        返回:
            str: 处理后的消息
        """
        processed_message = f"Python处理结果: '{message}' (长度: {len(message)}字符)"
        
        # 记录交互
        if hasattr(self.parent_window, 'python_output'):
            self.parent_window.python_output.append(f"[回显] 输入: {message}")
            self.parent_window.python_output.append(f"[回显] 输出: {processed_message}")
        
        return processed_message
    
    # ========================
    # 数据存储和管理方法
    # ========================
    
    @pyqtSlot(str, str)
    def store_data(self, key, value):
        """
        存储数据
        =========
        
        JavaScript可以调用此方法在Python端存储数据。
        展示了Python作为数据后端的使用模式。
        
        参数:
            key (str): 数据键
            value (str): 数据值
        """
        self.user_data[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat(),
            'type': type(value).__name__
        }
        
        # 发出数据更新信号
        self.data_updated.emit(self.user_data)
        
        # 记录操作
        if hasattr(self.parent_window, 'python_output'):
            self.parent_window.python_output.append(f"[数据存储] {key} = {value}")
        
        print(f"数据已存储: {key} = {value}")
    
    @pyqtSlot(str, result=str)
    def get_data(self, key):
        """
        获取存储的数据
        ===============
        
        JavaScript可以调用此方法从Python端获取数据。
        
        参数:
            key (str): 数据键
            
        返回:
            str: JSON格式的数据，如果不存在则返回错误信息
        """
        if key in self.user_data:
            data = self.user_data[key]
            return json.dumps(data, ensure_ascii=False)
        else:
            error_info = {"error": f"数据键 '{key}' 不存在"}
            return json.dumps(error_info, ensure_ascii=False)
    
    @pyqtSlot(result=str)
    def get_all_data(self):
        """
        获取所有存储的数据
        ===================
        
        返回Python端存储的所有数据。
        
        返回:
            str: JSON格式的所有数据
        """
        return json.dumps(self.user_data, ensure_ascii=False, indent=2)
    
    @pyqtSlot()
    def clear_data(self):
        """
        清空所有数据
        =============
        
        清空Python端存储的所有用户数据。
        """
        self.user_data.clear()
        
        # 发出数据更新信号
        self.data_updated.emit(self.user_data)
        
        # 记录操作
        if hasattr(self.parent_window, 'python_output'):
            self.parent_window.python_output.append("[数据管理] 所有数据已清空")
        
        print("所有用户数据已清空")
    
    # ========================
    # 文件操作方法
    # ========================
    
    @pyqtSlot(str, result=str)
    def read_file(self, file_path):
        """
        读取文件内容
        =============
        
        JavaScript可以调用此方法读取本地文件。
        出于安全考虑，实际应用中应该限制可访问的文件路径。
        
        参数:
            file_path (str): 文件路径
            
        返回:
            str: 文件内容或错误信息
        """
        try:
            # 安全检查：限制只能读取应用程序目录下的文件
            app_dir = os.path.dirname(os.path.abspath(__file__))
            abs_path = os.path.abspath(file_path)
            
            if not abs_path.startswith(app_dir):
                return json.dumps({"error": "安全限制：只能访问应用程序目录下的文件"}, ensure_ascii=False)
            
            if not os.path.exists(abs_path):
                return json.dumps({"error": f"文件不存在: {file_path}"}, ensure_ascii=False)
            
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = {
                "success": True,
                "file_path": file_path,
                "content": content,
                "size": len(content)
            }
            
            # 记录操作
            if hasattr(self.parent_window, 'python_output'):
                self.parent_window.python_output.append(f"[文件读取] {file_path} ({len(content)}字符)")
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
            return json.dumps(error_result, ensure_ascii=False)
    
    @pyqtSlot(result=str)
    def list_files(self):
        """
        列出应用程序目录下的文件
        =========================
        
        JavaScript可以调用此方法获取可用文件列表。
        
        返回:
            str: JSON格式的文件列表
        """
        try:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            files = []
            
            for item in os.listdir(app_dir):
                item_path = os.path.join(app_dir, item)
                if os.path.isfile(item_path):
                    files.append({
                        "name": item,
                        "path": item_path,
                        "size": os.path.getsize(item_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                    })
            
            result = {
                "success": True,
                "directory": app_dir,
                "files": files,
                "count": len(files)
            }
            
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e)
            }
            return json.dumps(error_result, ensure_ascii=False)
    
    # ========================
    # 计算和处理方法
    # ========================
    
    @pyqtSlot(str, result=str)
    def calculate(self, expression):
        """
        计算数学表达式
        ===============
        
        JavaScript可以调用此方法进行数学计算。
        展示了Python作为计算后端的能力。
        
        参数:
            expression (str): 数学表达式
            
        返回:
            str: JSON格式的计算结果
        """
        try:
            # 安全的表达式计算（限制可用函数）
            allowed_names = {
                k: v for k, v in __builtins__.items()
                if k in ['abs', 'round', 'min', 'max', 'sum', 'len']
            }
            allowed_names.update({
                'sin': __import__('math').sin,
                'cos': __import__('math').cos,
                'tan': __import__('math').tan,
                'sqrt': __import__('math').sqrt,
                'pi': __import__('math').pi,
                'e': __import__('math').e
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            response = {
                "success": True,
                "expression": expression,
                "result": result,
                "type": type(result).__name__
            }
            
            # 记录计算
            if hasattr(self.parent_window, 'python_output'):
                self.parent_window.python_output.append(f"[计算] {expression} = {result}")
            
            return json.dumps(response, ensure_ascii=False)
            
        except Exception as e:
            error_response = {
                "success": False,
                "expression": expression,
                "error": str(e)
            }
            return json.dumps(error_response, ensure_ascii=False)
    
    # ========================
    # 异步通信方法
    # ========================
    
    def send_message_to_js(self, message):
        """
        向JavaScript发送消息
        =====================
        
        Python主动向JavaScript发送消息的示例。
        这展示了Python到JavaScript的单向通信。
        
        参数:
            message (str): 要发送的消息
        """
        self.message_to_js.emit(message)
    
    def send_system_event(self, event_type, data):
        """
        发送系统事件
        =============
        
        向JavaScript发送系统级事件通知。
        
        参数:
            event_type (str): 事件类型
            data (str): 事件数据
        """
        self.system_event.emit(event_type, data)
    
    # ========================
    # 应用程序控制方法
    # ========================
    
    @pyqtSlot()
    def quit_application(self):
        """
        退出应用程序
        =============
        
        JavaScript可以调用此方法关闭整个应用程序。
        展示了Web前端对桌面应用的控制能力。
        """
        print("JavaScript请求退出应用程序")
        
        if hasattr(self.parent_window, 'python_output'):
            self.parent_window.python_output.append("[应用控制] 准备退出应用程序")
        
        # 延迟执行退出，给用户界面时间更新
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, self.parent_window.close)
    
    @pyqtSlot(str)
    def set_window_title(self, title):
        """
        设置窗口标题
        =============
        
        JavaScript可以调用此方法动态修改窗口标题。
        
        参数:
            title (str): 新的窗口标题
        """
        if self.parent_window:
            self.parent_window.setWindowTitle(title)
            
            if hasattr(self.parent_window, 'python_output'):
                self.parent_window.python_output.append(f"[窗口控制] 标题已更改为: {title}")
    
    # ========================
    # 调试和诊断方法
    # ========================
    
    @pyqtSlot(result=str)
    def get_debug_info(self):
        """
        获取调试信息
        =============
        
        返回当前应用程序状态的详细调试信息。
        
        返回:
            str: JSON格式的调试信息
        """
        debug_info = {
            "Python解释器": {
                "版本": sys.version,
                "可执行文件": sys.executable,
                "模块搜索路径": sys.path[:3],  # 只显示前3个路径
                "编码": sys.getdefaultencoding()
            },
            "应用程序状态": {
                "当前时间": datetime.now().isoformat(),
                "工作目录": os.getcwd(),
                "存储数据数量": len(self.user_data),
                "父窗口存在": self.parent_window is not None
            },
            "Web通道": {
                "已注册对象": ["bridge"],
                "通道状态": "活跃"
            }
        }
        
        return json.dumps(debug_info, ensure_ascii=False, indent=2)
    
    @pyqtSlot(str)
    def test_callback(self, data):
        """
        测试回调函数
        =============
        
        用于测试JavaScript到Python的通信是否正常工作。
        
        参数:
            data (str): 测试数据
        """
        print(f"收到JavaScript测试数据: {data}")
        
        if hasattr(self.parent_window, 'python_output'):
            self.parent_window.python_output.append(f"[测试回调] 收到数据: {data}")
        
        # 发送回应信号
        self.message_to_js.emit(f"Python已收到测试数据: {data}")

# ========================
# 使用说明和示例
# ========================

"""
JavaScript端使用示例：

1. 基本调用：
   window.bridge.show_message("Hello from JavaScript!");

2. 获取系统信息：
   window.bridge.get_system_info(function(result) {
       console.log("系统信息:", JSON.parse(result));
   });

3. 数据存储：
   window.bridge.store_data("username", "张三");
   window.bridge.get_data("username", function(result) {
       console.log("用户数据:", JSON.parse(result));
   });

4. 文件操作：
   window.bridge.read_file("static/example.txt", function(result) {
       var data = JSON.parse(result);
       if (data.success) {
           console.log("文件内容:", data.content);
       } else {
           console.error("读取失败:", data.error);
       }
   });

5. 数学计算：
   window.bridge.calculate("2 * 3 + sqrt(16)", function(result) {
       var data = JSON.parse(result);
       console.log("计算结果:", data.result);
   });

6. 监听Python信号：
   window.bridge.message_to_js.connect(function(message) {
       console.log("来自Python的消息:", message);
   });

注意事项：
- 所有异步调用都需要提供回调函数
- 复杂数据通过JSON字符串传递
- 确保在QWebChannel初始化完成后再调用Python方法
"""