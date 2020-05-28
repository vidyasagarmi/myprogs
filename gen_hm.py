from string import Template
import json
import ast
import requests
import pprint

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if hasattr(requests.packages.urllib3, 'disable_warnings'):
    requests.packages.urllib3.disable_warnings()

if hasattr(urllib3, 'disable_warnings'):
    urllib3.disable_warnings()


def ips(start, end):
    import socket, struct
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]

#ip_list = ips('1.1.1.1', '1.1.5.0')
#t = Template('{"name": "gsvc${n}", "groups":[{"index": 1,"name": "gsvc${n}-pool", "members":[{ "ip": {"type": "V4","addr": "${ip}"}}]}], "domain_names": [ "gsvc${n}.test.com"]}')

vs_t = Template('
        {   
            "services": [
                {   
                    "port": 9000
                }                                                                                                                                             
            ],  
            "vsvip_ref": "/api/vsvip/?name=vsvip-virtualservice-1", 
            "pool_ref": "/api/pool/?name=algo_pool", 
            "application_profile_ref": "/api/applicationprofile/?name=System-HTTP", 
            "name": "virtualservice-1"
        }') 
vip_t = Template('
        {   
            "vip": [
                {   
                    "ip_address": {
                        "type": "V4", 
                        "addr": "${net1}"
                    },  
                    "vip_id": "0" 
                }   
            ],  
            "name": "vsvip-virtualservice-1"
        }')

#url = 'https://10.140.4.202/api/gslbservice'
url = 'https://10.140.4.202/api/configuration/import?ignore_uuid=1'
i=1
gsvc_list = []
for iip in ip_list:
    i += 1
    data = t.substitute(n = i, ip = iip)
    #gsvc_json = ast.literal_eval(str(data))
    gsvc_list.append(json.loads(data))
    #response=requests.post(url, data=json.dumps(json_data), auth=('admin', 'admin'), verify=False, headers={"content-type": "application/json", 'X-Avi-Version':'18.2.2', 'X-Avi-Tenant':'admin'})

config_dict = {"configuration": {"VirtualService":vs_list, "VsVip":vip_list}}
#config_json = ast.literal_eval(str(config_dict))
response=requests.post(url, data=json.dumps(config_dict), auth=('admin', 'admin'), verify=False, headers={"content-type": "application/json", 'X-Avi-Version':'18.2.2', 'X-Avi-Tenant':'admin'})
print response
print response.text


def get_gslb():

    data = {"name": "gsvc2", "groups":[{"index": 1,"name": "gsvc2-pool", "members":[{ "ip": {"type": "V4","addr": "1.1.1.2"}}]}], "domain_names": [ "gsvc2.test.com"]}
    resp=requests.post(url, data=json.dumps(data), auth=('admin', 'admin'), verify=False, headers={"content-type": "application/json", 'X-Avi-Version':'18.2.2', 'X-Avi-Tenant':'admin'})  
    print resp
    print resp.json()
#get_gslb()
