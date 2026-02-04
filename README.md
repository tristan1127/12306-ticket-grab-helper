# 🚄 12306 智能抢票助手

一个基于 Python + Selenium 的 12306 自动抢票脚本，支持定时抢票、座位选择、多乘车人管理等功能。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## ✨ 功能特性

- 🎯 **精准定时抢票** - 支持设置北京时间定时开抢，秒级精度
- 💺 **智能座位分配** - 支持多种座位类型及座位位置选择（ABCDF座）
- 👥 **多乘车人管理** - 支持同时为多人抢票，自动分配座位
- 🔄 **自动重试机制** - 自动刷新票务状态，提高抢票成功率
- 🖥️ **交互式配置** - 友好的命令行交互界面，配置简单直观
- 📱 **扫码登录支持** - 安全便捷的扫码登录方式

## 📋 系统要求

### 必需环境
- **Python**: 3.7 或更高版本
- **浏览器**: Google Chrome（最新稳定版）
- **ChromeDriver**: 与 Chrome 版本匹配的驱动程序
- **操作系统**: Windows / macOS / Linux

### Python 依赖包
```
selenium>=4.0.0
```

## 🚀 快速开始

### 1. 安装 Python
访问 [Python 官网](https://www.python.org/downloads/) 下载并安装 Python 3.7+

### 2. 安装依赖
```bash
pip install selenium
```

### 3. 安装 ChromeDriver

#### 方法一：手动安装
1. 查看 Chrome 版本：`chrome://version/`
2. 下载对应版本的 [ChromeDriver](https://chromedriver.chromium.org/downloads)
3. 将 `chromedriver` 添加到系统 PATH

#### 方法二：使用 webdriver-manager（推荐）
```bash
pip install webdriver-manager
```

然后修改脚本第一行：
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# 替换 driver = webdriver.Chrome() 为：
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### 4. 运行脚本
```bash
python3 grab.py
```

## 📖 使用说明

### 基础配置

运行脚本后，按照提示依次输入：

1. **出发站**：如 `北京`
2. **目的地**：如 `上海`
3. **出发日期**：格式 `2026-01-01`
4. **车次**：如 `G1786`
5. **座位类型**：
   - `1` - 商务座
   - `2` - 一等座
   - `3` - 二等座
   - `4` - 软卧
   - `5` - 硬卧
   - `6` - 硬座
   - 可多选，用逗号分隔：`3,2`（优先二等座，其次一等座）

### 乘车人座位分配

脚本支持智能座位分配规则：

```
输入顺序 → 座位位置
第1个数字 → C座（靠过道）
第2个数字 → B座（中间）
第3个数字 → A座（靠窗）
第4个数字 → D座（靠过道）
第5个数字 → F座（靠窗）
```

**示例**：
- 输入 `1 2`：乘车人1坐C座，乘车人2坐B座
- 输入 `3 5 1`：乘车人3坐C座，乘车人5坐B座，乘车人1坐A座

### 定时抢票

脚本支持定时抢票功能：

1. 选择 `Y` 启用定时抢票
2. 输入开抢时间（北京时间），格式：`HH:MM:SS`
   - 例如：`13:00:00` 表示下午1点整开抢
3. 脚本会自动等待到指定时间，倒计时显示剩余时间
4. 时间到达后自动开始抢票流程

**技巧**：
- 建议提前 5-10 分钟运行脚本完成配置
- 定时精度约 0.5 秒，足以应对大部分抢票场景
- 可以随时按 `Ctrl+C` 跳过等待，立即开抢

## 🔧 高级配置

### 修改等待超时时间

在脚本中找到 `WebDriverWait(driver, 10)` 并修改数字（单位：秒）：
```python
# 默认等待 10 秒
WebDriverWait(driver, 10).until(...)

# 修改为等待 30 秒
WebDriverWait(driver, 30).until(...)
```

### 调整刷新频率

在定时等待部分修改：
```python
time.sleep(0.5)  # 每 0.5 秒刷新一次倒计时
```

### 无头模式运行

如需后台运行（无界面），添加以下代码：
```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
```

## ⚠️ 注意事项

### 使用限制
- ⚖️ **仅供学习交流使用**，请勿用于商业用途或黄牛抢票
- 🛡️ 遵守 12306 使用条款，不得恶意刷票或攻击服务器
- 🔒 建议使用自己的 12306 账号，保护个人信息安全

### 常见问题

**Q1: ChromeDriver 版本不匹配怎么办？**
- A: 确保 ChromeDriver 版本与 Chrome 浏览器版本一致，或使用 `webdriver-manager` 自动管理

**Q2: 脚本运行到一半卡住了？**
- A: 检查网络连接，或增加 `WebDriverWait` 的超时时间

**Q3: 无法选择座位？**
- A: 部分车次（如卧铺）不支持选座，脚本会自动跳过此步骤

**Q4: 定时抢票不准确？**
- A: 系统时间需校准，建议使用网络时间同步

**Q5: 提示"未查询到车次"？**
- A: 检查车次号是否正确，或该日期该车次是否开售

## 🛠️ 开发计划

- [ ] 支持多车次备选方案
- [ ] 添加自动支付功能
- [ ] 支持候补抢票
- [ ] 图形化配置界面（GUI）
- [ ] 微信/邮件通知功能
- [ ] Docker 容器化部署

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 💬 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [Issue](https://github.com/yourusername/12306-ticket-grabber/issues)
- 发送邮件至：tristanisolde08@gmail.com

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐ 支持一下！

---

**免责声明**：本工具仅供技术学习交流使用，使用者需自行承担使用风险。开发者不对因使用本工具导致的任何问题负责，包括但不限于账号封禁、订单异常等。请合理使用，共同维护良好的购票环境。
