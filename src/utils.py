"""
Helper methods for the app
"""

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from pathlib import Path
import configparser
import tiktoken


PARENT_FOLDER_PATH = Path(__file__).parent.parent
TOKEN_LIMIT = 8000


def get_api_key():
    config = configparser.ConfigParser()
    config.read(PARENT_FOLDER_PATH / 'config.ini')
    api_key = config['credentials']['api_key']
    return api_key


def get_most_relevant_chunks(question, KNOWLEDGE_BASE, k=10, fit_to_max_token=False):
    """ Embeds the question and returns the k closest chunks
    from the vector database

    Args:
        question (str): user input
        k (int, optional): number of chunks. Defaults to 10.

    Returns:
        _type_: List[Tuple[Document, float]]
    """
    embeddings = OpenAIEmbeddings(deployment='embed')

    vdb_chunks = FAISS.load_local(
        PARENT_FOLDER_PATH /  "vdb" / KNOWLEDGE_BASE ,
        embeddings,
        index_name="index")
    

    # TODO: I think it's best to start with similarity, but we can try mmr too
    retrieval_method = "similarity"
    if retrieval_method == "mmr":
        retrieved_chunks = vdb_chunks.max_marginal_relevance_search(
            question, k)
    else:
        # Uses L2 (euclid?) distance... -> lower score is 
        if fit_to_max_token:
            k = fit_context_to_token_limit(question, vdb_chunks)
        retrieved_chunks = vdb_chunks.similarity_search_with_score(question, k)
    
    return retrieved_chunks


def fit_context_to_token_limit(question, vdb):
    """ Adds as many chunks as possible - until max token limit is reached """
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    i = 1
    while True:
        retrieved_chunks = vdb.similarity_search_with_score(question, i)
        tokens = [len(enc.encode(j[0].page_content)) for j in retrieved_chunks]
        
        if sum(tokens) >= TOKEN_LIMIT:
            return i-1
        if i > len(retrieved_chunks):
            return i
        i += 1