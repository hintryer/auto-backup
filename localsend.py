import requests
import re
import os
from datetime import datetime

def fetch_localsend_windows_link():
    # LocalSend官方GitHub仓库API
    api_url = "https://api.github.com/repos/localsend/localsend/releases/latest"
    
    try:
        # 发送请求获取最新release信息
        response = requests.get(api_url)
        response.raise_for_status()  # 抛出HTTP错误（如404、500）
        release_data = response.json()
        
        # 提取版本号
        version = release_data.get("tag_name", "未知版本")
        print(f"检测到LocalSend最新版本：{version}")
        
        # 提取Windows x64 EXE安装包链接（通过正则匹配文件名）
        # 匹配规则：包含"windows-x86-64.exe"的资产
        assets = release_data.get("assets", [])
        windows_exe_link = None
        for asset in assets:
            if re.search(r"LocalSend-.*-windows-x86-64\.exe", asset.get("name", "")):
                windows_exe_link = asset.get("browser_download_url")
                break
        
        if not windows_exe_link:
            raise ValueError("未找到Windows x64 EXE安装包链接")
        
        # 生成MD文件内容
        md_content = f"""# LocalSend Windows最新版下载链接

更新时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}  
最新版本：{version}  

## 下载链接
- [Windows x64 安装包]({windows_exe_link})

> 链接自动获取自LocalSend官方GitHub Release，确保为最新版本。
"""
        
        # 创建保存目录（若不存在）
        os.makedirs("docs", exist_ok=True)
        # 保存到MD文件
        with open("docs/localsend_windows_latest.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"链接已成功保存到 docs/localsend_windows_latest.md")
        return True
        
    except Exception as e:
        print(f"获取链接失败：{str(e)}")
        return False

if __name__ == "__main__":
    success = fetch_localsend_windows_link()
    # 非0退出码会让Actions工作流报错
    exit(0 if success else 1)
