
# Cap One - Dev Class - Reston

https://tinyurl.com/cap-dev-3-26 

[Demos](https://drive.google.com/open?id=16zBQ_V1S3Zfkz7_TkWU98dEJQZugEaYV)

# Case Study

## Description

*Pets Book: The site for obnoxious Pet owners*

Required features:  
* People can upload pictures of their pets  
* Pictures are saved in cloud storage  
* They can add pet info (Firestore, Datastore, Cloud SQL)  
* Log into the Web site (Firebase Authentication)  
* Deploy it somewhere (App Engine, Compute Engine, Kubernetes)  
* Need to manage your code (Github.com, Google Cloud Source Repos)  

Bonus features:  
* Looks nice - Use material design to style your Web site  
* Gratuitous animations  
* Add some machine learning into your app  
* Anything else  


## Design Elements


### Web page

Python Flask running in AppEngine


### Login

Python container running in K8S. Uses Firebase for verification.


### User profiles

Stored in Firestore database.


### Verify and label pictures

Python container running in K8S. Use GCP Vision.

