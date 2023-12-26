# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /HWTracker

# Устанавливаем переменную окружения PYTHONUNBUFFERED в значение 1
ENV PYTHONUNBUFFERED=1

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Запуск команды при запуске контейнера
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
