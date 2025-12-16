import re

# Sample text (replace this with your actual text)
text = """
1. Summary:
   The provided logs indicate two instances where withdrawal transactions failed due to different reasons. The first instance occurred when attempting to insert a duplicate transaction record into the database, resulting in a unique constraint violation. The second instance was due to a NullPointerException in the service layer while processing a response. The affected account numbers in the first scenario were '543216789' and '123456789', while the second scenario did not provide the account number.

2. Incident/Scenario Report:

   **First Scenario:**
   - Time: 2025-02-01T16:30:00.165Z
   - Faced By: N/A (Automated process)
   - Trace Id: TRACE111222
   - Application: SpringBoot
   - Component: OracleDB
   - Additional Metadata: None

   **Second Scenario:**
   - Time: 2025-02-01T16:30:10.395Z
   - Faced By: N/A (Automated process)
   - Trace Id: TRACE556677
   - Application: SpringBoot
   - Component: Middleware
   - Additional Metadata: NullPointerException

3. Explanation:

   **First Scenario:**
   The first scenario involved an attempt to insert a duplicate transaction record into the database, causing a unique constraint violation. This error occurred when trying to insert a new transaction record with the same transaction ID as a previous one. The logs show that the transaction was aborted due to the database constraint violation, and the UI displayed an error message to the user.

   **Second Scenario:**
   The second scenario was caused by a NullPointerException in the service layer while processing a response. This error occurred when the Middleware failed to validate account information, resulting in a null response being sent to the SpringBoot application. The SpringBoot application then attempted to process this null response, leading to the NullPointerException and the transaction being aborted.

4. Expected Ideal Flow (Happy Path):

   **Withdrawal Transaction:**
   - User initiates a withdrawal request through the UI.
   - The UI sends a request to the SpringBoot application with the account number and amount.
   - The SpringBoot application validates the account number and amount.
   - The SpringBoot application sends a request to the Middleware to debit the specified account.
   - The Middleware processes the debit request and returns a successful response.
   - The SpringBoot application logs the transaction in the database and sends a confirmation message to the user.

5. Remediation / Recommendations:

   **First Scenario:**
   - Implement proper transaction handling and error checking in the database layer to prevent duplicate transaction records from being inserted.
   - Implement a mechanism to rollback the transaction if a unique constraint violation occurs.

   **Second Scenario:**
   - Improve error handling and validation in the Middleware to prevent null responses from being sent to the SpringBoot application.
   - Implement a mechanism to handle and log NullPointerExceptions in the SpringBoot application to provide better error messages to the user.
"""

# Define the headings
headings = [
    'Summary',
    'Incident/Scenario Report',
    'Explanation',
    'Expected Ideal Flow (Happy Path)',
    'Remediation / Recommendations'
]

# Initialize the dictionary with empty strings instead of None
response = dict.fromkeys(headings, "")

key = None
for line in text.split('\n'):
    skip_line = False
    for heading in headings:
        if heading in line:
            key = heading
            skip_line = True
            break  # Exit inner loop once the heading is found
    if not skip_line and key is not None:
        if line.strip(): 
            # Remove bold markers and preserve original line format
            line = line.replace("**", "")
            response[key] += line + "\n"

import pprint
pprint.pprint(response.)


print(response['Expected Ideal Flow (Happy Path)'])