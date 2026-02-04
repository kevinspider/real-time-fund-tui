# 🚀 基金监控助手

一个基于 Textual 框架开发的命令行基金实时监控工具，帮助您实时跟踪基金涨跌幅和行业板块资金流向。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Textual](https://img.shields.io/badge/Textual-7.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 功能特性

- 📊 **实时基金涨跌监控** - 自动获取并展示基金实时估值和涨跌幅
- 📈 **行业板块资金流向** - 实时展示上涨和下跌行业的资金流向情况
- 🔄 **自动刷新** - 可配置的定时刷新功能，确保数据实时性
- 🎨 **现代化 TUI 界面** - 基于 Textual 框架，提供美观的终端用户界面
- ⚡ **多线程加载** - 后台线程获取数据，UI 始终保持流畅响应
- 🎯 **智能重试机制** - 网络请求失败自动重试，提高数据获取成功率
- 🌓 **暗色主题** - 护眼的暗色界面设计

## 📸 界面预览

![](https://kevinspider-1258012111.cos.ap-shanghai.myqcloud.com/20260204175057.png)


应用包含三个 TAB 页面：

| TAB 页面 | 说明 |
|---------|------|
| 📊 基金涨跌 | 显示所有监控基金的实时涨跌幅，按涨幅降序排列 |
| 📈 上涨行业 | 显示资金流入最多的行业板块 |
| 📉 下跌行业 | 显示资金流出最多的行业板块 |

## 🛠️ 技术栈

- **Python 3.8+**
- **[Textual](https://github.com/Textualize/textual)** - 现代化的 Python TUI 框架
- **Requests** - HTTP 请求库

## 📦 安装

### 1. 克隆项目

```bash
git clone https://github.com/kevinspider/funds.git
cd funds
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install textual requests
```

### 3. 配置基金列表

编辑 `CONFIG.json` 文件，添加您想要监控的基金代码：

```json
{
    "funds": [
        "012920",
        "017730",
        "004206"
    ],
    "refresh_interval": 10,
    "top-K": 30,
    "req-retry": 10
}
```

#### 配置说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `funds` | 基金代码列表 | 必填 |
| `refresh_interval` | 数据刷新间隔（秒） | 10 |
| `top-K` | 行业板块显示数量 | 30 |
| `req-retry` | 网络请求重试次数 | 10 |

## 🚀 使用方法

### 启动应用

```bash
python main.py
```


### 键盘快捷键

| 按键 | 功能 |
|------|------|
| `q` | 退出程序 |
| `Ctrl+C` | 退出程序 |
| `鼠标点击` | 切换 TAB 页面|
| `左右方向键` | 切换 TAB 页面|

## 📁 项目结构

```
funds/
├── main.py           # 主程序入口（Textual 应用）
├── req.py            # 数据请求模块
├── CONFIG.json       # 配置文件
├── requirements.txt  # 依赖列表
└── README.md         # 项目说明
```

## 🔧 核心模块说明

### main.py

主程序文件，包含 Textual 应用实现：

- `FundApp` - 主应用类
- `refresh_data()` - 后台数据刷新（使用 `@work(thread=True)` 装饰器）
- `_update_ui()` - UI 更新逻辑（在主线程中执行）

### req.py

数据请求模块，负责获取基金和行业数据：

- `get_gszzl(fund_code, retry)` - 获取单只基金的实时数据
- `get_industry(retry)` - 获取行业板块资金流向数据

#### 数据来源

- **基金数据**: 天天基金网 (https://fundgz.1234567.com.cn)
- **行业数据**: 东方财富网 (http://push2.eastmoney.com)

## ⚠️ 注意事项

1. **网络连接**: 应用需要稳定的网络连接来获取实时数据
2. **数据延迟**: 基金估值数据存在一定延迟，仅供参考
3. **终端支持**: 建议使用支持真彩色的现代终端（如 iTerm2、Windows Terminal、GNOME Terminal）
4. **系统要求**: 支持 Python 3.8 及以上版本

## 🐛 常见问题

### Q: 为什么有些基金显示"数据获取失败"？

A: 可能是以下原因：
- 基金代码不正确
- 网络连接问题
- 基金公司暂停披露估值数据

### Q: 如何调整刷新频率？

A: 修改 `CONFIG.json` 中的 `refresh_interval` 参数（单位：秒）

### Q: 终端显示不正常怎么办？

A: 确保您的终端支持：
- 真彩色显示
- UTF-8 编码
- 足够的终端尺寸（建议 80x24 以上）


## TODO
- 收盘后接口数据错误的问题
    - 交易期间
    - 收盘新增接口
- 节假日判断
- 交易时间判断


## 📄 许可证

MIT License

---

⭐ 如果这个项目对您有帮助，请给个 Star！
