/**
 * PyQt5 WebView 示例应用 - JavaScript交互层
 * ============================================
 * 
 * 这个文件展示了如何在PyQt5 WebEngine中实现JavaScript与Python的双向通信。
 * 重点讲解QWebChannel的JavaScript端使用方法和最佳实践。
 * 
 * 技术要点：
 * - QWebChannel JavaScript API的使用
 * - 异步调用Python方法的模式
 * - 错误处理和用户体验优化
 * - 现代JavaScript ES6+特性的应用
 */

/**
 * 全局变量和状态管理
 * ===================
 */

// Python桥接对象，通过QWebChannel暴露
let bridge = null;

// 应用程序状态
const appState = {
    isChannelReady: false,
    logHistory: [],
    maxLogEntries: 100
};

/**
 * QWebChannel初始化
 * ==================
 * 
 * 这是PyQt5 WebEngine中JavaScript与Python通信的核心机制。
 * QWebChannel提供了异步、类型安全的通信方式。
 */

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    logMessage('info', 'DOM加载完成，开始初始化QWebChannel...');
    
    // 初始化QWebChannel
    // qt.webChannelTransport 是PyQt5自动注入的传输对象
    if (typeof qt !== 'undefined' && qt.webChannelTransport) {
        new QWebChannel(qt.webChannelTransport, function(channel) {
            // 获取Python注册的bridge对象
            bridge = channel.objects.bridge;
            
            if (bridge) {
                appState.isChannelReady = true;
                logMessage('success', 'QWebChannel初始化成功，Python桥接已建立');
                
                // 连接Python信号
                connectPythonSignals();
                
                // 隐藏加载指示器
                hideLoadingIndicator();
                
                // 执行初始化测试
                performInitialTests();
                
            } else {
                logMessage('error', '无法获取Python桥接对象');
                showError('Python桥接初始化失败');
            }
        });
    } else {
        logMessage('warning', 'QWebChannel传输对象不可用，可能不在PyQt5环境中运行');
        hideLoadingIndicator();
        showError('当前环境不支持QWebChannel，请在PyQt5 WebEngine中运行此页面');
    }
});

/**
 * Python信号连接
 * ================
 * 
 * 连接Python端发射的信号，实现Python到JavaScript的通信。
 */
function connectPythonSignals() {
    if (!bridge) return;
    
    try {
        // 连接消息信号
        if (bridge.message_to_js && bridge.message_to_js.connect) {
            bridge.message_to_js.connect(function(message) {
                logMessage('python', `来自Python的消息: ${message}`);
                showNotification(`Python消息: ${message}`, 'info');
            });
            logMessage('info', '已连接Python消息信号');
        }
        
        // 连接数据更新信号
        if (bridge.data_updated && bridge.data_updated.connect) {
            bridge.data_updated.connect(function(data) {
                logMessage('python', '数据已更新');
                console.log('Python数据更新:', data);
            });
            logMessage('info', '已连接Python数据更新信号');
        }
        
        // 连接系统事件信号
        if (bridge.system_event && bridge.system_event.connect) {
            bridge.system_event.connect(function(eventType, data) {
                logMessage('system', `系统事件: ${eventType} - ${data}`);
                showNotification(`系统事件: ${eventType}`, 'warning');
            });
            logMessage('info', '已连接Python系统事件信号');
        }
        
    } catch (error) {
        logMessage('error', `连接Python信号时出错: ${error.message}`);
    }
}

/**
 * 初始化测试
 * ============
 * 
 * 执行一系列测试以验证Python-JavaScript通信是否正常工作。
 */
function performInitialTests() {
    if (!bridge) return;
    
    logMessage('info', '开始执行初始化测试...');
    
    // 测试1: 获取Python版本
    bridge.get_python_version(function(version) {
        logMessage('test', `Python版本测试通过: ${version}`);
        document.getElementById('pythonInfo').textContent = version;
    });
    
    // 测试2: 测试回调功能
    setTimeout(() => {
        bridge.test_callback('初始化测试数据');
    }, 500);
    
    logMessage('success', '初始化测试完成');
}

