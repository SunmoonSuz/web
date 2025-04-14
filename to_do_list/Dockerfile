FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /to_do_list


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "to_do_list.wsgi:application"]