# TP1
# Mise en place d'un réseaux IP
```bash
ifconfig <nomInterface> <Ipaddress>
ifconfig <nomInterface> [down|up]
ifconfig <nomInterface> inet6 add <ipAddress>
tcpdump -i igb0 -vvxn
# -i INTERFACE
# -vv -v verbose
# -x print data of each packet
# -n dont convert adresses to names
# promiscuos mode capture toutes les trames du réseau

telnet 192.168.0.254

show running conf = show ru 
config
vlan X # create vlan X
no vlan X # delete vlan X faire attention aux orphelins

ifconfig vlan0 create 
ifconfig vlan0 vlandev igb0

sysctl net.inet.ip.forwarding=1

route 
route flush
route add 

```

## Question