/**
 * =============================
 * 系统信息获取功能
 * =============================
 */

/**
 * 获取系统信息
 */
function getSystemInfo() {
    if (!ensureChannelReady()) return;
    
    const infoElement = document.getElementById('systemInfo');
    infoElement.textContent = '正在获取系统信息...';
    
    bridge.get_system_info(function(result) {
        try {
            const systemInfo = JSON.parse(result);
            
            // 格式化显示系统信息
            let displayText = '';
            for (const [key, value] of Object.entries(systemInfo)) {
                displayText += `${key}: ${value}\n`;
            }
            
            infoElement.textContent = displayText;
            logMessage('info', '系统信息获取成功');
            
        } catch (error) {
            infoElement.textContent = `解析系统信息失败: ${error.message}`;
            logMessage('error', `解析系统信息失败: ${error.message}`);
        }
    });
}

/**
 * 获取Python版本信息
 */
function getPythonInfo() {
    if (!ensureChannelReady()) return;
    
    const infoElement = document.getElementById('pythonInfo');
    infoElement.textContent = '正在获取Python信息...';
    
    bridge.get_python_version(function(version) {
        infoElement.textContent = version;
        logMessage('info', `Python版本: ${version}`);
    });
}

/**
 * 获取调试信息
 */
function getDebugInfo() {
    if (!ensureChannelReady()) return;
    
    const infoElement = document.getElementById('debugInfo');
    infoElement.textContent = '正在获取调试信息...';
    
    bridge.get_debug_info(function(result) {
        try {
            const debugInfo = JSON.parse(result);
            infoElement.textContent = JSON.stringify(debugInfo, null, 2);
            logMessage('info', '调试信息获取成功');
        } catch (error) {
            infoElement.textContent = `解析调试信息失败: ${error.message}`;
            logMessage('error', `解析调试信息失败: ${error.message}`);
        }
    });
}

/**
 * =============================
 * 消息通信功能
 * =============================
 */

/**
 * 发送消息到Python
 */
function sendMessage() {
    if (!ensureChannelReady()) return;
    
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        showError('请输入要发送的消息');
        return;
    }
    
    bridge.log_message('info', `JavaScript发送消息: ${message}`);
    logMessage('send', `发送消息: ${message}`);
    
    // 清空输入框
    messageInput.value = '';
}

/**
 * 显示Python对话框
 */
function showAlert() {
    if (!ensureChannelReady()) return;
    
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim() || 'Hello from JavaScript!';
    
    bridge.show_message(message);
    logMessage('action', `显示对话框: ${message}`);
}

/**
 * =============================
 * 数据存储功能
 * =============================
 */

/**
 * 存储数据到Python
 */
function storeData() {
    if (!ensureChannelReady()) return;
    
    const key = document.getElementById('dataKey').value.trim();
    const value = document.getElementById('dataValue').value.trim();
    
    if (!key || !value) {
        showError('请输入数据键和值');
        return;
    }
    
    bridge.store_data(key, value);
    logMessage('data', `存储数据: ${key} = ${value}`);
    
    // 自动获取数据以验证存储
    setTimeout(() => getData(), 500);
}

/**
 * 从Python获取数据
 */
function getData() {
    if (!ensureChannelReady()) return;
    
    const key = document.getElementById('dataKey').value.trim();
    const resultElement = document.getElementById('dataResult');
    
    if (!key) {
        showError('请输入要获取的数据键');
        return;
    }
    
    resultElement.textContent = '正在获取数据...';
    
    bridge.get_data(key, function(result) {
        try {
            const data = JSON.parse(result);
            
            if (data.error) {
                resultElement.textContent = `错误: ${data.error}`;
                logMessage('error', data.error);
            } else {
                resultElement.textContent = JSON.stringify(data, null, 2);
                logMessage('data', `获取数据成功: ${key}`);
            }
        } catch (error) {
            resultElement.textContent = `解析数据失败: ${error.message}`;
            logMessage('error', `解析数据失败: ${error.message}`);
        }
    });
}

