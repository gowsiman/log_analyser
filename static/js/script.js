// Get the forms and button elements
const splunkLoginForm = document.getElementById('SplunkLoginForm');
const logConfigForm = document.getElementById('logConfigForm');
const questionForm = document.getElementById('QuestionForm');

// Splunk Login Title
const left_form_title = document.getElementById('splunk-login-title');

const logConfigForm_source_type = document.getElementById('source-type');
const logConfigForm_start_time = document.getElementById('start-time');
const logConfigForm_end_time = document.getElementById('end-time');
const logConfigForm_application_name = document.getElementById('application-name');
const logConfigForm_input_query = document.getElementById('input-query');
const SpinnerContainer = document.getElementById('spinner');

// SUGGESTIONS ELEMENTS
const suggestionsContainer = document.getElementById('suggestions-container');
const suggestionText = document.getElementById('suggestion-text');
const prevButton = document.getElementById('prev-suggestion');
const nextButton = document.getElementById('next-suggestion');
const suggestionCounter = document.getElementById('suggestion-counter');



// Get Test Connection Button
const testConnectionButton = document.getElementById('testConnectionButton');

// Analyze Logs Button
const analyzeLogsButton = document.getElementById('analyze-logs-button');

// Get the tab buttons
const rawLogsTabButton = document.getElementById('rawLogs-tab-button');
const AiAnalysisTabButton = document.getElementById('AIAnalysis-tab-button');
const happyPathTabButton = document.getElementById('happyPath-tab-button');


// DISABLE LOG CONFIG FORM ELEMENTS
logConfigForm.classList.add('disabled-form');
logConfigForm_source_type.disabled = true;
logConfigForm_start_time.disabled = true;
logConfigForm_end_time.disabled = true;
logConfigForm_application_name.disabled = true;
logConfigForm_input_query.disabled = true;
analyzeLogsButton.disabled = true;
analyzeLogsButton.style.background = 'grey';
analyzeLogsButton.style.cursor = 'not-allowed';




// Create an object to store the results-tab-data fetched data
const resultsTabData = {
    "RawLogs": "",
    "HappyPath": "",
    "Summary": "",
    "Explanation": "",
    "ExpectedFlow": "",
    "Remediation": "",
    "Report": ""
};


// Add an event listener to the Analyze Logs button
analyzeLogsButton.addEventListener('click', () => {

    // PREVENT DOM RELOAD ACTION
    event.preventDefault()

    spinner.classList.add('show');

    // DISABLE THE BUTTON AND ACTIONS
    analyzeLogsButton.disabled = true;
    analyzeLogsButton.style.cursor = 'not-allowed';
    analyzeLogsButton.style.background = 'grey';

    // Show loading state
    const logOutput = document.getElementById('logOutput');
    logOutput.textContent = "Analyzing logs...";

    // Get the values from the form elements
    const sourceType = logConfigForm_source_type.value;
    const startTime = logConfigForm_start_time.value;
    const endTime = logConfigForm_end_time.value;
    const applicationName = logConfigForm_application_name.value;
    const query = logConfigForm_input_query.value;

    // Create a JSON payload with the values
    const payload = {
        source_type: sourceType,
        start_time: startTime,
        end_time: endTime,
        application_name: applicationName,
        query: query
    };

    // Scroll down to the lower end of the page
    window.scrollTo(0, document.body.scrollHeight);

    // SHOW SPINNER
    SpinnerContainer.style.display = 'block';

    // Send the payload to the Flask endpoint using the Fetch API
    fetch('/AnalyzeLogs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {

        // Store the fetched data in the resultsData object
        resultsTabData.RawLogs = data.RawLogs;
        resultsTabData.HappyPath = data.HappyPath;
        resultsTabData.Summary = data.Summary;
        resultsTabData.Explanation = data.Explanation;
        resultsTabData.ExpectedFlow = data.ExpectedFlow;
        resultsTabData.Remediation = data.Remediation;
        resultsTabData.Report = data.Report;

        // HIDE SPINNER
        SpinnerContainer.style.display = 'none';


        // Set Active & Load the RawLogs tab content by default
        rawLogsTabButton.classList.add('active');
        loadTabContent('RawLogs');

    })
    .catch(error => console.error(error));


    // ENABLE THE BUTTON AND ACTIONS
    analyzeLogsButton.disabled = false;
    analyzeLogsButton.style.background = '#D32F2F';
    analyzeLogsButton.style.cursor = 'pointer';


});


