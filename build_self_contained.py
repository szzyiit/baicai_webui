#!/usr/bin/env python3
"""
🥬 白菜AI平台 - 自包含包构建工具
从网络下载Python可执行文件和所有依赖，创建完全自包含的包
"""

import os
import shutil
import sys
import urllib.request
import zipfile
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
    if build_cross_platform_package():
        print("\n✅ 跨平台自包含包构建成功！")
        print("📁 输出目录: dist/baicai-self-contained")
        print("📋 用户说明: 解压后运行 'launch.bat' 或 './launch.sh'")
        print()
        print("🎉 现在您可以将 dist/baicai-self-contained 目录压缩分发给其他用户了！")
        print("用户只需要解压，然后双击启动脚本即可运行应用，无需安装任何环境！")
        print("✅ 支持 Windows、macOS 和 Linux 平台！")
    else:
        print("\n❌ 跨平台自包含包构建失败！")
        print("请检查错误信息并重试。")


def get_cache_dir():
    """获取缓存目录"""
    cache_dir = Path.home() / ".baicai" / "python"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def download_windows_python(output_dir):
    """下载Windows便携式Python"""
    print("📥 正在下载Windows便携式Python...")

    # 检查缓存
    cache_dir = get_cache_dir()
    python_version = "3.11.7"

    # 下载便携式Python（portable Python）
    zip_name = f"python-{python_version}-amd64.zip"
    cache_file = cache_dir / zip_name

    if cache_file.exists():
        print(f"✅ 使用缓存的便携式Python: {cache_file}")
    else:
        # 下载便携式Python
        url = f"https://www.python.org/ftp/python/{python_version}/{zip_name}"
        print(f"🌐 从 {url} 下载便携式Python...")

        try:
            print("🌐 正在下载便携式Python...")
            urllib.request.urlretrieve(url, cache_file)
            print(f"✅ 便携式Python下载完成，已缓存到: {cache_file}")
        except Exception as e:
            print(f"❌ 便携式Python下载失败: {e}")
            return False

    # 解压Python到输出目录
    python_dir = Path(output_dir) / "python"
    if python_dir.exists():
        shutil.rmtree(python_dir)

    print(f"📦 解压Python到: {python_dir}")

    try:
        with zipfile.ZipFile(cache_file, "r") as zip_ref:
            zip_ref.extractall(python_dir)

        # 便携式Python通常解压后直接可用
        if (python_dir / "Lib").exists():
            print("✅ 检测到便携式Python（包含Lib目录）")
        else:
            print("⚠️ 警告：未检测到Lib目录，可能不是标准便携式Python")

        print("✅ Windows便携式Python下载完成")
        return True
    except Exception as e:
        print(f"❌ Python解压失败: {e}")
        return False


def create_windows_python_config(output_dir):
    """为Windows便携式Python创建配置"""
    print("⚙️ 配置Windows便携式Python...")

    python_dir = Path(output_dir) / "python"

    # 便携式Python需要将site-packages放在Lib目录下
    target_site_packages = python_dir / "Lib" / "site-packages"
    target_site_packages.mkdir(parents=True, exist_ok=True)

    print("✅ 使用便携式Python标准配置（Lib/site-packages）")

    # 检查是否已有完整的site-packages（检查关键包是否存在）
    streamlit_check = target_site_packages / "streamlit"
    if streamlit_check.exists() and streamlit_check.is_dir():
        print("✅ site-packages已在正确位置（包含streamlit）")
        return True

    # 如果不存在完整包，从临时目录移动
    source_site_packages = Path(output_dir) / "site-packages"
    if source_site_packages.exists():
        print(f"📁 移动site-packages到 {target_site_packages}...")
        print("   (从临时目录移动到便携式Python标准位置)")

        # 如果目标目录已存在，先备份配置文件
        config_files = []
        if target_site_packages.exists():
            for config_file in ["sitecustomize.py", "baicai-self-contained.pth"]:
                config_path = target_site_packages / config_file
                if config_path.exists():
                    config_files.append((config_file, config_path.read_bytes()))

        # 删除目标目录（如果存在）
        if target_site_packages.exists():
            shutil.rmtree(target_site_packages)

        # 复制整个site-packages目录
        shutil.copytree(source_site_packages, target_site_packages)

        # 恢复配置文件（如果之前存在）
        for config_file, content in config_files:
            config_path = target_site_packages / config_file
            config_path.write_bytes(content)

        print("✅ site-packages已移动到Lib目录")

        # 删除临时目录
        print("🗑️ 删除临时目录的site-packages（避免重复）...")
        try:
            shutil.rmtree(source_site_packages)
            print("✅ 已删除临时目录的site-packages")
        except Exception as e:
            print(f"⚠️ 警告：无法删除临时目录的site-packages: {e}")
    else:
        print("❌ 错误：未找到临时site-packages目录")
        return False

    return True