/**
 * 获取所有存储的数据
 */
function getAllData() {
    if (!ensureChannelReady()) return;
    
    const resultElement = document.getElementById('dataResult');
    resultElement.textContent = '正在获取所有数据...';
    
    bridge.get_all_data(function(result) {
        try {
            const allData = JSON.parse(result);
            resultElement.textContent = JSON.stringify(allData, null, 2);
            logMessage('data', '获取所有数据成功');
        } catch (error) {
            resultElement.textContent = `解析数据失败: ${error.message}`;
            logMessage('error', `解析数据失败: ${error.message}`);
        }
    });
}

/**
 * 清空所有数据
 */
function clearData() {
    if (!ensureChannelReady()) return;
    
    if (confirm('确定要清空所有存储的数据吗？')) {
        bridge.clear_data();
        document.getElementById('dataResult').textContent = '所有数据已清空';
        logMessage('data', '所有数据已清空');
    }
}

/**
 * =============================
 * 数学计算功能
 * =============================
 */

/**
 * 执行数学计算
 */
function calculate() {
    if (!ensureChannelReady()) return;
    
    const expression = document.getElementById('mathExpression').value.trim();
    const resultElement = document.getElementById('mathResult');
    
    if (!expression) {
        showError('请输入数学表达式');
        return;
    }
    
    resultElement.textContent = '正在计算...';
    
    bridge.calculate(expression, function(result) {
        try {
            const calcResult = JSON.parse(result);
            
            if (calcResult.success) {
                const displayText = `表达式: ${calcResult.expression}\n结果: ${calcResult.result}\n类型: ${calcResult.type}`;
                resultElement.textContent = displayText;
                logMessage('calc', `计算成功: ${calcResult.expression} = ${calcResult.result}`);
            } else {
                resultElement.textContent = `计算错误: ${calcResult.error}`;
                logMessage('error', `计算错误: ${calcResult.error}`);
            }
        } catch (error) {
            resultElement.textContent = `解析计算结果失败: ${error.message}`;
            logMessage('error', `解析计算结果失败: ${error.message}`);
        }
    });
}

/**
 * 插入数学示例公式
 */
function insertMathExample() {
    const examples = [
        '2 * 3 + sqrt(16)',
        'sin(pi/2) + cos(0)',
        'abs(-5) + round(3.7)',
        'max(1, 5, 3) + min(2, 8, 4)',
        'sqrt(25) * pi / 4'
    ];
    
    const randomExample = examples[Math.floor(Math.random() * examples.length)];
    document.getElementById('mathExpression').value = randomExample;
    logMessage('action', `插入示例公式: ${randomExample}`);
}

/**
 * =============================
 * 文件操作功能
 * =============================
 */

/**
 * 读取文件
 */
function readFile() {
    if (!ensureChannelReady()) return;
    
    const filePath = document.getElementById('filePath').value.trim();
    const resultElement = document.getElementById('fileResult');
    
    if (!filePath) {
        showError('请输入文件路径');
        return;
    }
    
    resultElement.textContent = '正在读取文件...';
    
    bridge.read_file(filePath, function(result) {
        try {
            const fileData = JSON.parse(result);
            
            if (fileData.success) {
                const displayText = `文件路径: ${fileData.file_path}\n文件大小: ${fileData.size}字符\n\n文件内容:\n${fileData.content}`;
                resultElement.textContent = displayText;
                logMessage('file', `文件读取成功: ${fileData.file_path}`);
            } else {
                resultElement.textContent = `读取文件失败: ${fileData.error}`;
                logMessage('error', `读取文件失败: ${fileData.error}`);
            }
        } catch (error) {
            resultElement.textContent = `解析文件数据失败: ${error.message}`;
            logMessage('error', `解析文件数据失败: ${error.message}`);
        }
    });
}

