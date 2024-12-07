# Use the official Debian slim image as the base image
FROM library/debian:bookworm-slim

# Set the user to root for elevated privileges during setup
USER root

# Create necessary directories in the container filesystem
RUN mkdir -p /opt/project/upload

# Set the working directory for subsequent instructions
WORKDIR /opt/project

# Copy a list of required Debian packages into the container
COPY debian_packages.txt /opt/project/debian_packages.txt

# Update package lists, install the listed packages, and clean up to reduce image size
RUN apt-get update --allow-insecure-repositories && \
    DEBIAN_FRONTEND=noninteractive xargs -a /opt/project/debian_packages.txt \
    apt-get install -y --allow-unauthenticated && \
    apt-get clean && \
    rm -rf /opt/project/debian_packages.txt

# Unset REQUESTS_CA_BUNDLE environment variable to handle a known issue with `requests` library
# Reference: https://github.com/psf/requests/issues/3829
ENV REQUESTS_CA_BUNDLE=

# Suppress Python warnings related to unverified HTTPS requests
ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"

# Set the mock server's hostname for use in the application
ENV MOCK_HOSTNAME=api-mock-server

# Copy certificate generation scripts and configuration files into the container
COPY rsa-cert-generation/create_certs.sh /root/ca/rsa/create_certs.sh
COPY rsa-cert-generation/root-openssl.conf /root/ca/rsa/openssl.cnf
COPY rsa-cert-generation/intermediate-openssl.conf /root/ca/rsa/intermediate/openssl.cnf

# Copy the application source code and binaries into the container
COPY app /opt/project/
COPY bin /opt/project/

# Generate RSA certificates using the provided script
RUN /root/ca/rsa/create_certs.sh

# Set the entrypoint to start the application when the container is run
ENTRYPOINT ["/opt/project/start.sh"]
