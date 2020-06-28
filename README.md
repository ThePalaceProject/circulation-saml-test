# circulation-saml-test

Testbed which could be used for testing SAML-based patron authentication in 
[Circulation Manager](https://github.com/NYPL-Simplified/circulation).

## Architecture

Project consists of the following modules:

- [metadata](./metadata) is a throwaway Dockerized busybox generating SAML metadata using [confd](https://github.com/kelseyhightower/confd)
- [ldap](./ldap) is a Dockerized version of [389 Directory Server](https://directory.fedoraproject.org/) based on [389ds](https://github.com/michel4j/389ds) GitHub project. Contains predefined test users described in [init-users.ldif.tmpl](./ldap/confd/templates/init-users.ldif.tmpl) and used by Shibboleth IdP as an authentication provider 
- [shibboleth-idp](./shibboleth-idp) is a Dockerized version of Shibboleth IdP based on [shibboleth-idp-dockerized](https://github.com/Unicon/shibboleth-idp-dockerized) and [dockerized-idp-testbed](https://github.com/UniconLabs/dockerized-idp-testbed) GitHub projects
- [flask-sp](flask-sp) is a Dockerized Python SP based using [OneLogin's python-saml library](https://github.com/onelogin/python-saml). Used for serving OPDS feeds
- [elasticsearch](./elasticsearch) is a Dockerized version of Elasticsearch with pre-installed analysis-icu plugin required by Circulation Manager
- [circulation-test](./circulation-test) is a Dockerized Flask application used for testing SAML authentication in Circulation Manager 
- [proxy](./proxy) is a Dockerized nginx reversed proxy based on [docker-nginx-with-confd](https://github.com/sysboss/docker-nginx-with-confd) GitHub project

The architecture of the testbed is shown in the picture below:
  ![Testbed architecture](docs/00-Testbed-architecture.png "Testbed architecture")
  
- `cm-test.hilbertteam.net` is a [circulation-test](./circulation-test) instance used for authenticating and downloading books using Circulation Manager (`cm.hilbertteam.net`)
- `cm.hilbertteam.net` is a Circulation Manager instance with a SAML authentication provider acting as a SAML Service Provider (SP)
- `idp.hilbertteam.net` is a [shibboleth-idp](./shibboleth-idp) instance acting as a SAML Identity Provider (IdP)
- `opds.hilbertteam.net` and `opds.hilbert.team` are two instances of [flask-sp](flask-sp) serving two different OPDS feeds using SAML 

## Usage

### Preparing the local environment
1. Update host names in [.env](./.env) file
2. Replace all the host names with `127.0.0.1` in `etc/hosts` file:
```
127.0.0.1     idp.hilbertteam.net
127.0.0.1     opds.hilbertteam.net
127.0.0.1     opds.hilbert.team
127.0.0.1     cm.hilbertteam.net
127.0.0.1     cm-test.hilbertteam.net
```
3. Build containers:
```bash
docker-compose build
```
4. Run [metadata](./metadata) service to generate SAML metadata first (we need to run it first because it's used by other services):
```bash
docker-compose up -d metadata
```
5. Run all other services:
```bash
docker-compose up -d
```

### Setting up Circulation Manager

#### Setting up a new administrator account 
1. Open [Circulation Manager](http://cm-test.hilbertteam.net) and set up an administrator account:
  ![Setting up an administrator account](docs/02-Setting-up-an-administrator-account.png "Setting up an administrator account")
  
2. Login into Circulation Manager:
  ![Logging into Circulation Manager](docs/01-Logging-into-Circulation-Manager.png "Logging into Circulation Manager")

#### Setting up a new library
3. Login into Circulation Manager:
  ![Setting up Circulation Manager](./docs/03-Setting-up-Circulation-Manager.png "Setting up Circulation Manager")
  
4. Start setting up a new library by clicking on **Create new library**:
  ![Setting up a new library](./docs/04-Setting-up-a-new-library.png "Setting up a new library")
  
5. Fill in new library details:
  ![Setting up a new library](./docs/05-Setting-up-a-new-library.png "Setting up a new library")
  
6. Scroll down, click on **Submit** and wait until new library is created:
  ![Setting up a new library](./docs/06-Setting-up-a-new-library.png "Setting up a new library")
  
#### Setting up new collections
7. Click on **Collections** to start setting up collections:
  ![Setting up a new collection](./docs/07-Setting-up-a-new-collection.png "Setting up a new collection")
  
8. Click on **Create new collection**:
  ![Setting up a new collection](./docs/08-Setting-up-a-new-collection.png "Setting up a new collection")
  
9. Fill in details of a new collection using `OPDS1_HOSTNAME` as a URL:
  ![Setting up a new collection](./docs/09-Setting-up-a-new-collection.png "Setting up a new collection")
  
10. Scroll down, associate the new collection with the library, click on **Add library** and then click on **Submit**:
  ![Setting up a new collection](./docs/10-Setting-up-a-new-collection.png "Setting up a new collection")
  
11. Create a new collection using `OPDS2_HOSTNAME` as a URL:
  ![Setting up a new collection](./docs/11-Setting-up-a-new-collection.png "Setting up a new collection")

#### Setting up a SAML authentication provider
12. Click on **Patron authentication** to start setting up a SAML authentication provider:
  ![Setting up a SAML authentication provider](./docs/12-Setting-up-a-patron-authentication.png "Setting up a SAML authentication provider")
  
13. Click on **Create new patron authentication service**:
  ![Setting up a SAML authentication provider](./docs/13-Setting-up-a-patron-authentication.png "Setting up a SAML authentication provider")
  
14. Fill in patron details using [cm.xml](./metadata/output/cm.xml) to fill in SP details and [idp.xml](./metadata/output/idp.xml) to fill in IdP details: 
  ![Setting up a SAML authentication provider](./docs/14-Setting-up-a-patron-authentication.png "Setting up a SAML authentication provider")
  
15. Scroll down, associate the library with the provider and click on **Add library**:
  ![Setting up a SAML authentication provider](./docs/15-Setting-up-a-patron-authentication.png "Setting up a SAML authentication provider")
  
16. Click on **Submit** to finish creating a new authentication provider:
  ![Setting up a SAML authentication provider](./docs/16-Setting-up-a-patron-authentication.png "Setting up a SAML authentication provider")
  
#### Setting up an Elasticsearch service
17. Click on **Search** to start setting up an Elasticsearch service:
  ![Setting up an Elasticsearch service](./docs/17-Setting-up-an-Elasticsearch-service.png "Setting up an Elasticsearch service")
  
18. Click on **Create new search service**:
  ![Setting up an Elasticsearch service](./docs/18-Setting-up-an-Elasticsearch-service.png "Setting up an Elasticsearch service")
  
19. Fill in details of an Elasticsearch service using `es` as a URL: 
  ![Setting up an Elasticsearch service](./docs/19-Setting-up-an-Elasticsearch-service.png "Setting up an Elasticsearch service")
  
#### Importing the OPDS feeds
20. Connect to the Circulation Manager's Docker container:
```bash
docker-compose exec cm bash
```

21. Activate a Python virtual environment:
```bash
source env/bin/activate
```

22. Import the OPDS feeds:
```bash
bin/opds_import_monitor
``` 

23. Update the Elasticsearch indices:
```bash
bin/search_index_refresh
```

### Testing SAML authentication

24. Open [Circulation Manager test application](http://cm-test.hilbertteam.net) and click on **Authenticate** to start authentication process: 
  ![Authenticating with Circulation Manager](./docs/20-Authenticating-with-Circulation-Manager.png "Authenticating with Circulation Manager")
  
25. Enter credentials from [init-users.ldif.tmpl](./ldap/confd/templates/init-users.ldif.tmpl): 
  ![Authenticating with Circulation Manager](./docs/21-Authenticating-with-Circulation-Manager.png "Authenticating with Circulation Manager")

Please note that sometimes LDAP server doesn't import correctly which results in authentication errors.
To resolve this issue you will need to do the following:
```bash
docker-compose exec ldap bash
ldapadd -x -D"cn=Directory Manager" -w${LDAP_MANAGER_PASSWORD} -f /init-users.ldif
```
  
26. Click on **Accept** on the consent screen: 
  ![Authenticating with Circulation Manager](./docs/22-Authenticating-with-Circulation-Manager.png "Authenticating with Circulation Manager")
  
27. Borrow a book clicking on **Borrow**, wait until the operation is finished and then return back:
  ![Borrowing a book](docs/27-Borrowing-a-book.png "Borrowing a book")
  
28. Download a book by clicking on **Download**:
  ![Downloading a book](docs/28-Downloading-a-book.png "Downloading a book")
  
29. Observe the downloaded book:
  ![Downloading a book](docs/29-Downloading-a-book.png "Downloading a book")