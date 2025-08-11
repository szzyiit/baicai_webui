#!/usr/bin/env python3
"""
🥬 白菜AI平台 - 自包含包构建工具
复制真正的Python可执行文件和所有依赖，创建完全自包含的包
"""
import os
import shutil
from pathlib import Path


def main():
    """主函数"""
    print("🥬 白菜AI平台 - 自包含包构建工具")
    print("=" * 50)
    print()
    print("正在构建自包含包...")
    print("这将复制真正的Python可执行文件和所有依赖，创建完全自包含的包")
    print()
    
    # 构建自包含包
    build_self_contained_package()
    
    print("\n✅ 自包含包构建成功！")
    print("📁 输出目录: dist/baicai-self-contained")
    print("📋 用户说明: 解压后运行 '启动应用.bat' 或 './启动应用.sh'")
    print()
    print("🎉 现在您可以将 dist/baicai-self-contained 目录压缩分发给其他用户了！")
    print("用户只需要解压，然后双击启动脚本即可运行应用，无需安装任何环境！")

def build_self_contained_package():
    """构建自包含包"""
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
        shutil.copy2(real_python, python_dir / "python")
        shutil.copy2(real_python, python_dir / "python3")
        shutil.copy2(real_python, python_dir / "python3.11")
        
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
            shutil.copy2(real_pip, python_dir / "pip")
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

def create_launch_scripts(output_dir):
    """创建启动脚本"""
    
    # Windows批处理文件
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
    
    with open(output_dir / "启动应用.bat", "w", encoding="gbk") as f:
        f.write(bat_content)
    
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
    # 创建sitecustomize.py文件，放在site-packages目录中
    site_packages = python_dir / "site-packages"
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
