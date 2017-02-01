A madlibs / consequences-type game running on Google App Engine

## Installing and setup on Ubuntu
1. Follow [these instructions](https://cloud.google.com/sdk/docs/#deb)
1. Install this package: `google-cloud-sdk-app-engine-python`
2. `gcloud init`


## Local Devserver
To run use `dev_appserver.py .` in project root.
* App is available on http://localhost:8080/
* Local Admin interface http://localhost:8000/instances

## `glcoud` commands
* Deploy:  `gcloud app deploy`
* List projects: `gcloud projects list`
* Change project project: `gcloud init`
