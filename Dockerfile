# Gunakan image Python yang ringan
FROM python:3.11-slim

# Install OS-level dependency
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Set workdir
WORKDIR /app

# Salin semua ke dalam container
COPY . /app

# Instal Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Buka port untuk Gunicorn
EXPOSE 8000

# Jalankan Gunicorn
CMD ["gunicorn", "sehatSulungProject.wsgi:application", "--bind", "0.0.0.0:8000"]
