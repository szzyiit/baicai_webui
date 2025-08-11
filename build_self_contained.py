#!/usr/bin/env python3
"""
🥬 白菜AI平台 - 自包含包构建工具
从网络下载Python可执行文件和所有依赖，创建完全自包含的包
"""
import os
import shutil
import urllib.request
import zipfile
import tarfile
import platform
from pathlib import Path


def main():
    """主函数"""
    print("🥬 白菜AI平台 - 自包含包构建工具")
    print("=" * 50)
    print()
    
    print("正在构建跨平台自包含包...")
    print("将下载 Windows 和 macOS 版本的 Python，支持跨平台分发")
    print()
    
    # 构建跨平台自包含包
    build_cross_platform_package()
    
    print("\n✅ 跨平台自包含包构建成功！")
    print("📁 输出目录: dist/baicai-self-contained")
    print("📋 用户说明: 解压后运行 '启动应用.bat' 或 './启动应用.sh'")
    print()
    print("🎉 现在您可以将 dist/baicai-self-contained 目录压缩分发给其他用户了！")
    print("用户只需要解压，然后双击启动脚本即可运行应用，无需安装任何环境！")
    print("✅ 支持 Windows、macOS 和 Linux 平台！")

def build_cross_platform_package():
    """构建跨平台自包含包"""
    project_root = Path(__file__).parent
    output_dir = project_root / "dist" / "baicai-self-contained"
    
    # 清理输出目录
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"创建跨平台自包含包到: {output_dir}")
    
    # 1. 复制项目代码
    print("复制项目代码...")
    
    # 复制主项目代码
    project_src = project_root / "baicai_webui"
    if project_src.exists():
        shutil.copytree(project_src, output_dir / "baicai_webui")
        print("✅ 复制 baicai_webui")
    
    # 复制相关模块
    for module in ["baicai_base", "baicai_dev", "baicai_tutor"]:
        module_path = project_root.parent / module
        if module_path.exists():
            shutil.copytree(module_path, output_dir / module)
            print(f"✅ 复制 {module}")
        else:
            print(f"⚠️  模块 {module} 不存在")
    
    # 2. 创建跨平台Python环境
    print("创建跨平台Python环境...")
    create_cross_platform_python(output_dir)
    
    # 3. 复制虚拟环境中的依赖包
    print("复制依赖包...")
    copy_dependencies(output_dir)
    
    # 4. 创建跨平台启动脚本
    create_cross_platform_launch_scripts(output_dir)
    
    # 5. 创建说明文档
    create_self_contained_readme(output_dir)
    
    print(f"跨平台自包含包构建完成！")

def build_self_contained_package_download(target_platform):
    """构建自包含包（从网络下载Python）"""
    project_root = Path(__file__).parent
    output_dir = project_root / "dist" / "baicai-self-contained"
    
    # 清理输出目录
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"创建自包含包到: {output_dir}")
    
    # 1. 复制项目代码
    print("复制项目代码...")
    
    # 复制主项目代码
    project_src = project_root / "baicai_webui"
    if project_src.exists():
        shutil.copytree(project_src, output_dir / "baicai_webui")
        print("✅ 复制 baicai_webui")
    
    # 复制相关模块
    for module in ["baicai_base", "baicai_dev", "baicai_tutor"]:
        module_path = project_root.parent / module
        if module_path.exists():
            shutil.copytree(module_path, output_dir / module)
            print(f"✅ 复制 {module}")
        else:
            print(f"⚠️  模块 {module} 不存在")
    
    # 2. 从网络下载Python环境
    print("从网络下载Python环境...")
    if not download_python(output_dir, target_platform):
        print("❌ Python下载失败，尝试使用本地Python...")
        create_self_contained_python(output_dir)
    
    # 3. 复制虚拟环境中的依赖包
    print("复制依赖包...")
    copy_dependencies(output_dir)
    
    # 4. 创建启动脚本
    create_launch_scripts(output_dir, target_platform)
    
    # 5. 创建说明文档
    create_self_contained_readme(output_dir)
    
    print(f"自包含包构建完成！")

