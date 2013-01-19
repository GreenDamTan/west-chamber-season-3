curl -iv http://www.ip-adress.com/proxy_list/ -H 'User-Agent:Mozilla/6.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' | grep '<td>' | awk -F'>|<' '/[01234567890]:[01234567890][0123456789]/ {print $3}' > httpproxy.list

#seq command is outdated, this version is recommended, ref: http://www.cyberciti.biz/faq/bash-for-loop/
for i in {1..10}; do
    curl -iv "http://www.cnproxy.com/proxy$i.html" -H 'User-Agent:Mozilla/6.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' | awk -F'>|<' '/<td>[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/ {print $5 ":" substr($7,19)}' | sed 's/+r/8/g' | sed 's/+d/0/g' | sed 's/+z/3/g' | sed 's/+m/4/g' | sed 's/+k/2/g' | sed 's/+l/9/g' | sed 's/+b/5/g' | sed 's/+i/7/g' | sed 's/+w/6/g' |sed 's/+c/1/g' |awk -F ')' '{print $1}' >> httpproxy.list
done

curl http://www.proxynova.com/proxy_list.txt --max-time 6 | awk  '/[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/ {print $1}' >> httpproxy.list
curl http://www.searchlores.org/pxylist2.txt | awk  '/[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/ {print $1}' >> httpproxy.list
curl http://www.freeproxy.ru/download/lists/goodproxy.txt | awk  '/[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/ {print $2}' >> httpproxy.list
curl http://www.binary-zone.com/files/MyProxyList.txt | awk  '/[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/ {print $1$2}' >> httpproxy.list

cat httpproxy.list | sort -n > tmp
mv tmp httpproxy.list

mkdir -p /tmp/proxies/good
cat httpproxy.list | awk '{print "curl http://www.huanqiu.com/license/servicelicense.htm --max-time 6 --proxy "$1 " -o /tmp/proxies/" $1}' | sh -x
find /tmp/proxies -maxdepth 1 -size 1230c | awk '{print "mv "$1" /tmp/proxies/good/"}'
