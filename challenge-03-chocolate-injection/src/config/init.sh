#!/bin/bash

# Prepare db folder
mkdir -p /var/www/db/
chmod -R 755 /var/www/db/
chown -R www-data:www-data /var/www/db/

sed -i "s/{{RANDOM-ADMIN-PASSWORD}}/$(openssl rand -hex 32)/" /var/www/html/includes/database.php

# Start apache
/usr/sbin/apache2ctl -D FOREGROUND
