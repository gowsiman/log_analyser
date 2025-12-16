from langchain_core.prompts import PromptTemplate
from backend import parse_documents

def get_relevant_snippets(llm, QUERY, PROMPT_TEMPLATE, results, error_summary=None):
    
   prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
   context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
   llm_chain = prompt | llm

   prompt_parameters = {
        "context": context_text,
        "query": QUERY,
   }

   if error_summary is not None:
      prompt_parameters.update({'error_summary':error_summary})

   response_text = llm_chain.invoke(prompt_parameters)
   response_text = response_text.content

   response_text = response_text.replace('<<< RESPONSE START >>>', '')
   response_text = response_text.replace('<<< RESPONSE END >>>', '')

   line = [line for line in response_text.split('\n') if line.strip()]
   response_text = '\n'.join(line)

   return response_text

def error_flow(llm, QUERY, results):
    PROMPT_TEMPLATE="""
You are tasked with extracting and presenting only the relevant error log snippets.

Your objective is to:
1. Identify and extract the exact log snippet that directly corresponds to the error in the query.
2. Identify and extract any preceding log snippets that are causally linked to this error.
3. Arrange the extracted logs in chronological order to depict the flow of events leading to the error.

Follow these steps:
1. Locate the Error: Scan the provided log context to find the log entry that matches or explicitly describes the error mentioned in the query.
2. Trace Back Relevant Logs: Identify logs that occurred before the error, which may have led to or contributed to the issue. This includes:
   - Warnings
   - Timeout messages
   - Failed connections or retries
   - Stack traces
3. Maintain Log Integrity: Extract only the necessary logs while preserving their original structure, order, and content.
4. Ensure Precision: Do NOT include irrelevant logs, even if they contain the same keywords as the error.

Important:
- NO explanations
- NO reformatting
- NO summaries or analysis
- ONLY the relevant raw log snippets in their original order

Format your response exactly as follows:

<<< RESPONSE START >>> 
<log snippet 1> 
<log snippet 2> 
... 
<log snippet N> 
<<< RESPONSE END >>>

Context for reference:
{context}

User Query:
{query}
"""
    error_flow_snippets = get_relevant_snippets(llm, QUERY, PROMPT_TEMPLATE, results)
    error_flow_snippets = parse_documents.parse_log_flow_snippets(error_flow_snippets)
    return error_flow_snippets

def success_flow(llm, QUERY, results, error_summary):
   PROMPT_TEMPLATE = """
You are tasked with extracting and presenting only the "happy path" log snippets that correspond to the provided query.

Your task is to:

1. Focus on Successful Log Entries:
   - Identify log entries that indicate success and normal operation
   - Exclude any log entries that denote issues

2. Construct a Flow of Events in the Happy Path:
   - Show the process progressing normally without interruptions
   - If no clear happy path logs exist, simulate a plausible flow based on context
   - Maximum 10 lines of log data

3. Ensure Accurate Log Order:
   - Present logs in chronological order
   - Keep the complete sequence intact

4. Maintain Log Integrity:
   - Do not modify or reformat logs
   - Present them exactly as they appear
   - No explanations or commentary

Format your response exactly as follows:

<<< RESPONSE START >>>
<log snippet 1>
<log snippet 2>
...
<log snippet N>
<<< RESPONSE END >>>

Context of log snippets:
{context}

Summary of the error:
{error_summary}

User's query:
{query}
"""

   success_flow_snippets = get_relevant_snippets(llm, QUERY, PROMPT_TEMPLATE, results, error_summary)
   success_flow_snippets = parse_documents.parse_log_flow_snippets(success_flow_snippets)
   return success_flow_snippets