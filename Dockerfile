FROM python:3.12.7-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py /app/app.py
COPY pages /app/pages
ENTRYPOINT [ "streamlit", "run", "app.py" ]