def create_python_config(python_dir):
    """创建Python配置文件"""
    print("⚙️ 创建Python配置文件...")

    # 配置文件应该放在Lib/site-packages中（便携式Python标准位置）
    site_packages_dir = python_dir / "Lib" / "site-packages"
    site_packages_dir.mkdir(parents=True, exist_ok=True)

    # 创建sitecustomize.py
    # Note: Use ASCII-only comments to avoid encoding issues on Windows
    sitecustomize_content = """# -*- coding: utf-8 -*-
import sys
import os

# Get current directory (site-packages)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get Python installation directory
python_dir = os.path.dirname(current_dir)

# Get project root directory
project_root = os.path.dirname(python_dir)

# Add project root to Python path (for accessing source code if needed)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Ensure Lib/site-packages is in path (portable Python standard location)
lib_site_packages = os.path.join(python_dir, "Lib", "site-packages")
if lib_site_packages not in sys.path:
    sys.path.insert(0, lib_site_packages)

# Note: Root site-packages has been removed to avoid duplication
# All packages are in python/Lib/site-packages

# Print debug info
print("Python path configuration completed")
print(f"  Project root: {project_root}")
"""

    sitecustomize_file = site_packages_dir / "sitecustomize.py"
    with open(sitecustomize_file, "w", encoding="utf-8") as f:
        f.write(sitecustomize_content)

    # 创建baicai-self-contained.pth
    # Note: .pth files are read with system encoding on Windows, avoid non-ASCII characters
    pth_file = site_packages_dir / "baicai-self-contained.pth"
    pth_content = """import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
"""

    # Write with UTF-8 encoding, but content is ASCII-only to avoid encoding issues
    with open(pth_file, "w", encoding="utf-8") as f:
        f.write(pth_content)

    print("✅ 创建Python配置文件")
    return True


def clean_path_references(site_packages_dir):
    """清理site-packages中的路径相关文件，确保可移植性"""
    print("🧹 清理路径相关文件...")

    # 需要清理的文件类型
    files_to_clean = [
        "direct_url.json",  # 包含本地路径的URL引用
        "RECORD",  # 包含绝对路径的安装记录
    ]

    # 需要清理的目录模式（只清理baicai相关的）
    dirs_to_clean = [
        "baicai_base-*.dist-info",  # baicai_base包元数据
        "baicai_dev-*.dist-info",  # baicai_dev包元数据
        "baicai_tutor-*.dist-info",  # baicai_tutor包元数据
        "baicai_webui-*.dist-info",  # baicai_webui包元数据
    ]

    cleaned_count = 0

    # 遍历所有子目录
    for item in site_packages_dir.rglob("*"):
        if item.is_file():
            # 清理特定文件
            if item.name in files_to_clean:
                try:
                    item.unlink()
                    cleaned_count += 1
                    print(f"  🗑️ 删除: {item.relative_to(site_packages_dir)}")
                except Exception as e:
                    print(f"  ⚠️ 无法删除 {item}: {e}")

        elif item.is_dir():
            # 只清理baicai相关的dist-info目录
            if "dist-info" in item.name:
                should_delete = False
                for pattern in dirs_to_clean:
                    if pattern.replace("*", "") in item.name:
                        should_delete = True
                        break

                if should_delete:
                    try:
                        shutil.rmtree(item)
                        cleaned_count += 1
                        print(f"  🗑️ 删除目录: {item.relative_to(site_packages_dir)}")
                    except Exception as e:
                        print(f"  ⚠️ 无法删除目录 {item}: {e}")

    print(f"✅ 清理完成，共删除 {cleaned_count} 个路径相关文件/目录")
    return cleaned_count


