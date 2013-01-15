项目目的
--------
* 不依赖代理服务器的本地翻墙代理工具。
* [Follow up](https://plus.google.com/b/108661470402896863593/)

使用方法
--------

* Linux/Mac

    1. 下载项目代码: [zip](https://github.com/liruqi/west-chamber-season-3/zipball/master)
    2. 解压缩，打开终端，cd 到代码目录，cd west-chamber-proxy; 启动代理：./wcproxy start；关闭代理：./wcproxy stop。
    3. 把浏览器HTTP/HTTPS 代理设置为 127.0.0.1:1998，或者使用pac 脚本设置自动代理。

* Windows
    
    尚不支持.

    1. 丢掉RST包. 尚无相关工具, 自己想办法.
    2. 下载 python 2.7，[32位](http://python.org/ftp/python/2.7.2/python-2.7.2.msi) / [64位](http://python.org/ftp/python/2.7.2/python-2.7.2.amd64.msi) ，然后下载[代码](https://github.com/liruqi/west-chamber-season-3/zipball/master)，解压缩，进入 west-chamber-proxy 文件夹，双击 westchamberproxy.py。
    3. 把浏览器HTTP/HTTPS 代理设置为 127.0.0.1:1998，或者使用pac 脚本设置自动代理。

* iOS/Android
    
    尚不支持. 可以尝试在局域网内的其它PC设备上安装本代理，然后把 iOS 设备的 HTTP 代理设置到该设备上。（或者在国内有服务器的同学，自己搭建HTTP 代理）

* SSL证书

    如果希望HTTPS代理正常使用，在Windows上用管理员权限、Mac 上用root 权限执行本代理即可。

代理设置
--------

* 浏览器代理设置
    做了一个 [.pac 文件](https://raw.github.com/liruqi/west-chamber-season-3/master/west-chamber-proxy/SwitchyPac.pac)。下载这个pac 文件，然后在浏览器代理设置中导入即可, IE, Firefox, Safari 都可以设置自动代理配置。

* Chrome浏览器+SwitchySharp扩展

    Chrome可以直接在高级选项中设置代理服务器，不过这样Chrome会修改系统的代理设置. 要实现Chrome自动代理配置，可以使用switchysharp扩展.
    首先安装[SwitchySharp](https://chrome.google.com/webstore/detail/dpplabbmogkhghncfbfdeeokoefdjegm), 安装后的设置：
   
    1. 在switchysharp选项页面，点击后面的导入/导出 -> “在线恢复备份”后面的输入框粘贴进下面的链接 http://west-chamber-season-3.googlecode.com/files/SwitchyOptions.bak
    2. 点击在线恢复备份 -> 确定 
    3. 点击SwitchySharp扩展图标 -> 自动切换模式

    到此浏览器代理配置成功。部分配置项也可以在网页上修改，直接打开代理地址即可（如 http://127.0.0.1:1998）

开发者
------
* [LIRUQI](http://liruqi.info)

代理原理
--------

1. 对抗关键词过滤/IP封锁: 轮训多个HTTP服务器, 丢RESET包
2. 对抗DNS污染: 修改PyDNS 库，实现丢弃GFW DNS 伪包。

问题反馈
--------
在[这里](https://github.com/liruqi/west-chamber-season-3/issues) 反馈各种问题。 

软件更新
-------
日常会有配置文件更新。如果有程序的更新，会在下载页面中给出。

TODO
----
* [ALL] 非Linux/Mac 系统的支持

UPDATE LOG
---
* 2011-11-23 解决android 客户端的远程 dns 解析的问题。
* 2011-11-24 对于IP被封锁的站点，走网页代理。
* 2012-01-08 联通的WLAN热点下失效的问题，联通自己解决了。[ref](http://weibo.com/1641981222/xFx46sR4c)
* 2012-01-05 HTTPS 支持。
* 2012-01-28 Windows 平台支持；国内站点 Comet 连接，停止重定向到网页代理。
* 2012-01-31 停止维护chrome extension, 而是类似于goagent，直接提供代理程序，以及 SwitchySharp 备份。
* 2012-02-24 修复Google plus 链接重定向错误 (plus.url.google.com => plus.url.google.com.hk)
* 2012-03-17 代码重构。python 脚本中去掉了进程控制，增加了多个命令行参数，进程控制由shell 脚本实现。 
* 2012-04-14 DNS解析结果中，移除被GFW 封锁的IP。
* 2012-04-14 支持UDP方式DNS解析，并丢弃GFW伪包。
* 2012-04-24 基本完成与GoAgent 的整合，直连失败后会走GoAgent 代理。
* 2013-01-08 放弃HTTP注入/GoAgent, 直接丢RESET包并轮训HTTP Proxy

