import os
import sys
import warnings
import json
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from backend import analyzer
from backend import extract_snippets
from backend import parse_documents


# Suppress all warnings
warnings.filterwarnings("ignore")

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = gemini_api_key



def init(APP_ID):
   llm = ChatGoogleGenerativeAI(
      model="gemini-2.0-flash",
      convert_system_message_to_human=True,
      temperature=0.1,
      top_p=0.95,
      top_k=40,
      max_output_tokens=2048,
   )

   CHROMA_PATH = f"chroma/{APP_ID}"
   embedding_function = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", \
                                             model_kwargs={'trust_remote_code': True})
   db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
   print("")
   return llm, db


def get_filtered_docs(db, APP_ID, TIME_FROM, TIME_TO):
   TIME_FROM = int(parse_documents.parse_unix_epoch_timestamp(TIME_FROM))
   TIME_TO = int(parse_documents.parse_unix_epoch_timestamp(TIME_TO))

   docs = db.get(
      where = {
         "$and": [
            {"APP_ID": APP_ID},  # Exact match for APP_ID
            {"Timestamp": {"$gte": TIME_FROM}},  # Greater than or equal to
            {"Timestamp": {"$lte": TIME_TO}}   # Less than or equal to
        ]
      }
   )

   count = len(docs['documents'])
   return count


def analyse(APP_ID, TIME_FROM, TIME_TO, QUERY):
   

   # output = {
   #    "RawLogs": "raw",
   #    "Summary": "summary",
   #    "Report": "report",
   #    "Explanation": "explanation",
   #    "ExpectedFlow": "expected_flow",
   #    "Remediation": "remediation",
   #    "HappyPath": "happy_path_snippet"
   # }
   # return output

   llm, db = init(APP_ID)

   log_entry_count = get_filtered_docs(db, APP_ID, TIME_FROM, TIME_TO)
   print(log_entry_count)

   results = analyzer.get_relevant_docs(db, llm, APP_ID, TIME_FROM, TIME_TO, QUERY)

   error_snippet = extract_snippets.error_flow(llm, QUERY, results)
   print(error_snippet)
   print("\n\n")

   analysis = analyzer.analyze_without_metadata(llm, QUERY, results, error_snippet)
   summary, report, explanation, expected_flow, remediation = parse_documents.parse_response(analysis)

   # DIAGRAM GENERATION ADDED HERE
   expected_flow_diagram_code = analyzer.generate_mermaidjs_diagram_code(llm, expected_flow)
   expected_flow_diagram_code = parse_documents.parse_mermaid_llm_output(expected_flow_diagram_code)

   print("RAW EXPECTED FLOW :", expected_flow)
   print("\n\n")
   print("DIAGRAM EXPECTED FLOW :", expected_flow_diagram_code)
   print("\n\n")

   # summary = f"<i>Analyzed {log_entry_count} log snippets...<i>\n\n" + summary
   print(analysis)
   print("\n\n")


   happy_path_snippet = extract_snippets.success_flow(llm, QUERY, results, analysis)
   print(happy_path_snippet)
   print("\n\n")

   output = {
      "RawLogs": error_snippet,
      "Summary": summary,
      "Report": report,
      "Explanation": explanation,
      "ExpectedFlow": expected_flow_diagram_code,
      "Remediation": remediation,
      "HappyPath": happy_path_snippet
   }

   
   import pprint
   pprint.pprint(output)


   # with open('output_.json', 'r') as f:
   #    text = json.load(f)
   #    # pprint.pprint(text)
   #
   # return text
   return output
   
if __name__ == "__main__":
   QUERY = "Show me the error hotspots in the logs for the selected time window"
   analyse('APP_4', '2025-02-01T00:39', '2025-02-05T21:40', QUERY)
