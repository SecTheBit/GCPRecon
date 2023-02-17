import argparse,ServiceAccountCheck,Modules
from Modules.GCP_APPEngine import GCP_Appengine
from Modules.GCP_ComputeEngine import ComputeEngine
from Modules.GCP_StorageBuckets import GCP_StorageBucket
from Modules import GCP_CloudSQL
from Modules import GCP_KubernetesEngine
from Colors import bcolors
import pyfiglet,time

import pandas as pd

def EnableModule(project_id,credentials_file):
    print(f"{bcolors.OKGREEN}[+]Fetching Details:{bcolors.ENDC}"+f"{bcolors.OKCYAN} GCP AppEngine{bcolors.ENDC}")
    result_appengine= GCP_Appengine.Recon_Appengine(project_id)
    print(f"{bcolors.OKGREEN}[+]Fetching Details:{bcolors.ENDC}"+f"{bcolors.OKCYAN} GCP Compute Engine{bcolors.ENDC}")
    result_computeEngine = ComputeEngine.Recon_ComputeEngine(project_id)
    print(f"{bcolors.OKGREEN}[+]Fetching Details:{bcolors.ENDC}"+f"{bcolors.OKCYAN} GCP Storage Buckets{bcolors.ENDC}")
    result_storagebucket= GCP_StorageBucket.ReconBucket(project_id,credentials_file)
    print(f"{bcolors.OKGREEN}[+]Fetching Details:{bcolors.ENDC}"+f"{bcolors.OKCYAN} GCP CloudSQL{bcolors.ENDC}")
    result_cloudsql = GCP_CloudSQL.CloudSQL.Recon_CloudSQL(project_id)
    print(f"{bcolors.OKGREEN}[+]Fetching Details:{bcolors.ENDC}"+f"{bcolors.OKCYAN} GCP Kubernetes Engine{bcolors.ENDC}")
    result_kubernetes = GCP_KubernetesEngine.GCP_KubernetesEngine.Recon_KubernetesEngine(project_id,credentials_file)
    output(result_computeEngine+result_appengine+result_storagebucket+result_cloudsql+result_kubernetes)
    #output(result_computeEngine+result_appengine+result_storagebucket+result_cloudsql)

def output(result_final):
    df = pd.DataFrame(data=result_final)
    df.to_excel("Op.xlsx",index=False)
    df.to_csv("Op.csv",index=False)
    print(f"{bcolors.OKGREEN}[+]Output Generated: Op.xlsx,Op.csv{bcolors.ENDC}")




if __name__ == '__main__' :
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-Credential", "--credentials", required=True, help="Service Account Credentials File")

    args = vars(arguments.parse_args())
    credentials_file = args['credentials']
    
    flags,project_id=ServiceAccountCheck.ServiceAccountChecks.PermissionCheck(credentials_file)
    #print(appengine_flags)
    if flags == "Access":
        banner=pyfiglet.figlet_format("GCPRecon")
        print(banner)
        time.sleep(2)
        print(f"{bcolors.OKGREEN}[+]Found Project ID : {bcolors.ENDC}"+"\033[34m"+str(project_id)+"\033[0m")
        EnableModule(project_id,credentials_file)


