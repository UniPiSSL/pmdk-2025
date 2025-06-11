FROM php:apache

# Copy challenge files
RUN rm -rf /var/www/html
COPY html /var/www/html
COPY flag.txt /var/www/flag.txt
COPY config/init.sh /var/www/init.sh
RUN chmod -R 777 /var/www/ && \
	chmod +x /var/www/init.sh

# Expose port
EXPOSE 80

CMD ["/bin/bash", "/var/www/init.sh"]
