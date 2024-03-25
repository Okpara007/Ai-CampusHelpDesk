FROM python:3-slim


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt ./

# Install psycopg2 with specific flags and environment variables
# RUN LIBRARY_PATH=/usr/local/lib:/usr/lib pip install psycopg2==2.9.9


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000


CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

