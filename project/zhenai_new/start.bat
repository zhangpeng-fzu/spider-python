@echo off
ECHO 正在检测python环境......
python -V

if ERRORLEVEL 1 (
	ECHO python未安装，开始安装python3.74 win64......
	start /wait python\python-3.7.4-amd64
	ECHO install python3.74 successfully......
) 

ECHO python已安装，开始安装依赖模块......
pip install requests
pip install stat
pip install shutil
pip install urllib3


ECHO python依赖模块已安装完成，开始启动程序......

python index.py

pause
exit