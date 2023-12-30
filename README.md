# RAG Streamlit Chatbot

This repository serves as an example for creating a streamlit application. The goal is to be able to quickly spin up a RAG chatbot (with a streamlit interface) that can answer questions about your own data.

## Prerequisites

To use the code in this repo, there are two things you need: data (duh) and a OpenAI API key.

First, provide the key in a file you call `config.ini` in this format:

```
[credentials]
api_key = <your_OpenAI_API_key>
```

Then, you must prepare your data. Using Langchain, a locally stored vector database will be created from the data. See `src/create_vdb.py` for implementation. So in essence:
1. Create a csv file where each row are text chunks, and contains the text in a column named "text".
2. Name the file _<your_data>.csv_ and save it in the data folder.
3. Set `KNOWLEDGE_BASE = "your_data"` in `create_vdb.py` and in `app.py`

Currently, there is an example for "hjertemedisin" (heart medicine) data, and you can see how the data is stored as a csv in `data/hjertemedisin.csv`

## Setup

Before starting, make sure you have [Python 3.x](https://www.python.org/downloads/) installed on your system.

### Step 1: Clone the Repository

Clone this repository to your local machine using Git:

```bash
git clone https://github.com/martinstiles/RAG-Streamlit-Chatbot
cd RAG-Streamlit-Chatbot
```

### Step 2: Activate Python Venv (optional)

Initialize the python environment by running the following command inside the project folder.

```bash
python -m venv venv
```

Activate the venv by running the following on **Windows**:

```bash
venv\Scripts\activate
```

or on **Mac** / **Linux**:
```bash
source venv/bin/activate
```


### Step 3: Install requirements

All required python packages are found in ```requirements.txt``` and can be installed by running:
```bash
pip install -r requirements.txt
```

## Create Vector Database

If you have followed the setup procedure, create a vector database by running `src/create_vdb.py`.


## Run the project

If you have created a vector database, the project can be run with the following command:

```bash
streamlit run src/app.py
```


## Create and run Docker Container

If you want, you can run the applicaiton in a Docker container. First, make sure you have Docker installed by running:

```bash
docker --version
```

To create a Docker image for the streamlit application on your local machine and run the following command:

```bash
docker build -t llm_demo .
```

Once the image has been created, you can run a container locally by running:

```bash
docker run -p 8501:8501 llm_demo
```

## Security Concerns

In general, you should never feed sensitive data into a public API. If you are trying to chat with your own private data and use a LLM API to accomplish it (like in this repo): make sure the data are non-sensitive.
