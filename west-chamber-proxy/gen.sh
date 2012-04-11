ip="74.125.71.0"
ip_prefix="74.125.71"

nmap -sS -p80 "$ip"/24 --host-timeout 5s --log-errors > .nmap5s.log

cat .nmap16s.log | grep "$ip_prefix" | awk -v ip_prefix="$ip_prefix" '{
    if (index($5, ip_prefix) > 0) print $5;
    else print substr($6, 2, length($6)-2);
}'
