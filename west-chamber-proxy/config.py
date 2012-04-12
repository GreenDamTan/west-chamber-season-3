#!/usr/bin/env python
# -*- coding: utf-8 -*-

gConfig = {
    "VERSION" : "20120325",
    "PROXY_SERVER" : "http://annjonescnch.appspot.com/",
    "PROXY_PASSWD" : "",
    #proxy without any content rewrite, to fetch IP blocked sites
    "PROXY_SERVER_SIMPLE" : "westchamberproxy.appspot.com",
    "BLOCKED_DOMAINS_URI" : "https://raw.github.com/liruqi/west-chamber-season-3/master/west-chamber-proxy/status/timedout.txt",
    "REMOTE_DNS" : "168.95.1.1",
    "SKIP_LOCAL_RESOLV" : False,
    "REDIRECT_DOMAINS": {
        "plus.url.google.com":"url",
        "plus.url.google.com.hk":"q|url"
    },
    "LOCAL_PORT" : 1998,
    "HSTS_DOMAINS" : {
        "developers.facebook.com": 1,
        "groups.google.com": 1,
        "www.paypal.com" : 1,
        "www.elanex.biz" : 1,
        "jottit.com" : 1,
        "sunshinepress.org" : 1,
        "www.noisebridge.net" : 1,
        "neg9.org" : 1,
        "riseup.net" : 1,
        "factor.cc" : 1,
        "splendidbacon.com" : 1,
        "aladdinschools.appspot.com" : 1,
        "ottospora.nl" : 1,
        "www.paycheckrecords.com" : 1,
        "market.android.com" : 1,
        "lastpass.com" : 1,
        "www.lastpass.com" : 1,
        "keyerror.com" : 1,
        "entropia.de" : 1,
        "romab.com" : 1,
        "logentries.com" : 1,
        "stripe.com" : 1,
        "twitter.com": 1,
        "www.twitter.com": 1,
        "facebook.com": 1,
        "www.facebook.com": 1,
    },
    #collect domains that support HTTPS, to reduce usage of web proxy
    "HSTS_ON_EXCEPTION_DOMAINS" : {
        "s.ytimg.com": 1,
        "i1.ytimg.com": 1,
        "i2.ytimg.com": 1,
        "i3.ytimg.com": 1,
        "i4.ytimg.com": 1,
        "i1.tdimg.com": 1,
        "i2.tdimg.com": 1,
        "i3.tdimg.com": 1,
        "i4.tdimg.com": 1,
        "bits.wikimedia.org": 1,
        "www.wikipedia.org": 1,
        "www.google-analytics.com": 1,
        "apps.facebook.com": 1,
        "graph.facebook.com": 1,
        "www.youtube.com": 1,
    },
    "BLOCKED_DOMAINS": {
        "baidu.jp" : True,
        "search.twitter.com" : True,
        "www.baidu.jp" : True,
        "www.nicovideo.jp": True,
        "ext.nicovideo.jp": True,
        "blog.roodo.com": True,
        "www.dwnews.com": True,
        "china.dwnews.com": True,
        "www.mediafire.com": True,
        "thepiratebay.org": True,
        "thepiratebay.se": True,
        "www.bbc.co.uk": True,
        "chinadigitaltimes.net": True,
        "www.wenxuecity.com": True,
        "bbs.wenxuecity.com": True,
        "www.blogger.com": True,
        "blogger.com": True,
    },
    "BLOCKED_IPS": {
        "70.86.20.29" : 1, #www.bullogger.com
        "69.93.206.250": 1, #www.xys.org,
        "174.121.98.156": 1,
        "50.22.53.157": 1,
        "50.22.53.155": 1,
        "72.32.231.8": 1,
        "174.121.66.230": 1,
        "107.20.170.126": 1,
        "204.236.224.226": 1,
        "69.163.223.11": 1, #letscorp.net
        "199.59.148.12": 1, "199.59.149.210": 1, #t.co
    },
    "CHINA_IP_LIST_FILE":"exclude-ip.json",
    "PAGE_RELOAD_HTML": """<html>
    <head>
        <script type="text/javascript" charset="utf-8">
            window.location.reload();
        </script>
    </head>
    <body>
    </body></html>""",
}

# 74.125.71.0/24
blockedIpString = """74.125.71.88
74.125.71.89
74.125.71.99
74.125.71.100
74.125.71.101
74.125.71.106
74.125.71.113
74.125.71.116
74.125.71.121
74.125.71.128
74.125.71.138
74.125.71.139
74.125.71.150
74.125.71.160
74.125.71.161
74.125.71.162
74.125.71.163
74.125.71.188
74.125.71.192"""

# 199.59.150.0/24
blockedIpString += """
199.59.150.7
199.59.150.8
199.59.150.9
199.59.150.10
199.59.150.11
199.59.150.12
199.59.150.39
199.59.150.40
199.59.150.41
199.59.150.42
199.59.150.43
199.59.150.44"""

for ip in blockedIpString.split("\n"):
    if len(ip) > 0:
        gConfig["BLOCKED_IPS"][ip] = 1


