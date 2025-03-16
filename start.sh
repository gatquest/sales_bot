#!/bin/bash

# Проверка содержимого директории с фронтендом
echo "Checking frontend files:"
ls -la /var/www/html/

# Запуск Nginx с выводом ошибок
echo "Starting Nginx..."
nginx -t
service nginx start
service nginx status

# Проверка логов Nginx
echo "Nginx error log:"
tail /var/log/nginx/error.log

# Запуск FastAPI
echo "Starting FastAPI server..."
cd /app/server
uvicorn main:app --host 0.0.0.0 --port 8000 