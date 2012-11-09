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

$IPTABLES -A INPUT -p tcp --dport 80 -m tcp --tcp-flags RST RST -m state --state ESTABLISHED $match_set -j DROP
$IPTABLES -I INPUT -p tcp --dport 80 -m conntrack --ctstate INVALID -j DROP
$IPTABLES -I INPUT -p tcp --dport 80 -m conntrack --ctstate INVALID -j LOG --log-prefix "state-invalid "
$IPTABLES -I INPUT -p tcp --dport 80 -m conntrack --ctstate ESTABLISHED --tcp-flags all syn -j DROP
$IPTABLES -I INPUT -p tcp --dport 80 -m conntrack --ctstate ESTABLISHED --tcp-flags all syn -j LOG --log-prefix "syn-after-sync "

exit 0
fi


IPFW=`which ipfw`
if [ -x "$IPFW" ]; then
    $IPFW add 1000 drop tcp from any to me tcpflags rst in
fi
