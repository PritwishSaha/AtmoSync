FROM python:3.13-slim

WORKDIR /app

COPY dashboard/requirements.txt ./dashboard/requirements.txt

RUN pip install --no-cache-dir -r ./dashboard/requirements.txt

COPY dashboard ./dashboard
COPY data/processed ./data/processed

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]