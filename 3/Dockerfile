# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для playwright
#
# apt-get update — обновляет список пакетов
# apt-get install -y curl — ставит curl (нужен playwright для скачивания браузеров)
# rm -rf /var/lib/apt/lists/* — удаляет временные файлы apt, чтобы уменьшить размер образа
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Создаём директорию для нашего приложения
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
# Устанавливаем браузеры для playwright
RUN playwright install --with-deps

# Копируем остальные файлы
COPY . /app

# Открываем нужный порт (например, 8000)
EXPOSE 8000

# Запуск сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