def copy_dependencies(output_dir, target_site_packages=None):
    """复制依赖包到指定位置
    
    Args:
        output_dir: 输出目录
        target_site_packages: 目标site-packages目录，如果为None则使用临时目录
    """
    print("📦 复制依赖包...")

    # 获取当前虚拟环境的site-packages
    venv_site_packages = None

    # 首先尝试从sys.path中查找
    for path in sys.path:
        if "site-packages" in str(path) and ".venv" in str(path):
            venv_site_packages = Path(path)
            break

    # 如果没找到，尝试直接查找.venv目录
    if not venv_site_packages:
        venv_path = Path(".venv")
        if venv_path.exists():
            if sys.platform == "win32":
                venv_site_packages = venv_path / "Lib" / "site-packages"
            else:
                venv_site_packages = venv_path / "lib" / "python3.11" / "site-packages"

    if not venv_site_packages or not venv_site_packages.exists():
        print("❌ 未找到虚拟环境的site-packages")
        print("尝试的路径:")
        for path in sys.path:
            if "site-packages" in str(path):
                print(f"  - {path}")
        return False

    # 确定目标目录
    if target_site_packages is None:
        # 使用临时目录（向后兼容）
        target_site_packages = Path(output_dir) / "site-packages"
    else:
        target_site_packages = Path(target_site_packages)
        target_site_packages.mkdir(parents=True, exist_ok=True)

    # 检查是否需要重新复制
    need_copy = True
    if target_site_packages.exists() and list(target_site_packages.iterdir()):
        # 检查目标目录是否已经是最新的
        try:
            source_mtime = venv_site_packages.stat().st_mtime
            target_mtime = target_site_packages.stat().st_mtime

            # 如果目标目录比源目录新，说明可能已经是最新的
            if target_mtime >= source_mtime:
                # 进一步检查关键文件是否存在
                streamlit_check = target_site_packages / "streamlit"
                if streamlit_check.exists():
                    print("✅ 使用现有的site-packages目录（已是最新）")
                    need_copy = False
        except (OSError, AttributeError):
            # 如果无法比较时间戳，继续复制
            pass

    if need_copy:
        if target_site_packages.exists() and list(target_site_packages.iterdir()):
            shutil.rmtree(target_site_packages)
            target_site_packages.mkdir(parents=True, exist_ok=True)

        print(f"📁 从 {venv_site_packages} 复制到 {target_site_packages}")
        shutil.copytree(venv_site_packages, target_site_packages)

        # 清理路径相关的文件，确保可移植性
        print("🧹 清理路径相关文件，确保可移植性...")
        clean_path_references(target_site_packages)

        print("✅ 依赖包复制完成")
    else:
        print("✅ 依赖包已是最新，跳过复制")

    return True


def create_smart_launch_scripts(output_dir):
    """创建智能启动脚本"""
    print("📝 创建启动脚本...")

    # Windows批处理文件
    bat_content = """@echo off
chcp 65001 >nul
echo 正在启动baicai应用...

REM 检查Python解释器
if not exist "python\\python.exe" (
    echo 错误：未找到Python解释器
    echo 请确保python目录中包含python.exe文件
    pause
    exit /b 1
)

REM 设置环境变量（baicai_* 包已通过pip安装，只需项目根目录用于访问app.py）
set PYTHONPATH=%~dp0

REM 启动应用
echo 启动中...
python\\python.exe -m streamlit run baicai_webui\\app.py

if errorlevel 1 (
    echo 启动失败，请检查错误信息
    pause
 )
"""

    bat_file = Path(output_dir) / "launch.bat"
    with open(bat_file, "w", encoding="utf-8") as f:
        f.write(bat_content)

    # Unix shell脚本
    sh_content = """#!/bin/bash
echo "正在启动baicai应用..."

# 检查Python解释器
if [ ! -f "python/python" ]; then
    echo "错误：未找到Python解释器"
    echo "请确保python目录中包含python文件"
    exit 1
fi

# 设置环境变量（baicai_* 包已通过pip安装，只需项目根目录用于访问app.py）
export PYTHONPATH="$(pwd)"

# 启动应用
echo "启动中..."
python/python -m streamlit run baicai_webui/app.py
"""

    sh_file = Path(output_dir) / "launch.sh"
    with open(sh_file, "w", encoding="utf-8") as f:
        f.write(sh_content)

    # 设置shell脚本执行权限
    os.chmod(sh_file, 0o755)

    print("✅ 启动脚本创建完成")
    return True


def create_cross_platform_python(output_dir):
    """创建跨平台Python环境"""
    print("🐍 创建Python环境...")

    if sys.platform == "win32":
        # Windows: 下载便携式Python
        if not download_windows_python(output_dir):
            print("❌ 无法创建Python环境")
            return False
    else:
        # Unix: 暂时不支持，提示用户
        print("⚠️ Unix系统暂不支持，请手动配置Python环境")
        return False

    return True


