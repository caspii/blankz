A madlibs / consequences-type game running on Google App Engine

## Installing and setup on Ubuntu
1. `sudo apt install google-cloud-sdk`
2. `gcloud init`
3. `gcloud components install app-engine-python`

## Local Devserver
To run use `dev_appserver.py .` in project root.
* App is available on http://localhost:8080/
* Local Admin interface http://localhost:8000/instances

## `glcoud` commands
* Deploy:  `gcloud app deploy`
* List projects: `gcloud projects list`
* Change project project: `gcloud init`