// Add an event listener to the testConnectionButton
testConnectionButton.addEventListener('click', () => {

    // Simulate a connection test (replace with actual connection test code)
    const isConnected = true; // Replace with actual connection test result

    // Get the values from the form elements
    const host = document.getElementById('splunk-host').value;
    const port = document.getElementById('splunk-port').value;
    const user = document.getElementById('splunk-user').value;
    const token = document.getElementById('splunk-token').value;

    // Create a JSON payload with the values
    const payload = {
        host: host,
        port: port,
        user: user,
        token: token
    };

    // Send the payload to the Flask endpoint using the Fetch API
    fetch('/TestConnection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // Check the status of the connection
        if (data.connection) {
            // Connection successful
            const promptElement = document.createElement('div');
            promptElement.textContent = 'Connection successful!';
            promptElement.style.color = 'green';
            promptElement.style.fontSize = '14px';
            promptElement.style.fontWeight = 'bold';
            promptElement.style.marginBottom = '10px';

            // Insert the prompt element above the test connection button
            testConnectionButton.parentNode.insertBefore(promptElement, testConnectionButton);

            // Disable the SplunkLoginForm
            testConnectionButton.disabled = true;
            testConnectionButton.style.background = 'grey';
            testConnectionButton.style.color = 'white';
            testConnectionButton.style.cursor = 'not-allowed';
            document.getElementById('splunk-host').disabled = true;
            document.getElementById('splunk-port').disabled = true;
            document.getElementById('splunk-user').disabled = true;
            document.getElementById('splunk-token').disabled = true;

            // Enable the logConfigForm
            logConfigForm.classList.remove('disabled-form');
            logConfigForm_source_type.disabled = false;
            logConfigForm_start_time.disabled = false;
            logConfigForm_end_time.disabled = false;
            logConfigForm_application_name.disabled = false;
            logConfigForm_input_query.disabled = false;
            analyzeLogsButton.disabled = false;
            analyzeLogsButton.style.background = '#D32F2F';
            analyzeLogsButton.style.cursor = 'pointer';


            // Make the prompt disappear after 3 seconds
            setTimeout(() => {
                promptElement.remove();

                // Hide the Splunk Login Form
                splunkLoginForm.style.display = 'none';

                // Change the Title From Splunk Login to
                left_form_title.textContent = "";

                // Show the Question Form
                questionForm.style.display = 'block';

            }, 3000);

        } else {
            // Connection failed
            const promptElement = document.createElement('div');
            promptElement.textContent = 'Connection failed. Please try again.';
            promptElement.style.color = 'red';
            promptElement.style.fontSize = '14px';
            promptElement.style.fontWeight = 'bold';
            promptElement.style.marginBottom = '10px';

            // Insert the prompt element above the test connection button
            testConnectionButton.parentNode.insertBefore(promptElement, testConnectionButton);

            // Make the prompt disappear after 3 seconds
            setTimeout(() => {
                promptElement.remove();
            }, 3000);
        }
    }).catch(error => console.error(error));
});


// Tab Switching Logic
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelectorAll('.tab-button').forEach(btn => 
            btn.classList.remove('active'));
        button.classList.add('active');
    });
});


// Add hover effect to buttons
document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('mouseenter', () => {
        button.style.transform = 'translateY(-2px)';
    });
    
    button.addEventListener('mouseleave', () => {
        button.style.transform = 'translateY(0)';
    });
});


// Add event listeners to the tab buttons
rawLogsTabButton.addEventListener('click', () => {
    loadTabContent('RawLogs');
});

AiAnalysisTabButton.addEventListener('click', () => {
    createAIAnalysisContainer()
    loadTabContent('AIAnalysis');
});

happyPathTabButton.addEventListener('click', () => {
    loadTabContent('HappyPath');
});

// Function to load the tab content
function loadTabContent(tabName) {
    const tabContentElement = document.getElementById('logOutput');
    const aiAnalysisContainer = document.getElementById('ai-analysis-container');

    // Load the content from the resultsData object
    if (tabName === 'RawLogs') {
        if (aiAnalysisContainer != null) {
            aiAnalysisContainer.style.display = 'none';  // Hide AI analysis sections
            clearAIAnalysisContent();  // Clear content when switching tabs
        }
        tabContentElement.innerHTML = resultsTabData.RawLogs;
    } else if (tabName === 'AIAnalysis') {

        // aiAnalysisContainer.style.display = 'block';  // Show AI analysis sections
        populateAIAnalysisContent();  // Populate the content if it's available

    } else if (tabName === 'HappyPath') {
        if (aiAnalysisContainer != null) {
            aiAnalysisContainer.style.display = 'none';  // Hide AI analysis sections
            clearAIAnalysisContent();  // Clear content when switching tabs
        }
        tabContentElement.innerHTML = resultsTabData.HappyPath;
    }
}

