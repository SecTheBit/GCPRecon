from google.cloud import appengine_admin_v1
import os

# creating appengine client for listing down services (applications hosted on appengine )
class GCP_Appengine:
    def Recon_Appengine(project_id):
        list_output=[]
        list_service_name=[]
        client = appengine_admin_v1.ServicesClient()
        request = appengine_admin_v1.ListServicesRequest(parent="apps/"+project_id)
        #print("enumerating about Appengines")
        response= client.list_services(request=request)
        for result in response:
            result = result.name
            list_service_name.append(result)
        #checking if custom domains are present
        client = appengine_admin_v1.ApplicationsClient()
        request = appengine_admin_v1.GetApplicationRequest(name="apps/"+project_id)
        response = client.get_application(request=request)
        mapped_domain = str(response.dispatch_rules[0].domain)
        mapped_service = str(response.dispatch_rules[0].service)
        mapped_service_version_url = ""
        max_time = 0
        for service in list_service_name:
            service = str(service)
            length_service = len(service.split("/"))
            service_name = service.split("/")[length_service-1]
            client = appengine_admin_v1.VersionsClient()
            request = appengine_admin_v1.ListVersionsRequest(parent=service)
            responses = client.list_versions(request=request)
            #print(responses)
            for response in responses:
                status = str(response.serving_status)
                #print(status)
                if (status == "ServingStatus.SERVING"):
                     #print(service+":"+mapped_service+":"+mapped_domain)
                    if(service_name == mapped_service and mapped_domain != ''):
                        #print("hello from if condition")
                        max_time_temp = response.create_time
                        max_time_temp = max_time_temp.timestamp()
                        if max_time_temp > max_time:
                            max_time_temp_store=max_time
                            max_time=max_time_temp
                            mapped_service_version_url_temp_store=mapped_service_version_url
                            mapped_service_version_url=response.version_url
                            if max_time_temp_store == 0:
                                continue
                            else:
                                #print(mapped_service_version_url_temp_store)
                                dict_op={'Asset Type':'Appengine','Asset Name':"Null",'Service Name':service_name,'Endpoint/URL':mapped_service_version_url,'Mapped Custom Domains':"Null",'Internal IP Address':'Null','Public IP Address':'Null','Open Ports':'Null','Public Access':'Null'}
                                list_output.append(dict_op)                    
                    
                    else: 
                        #print(response.version_url)
                        dict_op={'Asset Type':'Appengine','Asset Name':"Null",'Service Name':service_name,'Endpoint/URL':response.version_url,'Mapped Custom Domains':"Null",'Internal IP Address':'Null','Public IP Address':'Null','Open Ports':'Null','Public Access':'Null'}
                        list_output.append(dict_op)
            if(mapped_service_version_url != ''):           
                #print(mapped_service_version_url+"->"+mapped_domain)
                dict_op={'Asset Type':'Appengine','Asset Name':"Null",'Service Name':service_name,'Endpoint/URL':mapped_service_version_url,'Mapped Custom Domains':mapped_domain,'Internal IP Address':'Null','Public IP Address':'Null','Open Ports':'Null','Public Access':'Null'}
                list_output.append(dict_op)
                mapped_service_version_url=''  
        return list_output