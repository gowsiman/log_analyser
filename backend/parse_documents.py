from datetime import datetime
from dateutil.parser import parse
import os
import glob
import re


def parse_unix_epoch_timestamp(timestamp_str):
    try:
        # Convert the timestamp string to a datetime object
        timestamp_obj = parse(timestamp_str)
        
        # Convert to milliseconds if needed (multiply by 1000)
        epoch_milliseconds = int(timestamp_obj.timestamp() * 1000)
        
        return epoch_milliseconds
    
    except Exception as e:
        print(f"Error: {e}")
        return None


def process_all_log_files(directory):

    """Processes all log files in the specified directory and ensures proper spacing."""
    
    log_files = glob.glob(os.path.join(directory, "*.log"))  # Adjust the extension if needed
    # for file in log_files:
    #     add_delimiter_on_trace_change(file)
    add_delimiter(log_files)    


def add_delimiter_on_trace_change(input_file):
    with open(input_file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()

        previous_trace_id = None
        modified_lines = []

        for line in lines:
            # Extract traceId using regex (assuming format like '[TRACE1234]')
            match = re.search(r'\[(TRACE[0-9]+)\]', line)
            trace_id = match.group(1) if match else None

            if trace_id and trace_id != previous_trace_id:
                line = '|||' + line  # Add delimiter when traceId changes

            modified_lines.append(line)
            previous_trace_id = trace_id  # Update previous traceId

        f.writelines(modified_lines)




def add_delimiter(log_files):
    for file in log_files:
        with open(file, "r+", encoding="utf-8") as f:
            
            content = f.read()
            content = content.replace('|||', '')
            processed = preprocess_logs(content)
            f.seek(0)
            f.write(processed)

def preprocess_logs(log_text: str) -> str:
    # Regex to match common timestamp formats (customize as needed)
    TIMESTAMP_PATTERN = r"""
    ^
    (
        \[\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\] |  # e.g., [2023-10-05 12:34:56]
        \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z      |  # ISO 8601 (UTC)
        \d{10}\.\d{3}                              |  # Unix timestamp (e.g., 1672531200.123)
        \w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}               # e.g., Oct 05 12:34:56
    )
    """
    

    # Add '|||' before timestamps and strip leading delimiters
    processed = re.sub(
        pattern=TIMESTAMP_PATTERN,
        repl=r"|||\1",  # Insert delimiter before the timestamp
        string=log_text,
        flags=re.VERBOSE | re.MULTILINE
    )

    # Remove leading '|||' if present
    return processed.lstrip("|||")


def parse_mermaid_llm_output(llm_output):

    # Remove the enclosing characters like '```mermaid\n' and '```'
    if llm_output.startswith("```mermaid") and llm_output.endswith("```"):
        # Extract the content between '```mermaid\n' and '```'
        mermaid_code = llm_output[len("```mermaid\n"):-len("```")].strip()
        return mermaid_code
    else:
        return llm_output

def parse_response(text):
    # Define the headings
    headings = [
        ['Summary', 'Analysis'],
        ['Incident/Scenario Report', 'Incident Report', 'Scenario Report', 'Report :', 'Incident Details'],
        ['Explanation'],
        ['Expected Ideal Flow (Happy Path)', 'Expected Ideal Flow'],
        ['Remediation / Recommendations', 'Remediation', 'Recommendation']
    ]

    # Initialize the dictionary with empty strings instead of None
    keys = [heading[0] for heading in headings]
    response = dict.fromkeys(keys, "")

    key = None
    for line in text.split('\n'):
        skip_line = False
        for heading in headings:
            for name in heading:
                if name in line :
                    key = heading[0]
                    skip_line = True
                    break  # Exit inner loop once the heading is found
        if not skip_line and key is not None:
            if line.strip(): 
                # Remove bold markers and preserve original line format
                line = line.replace("**", "")
                line = line.replace("### **Answer**", "")
                line = line.replace("**Answer**", "")
                # print(len(line))
                if len(line) > 200:
                    line = line.split(". ")
                    line = '.\n'.join(line)

                line = line.strip()
                response[key] += line + "\n"
    
    response['Summary'] = add_bullets(response["Summary"])
    response['Explanation'] = add_bullets(response["Explanation"])
    

    if response['Summary'] == "":
        response['Summary'] = text

    return (
        response.get("Summary", "").strip(),
        response.get("Incident/Scenario Report", "").strip(),
        response.get("Explanation", "").strip(),
        response.get("Expected Ideal Flow (Happy Path)", "").strip(),
        response.get("Remediation / Recommendations", "").strip(),
    )


def parse_log_flow_snippets(log_flow):
    lines = log_flow.split('\n')
    if len(lines) > 5:
        lines = lines[:-1]
        # lines.append("\nContinues...")
    
    lines = list(dict.fromkeys(lines))
    return "\n".join(lines)

def add_bullets(text):
    lines = text.strip().split("\n")  # Split text into lines

    # Check if bullets are present
    if all(not re.match(r"(\d+\.\s+|[-•*])", line.strip()) for line in lines):
        # Add bullets to lines that are not empty
        lines = [f"* {line}" if line.strip() else line for line in lines]

    return "\n".join(lines)

if __name__ == '__main__':
    print(parse_unix_epoch_timestamp('2025-02-01T21:39'))
    # parse_response
    # pass