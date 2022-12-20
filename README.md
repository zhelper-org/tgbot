# zhelper TG BOT

使用方式：

1. 建立webhook的ssl证书，方式如下：
   
   ```shell
   openssl genrsa -out webhook_pkey.pem 2048
   openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
   ```
   
   其中common name填写webhook域名或ip

2. `cp .env.example .env`填写环境变量参数

3. `pip3 install -r requirements.txt`安装所需的包

4. `python3 run.py`启动