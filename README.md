# My Todo List App

一个简单实用的待办事项手机应用，使用 Kivy 和 KivyMD 开发。

## 功能特性

- ✅ 添加待办事项
- ✅ 删除待办事项  
- ✅ 自动保存数据
- ✅ Material Design 界面
- ✅ 跨平台支持

## 技术栈

- Python 3.9+
- Kivy 2.3.1
- KivyMD 1.2.0

## 本地运行

```bash
pip install -r requirements.txt
python main.py
```

## APK 构建

本项目配置了 GitHub Actions 自动构建，每次提交代码到 main/master 分支时会自动生成 APK 文件。

构建完成后可以在以下位置下载：
1. Actions 页面的 Artifacts
2. Releases 页面的发布文件

## 安装到手机

1. 下载生成的 APK 文件
2. 在安卓手机上启用"未知来源"安装
3. 安装 APK 文件即可使用
