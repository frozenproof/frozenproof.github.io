How to start both containers on this network and set up DataPower to interact with your application.

By the way, you need to follow the manual on the site, and have a clean working directory to run any of this because holy fucking.
# Step 0.1:
My configuration
```
root@snowdoll:/mnt/d/8_POC# docker network create chickenpizza
13ca6ac02f5783f6f85f75c2acb2bb82ddf3b4b72c9347066290cfff7fb71974
root@snowdoll:/mnt/d/8_POC# docker image list
REPOSITORY                                  TAG        IMAGE ID       CREATED          SIZE
8_poc-server                                latest     8347f7e579b7   42 minutes ago   1.15GB
icr.io/cpopen/datapower/datapower-limited   10.6.1.0   6fa293e80781   7 weeks ago      1.56GB
```
# Step 1: Run Your Prebuilt Application Container on chickenpizza
Replace 8_poc-server with the name of your prebuilt image and your_app_container with your desired container name.

```
docker run -d --name your_app_container --network chickenpizza 8_poc-server
```
My version is
```
docker run -d --name sexnow --network chickenpizza 8_poc-server
```

# Step 2: Run the IBM DataPower Container on chickenpizza
Next, start the DataPower container, connecting it to the same network:

DATAPOWER_ACCEPT_LICENSE environment variable or --accept-license flag not set. Set them and restart DataPower.

mkdir -p ./your_working_directory/{config,local,certs}
mkdir -p ./your_working_directory/{config,local,certs}

Run commands must not include comments
```
docker run -d --name datapower \
   --network chickenpizza \
   -p 9090:9090 \
   -p 5554:5554 \
   -e DATAPOWER_ACCEPT_LICENSE=true \
   -e DATAPOWER_INTERACTIVE=true\
   icr.io/cpopen/datapower/datapower-limited:10.6.1.0
```

```
 docker container stop datapower && docker container remove datapower &&
docker run -it --name datapower \
-v $(pwd)/config:/opt/ibm/datapower/drouter/config \
-v $(pwd)/local:/opt/ibm/datapower/drouter/local \
-v $(pwd)/certs:/opt/ibm/datapower/root/secure/usrcerts \
-e DATAPOWER_ACCEPT_LICENSE="true" \
-e DATAPOWER_INTERACTIVE="true" \
-p 9090:9090 \
icr.io/cpopen/datapower/datapower-limited:10.6.1.0

```
```
docker container start c095c9996480
```
```
docker exec -it datapower2 bash
docker exec -it datapower2 drouter
docker exec -it datapower drouter
docker start -i datapower

```
```
docker run -d --name datapower -e DATAPOWER_ACCEPT_LICENSE="true" -p 5550:5550 -p 9090:9090 icr.io/cpopen/datapower/datapower-limited:10.6.1.0
```
```
 docker container stop datapower && docker container remove datapower 
```
```
docker container stop datapower && docker container remove datapower && docker run -d --name datapower -e DATAPOWER_ACCEPT_LICENSE="true" -p 5550:5550 -p 9090:9090 icr.io/cpopen/datapower/datapower-limited:10.6.1.0
docker container stop datapower && docker container remove datapower && docker run -it --name datapower -e DATAPOWER_ACCEPT_LICENSE="true" -p 5550:5550 -p 9090:9090 icr.io/cpopen/datapower/datapower-limited:10.6.1.0

```
```
docker run -it --name datapower \
-v $(pwd)/config:/opt/ibm/datapower/drouter/config \
-v $(pwd)/local:/opt/ibm/datapower/drouter/local \
-v $(pwd)/certs:/opt/ibm/datapower/root/secure/usrcerts \
-e DATAPOWER_ACCEPT_LICENSE="true" \
-e DATAPOWER_INTERACTIVE="true" \
-p 9090:9090 \
icr.io/cpopen/datapower/datapower-limited:10.6.1.0
```
Default username and password is admin by the way.

```
configure terminal
web-mgmt
admin-state "enabled"
exit
write mem

```
Ctrl + P + Q
```
docker attach <container_name_or_id>
docker attach datapower
```
# Step 3: Configure DataPower to Route Requests to Your Application
- Access the DataPower Web GUI:

    - Open a browser and go to http://localhost:9090.
    - Log in with the default credentials if they haven’t been changed (admin/admin for development purposes).
    
- Set Up a Multi-Protocol Gateway (MPGW):

    - In the DataPower WebGUI, create a Multi-Protocol Gateway (MPGW) or API Gateway to route traffic.
    - Configure the MPGW to forward requests to http://your_app_container:<port>, where <port> is the port your application listens to inside the container. For example, if your app listens on port 8080, the backend URL would be http://your_app_container:8080.
    
- Configure Additional Policies (Optional):

    - In the MPGW configuration, you can add rules for authentication, transformation, or logging as required. For instance, you could set up SSL, add logging, or transform request/response data.

# Step 4: Test the Setup
Send a test request to DataPower:

- If DataPower is configured to receive API requests on a specific port, you could test by accessing http://localhost:<DataPower_port>.
- DataPower should route the request to your_app_container based on the settings you’ve configured.

This setup will allow DataPower to serve as a gateway for your application container, managing access, security, and transformations as needed. 