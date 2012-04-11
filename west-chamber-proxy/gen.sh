ip="74.125.71.0"
ip_prefix="74.125.71"

nmap -sS -p80 "$ip"/24 --host-timeout 16s --log-errors > .nmap16s.log
ssh liruqi@asuwish.cc 'sudo nmap -sS -p80 74.125.71.0/24 --host-timeout 16s --log-errors' > .nmap16s.remote.log

cat .nmap16s.log | grep "$ip_prefix" | awk -v ip_prefix="$ip_prefix" '{
    if (index($5, ip_prefix) > 0) print $5;
    else print substr($6, 2, length($6)-2);
}' > .availiplist.log

cat .nmap16s.remote.log | grep "$ip_prefix" | awk -v ip_prefix="$ip_prefix" '{
    if (index($4, ip_prefix) > 0) print substr($4, 1, length($4)-1);
    else print substr($5, 2, length($5)-3);
}' > .alliplist.log

diff .availiplist.log .alliplist.log | grep "^>" | awk '{print $2}'
