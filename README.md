# PyQt5 WebView 桌面应用程序示例

一个完整的示例项目，展示如何使用 PyQt5 的 WebView 组件与 PyQt 本身结合开发现代桌面应用程序。

## 🌟 项目特色

- **基础示例**: 简单易懂的 WebView 集成演示
- **高级示例**: Python 与 JavaScript 双向通信
- **数据库集成**: SQLite 数据持久化存储
- **文件操作**: 系统文件对话框集成
- **桌面通知**: 原生消息框通知功能
- **现代界面**: 响应式设计和动画效果

## 📋 功能概览

### 基础功能 (main.py)
- ✅ PyQt5 WebView 基本集成
- ✅ 菜单栏和状态栏
- ✅ HTML/CSS/JavaScript 支持
- ✅ 响应式界面设计
- ✅ 基本交互演示

### 高级功能 (advanced.py)
- ✅ Python-JavaScript 双向通信
- ✅ SQLite 数据库操作
- ✅ 文件选择对话框
- ✅ 桌面通知功能
- ✅ 多标签页界面
- ✅ 实时数据管理
- ✅ 工具栏和导航功能

## 🚀 快速开始

### 环境要求

- Python 3.6+
- PyQt5 5.15.0+
- PyQtWebEngine 5.15.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行示例

#### 基础示例
```bash
python main.py
```

#### 高级示例
```bash
python advanced.py
```

## 📁 项目结构

```
pyqtwebview/
├── main.py                 # 基础 WebView 示例
├── advanced.py             # 高级功能示例
├── basic_content.html      # 基础示例的 HTML 内容
├── advanced_content.html   # 高级示例的 HTML 内容
├── requirements.txt        # 项目依赖
├── README.md              # 项目文档
└── app_data.db            # SQLite 数据库文件 (运行时创建)
```

## 🎯 学习目标

通过本项目，您将学会：

1. **PyQt5 基础集成**
   - WebEngineView 组件的使用
   - 菜单栏和工具栏的创建
   - 窗口管理和布局设计

2. **Web 技术整合**
   - HTML5 现代特性的利用
   - CSS3 动画和样式设计
   - JavaScript 交互逻辑

3. **Python-JavaScript 通信**
   - QWebChannel 的配置和使用
   - 数据的双向传递
   - 异步调用处理

4. **数据库操作**
   - SQLite 的集成使用
   - 数据的增删改查
   - 数据表结构设计

5. **系统集成功能**
   - 文件对话框的调用
   - 桌面通知的实现
   - 系统信息的获取

## 🔧 核心技术

### WebChannel 通信机制

```python
# Python 端
class PythonBridge(QObject):
    @pyqtSlot(str, result=str)
    def get_data(self, request):
        # 处理来自 JavaScript 的请求
        return json.dumps(response_data)

# JavaScript 端
pythonBridge.get_data(request, function(result) {
    const data = JSON.parse(result);
    // 处理返回的数据
});
```

### 数据库操作

```python
# 数据保存
def save_data(self, name, value):
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (name, value) VALUES (?, ?)", 
                   (name, value))
    conn.commit()
    conn.close()
```

### 文件操作集成

```python
@pyqtSlot(result=str)
def select_file(self):
    file_path, _ = QFileDialog.getOpenFileName(
        None, "选择文件", "", "所有文件 (*)")
    return json.dumps({"path": file_path})
```

## 📖 使用指南

### 基础示例使用

1. 运行 `main.py` 启动基础示例
2. 通过菜单栏体验基本功能
3. 查看 HTML 内容的动画效果
4. 尝试不同的交互按钮

### 高级示例使用

1. 运行 `advanced.py` 启动高级示例
2. 使用标签页切换不同功能模块
3. 测试 Python-JavaScript 通信功能
4. 体验数据库的增删改查操作
5. 尝试文件选择和桌面通知功能

## 🎨 界面特色

- **现代设计**: 渐变背景、毛玻璃效果
- **响应式布局**: 适配不同窗口大小
- **动画效果**: 平滑的过渡和加载动画
- **交互反馈**: 按钮悬停和点击效果
- **信息展示**: 清晰的数据表格和状态显示

## 🛠️ 自定义开发

### 添加新的 Python 函数

1. 在 `PythonBridge` 类中添加新方法
2. 使用 `@pyqtSlot` 装饰器标记
3. 在 JavaScript 中调用新函数

### 扩展 HTML 界面

1. 修改对应的 HTML 文件
2. 添加新的 CSS 样式
3. 实现 JavaScript 交互逻辑

### 数据库结构扩展

1. 在 `init_database` 方法中添加新表
2. 实现对应的数据操作方法
3. 更新前端界面以支持新功能

## 🐛 常见问题

### Q: 程序启动时提示 PyQt5 未安装
**A**: 请使用 `pip install PyQt5 PyQtWebEngine` 安装必要的依赖包。

### Q: WebView 无法显示内容
**A**: 确保 HTML 文件存在且路径正确，检查控制台是否有错误信息。

### Q: Python-JavaScript 通信失败
**A**: 确认 QWebChannel 正确初始化，检查 `qwebchannel.js` 是否正确加载。

### Q: 数据库操作出错
**A**: 检查数据库文件权限，确保应用有读写权限。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📜 许可证

本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。

## 🙏 致谢

感谢 PyQt5 和 Qt 团队提供的优秀框架，让桌面应用开发变得如此简单高效。

---

**开始您的 PyQt5 WebView 开发之旅吧！** 🎉
