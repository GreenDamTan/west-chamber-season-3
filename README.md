本项目是一个关于GFW 的半研究性项目，尝试提供可用的翻墙方案，并找出关于GFW 的一些统计数据。之前完全不依赖代理服务器的方案已经无效，已删除相关代码。

双向丢包
--------
服务器、客户端同时丢掉GFW 的干扰包。服务器上脚本 server.sh ，客户端脚本 client.sh. 如果路由器可以设置 iptables 防火墙(如Tomato 或 OpenWRT)，直接在路由器上设置即可：

    iptables -I FORWARD -p tcp -m tcp --tcp-flags RST RST -j DROP
    
目前这种方法还有问题。第一次丢包可以成功,但GFW把双方IP记入缓存; 第二次会被GFW发的SYN+ACK 干扰(一般而言这个干扰包会比服务器的先返回, 发现的特征是windows size 小于5000), 而且GFW会封锁被缓存住的正常的通信数据包,所以即使丢包也无法正常通信.
学术上, 这种攻击被定义为 Off-Path TCP Sequence Number Inference Attack [PDF](http://web.eecs.umich.edu/~zhiyunq/pub/oakland12_TCP_sequence_number_inference.pdf)
因此, 目前这种方式只能保证大概20秒内, 可以进行一次HTTP通信.

修改本地hosts文件
----------------
修改本地的 hosts 文件，并使用https 方式访问。参考[smarthosts](http://code.google.com/p/smarthosts/)项目。

6to4
----
Using a 6to4 tunnel, that you can get for free at he.net is one great way to avoid problems with the GFW. I configured the tunnel into my router, and all of my devices worked without  problem once I enabled ipv6 on them. I should note that this method was aways especially fast. 

反DNS污染
---------
最近GFW DNS 污染模块升级，以前简单粗暴的丢包方案不可用。可以参考 [ChinaDNS](https://github.com/clowwindy/ChinaDNS) 的实现。

TCP连接混淆
-----------
首先说明一下，[这东西很不靠谱](http://gfwrev.blogspot.com/2010/03/gfw.html)，容易受GFW 的更新而影响。感觉是，目前就kernet 项目效果还行。西厢的原始项目和Windows 移植现在都不好用。

其它工具
--------
* [shadowsocks](https://github.com/clowwindy/shadowsocks) 非常好用的加密代理工具，提供本地 SOCKS5 代理，依赖境外服务器使用。客户端和服务端都很稳定。
* [greatfire.org](https://greatfire.org/)
* [gfwrev.blogspot.com](http://gfwrev.blogspot.com/)
