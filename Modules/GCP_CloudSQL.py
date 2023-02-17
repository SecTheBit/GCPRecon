from googleapiclient import discovery
class CloudSQL:
 
 def Recon_CloudSQL(project_id):
    list_output=[]
    sql_client = discovery.build('sqladmin', 'v1beta4')
    resp = sql_client.instances().list(project=project_id).execute()
    if resp is  not None:
        for data in resp['items']:
            if(data['ipAddresses'][0]['type'] != "PRIVATE"):
                if 'value' in data['settings']['ipConfiguration']['authorizedNetworks']:
                    #print(data['ipAddresses'][0]['ipAddress']+" is Accessible By "+data['settings']['ipConfiguration']['authorizedNetworks'][0]['value'])
                    dict_op={'Asset Type':'Cloud SQL','Asset Name':data['name'],'Service Name': 'Null','Endpoint/URL':'Null','Mapped Custom Domains':'Null','Internal IP Address':'Null','Public IP Address':data['ipAddresses'][0]['ipAddress'],'Open Ports':'3306,3307','Public Access':data['settings']['ipConfiguration']['authorizedNetworks'][0]['value']}  
                    list_output.append(dict_op)   
                else:
                    #print(data['ipAddresses'][0]['ipAddress'])
                    dict_op={'Asset Type':'Cloud SQL','Asset Name':data['name'],'Service Name': 'Null','Endpoint/URL':'Null','Mapped Custom Domains':'Null','Internal IP Address':'Null','Public IP Address':data['ipAddresses'][0]['ipAddress'],'Open Ports':'Null','Public Access':'No Public Access'}  
                    list_output.append(dict_op)

            else: 
                dict_op={'Asset Type':'Cloud SQL','Asset Name':data['name'],'Service Name': 'Null','Endpoint/URL':'Null','Mapped Custom Domains':'Null','Internal IP Address':data['ipAddresses'][0]['ipAddress'],'Public IP Address':'Null','Open Ports':'Null','Public Access':'No Public Access'}  
                list_output.append(dict_op)
    return list_output