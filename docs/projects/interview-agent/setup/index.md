# 环境搭建

本章节将指导你在 10 分钟内完成智能面试助手项目的环境搭建。

## 1. 安装 Python

确保你的电脑上安装了 Python 3.7 或更高版本。

### Windows
1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载最新版本的 Python
3. 运行安装程序，勾选 "Add Python to PATH"
4. 点击 "Install Now"

### Mac
1. 使用 Homebrew 安装：`brew install python`
2. 或从 [Python 官网](https://www.python.org/downloads/) 下载安装包

### Linux
1. 使用包管理器安装，如 Ubuntu：`sudo apt install python3 python3-pip`
2. 或从 [Python 官网](https://www.python.org/downloads/) 下载安装包

## 2. 下载项目代码

将智能面试助手项目代码下载到你的本地目录。

### 使用 Git 克隆（推荐）
```bash
git clone https://github.com/handsomeyx/my-interview-king.git
cd my-interview-king/docs/ai/05-engineering/interview-agent
```

### 直接下载
1. 访问 [GitHub 仓库](https://github.com/handsomeyx/my-interview-king)
2. 点击 "Code" 按钮，选择 "Download ZIP"
3. 解压 ZIP 文件到本地目录
4. 进入 `docs/ai/05-engineering/interview-agent` 目录

## 3. 安装依赖

在项目目录下运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

## 4. 配置 API Key

打开 `config.py` 文件，填写你的千问模型 API Key：

```python
# 千问模型 API Key
# 请在这里填写你的千问模型 API Key
OPENAI_API_KEY = "your_api_key_here"  # 填写你的千问模型 API Key

# 模型配置
MODEL_NAME = "qwen-max"  # 使用千问模型
```

### 获取 API Key
1. 访问 [阿里云百炼平台](https://model.aliyun.com/)
2. 登录你的阿里云账号
3. 进入 "API Key 管理" 页面
4. 点击 "创建 API Key"
5. 复制生成的 API Key

## 5. 验证环境

运行以下命令验证环境是否配置成功：

```bash
python test_qwen.py
```

如果看到以下输出，说明环境配置成功：

```
正在测试千问模型 API 调用...
测试成功！
回答: ...
```

## 常见问题

### 依赖安装失败
- 确保你使用了正确的 pip 命令
- 确保你的 Python 版本符合要求
- 尝试使用 `pip install --upgrade pip` 升级 pip

### API Key 错误
- 确保你填写了正确的 API Key
- 确保你的 API Key 有足够的余额
- 确保你的网络连接正常

### 运行时错误
- 检查你的 API Key 是否正确
- 检查你的网络连接是否正常
- 查看错误信息，根据错误提示进行排查

## 下一步

环境搭建完成后，你可以继续学习 [Agent 基础](./../agent-basics/) 章节，了解 Agent 的核心概念和实现。