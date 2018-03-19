sudo su postgres
#psql -c 'ALTER USER postgres WITH ENCRYPTED password "password"' postgres
psql -c 'CREATE USER pywps  WITH ENCRYPTED password "toto123"' postgres
psql -c 'CREATE DATABASE "pywps-demo" WITH OWNER = pywps' postgres
