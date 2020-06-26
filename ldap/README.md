# 389ds
Dockerized 389ds with TLS

389 Directory Server(389ds) is an enterprise-class Open Source LDAP server for Linux.

This image provides  a dockerized 389ds with TLS authentication support, data 
persistence  support through volumes and easy management of server certificates.


# Usage
The best way to use the image is with docker-compose by adapting the sample 
'docker-compose.yml' file.

    ldap:
      image: 389ds:latest
      hostname: ldap.example.com
      volumes:
        - ./data:/var/lib/dirsrv:Z
        - ./config:/etc/dirsrv:Z
        - ./logs:/var/log/dirsrv:Z
      environment:
        HOSTNAME: example.com
        LDAP_SUFFIX: dc=example,dc=com
        LDAP_ADMIN_USERNAME: admin
        LDAP_ADMIN_PASSWORD: admin
        LDAP_MANAGER_PASSWORD: admin
      ports:
        - 389:389
        - 636:636
      restart: always

Then run the service with

    docker-compose up


# Environment Variables
You can customize how the 389ds instance will be created through environment
variables.
HOSTNAME:  The hostname to use for the directory server by default this will be the fully qualified container hostname provided
in docker-compose.yml or the hostname provided through the --hostname from `docker run`. A fully qualified hostname is required

LDAP_SUFFIX:  The base DN of the directory instance (eg. "dc=example,dc=com"} default will be "dc=idptestbed" if not specified

LDAP_ADMIN_USERNAME:  The username of the default admin account to be created in LDAP, will be `admin` if not specified  

LDAP_ADMIN_PASSWORD:  The password for the default admin account password, will be same as LDAP_MANAGER_PASSWORD or `admin` if neither is specified    

LDAP_MANAGER_PASSWORD:  The password for the Directory Manager, will be same as LDAP_ADMIN_PASSWORD or `admin` if neither is specified  


# Volumes
To preserve configuration and data between restarts and recreating the container, the following volumes should be mounted

    /etc/dirsrv:  location where instance configuration data is stored. Must be empty initially  
    /var/lib/dirsrv:  database storage location. Must be empty initially  
    /var/log/dirsrv:  location where logs will be stored. Must be empty initially    


# Testing

    ldapsearch -x -ZZ -h localhost -D "cn=Directory Manager" -b "dc=example,dc=com" -W
