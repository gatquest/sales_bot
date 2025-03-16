FROM python:3.9

# Установка Nginx
RUN apt-get update && apt-get install -y nginx

# Настройка директории для статических файлов
RUN mkdir -p /var/www/html
RUN mkdir -p /var/www/images
RUN chown -R www-data:www-data /var/www/html
RUN chown -R www-data:www-data /var/www/images
RUN chmod -R 755 /var/www/html
RUN chmod -R 755 /var/www/images

# Настройка Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/sites-enabled/default

# Копирование готового билда Angular
WORKDIR /app
COPY client/dist/client/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html
RUN chmod -R 755 /var/www/html
RUN ls -la /var/www/html/

# Копирование папки с изображениями
COPY server/images/ /var/www/images/
RUN chown -R www-data:www-data /var/www/images
RUN chmod -R 755 /var/www/images
RUN ls -la /var/www/images/

# Настройка FastAPI
WORKDIR /app/server
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ .
RUN ls -la

# Скрипт для запуска обоих сервисов
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80 8000

CMD ["/start.sh"] 