// Function to populate the AI analysis sections with data
function populateAIAnalysisContent() {

    // Populate each subsection with data from the backend response
    document.getElementById('summary-section').querySelector('p').textContent = resultsTabData.Summary || 'No data available';
    document.getElementById('explanation-section').querySelector('p').textContent = resultsTabData.Explanation || 'No data available';
    document.getElementById('expectedflow-section').querySelector('p').textContent = resultsTabData.ExpectedFlow || 'No data available';
    document.getElementById('remediation-section').querySelector('p').textContent = resultsTabData.Remediation || 'No data available';
    document.getElementById('report-section').querySelector('p').textContent = resultsTabData.Report || 'No data available';
    mermaid.contentLoaded();
}

// Function to clear AI analysis content (useful when switching tabs)
function clearAIAnalysisContent() {
    document.getElementById('summary-section').querySelector('p').textContent = '';
    document.getElementById('explanation-section').querySelector('p').textContent = '';
    document.getElementById('expectedflow-section').querySelector('p').textContent = '';
    document.getElementById('remediation-section').querySelector('p').textContent = '';
    document.getElementById('report-section').querySelector('p').textContent = '';
    mermaid.contentLoaded();
}

function createAIAnalysisContainer() {
    // Create the HTML structure dynamically
    const aiAnalysisHTML = `
        <div class="ai-analysis-container">
            <div class="ai-analysis-tabs">
                <button class="tab-button active inner-tab" data-section="summary-section">Summary</button>
                <button class="tab-button inner-tab" data-section="explanation-section">Explanation</button>
                <button class="tab-button inner-tab" data-section="expectedflow-section">Event Sequence</button>
                <button class="tab-button inner-tab" data-section="remediation-section">Remediation</button>
                <button class="tab-button inner-tab" data-section="report-section">Impacted Entities</button>
            </div>
            <div class="ai-analysis-content">
                <div id="summary-section" class="sub-section active">
                    <p></p>
                </div>
                <div id="explanation-section" class="sub-section">
                    <p></p>
                </div>
                <div id="expectedflow-section" class="sub-section">
                    <p class="mermaid"></p>
                </div>
                <div id="remediation-section" class="sub-section">
                    <p></p>
                </div>
                <div id="report-section" class="sub-section">
                    <p></p>
                </div>
            </div>
        </div>
    `;

    const tabContentElement = document.getElementById('logOutput');

    tabContentElement.innerHTML = aiAnalysisHTML;
    
    showInnerContainer();
}

function showInnerContainer() {

    document.querySelectorAll(".inner-tab").forEach( button => {
        const buttons = document.querySelectorAll('.inner-tab')
        const sections = document.querySelectorAll(".sub-section");
        button.addEventListener("click", () => {
            // console.log("Clicked..")
            // Remove active class from all buttons and sections
            buttons.forEach((btn) => btn.classList.remove("active"));
            sections.forEach((section) => section.classList.remove("active"));

            // Add active class to clicked button and corresponding section
            button.classList.add("active");
            document.getElementById(button.dataset.section).classList.add("active");
        });
    });
}

// Example suggestion data (this can be fetched from an API or another source)
const suggestions = [
    "What was the cause of MemCache?",
    "How many withdrawal transaction errors happened?",
    "How many transaction took longer than expected?"
];

let currentSuggestionIndex = 0;

// Function to update the suggestion and the counter
function updateSuggestion() {
    suggestionText.textContent = suggestions[currentSuggestionIndex];
    suggestionCounter.textContent = `${currentSuggestionIndex + 1}/${suggestions.length}`;
}

// Show the suggestions box when the user clicks on the input field
logConfigForm_input_query.addEventListener('click', function() {
    if (!logConfigForm_input_query.value.trim()) {
//        suggestionsContainer.style.display = 'flex'; // Use flex to align items properly
//        updateSuggestion();
    }
});

// Handle the previous suggestion
prevButton.addEventListener('click', function() {
    if (currentSuggestionIndex > 0) {
        currentSuggestionIndex--;
        updateSuggestion();
    }
});

// Handle the next suggestion
nextButton.addEventListener('click', function() {
    if (currentSuggestionIndex < suggestions.length - 1) {
        currentSuggestionIndex++;
        updateSuggestion();
    }
});

// When the user clicks the suggestion bubble, fill the suggestion in the input
suggestionText.addEventListener('click', function() {
    logConfigForm_input_query.value = suggestions[currentSuggestionIndex];
    suggestionsContainer.style.display = 'none'; // Hide the suggestions after selecting
});

// Close the suggestion bubble when clicking outside the input field
document.addEventListener('click', function(event) {
    if (!logConfigForm_input_query.contains(event.target) && !suggestionsContainer.contains(event.target)) {
        suggestionsContainer.style.display = 'none';
    }
});

// Add event listeners to each question item
const questionItems = document.querySelectorAll('.question-item');
questionItems.forEach(item => {
    item.addEventListener('click', function() {
        // Fill the input-query field with the selected question
        logConfigForm_input_query.value = item.textContent;
    });
});

