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

### docker化