/**
 * 列出文件
 */
function listFiles() {
    if (!ensureChannelReady()) return;
    
    const resultElement = document.getElementById('fileResult');
    resultElement.textContent = '正在列出文件...';
    
    bridge.list_files(function(result) {
        try {
            const fileList = JSON.parse(result);
            
            if (fileList.success) {
                let displayText = `目录: ${fileList.directory}\n文件数量: ${fileList.count}\n\n文件列表:\n`;
                
                fileList.files.forEach(file => {
                    displayText += `- ${file.name} (${file.size}字节, 修改时间: ${file.modified})\n`;
                });
                
                resultElement.textContent = displayText;
                logMessage('file', `文件列表获取成功: ${fileList.count}个文件`);
            } else {
                resultElement.textContent = `获取文件列表失败: ${fileList.error}`;
                logMessage('error', `获取文件列表失败: ${fileList.error}`);
            }
        } catch (error) {
            resultElement.textContent = `解析文件列表失败: ${error.message}`;
            logMessage('error', `解析文件列表失败: ${error.message}`);
        }
    });
}

/**
 * =============================
 * JavaScript代码执行功能
 * =============================
 */

/**
 * 执行JavaScript代码
 */
function executeCode() {
    const code = document.getElementById('jsCode').value.trim();
    const resultElement = document.getElementById('codeResult');
    
    if (!code) {
        showError('请输入要执行的JavaScript代码');
        return;
    }
    
    try {
        logMessage('code', '开始执行JavaScript代码');
        
        // 创建一个安全的执行环境
        const result = eval(code);
        
        resultElement.textContent = `执行成功\n返回值: ${result !== undefined ? result : '(无返回值)'}`;
        logMessage('code', 'JavaScript代码执行成功');
        
    } catch (error) {
        resultElement.textContent = `执行错误: ${error.message}`;
        logMessage('error', `JavaScript执行错误: ${error.message}`);
    }
}

/**
 * 清空代码输入
 */
function clearCode() {
    document.getElementById('jsCode').value = '';
    document.getElementById('codeResult').textContent = '';
    logMessage('action', '代码输入已清空');
}

/**
 * 加载示例代码
 */
function loadExample() {
    const exampleCode = `// 测试Python-JavaScript通信示例
// ===================================

// 1. 获取系统信息
bridge.get_system_info(function(result) {
    const info = JSON.parse(result);
    console.log('系统信息:', info);
    bridge.log_message('info', '获取系统信息成功');
});

// 2. 存储和获取数据
bridge.store_data('测试键', '测试值');
bridge.get_data('测试键', function(result) {
    const data = JSON.parse(result);
    console.log('存储的数据:', data);
});

// 3. 数学计算
bridge.calculate('sqrt(16) + 2 * 3', function(result) {
    const calcResult = JSON.parse(result);
    if (calcResult.success) {
        console.log('计算结果:', calcResult.result);
    }
});

// 4. 测试回显功能
bridge.echo_message('Hello from JavaScript!', function(response) {
    console.log('回显响应:', response);
});

console.log('示例代码执行完成');`;

    document.getElementById('jsCode').value = exampleCode;
    logMessage('action', '示例代码已加载');
}

/**
 * =============================
 * 应用控制功能
 * =============================
 */

/**
 * 设置窗口标题
 */
function setWindowTitle() {
    if (!ensureChannelReady()) return;
    
    const title = document.getElementById('windowTitle').value.trim();
    
    if (!title) {
        showError('请输入新的窗口标题');
        return;
    }
    
    bridge.set_window_title(title);
    logMessage('control', `窗口标题已设置为: ${title}`);
}

/**
 * 测试回调功能
 */
