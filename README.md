本项目是一个关于GFW 的半研究性项目，尝试提供可用的翻墙方案，并找出关于GFW 的一些统计数据。之前完全不依赖代理服务器的方案已经无效，已删除相关代码。

jjproxy
-------
[jjproxy](https://github.com/liruqi/jjproxy) 可以直接用标准的HTTP/HTTPS代理服务器翻墙，需要自行搭建。

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
----using a 6to4 tunnel, that you can get for free at he.net is one great way to avoid problems with the gfw. I configured the tunnel into my router, and all of my devices worked without  problem oncee i enabled ipv6 on them.  i should note that this method was aways especially fast. 
 
反DNS污染
-------
修改hosts 文件部分解决了污染问题, 但是很可能不全. 要彻底解决DNS污染，设置国外的DNS 服务器，并本机丢弃GFW的 DNS伪包。

    a) 国外DNS服务器。大家比较熟悉的可能是[Google Public DNS](http://code.google.com/speed/public-dns/)。但是Google DNS经常出问题。先推荐两个，台湾中华电信的168.95.1.1 和 [OpenDNS](http://www.opendns.com/), 还不行，那就上午搜一个国外的DNS。

    b) 丢弃DNS伪包。
    建议使用 [ChinaDNS](https://github.com/clowwindy/ChinaDNS)
    有 iptables 的 Linux 环境带u32模块的话，可以直接用本项目中的 client.sh。 也可以尝试原始的[西厢项目](http://code.google.com/p/scholarzhang)，具体操作看西厢的文档。

其它值得尝试的方法：[如何本地避免GFW的DNS污染](http://liruqi.info/post/28775426009/how-to-avoid-dns-hijack-locally)

TCP连接混淆
-----------
首先说明一下，[这东西很不靠谱](http://gfwrev.blogspot.com/2010/03/gfw.html)，容易受GFW 的更新而影响。感觉是，目前就kernet 项目效果还行。西厢的原始项目和Windows 移植现在都不好用。

其它工具
--------
* [fqrouter](http://fqrouter.com/) 强大的开源翻墙工具，而且有详细的技术文档。测试过Android 版本，免配置，很好用。
* [shadowsocks](https://github.com/clowwindy/shadowsocks) 非常好用的加密代理工具，提供本地 SOCKS5 代理，依赖境外服务器使用。客户端和服务端都很稳定。
* [greatfire.org](https://greatfire.org/)
