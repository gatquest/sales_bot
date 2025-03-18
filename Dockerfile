FROM python:3.9-slim

# Установка Nginx и настройка директорий одним слоем
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/www/html /var/www/images && \
    chown -R www-data:www-data /var/www/html /var/www/images && \
    chmod -R 755 /var/www/html /var/www/images && \
    rm -f /etc/nginx/sites-enabled/default

# Настройка Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Настройка FastAPI - сначала копируем только requirements.txt
WORKDIR /app/server
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование готового билда Angular
WORKDIR /app
COPY client/dist/client/ /var/www/html/

# Копирование папки с изображениями
COPY server/images/ /var/www/images/

# Копирование серверного кода
WORKDIR /app/server
COPY server/ .

# Установка правильных прав доступа одним слоем
RUN chown -R www-data:www-data /var/www/html /var/www/images && \
    chmod -R 755 /var/www/html /var/www/images

# Скрипт для запуска обоих сервисов
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80 8000

CMD ["/start.sh"] 