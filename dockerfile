# Dockerfile
FROM php:8.2-apache

# Install system dependencies and zip extension (common for Composer)
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    && docker-php-ext-install pdo pdo_mysql

# Enable Apache Rewrite Module
RUN a2enmod rewrite

# Copy application files to the container
COPY . /var/www/html/

# Set working directory
WORKDIR /var/www/html

# CRITICAL: Set permissions for the web server user (www-data)
# This allows the script to write to users.json and error.log
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Render automatically sets port 80/10000, Apache listens on 80 by default.
# We expose port 80 to tell Docker this port is interesting.
EXPOSE 80