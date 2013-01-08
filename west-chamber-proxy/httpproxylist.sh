
curl -iv http://www.ip-adress.com/proxy_list/ -H 'User-Agent:Mozilla/6.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' | awk -F'>|<' '/<td>[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/ {print $3}' > httpproxy.list
curl -iv http://www.cnproxy.com/proxy1.html -H 'User-Agent:Mozilla/6.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' | awk -F'>|<' '/<td>[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/ {print $5 ":" substr($7,19)}' | sed 's/+r/8/g' | sed 's/+d/0/g' | sed 's/+z/3/g' | sed 's/+m/4/g' | sed 's/+k/2/g' | sed 's/+l/9/g' | sed 's/+b/5/g' | sed 's/+i/7/g' | sed 's/+w/6/g' |sed 's/+c/1/g' |awk -F ')' '{print $1}' >> httpproxy.list

cat httpproxy.list
