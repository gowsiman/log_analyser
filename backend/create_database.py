from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

import os
import sys
import shutil
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from backend import parse_documents
from backend import extract_metadata

def create(APP_ID):
    CHROMA_PATH = f"chroma/{APP_ID}"
    DATA_PATH = f"data/logs/{APP_ID}"
    generate_data_store(APP_ID, DATA_PATH, CHROMA_PATH)


def generate_data_store(APP_ID, DATA_PATH, CHROMA_PATH):
    documents = load_documents(DATA_PATH)
    chunks = split_text(APP_ID, DATA_PATH, documents)
    save_to_chroma(chunks, DATA_PATH, CHROMA_PATH)


def load_documents(DATA_PATH):
    parse_documents.process_all_log_files(DATA_PATH)
    loader = DirectoryLoader(DATA_PATH, glob="*.log")
    documents = loader.load()
    return documents


def split_text(APP_ID, DATA_PATH, documents: list[Document]):

    # First split by log entries
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["|||"],  # Split on the delimiter we added
        chunk_size=1000,      # Larger than the biggest log entry
        chunk_overlap=500,
        keep_separator=False, # Remove '|||' from the output
    )

    final_chunks = text_splitter.split_documents(documents)
    for chunk in final_chunks:
        if "|||" in chunk.page_content:
            chunk.page_content = chunk.page_content.replace("|||", "")

    log_snippets = '\n'.join([extract_metadata.extract_metadata_snippet(chunk.page_content) for chunk in final_chunks[:7]])

    metadata_keys = extract_metadata.get_metadata(log_snippets)

    # Create dictionary mapping metadata fields to values
    for chunk in final_chunks:
        metadata_snippet = extract_metadata.extract_metadata_snippet(chunk.page_content)
        metadata = metadata_snippet.split(' | ') 
        metadata_dict = dict(zip(metadata_keys[:4], metadata[:4]))
        metadata_dict = {'APP_ID': APP_ID, **metadata_dict}
        
        for key in ['Timestamp', 'Date', 'Datetime']:  # List of potential keys
            if key in metadata_dict.keys():
                timestamp_str = metadata_dict[key]
                timestamp = parse_documents.parse_unix_epoch_timestamp(timestamp_str)
                metadata_dict[key] = timestamp

        chunk.metadata = metadata_dict

    with open(f'{DATA_PATH}/chunks-metadata.json', 'w') as file:
        json.dump(final_chunks[0].metadata, file, indent=4) 
    
    return final_chunks


def save_to_chroma(chunks: list[Document], DATA_PATH, CHROMA_PATH):
    # Clear out the database first
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", model_kwargs={'trust_remote_code': True}), persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    create('APP_4')
