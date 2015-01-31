#! /bin/sh
# make sure to run as root

IPTABLES=`which iptables`
IPSET=`which ipset`

if [ -x "$IPTABLES" ]; then 
match_set=""

if [ -x "$IPSET" ]; then
    if $IPSET --version; then 
    if [ ! -f CHINA ]; then 
        wget "https://raw.github.com/liruqi/west-chamber-season-3/master/CHINA"
    fi
    match_set="-m set ! --match-set CHINA src"
    $IPSET -R < CHINA
    fi
fi

#TODO match HTTP
$IPTABLES -I INPUT -p tcp --tcp-flags RST RST $match_set -j DROP
$IPTABLES -I FORWARD -p tcp -s ! 192.168.0.0/16 --tcp-flags ALL SYN,ACK -m u32 --u32 "34&0xf0000000=0"  -j DROP
$IPTABLES -I FORWARD -p tcp --tcp-flags ALL SYN,ACK -m u32 --u32 "34&0xf0000000=0"  -j LOG --log-prefix "gfw-syn-ack "

exit 0
fi


IPFW=`which ipfw`
if [ -x "$IPFW" ]; then
    $IPFW add 1000 drop tcp from any to me tcpflags rst in
fi
