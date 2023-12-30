"""
Creates a vector database based on the data in the data folder
"""

import os
import pandas as pd
from pathlib import Path
from utils import get_api_key
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DataFrameLoader


os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://open-ai-embeddings.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = get_api_key()

KNOWLEDGE_BASE = "hjertemedisin"
PARENT_FOLDER_PATH = Path(__file__).parent.parent

embedding_model = OpenAIEmbeddings(deployment='embed')

df_data = pd.read_csv(encoding="utf8", index_col = 0,
                      filepath_or_buffer= PARENT_FOLDER_PATH  / "data" / f"{KNOWLEDGE_BASE}.csv")
loader = DataFrameLoader(df_data)

data = loader.load()

vdb_chunks = FAISS.from_documents(data, embedding_model)

# Stores it locally - automatically creates folder, so can be gitignored
vdb_chunks.save_local(PARENT_FOLDER_PATH / "vdb" / KNOWLEDGE_BASE  , index_name="index")
