import json
import ipaddress
import ast
import requests
import copy
from pprint import pprint


net1 = "100.64.26.0/24"
net1_svr_start_ip = 50 #100.64.26.50
net1_vip_start_ip = 200 #100.64.26.100
net2 = '100.64.27.0/24'
net2_svr_start_ip = 50 #100.64.27.50

def ips(start, end):
    import socket, struct
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]

#ip_list = ips('1.1.1.1', '1.1.5.0') 

def ip_from_net(network, start, count):
    ips = []
    net4 = ipaddress.ip_network(unicode(network))
    end = start+count
    for ip in range(start, end):
        ips.append(str(net4[ip]))
    return ips

def clear_server_conf(data):
    data['Pool'][0]['servers'] = []

def add_servers(data, net, start_ip, count):
    ips = ip_from_net(net, start_ip, count)
    for ip in ips:
        #u'servers': [{u'handle': u's_1', u'enabled': True, u'app_type': u'httptest', u'ratio': 1, u'ip': {u'type': u'V4', u'addr': u'${net1}'}}]}]
        server = {}
        server['enabled'] = True
        server['ip'] = {'addr':ip, 'type':"V4"}
        data['Pool'][0]['servers'].append(server)
        
def add_hms(data, count):
    hm = data['HealthMonitor'][0]
    pool = data['Pool'][0]
    data['HealthMonitor'] = []
    pool['health_monitor_refs'] = []
    for i in range (1, count+1):
        new_hm = copy.copy(hm)
        hm_name = "hm-https-"+str(i)
        new_hm['name'] = hm_name
        pool['health_monitor_refs'].append("/api/healthmonitor/?name="+hm_name)
        data['HealthMonitor'].append(new_hm)

def set_vip(data, net, start_ip, num):
    ips = ip_from_net(net, start_ip, num)
    vips = data['VsVip']
    print vips
    i = 0
    for vip in vips:
        vip['vip'][0]['ip_address']['addr'] = ips[i]
        i+=1

def gen_config():
    with open("https_config.json", "r") as read_file:
        data = json.load(read_file)

    set_vip(data, net1, net1_vip_start_ip, 1)
    clear_server_conf(data)
    add_servers(data, net1, net1_svr_start_ip, 150)
    add_servers(data, net2, net2_svr_start_ip, 150)
    add_hms(data, 30)
    #print data
    #print json.dumps(data, indent=2)
    return data


def configure_controller():
    config = gen_config()
    config_dict = {"configuration": config}
    url = 'https://10.79.169.3/api/configuration/import?ignore_uuid=1'
    config_json = ast.literal_eval(str(config_dict))
    #pprint(config_json)
    response=requests.post(url, data=json.dumps(config_dict), auth=('admin', 'admin'), verify=False, headers={"content-type": "application/json", 'X-Avi-Version':'20.1.1', 'X-Avi-Tenant':'admin'})
    print response
    print response.text

if __name__=="__main__":
    configure_controller()
