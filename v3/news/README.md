1. 基础环境搭建(注意配置环境变量)
    + python 3.5
    + mysql 5.6
    
2. 安装django
    + `pip install Django`
    
3. 安装mysqlclient
    + [文件下载地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
    + 其中cp35对应python3.5 win32表示window32位，win64表示windows64位系统。 下载mysqlclient-1.4.2-cp35-cp35m-win32.whl这个资源文件。 然后在该资源所在路径打开命令行使用如下命令安装：
    `pip install mysqlclient-1.4.2-cp35-cp35m-win32.whl`

4. 获取代码到本地环境
5. 配置和初始化数据库
    + 进入news/news目录，打开setting.py，修改数据库用户和密码
    ```
      DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
          'NAME': 'news',
          'USER': 'root',
          'PASSWORD': 'root',
          'HOST': 'localhost',
          'PORT': '3306'
          }
      }

    ```
    + 初始化数据库结构
      + 打开Navicat客户端，连接本地数据库，手动创建数据库，取名为news,编码为UTF-8
      + 进入news/config目录，使用Navicat客户端导入初始化脚本news.sql
    
    
5. 进入工程目录，可以看到manage.py，运行 `python3 manage.py runserver 0.0.0.0:8080` 启动工程。如果提示缺少模块，使用pip install安装即可
    
