# backend dockerfile is in the root directory to prevent import errors

FROM python:3.10-slim

WORKDIR /

LABEL org.opencontainers.image.source="https://github.com/mollyiverson/ACME10-HE-RAGApp"

RUN pip install --no-cache-dir gdown

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /backend

# Download large files from Google Drive 
RUN gdown "1aKMoiQpy9LoKpK0XdPptw_TUNm-I9U_0" -O /backend/app/data_processing/vector_search_data/index.faiss && \
    gdown "1TyTSuojE9wMWSUXMrC31atVkX2wcm3s-" -O /backend/app/data_processing/embeddings_data/text_embeddings.npy

ENV PYTHONPATH=/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