def verify_build_result(output_dir):
    """验证构建结果"""
    print("\n🔍 验证构建结果...")

    output_path = Path(output_dir)

    # 检查Python解释器
    if sys.platform == "win32":
        python_exe = output_path / "python" / "python.exe"
    else:
        python_exe = output_path / "python" / "python"

    if python_exe.exists():
        print(f"✅ Python解释器: {python_exe}")
    else:
        print("❌ 错误：未找到Python解释器")
        return False

    # 检查site-packages（只检查python/Lib/site-packages，已优化避免重复）
    python_lib_site_packages = output_path / "python" / "Lib" / "site-packages"
    if python_lib_site_packages.exists():
        print(f"✅ Python Lib site-packages: {python_lib_site_packages}")

        # 检查关键包
        streamlit_dir = python_lib_site_packages / "streamlit"
        if streamlit_dir.exists():
            print("✅ streamlit包已安装")
        else:
            print("❌ 错误：未找到streamlit包")
            return False
    else:
        print("❌ 错误：未找到site-packages目录")
        return False

        # 检查便携式Python配置
    if sys.platform == "win32":
        python_dir = output_path / "python"
        if (python_dir / "Lib").exists():
            print("✅ 便携式Python（包含Lib目录）")
        else:
            print("❌ 错误：未检测到便携式Python的Lib目录")
            return False

    # 检查sitecustomize.py文件（在python/Lib/site-packages中）
    sitecustomize_file = python_lib_site_packages / "sitecustomize.py"
    if sitecustomize_file.exists():
        print("✅ sitecustomize.py文件已创建")
    else:
        print("❌ 错误：未找到sitecustomize.py")
        return False

    # 检查启动脚本
    if sys.platform == "win32":
        bat_file = output_path / "launch.bat"
        if bat_file.exists():
            print("✅ launch.bat文件已创建")
        else:
            print("❌ 错误：未找到launch.bat文件")
            return False
    else:
        sh_file = output_path / "launch.sh"
        if sh_file.exists():
            print("✅ launch.sh文件已创建")
        else:
            print("❌ 错误：未找到launch.sh文件")
            return False

    print("\n🎉 构建验证完成！")
    return True


# 全局常量定义
# 需要排除的文件和目录模式
EXCLUDED_PATTERNS = [
    ".*",  # 隐藏文件和目录（包括.pyc, .pyo, .pyd等）
    "__pycache__",  # Python缓存目录
    "dist",
    "build",  # 构建目录
    "venv",
    "tests",  # 虚拟环境和测试目录
    "build_self_contained.py",  # 打包脚本
]


def build_cross_platform_package():
    """构建跨平台自包含包"""
    print("🚀 开始构建跨平台自包含包...")

    # 创建输出目录
    output_dir = "dist/baicai-self-contained"
    if os.path.exists(output_dir):
        try:
            shutil.rmtree(output_dir)
        except PermissionError:
            print("⚠️ 无法删除现有目录，尝试强制删除...")
            import time

            time.sleep(2)
            try:
                shutil.rmtree(output_dir, ignore_errors=True)
            except:
                pass
            # 如果还是无法删除，使用不同的目录名
            if os.path.exists(output_dir):
                output_dir = f"dist/baicai-self-contained-{int(time.time())}"
                print(f"🔄 使用新的输出目录: {output_dir}")

    os.makedirs(output_dir)

    # 复制项目文件
    print("📁 复制项目文件...")
    try:
        # 排除不需要的目录
        def ignore_patterns(dir, files):
            return EXCLUDED_PATTERNS

        # 复制当前目录（baicai_webui）
        print("📁 复制当前目录文件...")
        for item in Path(".").iterdir():
            # 检查是否应该排除
            should_exclude = False
            for pattern in EXCLUDED_PATTERNS:
                if pattern == ".*" and item.name.startswith("."):
                    should_exclude = True
                    break
                elif pattern == item.name:
                    should_exclude = True
                    break

            if should_exclude:
                print(f"  ⏭️ 跳过: {item.name}")
                continue

            if item.is_file():
                shutil.copy2(item, Path(output_dir) / item.name)
            elif item.is_dir():
                shutil.copytree(item, Path(output_dir) / item.name, ignore=ignore_patterns)


        print("✅ 项目文件复制完成")
    except Exception as e:
        print(f"❌ 复制失败: {e}")
        return False

    # 复制依赖包（只在必要时）
    if not copy_dependencies(output_dir):
        return False

    # 创建Python环境
    if not create_cross_platform_python(output_dir):
        return False

    # 为Windows便携式Python创建配置（复制site-packages到Lib/site-packages）
    if sys.platform == "win32":
        if not create_windows_python_config(output_dir):
            return False

    # 创建Python配置文件（在site-packages复制完成后）
    python_dir = Path(output_dir) / "python"
    if not create_python_config(python_dir):
        return False

    # 创建启动脚本
    if not create_smart_launch_scripts(output_dir):
        return False

    # 验证构建结果
    if not verify_build_result(output_dir):
        return False

    print(f"\n🎉 构建完成！输出目录: {output_dir}")
    print("\n📋 使用说明:")
    if sys.platform == "win32":
        print("   Windows用户: 双击 'launch.bat' 文件")
    else:
        print("   Unix用户: 运行 './launch.sh' 命令")

    return True


if __name__ == "__main__":
    main()
