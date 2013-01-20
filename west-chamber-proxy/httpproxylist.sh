#!/bin/bash

WORK_DIR=/tmp/proxylist
mkdir -p $WORK_DIR

curl -iv http://www.ip-adress.com/proxy_list/ -H 'User-Agent:Mozilla/6.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' | grep '<td>' | awk -F'>|<' '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+/ {print $3}' > $WORK_DIR/www.ip-adress.com.list

#seq command is outdated, this version is recommended, ref: http://www.cyberciti.biz/faq/bash-for-loop/
> /tmp/www.cnproxy.com.list
for i in {1..10}; do
    curl -iv "http://www.cnproxy.com/proxy$i.html" -H 'User-Agent:Mozilla/6.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' | awk -F'>|<' '/<td>[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/ {print $5 ":" substr($7,19)}' | sed 's/+r/8/g' | sed 's/+d/0/g' | sed 's/+z/3/g' | sed 's/+m/4/g' | sed 's/+k/2/g' | sed 's/+l/9/g' | sed 's/+b/5/g' | sed 's/+i/7/g' | sed 's/+w/6/g' |sed 's/+c/1/g' |awk -F ')' '{print $1}' >> $WORK_DIR/www.cnproxy.com.list
done

curl http://www.proxynova.com/proxy_list.txt --max-time 6 | awk  '/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/ {print $1}' >> $WORK_DIR/www.proxynova.com.list
curl http://www.searchlores.org/pxylist2.txt | awk  '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/ {print $1}' >> $WORK_DIR/www.searchlores.org.list
curl http://www.freeproxy.ru/download/lists/goodproxy.txt | awk  '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/ {print $2}' >> $WORK_DIR/www.freeproxy.ru.list
curl http://www.binary-zone.com/files/MyProxyList.txt | awk  '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/ {print $1$2}' >> $WORK_DIR/www.binary-zone.com.list

for domain in "www.ip-adress.com" "www.cnproxy.com" "www.proxynova.com" "www.searchlores.org" "www.freeproxy.ru" "www.binary-zone.com"

do
    echo "checking " $domain "..."
    DIR="$WORK_DIR/$domain/"
    mkdir -p $DIR
    cat $WORK_DIR/$domain".list" | mawk -v prefix=$DIR '{print "curl http://www.huanqiu.com/license/servicelicense.htm --max-time 6 --proxy "$1 " -o " prefix $1}' | sh -x
    cd $DIR
    find $DIR -maxdepth 1 -size 1230c | awk '{print "cp "$1" /tmp/proxies/good/"}'

done

