<!DOCTYPE html>
<html>

<head>
  <title>PDF Question Answering Bot</title>
</head>

<body>

  <h1>PDF Question Answering Bot</h1>

  <p>The PDF Question Answering Bot is a Python script that leverages the OpenAI API to generate answers for questions asked on a PDF document. It extracts text from a PDF, processes user questions, and provides ranked answers based on similarity scores. The script uses concurrent processing and caching for efficient performance.</p>

  <h2>Requirements</h2>

  <ul>
    <li>Python 3.x</li>
    <li>PyPDF2</li>
    <li>openai</li>
    <li>spacy</li>
  </ul>

  <h2>Installation</h2>

  <ol>
    <li>Clone the repository:</li>
  </ol>

  <pre><code>git clone https://github.com/your-username/pdf-question-answering-bot.git</code></pre>

  <ol start="2">
    <li>Install the required Python dependencies:</li>
  </ol>

  <pre><code>pip install PyPDF2 openai spacy</code></pre>

  <ol start="3">
    <li>Download the spaCy English language model:</li>
  </ol>

  <pre><code>python -m spacy download en_core_web_md</code></pre>

  <ol start="4">
    <li>Obtain an API key from OpenAI. Sign up at <a href="https://openai.com">https://openai.com</a> and follow the instructions to get your API key.</li>
  </ol>

  <ol start="5">
    <li>Update the <code>API_KEY</code> variable in the <code>pdf_question_answering_bot.py</code> file with your OpenAI API key.</li>
  </ol>

  <h2>Usage</h2>

  <ol>
    <li>Place your PDF file in the same directory as the <code>pdf_question_answering_bot.py</code> file.</li>
    <li>Run the script:</li>
  </ol>

  <pre><code>python pdf_question_answering_bot.py &lt;pdf_file_path&gt;</code></pre>

  <ol start="3">
    <li>Enter your questions one by one. To quit, enter 'q'.</li>
    <li>The script will process the PDF and provide answers based on your questions.</li>
  </ol>

  <h2>Contributing</h2>

  <p>Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.</p>

  <h2>License</h2>

  <p>MIT License</p>

</body>

</html>
