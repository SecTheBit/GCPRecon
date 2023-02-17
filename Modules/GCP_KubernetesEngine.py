#!/bin/python3
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client as CL
from googleapiclient import discovery
import warnings
warnings.filterwarnings("ignore")
import google.auth,google.auth.transport.requests,re
from google.oauth2 import service_account 
from Colors import bcolors


def generateToken(ServiceAccountFile):
    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    credentials = service_account.Credentials.from_service_account_file(ServiceAccountFile,scopes=scopes)
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    access_token = credentials.token
    return access_token

class GCP_KubernetesEngine:
     def Recon_KubernetesEngine(project_id,serviceAccountFile):
        list_output=[]
        try:
            with open("locations.txt","r") as f:
                data=f.readlines()
        except:
             print("[+] Some Error Occured with locations.txt file")
             exit(0)
        for locations in data:
            locations = locations.strip()
            service = discovery.build('container', 'v1')
            parent="projects/endless-force-372307/locations/"+locations
            request = service.projects().locations().clusters().list(parent=parent)
            response = request.execute()
            if response:
                if(response["clusters"][0]["name"] != None):
                    cluster_name = response['clusters'][0]['name']
                    # create client for clustermanagerclient using google cloud API for getting cluster information
                    cluster_manager_client = ClusterManagerClient()
                    names="projects/"+project_id+"/locations/"+locations+"/clusters/"+cluster_name
                    cluster = cluster_manager_client.get_cluster(name=names)
                    ## creating kubernetes configuration using kubernetes module in python
                    configuration = CL.Configuration()
                    # using the cluster varibale here 
                    configuration.host = f"https://{cluster.endpoint}:443" 
                    configuration.verify_ssl = False
                    tokensss=generateToken(serviceAccountFile)
                    ## passing the access token generated from service account to make Kubernetes python library work
                    configuration.api_key = {"authorization": "Bearer " + tokensss}
                    CL.Configuration.set_default(configuration)
                    try:
                             ## listing services in cluster
                        v1 = CL.CoreV1Api()
                        services = v1.list_service_for_all_namespaces(watch=False)
                        #print(services)
                    except:
                        print(f"{bcolors.WARNING}[+]Some error occured may be due to access token, Quitting...bcolors.ENDC")
                        exit(0)
                             ## checking if services are exposed to public or not
                    for svc in services.items:
                        #print(svc)
                        #print(svc.spec.ports[0].target_port)
                        if(svc.status.load_balancer.ingress != None): 
                            #print("Ip Address: {0} Port: {1} ".format(svc.status.load_balancer.ingress[0].ip,svc.spec.ports[0].target_port))
                            dict_op={'Asset Type':'Kubernetes Engine','Asset Name':'Null','Service Name': svc.metadata.name,'Endpoint/URL':'Null','Mapped Custom Domains':'Null','Internal IP Address':'Null','Public IP Address':svc.status.load_balancer.ingress[0].ip,'Open Ports':svc.spec.ports[0].target_port,'Public Access':'Null'}  
                            list_output.append(dict_op)
        return list_output
        
                                    
                                    

       

  