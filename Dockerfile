FROM kivy/buildozer:latest

# 复制项目文件
COPY . /app
WORKDIR /app

# 设置权限
RUN chmod +x /app/main.py

# 构建 APK
CMD ["buildozer", "android", "debug"]
