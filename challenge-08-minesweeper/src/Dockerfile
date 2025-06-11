FROM php:apache

# Copy challenge files
RUN rm -rf /var/www/html
COPY html/index.html /var/www/html/index.html
COPY html/script.js /var/www/html/script.js

# Expose port
EXPOSE 80
