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
    match_set="-m set --match-set CHINA src"
    $IPSET -R < CHINA
    fi
fi

$IPTABLES -I INPUT -p tcp -m multiport --dports 80,443 --tcp-flags RST RST  $match_set -j DROP
$IPTABLES -I INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate ESTABLISHED --tcp-flags all syn -j DROP
$IPTABLES -I INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate ESTABLISHED --tcp-flags all syn -j LOG --log-prefix "syn-after-sync "
$IPTABLES -I INPUT -p tcp -m tcp -m multiport --dports 80,443 --tcp-flags FIN,SYN,RST,PSH,ACK,URG PSH,ACK -m conntrack --ctstate INVALID -j DROP
$IPTABLES -I INPUT -p tcp -m tcp -m multiport --dports 80,443 --tcp-flags FIN,SYN,RST,PSH,ACK,URG PSH,ACK -m conntrack --ctstate INVALID -j LOG --log-prefix "p.state-invalid"
exit 0
fi


IPFW=`which ipfw`
if [ -x "$IPFW" ]; then
    $IPFW add 1000 drop tcp from any to me tcpflags rst in
fi
