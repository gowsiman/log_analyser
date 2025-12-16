from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
import re

def extract_metadata_snippet(log_snippet):
    log_snippet = log_snippet.replace('[', '')
    log_snippet = log_snippet.replace(' ]', '')
    log_snippet = log_snippet.replace(']', '')
    metadatas = log_snippet.split(' ')
    # print(metadatas)
    return " | ".join(metadatas[:6])

def get_metadata(log_snippet):
    
    PROMPT_TEMPLATE = '''
You are tasked with analyzing log data to extract metadata fields that represent the unique identifiers for each row in the log. 
These metadata fields consist of the first five to six words of each log entry, which should be used to uniquely identify the row. 
You are not concerned with any content beyond these words, just the initial part of each row. Your role is to identify appropriate, 
generic keyword names for each of these fields, keeping the field names general yet descriptive.

Task:
Look at the following log snippet and suggest suitable generic keyword names for the first five to six words of each row. 
These should be fields that can uniquely identify the log entry, based on the beginning of the line. 
Focus on identifying patterns for these metadata fields.

Corner Cases to Handle:
If the log entries are too short (fewer than 6 words), treat the entire entry as metadata.
If the log starts with a timestamp or similar recurring pattern, treat those patterns as part of the metadata.
If there are special symbols or inconsistent formatting (e.g., nested key-value pairs), 
ignore the symbols and focus on the core identifying elements.

Guidelines:
STRICTLY DO NOT EXCEED 7 LINES IN YOUR RESPONSE.
YOUR RESPONSE SHOULD ONLY HAVE METADATA FIELD NAMES ONE AFTER ANOTHER.
The keyword names should be generic and descriptive, applicable to a variety of log formats.
If there are fewer than six words in the snippet, ensure you list all available fields.
Each field should have only word (Don't generate longer names)
Order of listing should be same as the order in which these fields appear in log entry.

Log Snippet for Reference:
{log_snippet}

Response Format:
(STRICTLY FORMAT YOUR RESPONSE AS BELOW. ANY DEVIATION IN THE FORMAT WOULD BE PENALIZED)

<start of response>
1.key1
2.key2
3.key3
4.key4
5.key5
<end of response>

    '''

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
     
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2", 
        max_new_tokens=512,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=0.01,
        repetition_penalty=1.03
    )

    llm_chain = prompt | llm
    response_text = llm_chain.invoke({"log_snippet": log_snippet})
    metadata_list = re.findall(r"\d+\.\s*(.+)", response_text)

    # print(metadata_list)
    return metadata_list
