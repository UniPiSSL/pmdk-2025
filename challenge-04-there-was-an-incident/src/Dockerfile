# Ubuntu Image
FROM ubuntu:latest

# Install required packages
RUN apt-get update && \
    apt-get install -y openssh-server zip unzip && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /var/run/sshd

# Add a non-root user
RUN useradd -m support && \
    echo 'support:password123' | chpasswd && \
    usermod --shell /bin/bash support && \
    mkdir /home/support/.ssh && \
    chmod 700 /home/support/.ssh

# Copy files on the server
COPY ./files/documents /home/support/documents
COPY ./files/setup.sh /tmp/setup.sh
COPY ./files/init.sh /init.sh

# Expose SSH port
EXPOSE 22

# Init container
CMD ["/bin/bash", "/init.sh"]
