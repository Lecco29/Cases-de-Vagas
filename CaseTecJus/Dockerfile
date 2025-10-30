FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Default to starting both API and UI via a simple process manager
CMD sh -c "\
  uvicorn Regras.api:app --host 0.0.0.0 --port 8000 & \
  streamlit run Interface/streamlit_app.py --server.port 8501 --server.address 0.0.0.0\
"


