FROM ubuntu:22.04

# Add socat
RUN apt-get update && apt-get install -y socat && apt-get install -y iputils-ping \
	&& rm -rf /var/lib/apt/lists/*

# Copy files
RUN mkdir -p /opt/app
COPY app/ /opt/app/
WORKDIR /opt/app
RUN chmod +x ./start.sh
RUN chmod a+r ./flag.txt

# Add user
RUN useradd -m ctflib

# Expose port and run
EXPOSE 4242
CMD ["/opt/app/start.sh"]
