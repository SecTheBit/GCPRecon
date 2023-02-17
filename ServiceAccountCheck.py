import os,google.cloud
from google.oauth2 import service_account
import googleapiclient.discovery,json
from Colors import bcolors


roles_required = ['roles/appengine.appViewer','roles/compute.viewer','roles/cloudsql.viewer','roles/container.viewer']
def fetchprojectID(service_account_file):
    try:
       file = open(service_account_file)
       data = json.load(file)
    except Exception as e:
       print(f"{bcolors.FAIL}[+] Error Opening in Credentials File : {bcolors.ENDC}",e)
       exit(0)
    project_id=data['project_id']
    return project_id

class ServiceAccountChecks:
    #appengine_flag = "Access"
    flag = "No Access"
    def PermissionCheck(ServiceAccountFile):
        PROJECT_ID=fetchprojectID(ServiceAccountFile)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ServiceAccountFile
        creds = service_account.Credentials.from_service_account_file(filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],scopes=['https://www.googleapis.com/auth/cloud-platform'])
        service = googleapiclient.discovery.build('iam', 'v1', credentials=creds)
        try:
            roles = service.roles().queryGrantableRoles(body={'fullResourceName':'//cloudresourcemanager.googleapis.com/projects/'+PROJECT_ID}).execute()
        except:
            print(f"{bcolors.FAIL}[+]Roles Not Assigned, Please Assign roles/iam.securityReviewer Role To Service Account {bcolors.ENDC}")
            exit(0)
        count=0
        for role in roles['roles']:
            #print(role['name'])
            for roles_req in roles_required:
                if role['name'] == roles_req:
                #print(roles_required['appengine'])
                    count +=1
                    flag = "Access"
            #else:
                #print("Roles Not Assgined for...")
        if count < len(roles_required):
            flag = "No Access"
            print(f"{bcolors.FAIL}[+]Some Permission Missings{bcolors.ENDC}")
            exit(0)
        return flag,PROJECT_ID
        