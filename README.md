# circulation-saml-test

Testbed which could be used for testing SAML-based patron authentication in 
[Circulation Manager](https://github.com/NYPL-Simplified/circulation).

Project consists of the following modules:

- [metadata](./metadata) is a Dockerized busybox generating SAML metadata using [confd](https://github.com/kelseyhightower/confd)
- [ldap](./ldap) is a Dockerized version of [389 Directory Server](https://directory.fedoraproject.org/) based on [389ds](https://github.com/michel4j/389ds) GitHub project
- [shibboleth-idp](./shibboleth-idp) is a Dockerized version of Shibboleth IdP based on [shibboleth-idp-dockerized](https://github.com/Unicon/shibboleth-idp-dockerized) and [dockerized-idp-testbed](https://github.com/UniconLabs/dockerized-idp-testbed) GitHub projects
- [flask-sp](flask-sp) is a Dockerized Python SP based using [OneLogin's python-saml library](https://github.com/onelogin/python-saml) and serving OPDS feeds
- [elasticsearch](./elasticsearch) is a Dockerized version of Elasticsearch with pre-installed analysis-icu plugin required by Circulation Manager
- [circulation-test](./circulation-test) is a Dockerized Flask application used for testing SAML authentication in Circulation Manager 
- [proxy](./proxy) is a Dockerized nginx reversed proxy based on [docker-nginx-with-confd](https://github.com/sysboss/docker-nginx-with-confd) GitHub project

## Usage

To run this project locally please do the following:

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
