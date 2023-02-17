from googleapiclient import discovery

def OpenPorts(project_id):
    firewall_config ={}
    service = discovery.build('compute', 'v1')
    request = service.firewalls().list(project=project_id)
    if request is not None:
        response=request.execute()
        for firewall in response['items']:
            if 'targetTags' in firewall and 'allowed' in firewall:
            ## check if ingress rules are defined on specific ports
                for key in firewall['allowed'][0].keys():
                    if(key == "ports"):
                        for networktags in firewall['targetTags']:
                            #print(networktags)
                            if networktags not in firewall_config:
                               firewall_config[networktags]=[]
                            #print( firewall['allowed'][0]['ports'])
                            firewall_config[networktags] += (x for x in firewall['allowed'][0]['ports'])
    #print(firewall_config)
    return firewall_config
            
class ComputeEngine:

    def Recon_ComputeEngine(project_id):
        list_output=[]
        service_client= discovery.build('compute','v1')
        request=service_client.instances().aggregatedList(project=project_id)
        if request is not None:
            response = request.execute()
            for data in response['items'].items():
                for key,value in data[1].items():
                    if(key == "instances"):
                        firewall_config = OpenPorts(project_id)
                        for instances in data[1]['instances']:
                            if 'tags' in instances:
                                if 'items' in  instances['tags']:
                                    #print("hello")
                                    for tags in instances['tags']['items']:
                                        ports=None
                                        if tags in firewall_config:
                                            ports = firewall_config[tags]
                                            total_ports=""
                                            for port in ports:
                                                total_ports=total_ports+str(port)+","
                                            dict_op={'Asset Type':'Compute Engine','Asset Name':instances['name'],'Service Name': 'Null','Endpoint/URL':'Null','Mapped Custom Domains':'Null','Internal IP Address':instances['networkInterfaces'][0]['networkIP'],'Public IP Address':instances['networkInterfaces'][0]['accessConfigs'][0]['natIP'],'Open Ports':total_ports,'Public Access':'Null'}     
                                            list_output.append(dict_op)
                        break
    
        #print(list_output)
        return list_output