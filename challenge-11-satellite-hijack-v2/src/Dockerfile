FROM oven/bun:slim

# set environment variables
ENV APP_PORT=8000

# Copy challenge files
RUN mkdir -p /opt/app
COPY app/ /opt/app/
WORKDIR /opt/app

# Install dependencies
RUN bun install

# Execute
EXPOSE 8000
CMD ["app.ts"]
