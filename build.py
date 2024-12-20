import os
import platform
import subprocess
import urllib.request

def download_icon(url, save_path):
    """Download icon from URL"""
    try:
        urllib.request.urlretrieve(url, save_path)
        return True
    except Exception as e:
        print(f"Failed to download icon: {e}")
        return False

def build_for_platform():
    system = platform.system().lower()
    
    # 在线图标资源
    icons = {
        'windows': 'https://raw.githubusercontent.com/microsoft/markitdown/main/assets/icon.ico',
        'darwin': 'https://raw.githubusercontent.com/microsoft/markitdown/main/assets/icon.icns',
        'linux': 'https://raw.githubusercontent.com/microsoft/markitdown/main/assets/icon.png'
    }
    
    # 创建临时目录存放下载的图标
    os.makedirs('temp_assets', exist_ok=True)
    icon_path = None
    
    # 下载对应平台的图标
    if system in icons:
        icon_ext = icons[system].split('.')[-1]
        icon_path = f'temp_assets/icon.{icon_ext}'
        if not download_icon(icons[system], icon_path):
            icon_path = None
    
    # 基本的 PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', f'markitdown-{system}'
    ]
    
    # 添加图标配置（如果成功下载）
    if icon_path:
        cmd.extend(['--icon', icon_path])
    
    # 添加主程序
    cmd.append('main.py')
    
    # 执行打包命令
    subprocess.run(cmd)
    
    # 清理临时文件
    if os.path.exists('temp_assets'):
        import shutil
        shutil.rmtree('temp_assets')

if __name__ == '__main__':
    build_for_platform()