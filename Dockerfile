FROM python:3.12-slim

WORKDIR / app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

EXPOSE 8000 8501 

CMD ["./start.sh"]
