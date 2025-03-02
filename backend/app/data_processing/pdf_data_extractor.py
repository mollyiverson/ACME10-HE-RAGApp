import pymupdf
import os
import pandas as pd

def extract_text_from_pdfs(dir):
    texts = []
    for file in os.listdir(dir):
        if file.endswith('.pdf'):
            path = os.path.join(dir, file)
            doc = pymupdf.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            texts.append(text)
    return texts

def texts_to_dataframe(texts):
    df = pd.DataFrame(texts, columns=['text'])
    return df

def save_dataframe_to_parquet(df, output_path):
    df.to_parquet(output_path)

# Example usage
if __name__ == "__main__":
    dir = 'backend/app/data_processing/embeddings_data/embeddings_pdf'
    output_path = 'backend/app/data_processing/pdf_data.parquet'

    texts = extract_text_from_pdfs(dir)
    df = texts_to_dataframe(texts)
    save_dataframe_to_parquet(df, output_path)