### 新建一个环境
conda create --name webdriver python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

### 激活之
conda activate webdriver

### 安装依赖

pip install lightbus

作为一个服务端，当然是需要lightbus来暴露服务给整个集群的

参考：https://www.geeksforgeeks.org/driving-headless-chrome-with-python/

安装chrome那边的依赖

pip install selenium

### 写个测试程序试试

	import time
	  
	from selenium import webdriver
	  
	# initializing webdriver for Chrome
	driver = webdriver.Chrome()
	  
	# getting GeekForGeeks webpage
	driver.get('https://www.geeksforgeeks.org')
	  
	# sleep for 5 seconds just to see that
	# the browser was opened indeed
	time.sleep(5)
	  
	# closing browser
	driver.close()

### 报错找不到chrome
(webdriver) lemonhall@yuningdeMBP:~/webdriver$ python test1.py
Traceback (most recent call last):
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/selenium/webdriver/common/service.py", line 71, in start
    self.process = subprocess.Popen(cmd, env=self.env,
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/subprocess.py", line 858, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/subprocess.py", line 1704, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'chromedriver'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "test1.py", line 6, in <module>
    driver = webdriver.Chrome()
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/selenium/webdriver/chrome/webdriver.py", line 69, in __init__
    super().__init__(DesiredCapabilities.CHROME['browserName'], "goog",
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/selenium/webdriver/chromium/webdriver.py", line 89, in __init__
    self.service.start()
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/selenium/webdriver/common/service.py", line 81, in start
    raise WebDriverException(
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/home

### 下载
 wget https://chromedriver.storage.googleapis.com/104.0.5112.29/chromedriver_mac64.zip

 这东西好小，有一种不祥的预感，这货肯定是不包含chrome本身的

 所以还是要从chrome，headless那块开始入手

 解压之

 pwd一下

 /Users/lemonhall/webdriver

 配置一下PATH
 export PATH=/Users/lemonhall/webdriver:$PATH


 ### 安全问题

 再次python test1.py
 会弹出安全问题，到配置，安全与隐私里通过driver的安全性


### 版本匹配性报错。。。。额，好吧

 然后又报错了：
   File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/selenium/webdriver/remote/errorhandler.py", line 247, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 104
Current browser version is 103.0.5060.114 with binary path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

哦吼

wget https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_mac64.zip

OK,更换了driver，成功了

### headless

	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options

	# instance of Options class allows
	# us to configure Headless Chrome
	options = Options()

	# this parameter tells Chrome that
	# it should be run without UI (Headless)
	options.headless = True

	# initializing webdriver for Chrome with our options
	driver = webdriver.Chrome(options=options)

	# getting GeekForGeeks webpage
	driver.get('https://www.geeksforgeeks.org')

	# We can also get some information
	# about page in browser.
	# So let's output webpage title into
	# terminal to be sure that the browser
	# is actually running.
	print(driver.title)

	# close browser after our manipulations
	driver.close()

python test_headless.py

之前的例子竟然是真的打开了游览器，行吧，这次看看headless

	(webdriver) lemonhall@yuningdeMBP:~/webdriver$ python test_headless.py
	GeeksforGeeks | A computer science portal for geeks
	(webdriver) lemonhall@yuningdeMBP:~/webdriver$

好的，成功了

### 加入lightbus的配置文件

	# Root configuration
	bus:
	  # Bus configuration

	  schema:
	    # Schema configuration

	    transport:
	      # Transport selector config

	      redis:
	        url: "redis://192.168.50.233:18505/0"

	apis:
	  # API configuration listing

	  default:
	    # Api config

	    event_transport:
	      # Transport selector configuration
	      redis:
	        url: "redis://192.168.50.233:18505/0"

	    rpc_transport:
	      # Transport selector configuration
	      redis:
	        url: "redis://192.168.50.233:18505/0"

	    result_transport:
	      # Transport selector configuration
	      redis:
	        url: "redis://192.168.50.233:18505/0"

lightbus.yaml

### 又是配置全局的配置文件的地址

export LIGHTBUS_CONFIG="/Users/lemonhall/webdriver/lightbus.yaml"


### 加入__init__.py

声明自己是个模块

### 编写服务声明

	# File: bus.py
	import lightbus

	bus = lightbus.create()

	class HelloApi(lightbus.Api):

	    class Meta:
	        name = 'hello'

	    def world(self):
	        return "Hello World!"

	# Register this API with Lightbus. Lightbus will respond to 
	# remote procedure calls for registered APIs, as well as allow you 
	# as the developer to fire events on any registered APIs.
	bus.client.register_api(HelloApi())

以上算是例子，修改成以下类似

	# File: bus.py
	import lightbus
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options

	bus = lightbus.create()
	# instance of Options class allows
	# us to configure Headless Chrome
	options = Options()

	# this parameter tells Chrome that
	# it should be run without UI (Headless)
	options.headless = True

	# initializing webdriver for Chrome with our options
	driver = webdriver.Chrome(options=options)


	class getLantStatus(lightbus.Api):

	    class Meta:
	        name = 'getLantStatus'

	    def get(self):
	    	# getting GeekForGeeks webpage
			driver.get('https://www.geeksforgeeks.org')

			# We can also get some information
			# about page in browser.
			# So let's output webpage title into
			# terminal to be sure that the browser
			# is actually running.
			print(driver.title)
	        return driver.title

	# Register this API with Lightbus. Lightbus will respond to 
	# remote procedure calls for registered APIs, as well as allow you 
	# as the developer to fire events on any registered APIs.
	bus.client.register_api(getLantStatus())

### 注册并运行
lightbus run

### 报错
	Traceback (most recent call last):
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/bin/lightbus", line 5, in <module>
	    from lightbus.commands import lightbus_entry_point
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/__init__.py", line 1, in <module>
	    from lightbus.utilities.logging import configure_logging
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/utilities/logging.py", line 6, in <module>
	    from lightbus.config import Config
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/config/__init__.py", line 1, in <module>
	    from .config import Config
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/config/config.py", line 11, in <module>
	    from lightbus.schema.hints_to_schema import python_type_to_json_schemas, SCHEMA_URI
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/schema/__init__.py", line 1, in <module>
	    from .schema import Schema, Parameter, WildcardParameter
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/schema/schema.py", line 27, in <module>
	    from lightbus.transports.registry import SchemaTransportPoolType
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/transports/__init__.py", line 14, in <module>
	    from lightbus.transports.redis.rpc import RedisRpcTransport
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/transports/redis/__init__.py", line 1, in <module>
	    from lightbus.transports.redis.event import RedisEventTransport
	  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/transports/redis/event.py", line 19, in <module>
	    from aioredis import ConnectionClosedError, ReplyError
	ImportError: cannot import name 'ConnectionClosedError' from 'aioredis' (/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/aioredis/__init__.py)


又是这个

哦哦哦，这次终于找到问题了

需要 

* pip install aioredis==1.3.0

之前一直忘记记录这个问题了，下次直接用那个什么著名的包管理器，锁版本号

	(webdriver) lemonhall@yuningdeMBP:~/webdriver$ lightbus run
	MainThread | lightbus.creation              | Importing bus.py from bus
	MainThread | lightbus.creation              | Loading config from /Users/lemonhall/webdriver/lightbus.yaml
	MainThread | lightbus.commands.run          | Lightbus is setting up:
	           |                                |     ∙ service_name (set with -s or LIGHTBUS_SERVICE_NAME)  : mute-silence-687
	           |                                |     ∙ process_name (with with -p or LIGHTBUS_PROCESS_NAME) : cyvk
	           |                                |
	MainThread | lightbus.commands.run          | Default transports are setup as follows:
	           |                                |     ∙ RPC transport    : TransportPool @ redis://192.168.50.233:18505/0
	           |                                |     ∙ Result transport : TransportPool @ redis://192.168.50.233:18505/0
	           |                                |     ∙ Event transport  : TransportPool @ redis://192.168.50.233:18505/0
	           |                                |     ∙ Schema transport : TransportPool @ redis://192.168.50.233:18505/0
	           |                                |
	MainThread | lightbus.commands.run          | No plugins loaded
	MainThread | lightbus.client.bus_client     | Enabled features (3):
	           |                                |     ∙ rpcs
	           |                                |     ∙ events
	           |                                |     ∙ tasks
	           |                                |
	MainThread | lightbus.client.bus_client     | Disabled features (0):
	           |                                |
	MainThread | lightbus.client.bus_client     | APIs in registry (3):
	           |                                |     ∙ internal.state
	           |                                |     ∙ internal.metrics
	           |                                |     ∙ getLantStatus
	           |                                |
	MainThread | lightbus.client.bus_client     | Loaded the following remote schemas (4):
	           |                                |     ∙ getLantStatus
	           |                                |     ∙ hello
	           |                                |     ∙ internal.metrics
	           |                                |     ∙ internal.state
	           |                                |
	MainThread | lightbus.client.bus_client     | Loaded the following local schemas (4):
	           |                                |     ∙ internal.state
	           |                                |     ∙ internal.metrics
	           |                                |     ∙ getLantStatus
	           |                                |
	MainThread | lightbus.client.bus_client     | Executing before_worker_start & on_start hooks...
	MainThread | lightbus.client.bus_client     | Execution of before_worker_start & on_start hooks was successful


### 测试

再开一个console

* conda activate webdriver

激活一个lightbus环境

* cd webdriver

切换目录

* export LIGHTBUS_CONFIG="/Users/lemonhall/webdriver/lightbus.yaml"

配置文件声明好

* pip install bpython

安装一个shell 的依赖

* lightbus shell

运行失败，不搞了，这样

新建一个目录，叫caller

在下面新增一个__init__.py

然后再新建一个文件叫bus.py

	# File: ./caller/bus.py
	import lightbus

	bus = lightbus.create()

切到caller目录
* cd caller

* lightbus shell

ok，拿到一个shell了

然后敲入

* bus.getLantStatus.get()

	(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$ lightbus shell
	>>> bus.getLantStatus.get()
	'GeeksforGeeks | A computer science portal for geeks'
	>>>

ok，拿到预期的结果了

### 编写正式的消费者

	# Import our service's bus client
	from bus import bus

	# Call the check_password() procedure on our auth API
	status = bus.getLantStatus.get()

	print(status)

在caller目录下新建一个文件，我叫getStatus.py

	(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$ python getStatus.py
	GeeksforGeeks | A computer science portal for geeks
	(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$

好了，测试成功

### 守护进程化

新建好supervisord.conf

记住
	[inet_http_server]         ; inet (TCP) server disabled by default
	port=0.0.0.0:9001          ; ip_address:port specifier, *:port for all iface
	username=user              ; default is no username (open server)
	password=zii210^&@         ; default is no password (open server)


然后配置好

	[program:getLantStatus]
	command=lightbus run
	directory=/Users/lemonhall/webdriver
	stdout_logfile=/Users/lemonhall/webdriver/std_out.log
	stderr_logfile=/Users/lemonhall/webdriver/std_err.log
	environment=LIGHTBUS_CONFIG="/Users/lemonhall/webdriver/lightbus.yaml"

安装 pip install supervisor

* 前台运行来测试一下

supervisord -n -c supervisord.conf

* http://localhost:9001/logtail/getLantStatus/stderr

	8.50.233:18505/0[0m[0m, Schema transport:TransportPool @ [01mredis://192.168.50.233:18505/0[0m[0m
	MainThread | lightbus.commands.run          | No plugins loaded
	MainThread | lightbus.client.bus_client     | Enabled features (3): rpcs, events, tasks
	MainThread | lightbus.client.bus_client     | Disabled features (0): 
	MainThread | lightbus.client.bus_client     | APIs in registry (3): internal.state, internal.metrics, getLantStatus
	MainThread | lightbus.client.bus_client     | Loaded the following remote schemas (4): internal.metrics, hello, getLantStatus, internal.state
	MainThread | lightbus.client.bus_client     | Loaded the following local schemas (4): internal.state, internal.metrics, getLantStatus
	MainThread | lightbus.client.bus_client     | Executing before_worker_start & on_start hooks...
	MainThread | lightbus.client.bus_client     | Execution of before_worker_start & on_start hooks was successful
	MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 2.1 seconds
	MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 440.3 milliseconds
	MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 374.14 milliseconds
	MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 411.06 milliseconds
	MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 405.05 milliseconds

* 正式运行就更简单了，去掉n就行了

supervisord -c supervisord.conf

### github上传结果
	git init
	git add .
	git commit -m "first commit"
	git branch -M 'main'
	git remote add origin git@github.com:lemonhall/headlessStatus_checker.git
	git push -u origin 'main'


### 项目地址
https://github.com/lemonhall/headlessStatus_checker


### 启动本机的docker desktop，这东西的依赖可不是一般的多

https://registry.hub.docker.com/layers/ubuntu/library/ubuntu/20.04/images/sha256-b2339eee806d44d6a8adc0a790f824fb71f03366dd754d400316ae5a7e3ece3e?context=explore

docker pull ubuntu:20.04

抓取一个特定的ubuntu版本


* apt update
更新一下

装个 vim

apt install vim

### 改镜像的源

https://mirror.tuna.tsinghua.edu.cn/help/ubuntu/
改用清华的源，否则太慢了

vim /etc/apt/sources.list
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse

apt update


### apt报错了
https://serverfault.com/questions/1093511/apt-get-update-failing-because-of-certificate-validation

我大概明白为啥报错了

是拉错包了

重来


docker pull ubuntu:jammy


我擦，又报错？

docker pull ubuntu

apt install ca-certificates

cp /etc/apt/sources.list /etc/apt/sources.list.bak

还是备份一下吧

OK,这次正常了，看来确实是需要
apt upgrade
以及
apt install ca-certificates
先
真痛苦


### 镜像正常化一下

unminimize

### 安装python3
* apt install python3

这家伙竟然只能这么装

### 安装 pip
* apt install pip

### 容器->镜像化
https://www.douban.com/note/831572686/?_i=8323729uSf06nF


	(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$ docker ps -a
	CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS                      PORTS     NAMES
	295547b68b8d   ubuntu:latest                       "bash"                   15 minutes ago   Exited (137) 1 second ago             beautiful_rubin
	8bda88011d0f   k8slens/lens-dd-extension-k0s:dev   "/sbin/tini -- /bin/…"   2 days ago       Exited (143) 2 days ago               lens-k8s
	(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$

* docker ps -a

* docker commit -m "ubuntu with tsinghua source and python/pip install" -a "lemonhall" 295547b68b8d lemonhall/ubuntu_python:v1

提交容器到镜像


## push的小技巧

首先需要在自己的空间下build
docker build -t lemonhall/apns:v1 .
docker login
docker push lemonhall/apns:v1

这样就能成功的push了

参考这些push小技巧，那么就有了
docker push lemonhall/ubuntu_python:v1

然后我就可以把这个镜像推到我个人的库下面去了

简单多了

这样之后我待会写Dockerfile的时候就可以写成

FROM lemonhall/ubuntu_python:v1

其实就是暂存一下工作，不过这个镜像是方便多了，否则总是从ubuntu的官方镜像开始，太可怕了

远方的库就只要234MB，加上基础包，就很小

### 使用新的镜像来run一个新的容器

### 接下来安装chrome

apt install -y chromium-browser

### 安装git
apt install -y git


### clone刚才的代码
git clone https://github.com/lemonhall/headlessStatus_checker.git

cd headlessStatus_checker/

### 安装依赖
pip install selenium


### 报错
	root@f1c05a4d5300:~/headlessStatus_checker# python3 test1.py
	Traceback (most recent call last):
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/common/service.py", line 71, in start
	    self.process = subprocess.Popen(cmd, env=self.env,
	  File "/usr/lib/python3.10/subprocess.py", line 966, in __init__
	    self._execute_child(args, executable, preexec_fn, close_fds,
	  File "/usr/lib/python3.10/subprocess.py", line 1842, in _execute_child
	    raise child_exception_type(errno_num, err_msg, err_filename)
	FileNotFoundError: [Errno 2] No such file or directory: 'chromedriver'

	During handling of the above exception, another exception occurred:

	Traceback (most recent call last):
	  File "/root/headlessStatus_checker/test1.py", line 6, in <module>
	    driver = webdriver.Chrome()
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/chrome/webdriver.py", line 69, in __init__
	    super().__init__(DesiredCapabilities.CHROME['browserName'], "goog",
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/chromium/webdriver.py", line 89, in __init__
	    self.service.start()
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/common/service.py", line 81, in start
	    raise WebDriverException(
	selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/home


### 报错

	root@f1c05a4d5300:~/headlessStatus_checker# chromium-browser --version

	Command '/usr/bin/chromium-browser' requires the chromium snap to be installed.
	Please install it with:

	snap install chromium

	root@f1c05a4d5300:~/headlessStatus_checker#

	root@f1c05a4d5300:~/headlessStatus_checker#

### snap install chromium 报错

	root@f1c05a4d5300:~/headlessStatus_checker# snap install chromium
	error: cannot communicate with server: Post "http://localhost/v2/snaps/chromium": dial unix /run/snapd.socket: connect: no such file or directory


root@f1c05a4d5300:~/headlessStatus_checker# systemctl unmask snapd.service
root@f1c05a4d5300:~/headlessStatus_checker# systemctl enable snapd.service
root@f1c05a4d5300:~/headlessStatus_checker# systemctl start snapd.service
System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down
root@f1c05a4d5300:~/headlessStatus_checker#

参考：https://askubuntu.com/questions/1258137/cannot-communicate-with-server-post-http-localhost-v2-apps-dial-unix-run-sn

试图解决失败，需要安装systemctl先

apt install systemctl
apt install snap snapd

root@f1c05a4d5300:~/headlessStatus_checker# systemctl status snapd.service
snapd.service -
    Loaded: masked (None, masked)
    Active: inactive (dead)
root@f1c05a4d5300:~/headlessStatus_checker#

哎，看来又是依赖冲突了

apt install snapd

### 搁置
wget https://chromedriver.storage.googleapis.com/104.0.5112.29/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

export PATH=/root/headlessStatus_checker:$PATH


### 报错

root@f1c05a4d5300:~/headlessStatus_checker# python3 test_headless.py
Traceback (most recent call last):
  File "/root/headlessStatus_checker/test_headless.py", line 13, in <module>
    driver = webdriver.Chrome(options=options)
  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/chrome/webdriver.py", line 69, in __init__
    super().__init__(DesiredCapabilities.CHROME['browserName'], "goog",
  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/chromium/webdriver.py", line 89, in __init__
    self.service.start()
  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/common/service.py", line 98, in start
    self.assert_process_still_running()
  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/common/service.py", line 110, in assert_process_still_running
    raise WebDriverException(
selenium.common.exceptions.WebDriverException: Message: Service chromedriver unexpectedly exited. Status code was: 127

root@f1c05a4d5300:~/headlessStatus_checker#



### 直接运行
root@f1c05a4d5300:~/headlessStatus_checker# chromedriver
chromedriver: error while loading shared libraries: libnss3.so: cannot open shared object file: No such file or directory
root@f1c05a4d5300:~/headlessStatus_checker#

### 安装依赖

apt install libnss3

就是缺了一个叫libnss3的东西

	root@f1c05a4d5300:~/headlessStatus_checker# chromedriver
	Starting ChromeDriver 103.0.5060.53 (a1711811edd74ff1cf2150f36ffa3b0dae40b17f-refs/branch-heads/5060@{#853}) on port 9515
	Only local connections are allowed.
	Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
	[1658326654.842][SEVERE]: bind() failed: Cannot assign requested address (99)
	ChromeDriver was started successfully.
	^C

成功运行

### 报错

	root@f1c05a4d5300:~/headlessStatus_checker# python3 test_headless.py
	Traceback (most recent call last):
	  File "/root/headlessStatus_checker/test_headless.py", line 13, in <module>
	    driver = webdriver.Chrome(options=options)
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/chrome/webdriver.py", line 69, in __init__
	    super().__init__(DesiredCapabilities.CHROME['browserName'], "goog",
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/chromium/webdriver.py", line 92, in __init__
	    super().__init__(
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/remote/webdriver.py", line 277, in __init__
	    self.start_session(capabilities, browser_profile)
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/remote/webdriver.py", line 370, in start_session
	    response = self.execute(Command.NEW_SESSION, parameters)
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/remote/webdriver.py", line 435, in execute
	    self.error_handler.check_response(response)
	  File "/usr/local/lib/python3.10/dist-packages/selenium/webdriver/remote/errorhandler.py", line 247, in check_response
	    raise exception_class(message, screen, stacktrace)
	selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary
	Stacktrace:
	#0 0x55fe1f11bb13 <unknown>
	#1 0x55fe1ef22688 <unknown>
	#2 0x55fe1ef44e78 <unknown>
	#3 0x55fe1ef425aa <unknown>
	#4 0x55fe1ef7d64a <unknown>
	#5 0x55fe1ef777a3 <unknown>
	#6 0x55fe1ef4d0ea <unknown>
	#7 0x55fe1ef4e225 <unknown>
	#8 0x55fe1f1632dd <unknown>
	#9 0x55fe1f1672c7 <unknown>
	#10 0x55fe1f14d22e <unknown>
	#11 0x55fe1f1680a8 <unknown>
	#12 0x55fe1f141bc0 <unknown>
	#13 0x55fe1f1846c8 <unknown>
	#14 0x55fe1f184848 <unknown>
	#15 0x55fe1f19ec0d <unknown>
	#16 0x7f15a85ffb43 <unknown>

	root@f1c05a4d5300:~/headlessStatus_checker#

### 安装一个chrome算了
https://tecadmin.net/setup-selenium-with-python-on-ubuntu-debian/

* 安装key
wget -nc https://dl-ssl.google.com/linux/linux_signing_key.pub 
cat linux_signing_key.pub | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/linux_signing_key.gpg  >/dev/null 

cat linux_signing_key.pub | gpg --dearmor | tee /etc/apt/trusted.gpg.d/linux_signing_key.gpg  >/dev/null 

* 加入源

sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/chrome.list' 

* 安装
apt update
apt install google-chrome-stable


* 看一下版本号
root@f1c05a4d5300:~/headlessStatus_checker# google-chrome --version
Google Chrome 103.0.5060.134
root@f1c05a4d5300:~/headlessStatus_checker#

* 重新下一下104的驱动
wget https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_linux64.zip


### 试试新的例子
pip install selenium webdriver-manager

	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.chrome.service import Service
	from webdriver_manager.chrome import ChromeDriverManager
	 
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
	 
	driver.get("https://python.org")
	print(driver.title)
	driver.close()

root@f1c05a4d5300:~/headlessStatus_checker# python3 test3.py

Welcome to Python.org
root@f1c05a4d5300:~/headlessStatus_checker#


成功，我看大概率是另外两个开关让这事儿搞定的

### 把其它的依赖也搞定

pip install lightbus

降级aio
pip install aioredis==1.3.0

export LIGHTBUS_CONFIG="/root/headlessStatus_checker/lightbus.yaml"

### 修改bus.py

	# File: bus.py
	import lightbus
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.chrome.service import Service
	from webdriver_manager.chrome import ChromeDriverManager

	bus = lightbus.create()

	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


	class getLantStatus(lightbus.Api):

	    class Meta:
	        name = 'getLantStatus'

	    def get(self):
	        driver.get('https://www.geeksforgeeks.org')
	        print(driver.title)
	        return driver.title

	# Register this API with Lightbus. Lightbus will respond to 
	# remote procedure calls for registered APIs, as well as allow you 
	# as the developer to fire events on any registered APIs.
	bus.client.register_api(getLantStatus())

### 试运行

lightbus run

### 又又又又报错

Traceback (most recent call last):
  File "/usr/local/bin/lightbus", line 8, in <module>
    sys.exit(lightbus_entry_point())
  File "/usr/local/lib/python3.10/dist-packages/lightbus/commands/__init__.py", line 31, in lightbus_entry_point
    run_command_from_args()
  File "/usr/local/lib/python3.10/dist-packages/lightbus/commands/__init__.py", line 61, in run_command_from_args
    parsed_args.func(parsed_args, config, plugin_registry, **extra)
  File "/usr/local/lib/python3.10/dist-packages/lightbus/commands/run.py", line 66, in handle
    self._handle(args, config, plugin_registry)
  File "/usr/local/lib/python3.10/dist-packages/lightbus/commands/run.py", line 133, in _handle
    bus.client.run_forever()
  File "/usr/local/lib/python3.10/dist-packages/lightbus/client/bus_client.py", line 151, in run_forever
    block(self.start_worker())
  File "/usr/local/lib/python3.10/dist-packages/lightbus/utilities/async_tools.py", line 44, in block
    raise e
  File "/usr/local/lib/python3.10/dist-packages/lightbus/utilities/async_tools.py", line 39, in block
    val = loop.run_until_complete(coroutine)
  File "/usr/lib/python3.10/asyncio/base_events.py", line 646, in run_until_complete
    return future.result()
  File "/usr/local/lib/python3.10/dist-packages/lightbus/client/bus_client.py", line 207, in start_worker
    await self.schema.add_api(api)
  File "/usr/local/lib/python3.10/dist-packages/lightbus/schema/schema.py", line 80, in add_api
    await self.schema_transport.store(api.meta.name, schema, ttl_seconds=self.max_age_seconds)
  File "/usr/local/lib/python3.10/dist-packages/lightbus/transports/pool.py", line 167, in fn_pool_wrapper
    return await getattr(transport, item)(*args, **kwargs)
  File "/usr/local/lib/python3.10/dist-packages/lightbus/transports/redis/schema.py", line 43, in store
    with await self.connection_manager() as redis:
  File "/usr/local/lib/python3.10/dist-packages/lightbus/transports/redis/utilities.py", line 166, in connection_manager
    self._redis_pool = await aioredis.create_redis_pool(**self.connection_parameters)
  File "/usr/local/lib/python3.10/dist-packages/aioredis/commands/__init__.py", line 188, in create_redis_pool
    pool = await create_pool(address, db=db,
  File "/usr/local/lib/python3.10/dist-packages/aioredis/pool.py", line 49, in create_pool
    pool = cls(address, db, password, encoding,
  File "/usr/local/lib/python3.10/dist-packages/aioredis/pool.py", line 94, in __init__
    self._cond = asyncio.Condition(lock=Lock(loop=loop), loop=loop)
  File "/usr/lib/python3.10/asyncio/locks.py", line 78, in __init__
    super().__init__(loop=loop)
  File "/usr/lib/python3.10/asyncio/mixins.py", line 17, in __init__
    raise TypeError(
TypeError: As of 3.10, the *loop* parameter was removed from Lock() since it is no longer necessary
root@f1c05a4d5300:~/headlessStatus_checker#


核心就是这一句：
TypeError: As of 3.10, the *loop* parameter was removed from Lock() since it is no longer necessary



### 试图解决
参考资料：https://zhuanlan.zhihu.com/p/45329974

apt remove python3

apt install software-properties-common -y

add-apt-repository ppa:deadsnakes/ppa -y

apt update

python3.8 --version


### 重建链接
root@f1c05a4d5300:~/headlessStatus_checker# which python3
/usr/bin/python3
root@f1c05a4d5300:~/headlessStatus_checker# ls /usr/bin/python3
/usr/bin/python3
root@f1c05a4d5300:~/headlessStatus_checker# ls -l /usr/bin/python3
lrwxrwxrwx 1 root root 10 Mar 25 20:41 /usr/bin/python3 -> python3.10
root@f1c05a4d5300:~/headlessStatus_checker# which python3.8
/usr/bin/python3.8
root@f1c05a4d5300:~/headlessStatus_checker#



root@f1c05a4d5300:~/headlessStatus_checker# ln /usr/bin/python3 /usr/bin/python3.8
ln: failed to create hard link '/usr/bin/python3.8': File exists
root@f1c05a4d5300:~/headlessStatus_checker#

alias python3=python3.8

### 选择优先级

参考：https://stackoverflow.com/questions/71034111/how-to-set-default-python3-to-python-3-9-instead-of-python-3-8-in-ubuntu-20-04-l

update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2

update-alternatives --config python3

然后手工选择好


### 继续报错

root@f1c05a4d5300:~/headlessStatus_checker# lightbus run
Traceback (most recent call last):
  File "/usr/local/bin/lightbus", line 5, in <module>
    from lightbus.commands import lightbus_entry_point
ModuleNotFoundError: No module named 'lightbus'
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker# pip
bash: /usr/bin/pip: No such file or directory
root@f1c05a4d5300:~/headlessStatus_checker# pip3
bash: pip3: command not found
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker#
root@f1c05a4d5300:~/headlessStatus_checker#

### 安装pip
https://pip.pypa.io/en/stable/installation/

wget https://bootstrap.pypa.io/get-pip.py

### 报错
https://askubuntu.com/questions/1239829/modulenotfounderror-no-module-named-distutils-util

root@f1c05a4d5300:~/headlessStatus_checker# python3.8 get-pip.py
Traceback (most recent call last):
  File "get-pip.py", line 33593, in <module>
    main()
  File "get-pip.py", line 135, in main
    bootstrap(tmpdir=tmpdir)
  File "get-pip.py", line 111, in bootstrap
    monkeypatch_for_cert(tmpdir)
  File "get-pip.py", line 92, in monkeypatch_for_cert
    from pip._internal.commands.install import InstallCommand
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/commands/__init__.py", line 9, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/cli/base_command.py", line 15, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/cli/cmdoptions.py", line 24, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/cli/parser.py", line 12, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/configuration.py", line 26, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/utils/logging.py", line 29, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/utils/misc.py", line 42, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/locations/__init__.py", line 14, in <module>
  File "<frozen zipimport>", line 259, in load_module
  File "/tmp/tmp9le4dwj0/pip.zip/pip/_internal/locations/_distutils.py", line 9, in <module>
ModuleNotFoundError: No module named 'distutils.cmd'
root@f1c05a4d5300:~/headlessStatus_checker# apt-get install python3-distutils

### 解决之

apt install python3.8-distutils

python3.8 get-pip.py

### 重新以3.8的身份安装lightbus

pip3 install lightbus

降级
pip3 install aioredis==1.3.0


### 报错
root@f1c05a4d5300:~/headlessStatus_checker# lightbus run
MainThread | lightbus.creation              | Importing bus.py from bus
Failed to import bus module 'bus'.

    Perhaps you need to set the LIGHTBUS_MODULE environment variable? Alternatively you may need to configure your PYTHONPATH.

    Error was: No module named 'selenium'
root@f1c05a4d5300:~/headlessStatus_checker#

### 解决之

pip install webdriver_manager
pip install selenium


### 成功
root@f1c05a4d5300:~/headlessStatus_checker# lightbus run
MainThread | lightbus.creation              | Importing bus.py from bus
MainThread | lightbus.creation              | Loading config from /root/headlessStatus_checker/lightbus.yaml

MainThread | lightbus.commands.run          | Lightbus is setting up:
           |                                |     ∙ service_name (set with -s or LIGHTBUS_SERVICE_NAME)  : wandering-moon-880
           |                                |     ∙ process_name (with with -p or LIGHTBUS_PROCESS_NAME) : stev
           |                                |
MainThread | lightbus.commands.run          | Default transports are setup as follows:
           |                                |     ∙ RPC transport    : TransportPool @ redis://192.168.50.233:18505/0
           |                                |     ∙ Result transport : TransportPool @ redis://192.168.50.233:18505/0
           |                                |     ∙ Event transport  : TransportPool @ redis://192.168.50.233:18505/0
           |                                |     ∙ Schema transport : TransportPool @ redis://192.168.50.233:18505/0
           |                                |
MainThread | lightbus.commands.run          | No plugins loaded
MainThread | lightbus.client.bus_client     | Enabled features (3):
           |                                |     ∙ rpcs
           |                                |     ∙ events
           |                                |     ∙ tasks
           |                                |
MainThread | lightbus.client.bus_client     | Disabled features (0):
           |                                |
MainThread | lightbus.client.bus_client     | APIs in registry (3):
           |                                |     ∙ internal.state
           |                                |     ∙ internal.metrics
           |                                |     ∙ getLantStatus
           |                                |
MainThread | lightbus.client.bus_client     | Loaded the following remote schemas (4):
           |                                |     ∙ internal.metrics
           |                                |     ∙ hello
           |                                |     ∙ getLantStatus
           |                                |     ∙ internal.state
           |                                |
MainThread | lightbus.client.bus_client     | Loaded the following local schemas (4):
           |                                |     ∙ internal.state
           |                                |     ∙ internal.metrics
           |                                |     ∙ getLantStatus
           |                                |
MainThread | lightbus.client.bus_client     | Executing before_worker_start & on_start hooks...
MainThread | lightbus.client.bus_client     | Execution of before_worker_start & on_start hooks was successful


太不容易了，说白了就是lightbus依赖了3.8

暂时不想去解决它的依赖问题

### 笔记本上测试之
conda activate webdriver

cd werdriver
cd caller

export LIGHTBUS_CONFIG="/Users/lemonhall/webdriver/lightbus.yaml"



服务端：
MainThread | lightbus.client.bus_client     | Executing before_worker_start & on_start hooks...
MainThread | lightbus.client.bus_client     | Execution of before_worker_start & on_start hooks was successful
GeeksforGeeks | A computer science portal for geeks
MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 5.1 seconds


正常返回了内容了

但是调用端

(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$ python3 getStatus.py
Connection <RedisConnection [db:0]> has pending commands, closing it.
Traceback (most recent call last):
  File "getStatus.py", line 5, in <module>
    status = bus.getLantStatus.get()
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/path.py", line 75, in __call__
    return self.call(*args, **kwargs)
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/path.py", line 86, in call
    return block(self.call_async(*args, **kwargs, bus_options=bus_options), timeout=rpc_timeout)
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/utilities/async_tools.py", line 44, in block
    raise e
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/utilities/async_tools.py", line 41, in block
    val = loop.run_until_complete(asyncio.wait_for(coroutine, timeout=timeout))
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/asyncio/base_events.py", line 616, in run_until_complete
    return future.result()
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/asyncio/tasks.py", line 494, in wait_for
    return fut.result()
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/path.py", line 102, in call_async
    return await self.client.call_rpc_remote(
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/client/bus_client.py", line 65, in _wrapped
    result = await fn(self, *args, **kwargs)
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/client/bus_client.py", line 371, in call_rpc_remote
    return await self.rpc_result_client.call_rpc_remote(
  File "/Users/lemonhall/opt/anaconda3/envs/webdriver/lib/python3.8/site-packages/lightbus/client/subclients/rpc_result.py", line 129, in call_rpc_remote
    raise LightbusTimeout(
lightbus.exceptions.LightbusTimeout: Timeout when calling RPC getLantStatus.get after waiting for 5.03 seconds. It is possible no Lightbus process is serving this API, or perhaps it is taking too long to process the request. In which case consider raising the 'rpc_timeout' config option.
(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$


### 解决timeout
在lightbus.yaml里面

apis:
  # API configuration listing

  default:
    # Api config
    rpc_timeout : 15


将api的timeout时间调配为15秒

参考官方文档：https://lightbus.org/latest/reference/configuration/#api-configuration-listing


### 安装好supervisor

pip3 install supervisor

修改config

[program:getLantStatus]
command=lightbus run
directory=/root/headlessStatus_checker
stdout_logfile=/root/headlessStatus_checker/std_out.log
stderr_logfile=/root/headlessStatus_checker/std_err.log
environment=LIGHTBUS_CONFIG="/root/headlessStatus_checker/lightbus.yaml"

前台模式测试一下

supervisord -n -c supervisord.conf


好了，没有问题了，继续搞事情

## 再一次容器镜像化

### 容器->镜像化
https://www.douban.com/note/831572686/?_i=8323729uSf06nF


	(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$ docker ps -a
	CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS                      PORTS     NAMES
	295547b68b8d   ubuntu:latest                       "bash"                   15 minutes ago   Exited (137) 1 second ago             beautiful_rubin
	8bda88011d0f   k8slens/lens-dd-extension-k0s:dev   "/sbin/tini -- /bin/…"   2 days ago       Exited (143) 2 days ago               lens-k8s
	(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$

* docker ps -a

* docker commit -m "ubuntu with tsinghua source and python/pip install" -a "lemonhall" 295547b68b8d lemonhall/ubuntu_python:v1

提交容器到镜像


## push的小技巧

首先需要在自己的空间下build
docker build -t lemonhall/apns:v1 .
docker login
docker push lemonhall/apns:v1

这样就能成功的push了

参考这些push小技巧，那么就有了
docker push lemonhall/ubuntu_python:v1

然后我就可以把这个镜像推到我个人的库下面去了

简单多了

这样之后我待会写Dockerfile的时候就可以写成

FROM lemonhall/ubuntu_python:v1

其实就是暂存一下工作，不过这个镜像是方便多了，否则总是从ubuntu的官方镜像开始，太可怕了

远方的库就只要234MB，加上基础包，就很小

### ps -a
(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$ docker ps -a
CONTAINER ID   IMAGE                               COMMAND                  CREATED       STATUS                    PORTS     NAMES
f1c05a4d5300   lemonhall/ubuntu_python:v1          "bash"                   2 hours ago   Up 2 hours                          cranky_wescoff
8bda88011d0f   k8slens/lens-dd-extension-k0s:dev   "/sbin/tini -- /bin/…"   2 days ago    Exited (143) 2 days ago             lens-k8s
(webdriver) lemonhall@yuningdeMBP:~/webdriver/caller$

### docker commit

docker commit -m "ubuntu with chrome/selenium/lightbus " -a "lemonhall" f1c05a4d5300 lemonhall/ubuntu_selenium:v1

得到了一个1.65G的镜像

### docker push

docker login
docker push lemonhall/ubuntu_selenium:v1


### 修改bus.py
https://selenium-python.readthedocs.io/

	# File: bus.py
	import lightbus
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.chrome.service import Service
	from webdriver_manager.chrome import ChromeDriverManager
	from selenium.webdriver.common.by import By

	bus = lightbus.create()

	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


	class getLantStatus(lightbus.Api):

	    class Meta:
	        name = 'getLantStatus'

	    def get(self):
	        driver.get("http://192.168.50.233:13233/#/replica")
	        lantern_status_element = driver.find_element(By.ID,"lantern__status_module")
	        if lantern_status_element:
	            lantern_status_text = lantern_status_element.find_element(By.CLASS_NAME, "text")
	            if lantern_status_text:
	                #print(lantern_status_text)
	                #get_methods(lantern_status_text)
	                print(lantern_status_text.text)
	                return lantern_status_text.text
	            else:
	                return "unknown status"
	        else:
	            return "unknown status"
	# Register this API with Lightbus. Lightbus will respond to
	# remote procedure calls for registered APIs, as well as allow you
	# as the developer to fire events on any registered APIs.
	bus.client.register_api(getLantStatus())



MainThread | lightbus.client.bus_client     | Executing before_worker_start & on_start hooks...
MainThread | lightbus.client.bus_client     | Execution of before_worker_start & on_start hooks was successful
已连接，没有管理系统代理
MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 1.57 seconds
已连接，没有管理系统代理
MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed getLantStatus.get in 586.69 milliseconds


## 非常好，运行都能控制在2秒以内了，这就很好

### 部署到群晖里面去

打开控制面板，开22端口，拿到console
ssh lemonhall@192.168.50.233

### 拉去最新的镜像
sudo docker pull lemonhall/ubuntu_python:v1
sudo docker pull lemonhall/ubuntu_selenium:v1

### 拿到一个bash
在群晖的ssh里面，拿到，这样才好复制粘贴

docker ps -a

lemonhall@nas16t:~$ sudo docker ps -a
Password:
CONTAINER ID   IMAGE                                  COMMAND                  CREATED         STATUS                     PORTS                                                                                                                      NAMES
bdaaf7285b73   lemonhall/ubuntu_selenium:v1           "bash"                   9 minutes ago   Up 9 minutes               0.0.0.0:14901->9001/tcp                                                                                                    getLanternStatus
3eb441e3fc7d   ubuntu:latest                          "bash"                   17 hours ago    Up 14 hours                0.0.0.0:4322->22/tcp, 0.0.0.0:13128->3128/tcp, 0.0.0.0:13129->3129/tcp, 0.0.0.0:13233->8080/tcp, 0.0.0.0:13901->9001/tcp   lantern
caf8080cd10c   tzahi12345/youtubedl-material:latest   "/app/entrypoint.sh …"   22 hours ago    Up 21 hours                17442/tcp


* sudo docker exec -it bdaaf7285b73 bash

### 进程太多了，有问题

* sudo docker exec -it bdaaf7285b73 bash

### 最后发现没啥问题。。。。。

chrome开起来就是4、5个进程，高消耗啊






