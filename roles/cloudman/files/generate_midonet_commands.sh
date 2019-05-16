#!/bin/bash
# quick and dirty script to generate tunzone commands
# inspect output (midonet_commands_limited.txt) rigorously
unset http_proxy
unset https_proxy

TUNNEL_ZONE=$1

rm midonet_*

midonet-cli -e host list | grep -E "rccom|rcgpu|rchim" > midonet_monash_hosts.txt

while read l; do
        midonet_host=$(echo $l | awk -F ' ' '{print $2}')
        host_name=$(echo $l | awk -F ' ' '{print $4}')
        #remove domain is present
        host_name=${host_name%%.*}
        ip_address=$(echo $host_name | xargs -n 1 -I {} dig +short {}-dn.erc.monash.edu.au)
        if [[ $ip_address == '' ]]; then
                echo "ERROR: no addhost entry for $host_name"
                is_error="True"
        else
                echo "midonet-cli -e tunnel-zone ${TUNNEL_ZONE} add member host ${midonet_host} address ${ip_address}" >> midonet_commands.txt
        fi
done <midonet_monash_hosts.txt

#remove nodes already added
midonet-cli -e tunnel-zone $TUNNEL_ZONE list member >> midonet_tunnelzone_members.txt
grep -E "\.96\.|\.97\.|\.98\.|\.99\.|\.100\.|\.101\.|\.102\.|\.103\.|\.104\.|\.105\.|\.106\.|\.107\.|\.108\.|\.109\.|\.110\.|\.111\." midonet_tunnelzone_members.txt > midonet_monash_tunnelzone_members.txt

cat midonet_monash_tunnelzone_members.txt | awk -F ' ' '{print $6}' >> midonet_monash_tz_ips.txt

grep_command=$(cat midonet_monash_tunnelzone_members.txt  | awk -F ' ' '{print $6}' | tr '\n' '|')
cat midonet_commands.txt | grep -v -E "${grep_command%?}" > midonet_commands_limited.txt
