"""
Methods for retrieving message strings
"""


def get_system_message():
    return """
    You are a helpful assistant.
    Instructions:
    - Only answer questions in Norweigan.
    - Always include the relevant paragraph in the answer. "
    """


def get_human_message(question, search_results):
    return f"""
    Use the below context to answer the subsequent question. If the answer cannot be found, write "I don't know."

    Context:
    \"\"\"
    {search_results}
    \"\"\"
    
    Question: {question}
    """
