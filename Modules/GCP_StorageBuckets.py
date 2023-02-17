from google.cloud import storage
import requests
import google.auth,google.auth.transport.requests
from google.oauth2 import service_account 


permissions = ['storage.buckets.delete','storage.buckets.get','storage.buckets.getIamPolicy','storage.buckets.setIamPolicy','storage.buckets.update','storage.objects.create','storage.objects.create','storage.objects.get','storage.objects.get','storage.objects.get']
scopes = ['https://www.googleapis.com/auth/cloud-platform']


def authenticatedAccess(bucket,access_token):
    url="https://www.googleapis.com/storage/v1/b"+bucket
    headervalue= "Bearer "+access_token
    try:
         response = requests.get(url,headers={"Authorization": headervalue}).json()
    except:
          response = None
    auth_permissions=""
    if response != None and response.get('permissions') != None:
        for permissions in response.get('permissions'):
            auth_permissions=auth_permissions+permissions+","
    else:
         return "NO Public Access"
    return auth_permissions
def publicAccess(bucket):
     total_permission = ""
     response = requests.head('https://www.googleapis.com/storage/v1/b/{}'.format(bucket))
     if response.status_code not in [400,404,403]:
         unauth_request = requests.get('https://www.googleapis.com/storage/v1/b/{}/iam/testPermissions?permissions=storage.buckets.delete&permissions=storage.buckets.get&permissions=storage.buckets.getIamPolicy&permissions=storage.buckets.setIamPolicy&permissions=storage.buckets.update&permissions=storage.objects.create&permissions=storage.objects.delete&permissions=storage.objects.get&permissions=storage.objects.list&permissions=storage.objects.update'.format(bucket)).json()
         if unauth_request.get('permissions') != None:
             for permissions in unauth_request.get('permissions'):
                 total_permission = total_permission + permissions +","
         else:
             return "NO Public Access"        
     else:
         return "NO Public Access"
     
     return total_permission
         

class GCP_StorageBucket:
    def ReconBucket(project_id,serviceAccountFile):
        list_output=[]
        storage_client = storage.Client()
        buckets = storage_client.list_buckets(project=project_id)
        for bucket in buckets:
            unauth_permissions = publicAccess(bucket.name)
            if unauth_permissions == "NO":
                credentials = service_account.Credentials.from_service_account_file(serviceAccountFile,scopes=scopes)
                auth_req = google.auth.transport.requests.Request()
                credentials.refresh(auth_req)
                access_token = credentials.token
                auth_result= authenticatedAccess(bucket.name,access_token)
                dict_op={'Asset Type':'Storage Bucket','Asset Name':bucket.name,'Service Name': 'Null','Endpoint/URL':'Null','Mapped Custom Domains':'Null','Internal IP Address':'Null','Public IP Address':'Null','Open Ports':'Null','Public Access':auth_result}     
                list_output.append(dict_op)
            else:
                dict_op={'Asset Type':'Storage Bucket','Asset Name':bucket.name,'Service Name': 'Null','Endpoint/URL':'Null','Mapped Custom Domains':'Null','Internal IP Address':'Null','Public IP Address':'Null','Open Ports':'Null','Public Access':unauth_permissions}     
                list_output.append(dict_op)
        return list_output
