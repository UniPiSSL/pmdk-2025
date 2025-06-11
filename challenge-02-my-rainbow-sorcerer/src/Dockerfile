FROM python:slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add socat
RUN apt-get update && apt-get install -y socat \
    && rm -rf /var/lib/apt/lists/*

# Copy challenge files
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY app/ /opt/app/

# Install requirements
RUN pip install -r requirements.txt

# Expose port and run
EXPOSE 1337

CMD socat TCP4-LISTEN:1337,reuseaddr,fork EXEC:"python server.py",stderr,pty,iexten=0,echo=0
