#!/bin/bash

mkdir LDAP
cd ./LDAP
git clone https://github.com/osixia/docker-openldap.git
git clone https://github.com/osixia/docker-phpLDAPadmin.git
docker run --rm -p 389:389 -p 636:636 --name ldap-service --hostname ldap-service -v '/Users/su/tmp/openldap/database:/var/lib/ldap' -v '/Users/su/tmp/openldap/config:/etc/ldap/slapd.d' --detach osixia/openldap:1.2.4
docker run --rm -p 6443:443 --name phpldapadmin-service --hostname phpldapadmin-service --link ldap-service:ldap-host --env PHPLDAPADMIN_LDAP_HOSTS=ldap-host --detach osixia/phpldapadmin:0.8.0
cd ..
cd Ldap-and-Google-Authenticator
sudo python3 main.py
