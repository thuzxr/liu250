# python get_command_for_router.py 1 # print commands for configuring ZURI

import sys
from collections import defaultdict

GROUP_ID = '68'
routers = ['','ZURI','BASE','GENE','LUGA','MUNI','LYON','VIEN','MILA']
pairs_ip = {}
pairs_ip[(1,2)]='.0.1.'
pairs_ip[(1,3)]='.0.2.'
pairs_ip[(1,4)]='.0.3.'
pairs_ip[(1,5)]='.0.4.'
pairs_ip[(1,7)]='.0.5.'
pairs_ip[(2,3)]='.0.6.'
pairs_ip[(2,5)]='.0.7.'
pairs_ip[(2,6)]='.0.8.'
pairs_ip[(3,4)]='.0.9.'
pairs_ip[(3,6)]='.0.10.'
pairs_ip[(4,8)]='.0.11.'
pairs_ip[(4,7)]='.0.12.'

subnets = defaultdict(lambda:set())

# reverse for further query
def init_pairs():
    cp = pairs_ip.copy()
    for p in cp:
        a, b = p
        pairs_ip[(a, b)] = GROUP_ID + pairs_ip[(a, b)]

        subnets[a].add(pairs_ip[(a, b)] + '0/24')
        subnets[b].add(pairs_ip[(a, b)] + '0/24')

        pairs_ip[(b, a)] = pairs_ip[(a, b)] + '2/24'
        pairs_ip[(a, b)] += '1/24'


def get_inter_router_command(router_id):
    cmd = ''
    for p in pairs_ip:
        if p[0] == router_id:
            cmd += 'interface port_%s\n' %(routers[p[1]])
            cmd += 'ip address %s\n' %(pairs_ip[p])
    return cmd

def get_router_loopback(router_id):
    cmd = ''
    cmd += 'interface lo\n'
    cmd += 'ip address '+ GROUP_ID+'.%s.0.1/24\n'%(str(150 + router_id))

    subnets[router_id].add(GROUP_ID+'.%s.0.0/24'%(str(150 + router_id)))

    return cmd

def get_router_to_host_command(router_id):
    cmd = ''
    cmd += 'interface host\n'
    # at rounter connected to host
    cmd += 'ip address '+ GROUP_ID + '.%s.0.2/24' %(str(router_id + 100))
    return cmd

def get_router_ospf_command(router_id):
    cmd = ''
    cmd += 'conf t\nrouter ospf\n'
    for s in subnets[router_id]:
        cmd += 'network %s area 0\n' %(s)
    return cmd

init_pairs()
router_id = int(sys.argv[1])
print('************************************************')
print('configure interface for router')
print('************************************************')
print('conf t')
print(get_inter_router_command(router_id))
print(get_router_loopback(router_id))
print(get_router_to_host_command(router_id))
print('exit\nexit\nexit\n')

print('###########################################\nconfigure host###########################################\n'+'ip address add '+ GROUP_ID + '.%s.0.1/24' %(str(router_id + 100)) + ' dev %srouter' %(routers[router_id]))
print('ip route add default via '+GROUP_ID + '.%s.0.2' %(str(router_id + 100)))
print('exit\n')

print('************************************************')
print('configure ospf for router')
print('************************************************')
print(get_router_ospf_command(router_id))
print('exit\nexit\nexit\n')
