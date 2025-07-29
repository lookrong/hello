@echo off
echo Building APK using Docker...
docker build -t mytodoapp .
docker run --rm -v %cd%/bin:/app/bin mytodoapp
echo APK built successfully! Check the bin folder.
pause

