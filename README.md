<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Contract Analyzer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
            line-height: 1.6;
        }

        header {
            background-color: #333;
            color: white;
            padding: 1rem;
            text-align: center;
        }

        section {
            padding: 2rem;
        }

        h1, h2, h3 {
            color: #333;
        }

        pre {
            background-color: #333;
            color: white;
            padding: 1rem;
            border-radius: 5px;
            font-family: monospace;
            overflow-x: auto;
        }

        ul {
            list-style-type: none;
            padding-left: 0;
        }

        li {
            margin: 0.5rem 0;
        }

        footer {
            text-align: center;
            padding: 1rem;
            background-color: #333;
            color: white;
        }

        a {
            color: #007bff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>

<body>

    <header>
        <h1>AI Contract Analyzer</h1>
    </header>

    <section>
        <h2>Project Overview</h2>
        <p>Welcome to the <strong>AI Contract Analyzer</strong>! This tool helps legal professionals analyze contracts using AI. The system performs contract analysis, risk assessment, and provides suggestions for optimizing contract clauses.</p>

        <h2>Project Structure</h2>
        <pre>
ai-contract-analyzer/
├── app.py                  # Main Streamlit application
├── contract_analyzer.py    # Core analysis system
├── prompts.py              # AI prompts for different analysis tasks
├── ui_styles.py            # UI styling for Streamlit
├── help_content.py         # Help tab content
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
        </pre>

        <h2>Installation Instructions</h2>
        <h3>1. Create a Conda Environment</h3>
        <p>To set up the project, first create a Conda environment:</p>
        <pre>
conda create -n lang6 python=3.11 -y
conda activate lang6
        </pre>

        <h3>2. Install Project Dependencies</h3>
        <p>Use <code>pip</code> to install all required dependencies:</p>
        <pre>
pip install -r requirements.txt
        </pre>

        <h3>3. Set Your OpenAI API Key</h3>
        <p>You will need to set your OpenAI API key for the application to function. You can do this by setting an environment variable:</p>
        <pre>
export OPENAI_API_KEY="your-api-key"
        </pre>
        <p>Alternatively, you can provide the API key through the application UI.</p>

        <h3>4. Run the Application</h3>
        <p>Once the setup is complete, you can run the Streamlit application with the following command:</p>
        <pre>
streamlit run app.py
        </pre>
        <p>This will start the application, and you can begin uploading and analyzing contracts.</p>

        <h2>Features</h2>
        <ul>
            <li><strong>Upload Contracts:</strong> Supports PDF, DOCX, and TXT formats.</li>
            <li><strong>Contract Analysis:</strong> AI-powered analysis using GPT-based models.</li>
            <li><strong>Risk Assessment:</strong> Evaluates legal, financial, operational, and reputational risks.</li>
            <li><strong>Recommendations:</strong> Provides suggestions for improving contract clauses.</li>
            <li><strong>Executive Summary:</strong> Generates a concise summary of the contract analysis.</li>
        </ul>

        <h2>Dependencies</h2>
        <p>The project depends on the following Python libraries:</p>
        <ul>
            <li><strong>streamlit</strong> - For creating the web interface.</li>
            <li><strong>openai</strong> - For interacting with OpenAI models.</li>
            <li><strong>langchain</strong> - For AI-driven contract analysis.</li>
            <li><strong>PyPDF2</strong> - For parsing PDF documents.</li>
            <li><strong>python-docx</strong> - For parsing DOCX documents.</li>
        </ul>

        <h2>Contributing</h2>
        <p>We welcome contributions! If you'd like to contribute, follow these steps:</p>
        <ul>
            <li>Fork the repository</li>
            <li>Create a new branch</li>
            <li>Make your changes</li>
            <li>Test your changes</li>
            <li>Submit a pull request</li>
        </ul>

        <h2>License</h2>
        <p>This project is licensed under the <strong>MIT License</strong> - see the <a href="LICENSE" target="_blank">LICENSE</a> file for details.</p>
    </section>

    <footer>
        <p>&copy; 2025 AI Contract Analyzer | All Rights Reserved</p>
    </footer>

</body>

</html>
