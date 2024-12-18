# LLM-Powered SIEM Correlation Engine

This project demonstrates a small-scale Security Information and Event Management (SIEM) system that utilizes Large Language Models (LLMs) to analyze log files and identify potential cybersecurity incidents. The system processes log chunks, maintains a sliding window of context, and uses a GPT-4o model to detect and summarize incidents.

# Log Credits

Los Alamos National Laboratory

# Overview
This SIEM system reads log files, processes them in sequence, and uses an LLM to analyze each chunk for potential incidents. By maintaining a sliding window of previous log chunks, the system can correlate events across multiple logs to detect complex patterns or anomalies.

# Prerequisites
- Python 3.8 or higher
- Install required Python packages:

``` pip install python-dotenv```
- Obtain an OpenAI API key and set it as an environment variable "OPENAI_API_KEY" in the .env.example file. Rename this file to ".env".

# Installation
1. Clone the repository:

     ``` git clone https://github.com/charliepaks/aisiem.git ```

2. Install dependencies:

   ``` cd aisiem```

   ``` poetry install```

   ``` poetry shell```

# Usage
1. Ensure your log files are in the ./logs/processing/source_logs folder and are named with a .log extension. You can use the log files in the project or put in your own logs. Don't use very large log files as you may encouter rate limiting issues with the OpenAI API.

2. Run the main script:

   ``` python siem.py```

The system will process each log chunk, analyze it for incidents, and print any detected incidents to the console.

# Sliding Window Context
- The system maintains a sliding window of previous log chunks to provide context to the LLM.
- The size of the sliding window is defined by SLIDING_WINDOW.
- For each new chunk, the LLM is provided with the context from the previous chunks in the window.

# Output Format
For each detected incident, the LLM generates output in the following format:


---- Alert  ----

Incident Title: 

Incident Description: 

Severity: 

Affected Asset/Identity: 

Recommendation: 

---- End ----

<img width="1105" alt="Screenshot 2024-12-17 at 2 53 11 PM" src="https://github.com/user-attachments/assets/774c1211-a642-4e3a-968a-0292ffdeb632" />

# Contributing
Contributions are welcome! Please open an issue or submit a pull request.

# License
This project is licensed under the MIT License.



