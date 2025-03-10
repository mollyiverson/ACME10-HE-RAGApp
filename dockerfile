# backend dockerfile is in the root directory to prevent import errors
FROM python:3.10-slim

WORKDIR /

LABEL org.opencontainers.image.source="https://github.com/mollyiverson/ACME10-HE-RAGApp"

RUN apt-get update && apt-get install -y wget

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /backend

RUN wget -O /backend/app/data_processing/vector_search_data/index.faiss \
    "https://huggingface.co/datasets/miverson9/acme10-he-ragapp-embeddings/resolve/main/index.faiss" && \
    wget -O /backend/app/data_processing/embeddings_data/text_embeddings.npy \
    "https://huggingface.co/datasets/miverson9/acme10-he-ragapp-embeddings/resolve/main/text_embeddings.npy"

ENV PYTHONPATH=/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
