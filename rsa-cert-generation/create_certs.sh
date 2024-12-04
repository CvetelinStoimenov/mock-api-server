#!/usr/bin/env bash

##################################################################################################
# ROOT CA
mkdir -p /root/ca/rsa/certs /root/ca/rsa/csr /root/ca/rsa/newcerts /root/ca/rsa/private /root/ca/rsa/volumed_dir
#Read and write to root in private folder
chmod 700 /root/ca/rsa/private
touch /root/ca/rsa/index.txt
#Echo the user id
echo 1000 > /root/ca/rsa/serial
echo 1000 > /root/ca/rsa/crlnumber
#Generating the root key for the Certificate Authority | For simplicity without passphrase for usage within docker
openssl genrsa -out /root/ca/rsa/private/ca.key.pem 4096
#Read-only rights to the running user , root in this cases, as there is no need for any changes to the tls_test_server.Dockerfile to declare another user and simplicity
chmod 777 /root/ca/rsa/private/ca.key.pem
#Now let's create the certificate for the authority and pass along the subject as will be ran in non-interactive mode
openssl req -config /root/ca/rsa/openssl.cnf \
      -key /root/ca/rsa/private/ca.key.pem \
      -new -x509 -days 3650 -sha256 -extensions v3_ca \
      -out /root/ca/rsa/certs/ca.cert.pem \
      -subj "/C=UA/ST=Rivne/L=Rivne/O=SoftServerAcademy/OU=Engineering/CN=SoftServer Engineering Root CA"

#Grant everyone reading rights
chmod 777 /root/ca/rsa/certs/ca.cert.pem
##################################################################################################
# INTERMEDIATE CA
#Now that we created the root pair, we should use and intermediate one.
#This part is the same as above except for the folder
mkdir -p /root/ca/rsa/intermediate/certs /root/ca/rsa/intermediate/csr /root/ca/rsa/intermediate/newcerts /root/ca/rsa/intermediate/private
chmod 700 /root/ca/rsa/intermediate/private

#We must create a serial file to add serial numbers to our certificates - This will be useful when revoking as well
echo 2000 > /root/ca/rsa/intermediate/serial
echo 2000 > /root/ca/rsa/intermediate/crlnumber
touch /root/ca/rsa/intermediate/index.txt

openssl genrsa -out /root/ca/rsa/intermediate/private/intermediate.key.pem 4096
chmod 777 /root/ca/rsa/intermediate/private/intermediate.key.pem

#Creating the intermediate certificate signing request using the intermediate ca config
openssl req -config /root/ca/rsa/intermediate/openssl.cnf \
      -key /root/ca/rsa/intermediate/private/intermediate.key.pem \
      -new -sha256 \
      -out /root/ca/rsa/intermediate/csr/intermediate.csr.pem \
      -subj "/C=UA/ST=Rivne/L=Rivne/O=SoftServerAcademy/OU=Engineering/CN=SoftServer Engineering Intermediate CA"

#Creating an intermediate certificate, by signing the previous csr with the CA key based on root ca config with the directive v3_intermediate_ca extension to sign the intermediate CSR
echo -e "y\ny\n" | openssl ca -config /root/ca/rsa/openssl.cnf \
      -extensions v3_intermediate_ca \
      -days 3650 -notext -md sha256 \
      -in /root/ca/rsa/intermediate/csr/intermediate.csr.pem \
      -out /root/ca/rsa/intermediate/certs/intermediate.cert.pem

#Grant everyone reading rights
chmod 777 /root/ca/rsa/intermediate/certs/intermediate.cert.pem
##################################################################################################
# CN = MOCK HOSTNAME
##################################################################################################
sed -i "s+<mock-hostname>+$MOCK_HOSTNAME+g" /root/ca/rsa/intermediate/openssl.cnf

#First generate the key for the server
openssl genrsa \
      -out /root/ca/rsa/intermediate/private/mock.key.pem 4096
chmod 777 /root/ca/rsa/intermediate/private/mock.key.pem

#Then create the certificate signing request
openssl req -config /root/ca/rsa/intermediate/openssl.cnf \
      -key /root/ca/rsa/intermediate/private/mock.key.pem \
      -new -sha256 -out /root/ca/rsa/intermediate/csr/mock.csr.pem \
      -subj "/C=UA/ST=Rivne/L=Rivne/O=SoftServerAcademy/OU=Engineering/CN=$MOCK_HOSTNAME"

#Now sign it with the intermediate CA
echo -e "y\ny\n" | openssl ca -config /root/ca/rsa/intermediate/openssl.cnf \
      -extensions leaf_cert -days 365 -notext -md sha256 \
      -in /root/ca/rsa/intermediate/csr/mock.csr.pem \
      -out /root/ca/rsa/intermediate/certs/mock.cert.pem

chmod 777 /root/ca/rsa/intermediate/certs/mock.cert.pem
##################################################################################################
# Creating chains and copy certs to the volumed_dir
##################################################################################################
#Creating certificate chain with intermediate and root
cat /root/ca/rsa/intermediate/certs/intermediate.cert.pem \
      /root/ca/rsa/certs/ca.cert.pem > /root/ca/rsa/certs/ca-chain.cert.pem
chmod 777 /root/ca/rsa/certs/ca-chain.cert.pem

#Creating full certificate chain
cat /root/ca/rsa/intermediate/certs/mock.cert.pem \
      /root/ca/rsa/intermediate/certs/intermediate.cert.pem \
      /root/ca/rsa/certs/ca.cert.pem > /root/ca/rsa/certs/full-chain.cert.pem
chmod 777 /root/ca/rsa/certs/full-chain.cert.pem

# Copy single certs to volumed_dir
cp /root/ca/rsa/certs/ca-chain.cert.pem /root/ca/rsa/volumed_dir/ca-chain.cert.pem
cp /root/ca/rsa/certs/full-chain.cert.pem /root/ca/rsa/volumed_dir/full-chain.cert.pem
cp /root/ca/rsa/certs/ca.cert.pem /root/ca/rsa/volumed_dir/ca.cert.pem
cp /root/ca/rsa/intermediate/certs/intermediate.cert.pem /root/ca/rsa/volumed_dir/intermediate.cert.pem
cp /root/ca/rsa/intermediate/certs/mock.cert.pem /root/ca/rsa/volumed_dir/mock.cert.pem
cp /root/ca/rsa/intermediate/private/mock.key.pem /root/ca/rsa/volumed_dir/mock.key.pem
##################################################################################################