function testCallback() {
    if (!ensureChannelReady()) return;
    
    const testData = `测试数据_${new Date().getTime()}`;
    bridge.test_callback(testData);
    logMessage('test', `发送测试回调数据: ${testData}`);
}

/**
 * 退出应用程序
 */
function quitApp() {
    if (!ensureChannelReady()) return;
    
    if (confirm('确定要退出应用程序吗？')) {
        bridge.quit_application();
        logMessage('control', '应用程序退出指令已发送');
    }
}

/**
 * =============================
 * 日志和用户界面辅助功能
 * =============================
 */

/**
 * 记录日志消息
 * 
 * @param {string} type - 日志类型 (info, error, success, warning, etc.)
 * @param {string} message - 日志消息
 */
function logMessage(type, message) {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] [${type.toUpperCase()}] ${message}`;
    
    // 添加到日志历史
    appState.logHistory.push(logEntry);
    
    // 限制日志条数
    if (appState.logHistory.length > appState.maxLogEntries) {
        appState.logHistory.shift();
    }
    
    // 更新日志显示
    updateLogDisplay();
    
    // 同时输出到浏览器控制台
    console.log(logEntry);
}

/**
 * 更新日志显示
 */
function updateLogDisplay() {
    const logOutput = document.getElementById('logOutput');
    if (logOutput) {
        logOutput.textContent = appState.logHistory.join('\n');
        // 自动滚动到底部
        logOutput.scrollTop = logOutput.scrollHeight;
    }
}

/**
 * 清空日志
 */
function clearLog() {
    appState.logHistory = [];
    updateLogDisplay();
    logMessage('action', '日志已清空');
}

/**
 * 显示错误消息
 * 
 * @param {string} message - 错误消息
 */
function showError(message) {
    logMessage('error', message);
    alert(`错误: ${message}`);
}

/**
 * 显示通知
 * 
 * @param {string} message - 通知消息
 * @param {string} type - 通知类型
 */
function showNotification(message, type = 'info') {
    logMessage(type, message);
    
    // 创建临时通知元素
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#e74c3c' : type === 'warning' ? '#f39c12' : '#3498db'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        max-width: 300px;
        word-wrap: break-word;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, 3000);
}

/**
 * 确保通信通道已准备就绪
 * 
 * @returns {boolean} 通道是否准备就绪
 */
function ensureChannelReady() {
    if (!appState.isChannelReady || !bridge) {
        showError('Python-JavaScript通信通道未准备就绪，请等待初始化完成');
        return false;
    }
    return true;
}

/**
 * 隐藏加载指示器
 */
function hideLoadingIndicator() {
    const indicator = document.getElementById('loadingIndicator');
    if (indicator) {
        indicator.classList.add('hidden');
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        }, 500);
    }
}

/**
 * =============================
 * CSS动画定义 (通过JavaScript添加)
 * =============================
 */

// 添加动画样式到页面
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

/**
 * =============================
 * 页面卸载处理
 * =============================
 */

// 页面卸载时的清理工作
window.addEventListener('beforeunload', function(event) {
    if (bridge && appState.isChannelReady) {
        // 这里可以执行一些清理工作
        logMessage('info', '页面即将卸载，执行清理操作');
    }
});

/**
 * =============================
 * 键盘快捷键支持
 * =============================
 */

document.addEventListener('keydown', function(event) {
    // Ctrl+Enter 执行代码
    if (event.ctrlKey && event.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.id === 'jsCode') {
            event.preventDefault();
            executeCode();
        }
    }
    
    // F12 切换调试信息
    if (event.key === 'F12') {
        event.preventDefault();
        getDebugInfo();
    }
});

/**
 * =============================
 * 开发者工具和调试辅助
 * =============================
 */

// 将主要对象暴露到全局作用域，便于调试
window.pyqtApp = {
    bridge,
    appState,
    logMessage,
    ensureChannelReady,
    version: '1.0.0'
};

// 初始化完成日志
logMessage('info', 'JavaScript应用初始化完成，等待QWebChannel连接...');