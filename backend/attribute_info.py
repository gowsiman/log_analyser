from langchain.chains.query_constructor.schema import AttributeInfo
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
import json


def get_metadata_info(DATA_PATH, metadata):
    PROMPT_TEMPLATE = '''
        Below is the JSON of some metadata information.
        {metadata}

        For each of the field in it, I want you to generate the following key value pairs
        that tells more about each field.
        - name
        - description
        - type (integer, string, float)

        Only give me the entire json for it.

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
    response_text = llm_chain.invoke({"metadata": metadata})
    metadata_info = json.loads(response_text)

    with open(f"{DATA_PATH}/metadata-info.json", "w+") as file:
        json.dump(metadata_info, file, indent=4)

    return metadata_info

def get_attribute_info(APP_ID):

    DATA_PATH = f"data/logs/{APP_ID}"
    with open(f"{DATA_PATH}/chunks-metadata.json", 'r') as file:
        metadata = file.read()
    
    metadata_info = get_metadata_info(DATA_PATH, metadata)

    metadata_field_info = [AttributeInfo(name=metadata, description=info['description'], type=info['type']) for metadata, info in metadata_info.items()]

    return metadata_field_info

if __name__ == '__main__':
    print(get_attribute_info())