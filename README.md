### What's GCPRecon
GCPRecon is a tool written in python, which helps to fetch all publicly available Data from provided GCP Account, using Service Account Credentials.

### Motive
There are not many tools available which are covering all the produts of Google Cloud Platforms. This motivates me to build GCPRecon for Security Researchers, which can come handy while doing Audits/Pentesting.

### Products Covered

* Compute Engine
* App Engine
* Kubernetes Engine
* CloudSQL
* Cloud Storage

### Installing GCPRecon

```
git clone https://github.com/SecTheBit/GCPRecon
```
```
pip install requirements.txt
```
```
Give Required Permissions to Service Account
```

### Roles Required

* roles/appengine.appViewer
* roles/compute.viewer
* roles/cloudsql.viewer
* roles/container.viewer
* roles/iam.securityReviewer

### How to use GCPRecon

` python3 GCPRecon.py --credentials <path to service account file> `

![GCPRecon](https://github.com/SecTheBit/GCPRecon/blob/main/gcprecon.png)

### Output Formats
* Currently it Supports only xlsx and csv format.

### Assigning Roles to Service Account

1. Go to https://console.cloud.google.com
2. Log in to your GCP Account
3. Click on Hamburger icon on left hand side and select "IAM & Admin"
4. Click on Grant Access
5. In principal box , select your GCP Service Account
6. Go to Roles and select following roles (Only Read Access will be Required)
   * App Engine Viewer
   * Cloud SQL Viewer
   * Compute Viewer
   * Kubernetes Engine Viewer
   * IAM Security Reviewer
   