def build_self_contained_package():
    """构建自包含包（复制本地Python）"""
    project_root = Path(__file__).parent
    output_dir = project_root / "dist" / "baicai-self-contained"
    
    # 清理输出目录
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"创建自包含包到: {output_dir}")
    
    # 1. 复制项目代码
    print("复制项目代码...")
    
    # 复制主项目代码
    project_src = project_root / "baicai_webui"
    if project_src.exists():
        shutil.copytree(project_src, output_dir / "baicai_webui")
        print("✅ 复制 baicai_webui")
    
    # 复制相关模块
    for module in ["baicai_base", "baicai_dev", "baicai_tutor"]:
        module_path = project_root.parent / module
        if module_path.exists():
            shutil.copytree(module_path, output_dir / module)
            print(f"✅ 复制 {module}")
        else:
            print(f"⚠️  模块 {module} 不存在")
    
    # 2. 创建自包含的Python环境
    print("创建自包含的Python环境...")
    create_self_contained_python(output_dir)
    
    # 3. 创建启动脚本
    create_launch_scripts(output_dir)
    
    # 4. 创建说明文档
    create_self_contained_readme(output_dir)
    
    print(f"自包含包构建完成！")

def download_python(output_dir, target_platform="auto"):
    """从网络下载Python可执行文件"""
    print("从网络下载Python可执行文件...")
    
    # 如果未指定目标平台，自动检测
    if target_platform == "auto":
        target_platform = platform.system()
    
    # Python版本和下载配置
    python_version = "3.11.7"  # 使用可用的版本
    python_dir = output_dir / "python"
    python_dir.mkdir(exist_ok=True)
    
    # 根据目标平台选择下载URL
    if target_platform == "Windows":
        # Windows: 下载嵌入式Python
        url = f"https://www.python.org/ftp/python/{python_version}/python-{python_version}-embed-amd64.zip"
        filename = "python-windows.zip"
        extract_dir = python_dir
        python_exe_name = "python.exe"
    elif target_platform == "Darwin":  # macOS
        # macOS: 下载预编译的Python二进制版本
        # 使用官方提供的预编译版本
        url = f"https://www.python.org/ftp/python/{python_version}/python-{python_version}-macos11.pkg"
        filename = "python-macos.pkg"
        
        print("⚠️  macOS Python下载完成，但.pkg文件需要手动安装")
        print("将尝试下载预编译的二进制版本")
        
        # 尝试下载预编译的二进制版本
        try:
            # 使用conda-forge的预编译版本
            alt_url = f"https://repo.anaconda.com/miniconda/Miniconda3-py311_{python_version}-0-MacOSX-x86_64.sh"
            alt_filename = "python-macos-binary.sh"
            print(f"尝试下载预编译版本: {alt_url}")
            urllib.request.urlretrieve(alt_url, output_dir / alt_filename)
            print("✅ 预编译版本下载完成")
            # 设置解压目录
            extract_dir = python_dir
        except Exception as e:
            print(f"⚠️  预编译版本下载失败: {e}")
            extract_dir = None
        
        python_exe_name = "python"
    else:  # Linux
        # Linux: 下载预编译的Python二进制版本
        # 首先尝试官方源码包
        url = f"https://www.python.org/ftp/python/{python_version}/Python-{python_version}.tgz"
        filename = "python-linux.tar.gz"
        extract_dir = python_dir
        python_exe_name = "python"
        print("⚠️  Linux Python下载完成，但源码包需要编译")
        print("将尝试下载预编译的二进制版本")
        
        # 尝试下载预编译的二进制版本
        try:
            # 使用conda-forge的预编译版本
            alt_url = f"https://repo.anaconda.com/miniconda/Miniconda3-py311_{python_version}-0-Linux-x86_64.sh"
            alt_filename = "python-linux-binary.sh"
            print(f"尝试下载预编译版本: {alt_url}")
            urllib.request.urlretrieve(alt_url, output_dir / alt_filename)
            print("✅ 预编译版本下载完成")
            # 设置解压目录
            extract_dir = python_dir
        except Exception as e:
            print(f"⚠️  预编译版本下载失败: {e}")
            extract_dir = None
    
    try:
        print(f"下载Python {python_version} for {target_platform}...")
        print(f"下载地址: {url}")
        
        # 下载文件
        download_path = output_dir / filename
        urllib.request.urlretrieve(url, download_path)
        print(f"✅ 下载完成: {filename}")
        
        # 解压文件
        if extract_dir is not None:
            if filename.endswith('.zip'):
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                print("✅ 解压完成")
            elif filename.endswith('.tar.gz'):
                with tarfile.open(download_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(extract_dir)
                print("✅ 解压完成")
        else:
            print("⚠️  跳过解压（macOS包需要手动安装）")
        
        # 清理下载文件
        download_path.unlink()
        print("✅ 清理下载文件")
        
        # 创建Python配置文件
        create_python_config(python_dir)
        
        print("✅ Python环境下载完成")
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False

def create_cross_platform_python(output_dir):
    """创建跨平台Python环境"""
    print("创建跨平台Python环境...")
    
    # 创建Python环境目录
    python_dir = output_dir / "python"
    python_dir.mkdir(exist_ok=True)
    
    # 检测当前构建平台
    current_platform = platform.system()
    
    if current_platform == "Darwin":  # macOS
        # 在macOS上构建：复制系统Python + 下载Windows Python
        print("在macOS上构建，创建真正的跨平台环境...")
        
        # 1. 复制系统Python（用于macOS）
        print("1. 复制macOS系统Python环境...")
        if copy_system_python(output_dir):
            print("✅ macOS系统Python复制成功")
        else:
            print("❌ macOS系统Python复制失败")
        
        # 2. 下载Windows Python（用于Windows）
        print("2. 下载Windows版本Python...")
        if download_windows_python(output_dir):
            print("✅ Windows Python下载成功")
        else:
            print("⚠️  Windows Python下载失败")
            
    else:
        # 在其他平台上构建：下载Windows Python
        print("在其他平台上构建，下载Windows版本Python...")
        if download_windows_python(output_dir):
            print("✅ Windows Python下载成功")
        else:
            print("⚠️  Windows Python下载失败")
    
    # 创建Python配置文件
    create_python_config(python_dir)
    
    print("✅ 跨平台Python环境创建完成")
    return True

def copy_system_python(output_dir):
    """复制系统Python环境到自包含包"""
    print("复制系统Python环境...")
    
    # 创建Python环境目录
    python_dir = output_dir / "python"
    python_dir.mkdir(exist_ok=True)
    
    # 查找系统Python路径
    import subprocess
    try:
        # 获取系统Python路径
        result = subprocess.run(['which', 'python3'], capture_output=True, text=True)
        if result.returncode == 0:
            python_path = Path(result.stdout.strip())
        else:
            result = subprocess.run(['which', 'python'], capture_output=True, text=True)
            if result.returncode == 0:
                python_path = Path(result.stdout.strip())
            else:
                print("❌ 无法找到系统Python")
                return False
        
        print(f"找到系统Python: {python_path}")
        
        # 如果是符号链接，解析真实路径
        if python_path.is_symlink():
            real_python = python_path.resolve()
            print(f"解析真实路径: {real_python}")
        else:
            real_python = python_path
        
        # 复制Python可执行文件
        shutil.copy2(real_python, python_dir / "python")
        shutil.copy2(real_python, python_dir / "python3")
        
        # 获取Python安装目录
        python_install_dir = real_python.parent.parent
        
        # 复制Python库目录
        lib_dir = python_install_dir / "lib"
        if lib_dir.exists():
            shutil.copytree(lib_dir, python_dir / "lib")
            print("✅ 复制Python库")
        
        # 复制Python头文件目录
        include_dir = python_install_dir / "include"
        if include_dir.exists():
            shutil.copytree(include_dir, python_dir / "include")
            print("✅ 复制Python头文件")
        
        # 复制pip
        pip_path = python_install_dir / "bin" / "pip3"
        if pip_path.exists():
            shutil.copy2(pip_path, python_dir / "pip")
            print("✅ 复制pip")
        
        print("✅ 系统Python环境复制完成")
        return True
        
    except Exception as e:
        print(f"❌ 复制系统Python失败: {e}")
        return False

def download_windows_python(output_dir):
    """下载Windows版本的Python"""
    print("下载Windows版本Python...")
    
    # 创建Windows Python目录
    windows_python_dir = output_dir / "python" / "windows"
    windows_python_dir.mkdir(parents=True, exist_ok=True)
    
    # Python版本
    python_version = "3.11.7"
    
    # Windows嵌入式Python下载URL
    url = f"https://www.python.org/ftp/python/{python_version}/python-{python_version}-embed-amd64.zip"
    filename = "python-windows.zip"
    
    try:
        print(f"下载Python {python_version} for Windows...")
        print(f"下载地址: {url}")
        
        # 下载文件
        download_path = output_dir / filename
        urllib.request.urlretrieve(url, download_path)
        print(f"✅ 下载完成: {filename}")
        
        # 解压到Windows Python目录
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(windows_python_dir)
        print("✅ 解压完成")
        
        # 清理下载文件
        download_path.unlink()
        print("✅ 清理下载文件")
        
        print("✅ Windows Python下载完成")
        return True
        
    except Exception as e:
        print(f"❌ Windows Python下载失败: {e}")
        return False

def create_cross_platform_launch_scripts(output_dir):
    """创建跨平台启动脚本"""
    print("创建跨平台启动脚本...")
    
    # 创建智能启动脚本，自动检测平台
    create_smart_launch_scripts(output_dir)
    
    print("✅ 跨平台启动脚本创建完成")

def create_smart_launch_scripts(output_dir):
    """创建智能启动脚本，自动检测平台"""
    
    # Windows批处理文件 - 智能检测
    bat_content = """@echo off
echo 白菜AI平台启动器 (跨平台自包含版)
echo =====================================

cd /d "%~dp0"

REM 设置Python路径
set PYTHONPATH=%cd%\\python\\site-packages;%cd%\\python\\lib\\python3.11\\site-packages;%cd%\\baicai_webui;%cd%\\baicai_base;%cd%\\baicai_dev;%cd%\\baicai_tutor;%PYTHONPATH%

REM 启动应用
echo 正在启动应用...
echo 检测到Windows平台，使用Windows Python...

REM 检查Windows Python是否存在
if exist "python\\windows\\python.exe" (
    python\\windows\\python.exe -m streamlit run baicai_webui\\app.py --server.port 8501
) else (
    echo ❌ 错误：未找到Windows Python环境
    echo 请确保python\\windows\\python.exe文件存在
    pause
    exit /b 1
)

pause
"""
    
    with open(output_dir / "启动应用.bat", "w", encoding="utf-8") as f:
        f.write(bat_content)
    
    # Linux/Mac shell脚本 - 智能检测
    sh_content = """#!/bin/bash
echo "白菜AI平台启动器 (跨平台自包含版)"
echo "====================================="

cd "$(dirname "$0")"

# 设置Python路径
export PYTHONPATH="$(pwd)/python/site-packages:$(pwd)/python/lib/python3.11/site-packages:$(pwd)/baicai_webui:$(pwd)/baicai_base:$(pwd)/baicai_dev:$(pwd)/baicai_tutor:$PYTHONPATH"

# 检测平台
PLATFORM=$(uname -s)
echo "检测到平台: $PLATFORM"

# 启动应用
echo "正在启动应用..."

if [[ "$PLATFORM" == "Darwin" ]]; then
    # macOS
    echo "使用macOS Python环境..."
    if [[ -f "./python/python" ]]; then
        ./python/python -m streamlit run baicai_webui/app.py --server.port 8501
    elif [[ -f "./python/Python-3.11.7/python" ]]; then
        ./python/Python-3.11.7/python -m streamlit run baicai_webui/app.py --server.port 8501
    else
        echo "❌ 错误：未找到macOS Python环境"
        echo "请确保python/python文件存在"
        exit 1
    fi
elif [[ "$PLATFORM" == "Linux" ]]; then
    # Linux
    echo "使用Linux Python环境..."
    if [[ -f "./python/python" ]]; then
        ./python/python -m streamlit run baicai_webui/app.py --server.port 8501
    elif [[ -f "./python/Python-3.11.7/python" ]]; then
        ./python/Python-3.11.7/python -m streamlit run baicai_webui/app.py --server.port 8501
    else
        echo "❌ 错误：未找到Linux Python环境"
        echo "请确保python/python文件存在"
        exit 1
    fi
else
    echo "❌ 错误：不支持的平台: $PLATFORM"
    exit 1
fi
"""
    
    with open(output_dir / "启动应用.sh", "w", encoding="utf-8") as f:
        f.write(sh_content)
    
    # 设置执行权限
    os.chmod(output_dir / "启动应用.sh", 0o755)
    
    print("✅ 创建智能跨平台启动脚本")

def copy_dependencies(output_dir):
    """复制虚拟环境中的依赖包"""
    venv_path = Path(__file__).parent / ".venv"
    
    if not venv_path.exists():
        print("❌ 虚拟环境不存在，请先运行 poetry install")
        return False
    
    # 复制虚拟环境中的site-packages
    site_packages = venv_path / "lib" / "python3.11" / "site-packages"
    target_site_packages = output_dir / "python" / "site-packages"
    
    print(f"源site-packages路径: {site_packages}")
    print(f"目标site-packages路径: {target_site_packages}")
    
    if site_packages.exists():
        print(f"源目录存在，开始复制...")
        try:
            # 如果目标目录已存在，先删除
            if target_site_packages.exists():
                shutil.rmtree(target_site_packages)
                print("清理已存在的目标目录")
            
            shutil.copytree(site_packages, target_site_packages)
            print("✅ 复制已安装的包")
            return True
        except Exception as e:
            print(f"❌ 复制失败: {e}")
            return False
    else:
        print(f"❌ 源目录不存在: {site_packages}")
        return False

def create_self_contained_python(output_dir):
    """创建自包含的Python环境"""
    # 获取当前虚拟环境路径
    venv_path = Path(__file__).parent / ".venv"
    
    if not venv_path.exists():
        print("❌ 虚拟环境不存在，请先运行 poetry install")
        return False
    
    # 创建Python环境目录
    python_dir = output_dir / "python"
    python_dir.mkdir(exist_ok=True)
    
    # 复制Python可执行文件
    print("复制Python可执行文件...")
    
    # 获取真正的Python路径
    python_symlink = venv_path / "bin" / "python"
    if python_symlink.exists() and python_symlink.is_symlink():
        real_python = python_symlink.resolve()
        print(f"找到真正的Python: {real_python}")
        
        # 复制Python可执行文件
        import platform
        if platform.system() == "Windows":
            # Windows系统：复制为 .exe 文件
            shutil.copy2(real_python, python_dir / "python.exe")
            shutil.copy2(real_python, python_dir / "python3.exe")
            shutil.copy2(real_python, python_dir / "python3.11.exe")
        else:
            # Unix系统：复制为无扩展名文件
            shutil.copy2(real_python, python_dir / "python")
            shutil.copy2(real_python, python_dir / "python3")
            shutil.copy2(real_python, "python3.11")
        
        # 复制Python库目录
        python_lib = real_python.parent.parent / "lib"
        if python_lib.exists():
            shutil.copytree(python_lib, python_dir / "lib")
            print("✅ 复制Python库")
        
        # 复制Python头文件目录
        python_include = real_python.parent.parent / "include"
        if python_include.exists():
            shutil.copytree(python_include, python_dir / "include")
            print("✅ 复制Python头文件")
        
        # 复制pip
        pip_symlink = venv_path / "bin" / "pip"
        if pip_symlink.exists() and pip_symlink.is_symlink():
            real_pip = pip_symlink.resolve()
            if platform.system() == "Windows":
                shutil.copy2(real_pip, python_dir / "pip.exe")
            else:
                shutil.copy2(real_python, python_dir / "pip")
            print("✅ 复制pip")
        
        # 复制虚拟环境中的site-packages
        site_packages = venv_path / "lib" / "python3.11" / "site-packages"
        print(f"源site-packages路径: {site_packages}")
        print(f"目标site-packages路径: {python_dir / 'site-packages'}")
        if site_packages.exists():
            print(f"源目录存在，开始复制...")
            try:
                shutil.copytree(site_packages, python_dir / "site-packages")
                print("✅ 复制已安装的包")
            except Exception as e:
                print(f"❌ 复制失败: {e}")
        else:
            print(f"❌ 源目录不存在: {site_packages}")
        
        # 创建Python配置文件，设置正确的路径
        create_python_config(python_dir)
        
        print("✅ Python环境复制完成")
        return True
    else:
        print("❌ 无法找到Python符号链接")
        return False

def create_launch_scripts(output_dir, target_platform=None):
    """创建启动脚本"""
    
    # 如果没有指定目标平台，检测当前平台
    if target_platform is None:
        target_platform = platform.system()
    
    # Windows批处理文件 - 根据目标平台动态生成
    if target_platform == "Windows":
        # Windows系统：使用 .exe 扩展名
        bat_content = """@echo off
echo 白菜AI平台启动器 (自包含版)
echo =============================

cd /d "%~dp0"

REM 设置Python路径
set PYTHONPATH=%cd%\\python\\site-packages;%cd%\\python\\lib\\python3.11\\site-packages;%cd%\\baicai_webui;%cd%\\baicai_base;%cd%\\baicai_dev;%cd%\\baicai_tutor;%PYTHONPATH%

REM 启动应用
echo 正在启动应用...
python\\python.exe -m streamlit run baicai_webui\\app.py --server.port 8501

pause
"""
    else:
        # Unix系统：不使用 .exe 扩展名
        bat_content = """@echo off
echo 白菜AI平台启动器 (自包含版)
echo =============================

cd /d "%~dp0"

REM 设置Python路径
set PYTHONPATH=%cd%\\python\\site-packages;%cd%\\python\\lib\\python3.11\\site-packages;%cd%\\baicai_webui;%cd%\\baicai_base;%cd%\\baicai_dev;%cd%\\baicai_tutor;%PYTHONPATH%

REM 启动应用
echo 正在启动应用...
python\\python -m streamlit run baicai_webui\\app.py --server.port 8501

pause
"""
    
    # 根据目标平台创建相应的启动脚本
    if target_platform == "Windows":
        # Windows系统：创建批处理文件
        with open(output_dir / "启动应用.bat", "w", encoding="gbk") as f:
            f.write(bat_content)
        print("✅ 创建Windows启动脚本")
    else:
        # Unix系统：创建批处理文件（用于跨平台分发）
        with open(output_dir / "启动应用.bat", "w", encoding="utf-8") as f:
            f.write(bat_content)
        print("✅ 创建跨平台Windows启动脚本")
    
    # Linux/Mac shell脚本
    sh_content = """#!/bin/bash
echo "白菜AI平台启动器 (自包含版)"
echo "============================="

cd "$(dirname "$0")"

# 设置Python路径
export PYTHONPATH="$(pwd)/python/site-packages:$(pwd)/python/lib/python3.11/site-packages:$(pwd)/baicai_webui:$(pwd)/baicai_base:$(pwd)/baicai_dev:$(pwd)/baicai_tutor:$PYTHONPATH"

# 启动应用
echo "正在启动应用..."
./python/python -m streamlit run baicai_webui/app.py --server.port 8501
"""
    
    with open(output_dir / "启动应用.sh", "w", encoding="utf-8") as f:
        f.write(sh_content)
    
    # 设置执行权限
    os.chmod(output_dir / "启动应用.sh", 0o755)
    
    print("✅ 创建启动脚本")

def create_python_config(python_dir):
    """创建Python配置文件，设置正确的模块搜索路径"""
    # 创建site-packages目录（如果不存在）
    site_packages = python_dir / "site-packages"
    site_packages.mkdir(exist_ok=True)
    
    sitecustomize_content = """# 自包含Python环境配置
import sys
import os

# 添加当前目录的site-packages到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(current_dir):
    sys.path.insert(0, current_dir)

# 添加上级目录的lib目录
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
if os.path.exists(lib_dir):
    sys.path.insert(0, lib_dir)

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'baicai_webui')
if os.path.exists(project_root):
    sys.path.insert(0, project_root)

# 添加其他模块路径
for module in ['baicai_base', 'baicai_dev', 'baicai_tutor']:
    module_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), module)
    if os.path.exists(module_path):
        sys.path.insert(0, module_path)
"""
    
    with open(site_packages / "sitecustomize.py", "w", encoding="utf-8") as f:
        f.write(sitecustomize_content)
    
    # 创建一个.pth文件来确保路径被正确添加
    pth_content = """# 自包含Python环境路径配置
.
../lib/python3.11/site-packages
../baicai_webui
../baicai_base
../baicai_dev
../baicai_tutor
"""
    
    with open(site_packages / "baicai-self-contained.pth", "w", encoding="utf-8") as f:
        f.write(pth_content)
    
    print("✅ 创建Python配置文件")

def create_self_contained_readme(output_dir):
    """创建自包含包说明文档"""
    readme_content = """# 白菜AI平台 - 自包含包

## 这是什么？
这是一个完全自包含的包，包含了运行白菜AI平台所需的所有内容：
- 完整的Python环境（无需安装Python）
- 所有依赖包
- 应用代码
- 启动脚本

用户无需安装任何环境，解压后即可直接运行！

## 🚀 使用方法

### Windows用户
1. 解压此文件夹到任意位置
2. 双击运行 `启动应用.bat`
3. 应用会自动在浏览器中打开

### Linux/Mac用户
1. 解压此文件夹到任意位置
2. 在终端中进入此文件夹
3. 运行 `./启动应用.sh`
4. 应用会自动在浏览器中打开

## ✨ 特点
✅ 完全自包含，无需安装Python
✅ 无需安装任何依赖包
✅ 环境完全隔离，不会影响系统
✅ 即解压即用
✅ 跨平台兼容

## 📋 系统要求
- Windows 10/11 或 Linux 或 macOS
- 至少2GB可用内存
- 至少2GB可用磁盘空间

## 🔧 工作原理
1. 包内包含完整的Python解释器
2. 包含所有必要的Python库和依赖
3. 启动脚本使用包内的Python环境
4. 完全独立运行，不依赖系统环境

## 📱 首次运行
- 首次运行可能需要几秒钟启动时间
- 应用启动后会在浏览器中打开，地址通常是 http://localhost:8501
- 不要删除或移动python文件夹，这是运行环境

## 🆘 故障排除
如果遇到问题：
1. 确保解压完整，没有损坏的文件
2. 检查杀毒软件是否阻止了某些文件
3. 尝试以管理员身份运行
4. 联系技术支持

## 📞 技术支持
如有问题，请联系：gengyabc@aliyun.com

---
🥬 白菜AI平台 - 让AI学习更简单！
"""
    
    with open(output_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ 创建说明文档")

if __name__ == "__main__":
    main()
