import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

# Configuration
CHUNKS_FOLDER = "./logs/processing/source_logs"  # Folder containing pre-existing log chunks
SLIDING_WINDOW = 1  # Number of previous chunks to retain as context

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)
prompt_template = PromptTemplate(
    input_variables=["context", "chunk"],
    template = """You are an expert in cybersecurity incident analysis. Carefully analyze the provided log entries for potential cybersecurity incidents, leveraging prior context to identify patterns, correlations, or anomalies.

    Context (previous logs for correlation): 
    {context}

    New Log Entries (current analysis focus): 
    {chunk}

    Based on the analysis, identify and summarize any detected incidents. For each incident, provide the following details in a structured format:
    ---- Alert <Sequential ID> ----
    Incident Title: A brief title summarizing the incident.
    Incident Description: A detailed explanation of the incident, including how it was identified and any relevant correlations with the prior context.
    Severity: Categorize the severity as Low, Medium, High, or Critical based on the potential impact.
    Affected Asset/Identity: Specify the impacted system, service, or identity.
    Recommendation: Provide actionable steps to mitigate or resolve the incident.

    ---- End ----

    Ensure you keep strictly to the format above in text and not mark down. Do not add any other fields thata re not specified in this prompt."""
)
chain = LLMChain(llm=llm, prompt=prompt_template)

# Sliding context window
context_window = []

def read_chunk(filepath):
    """Read a log chunk from file."""
    with open(filepath, "r") as file:
        return file.read()

def process_chunk(chunk):
    """Analyze a chunk and correlate with the sliding window context."""
    global context_window

    # Prepare context from the previous chunk
    context = context_window[-1] if context_window else ""
    
    # Analyze the current chunk
    result = chain({"context": context, "chunk": chunk}, ).get("text", "").strip()
    
    # Check if an incident is identified in the result
    if "incident" in result.lower() or "alert" in result.lower():
        print(result)
        print("-------------\n")
    
    # Update the sliding window
    context_window.append(chunk)
    if len(context_window) > SLIDING_WINDOW:
        context_window.pop(0)

# Main processing loop
if __name__ == "__main__":
    print("Starting LLM-Powered SIEM Correlation Engine...")
    id = 0
    # Get the list of chunk files
    chunk_files = sorted(
        [os.path.join(CHUNKS_FOLDER, f) for f in os.listdir(CHUNKS_FOLDER) if f.endswith(".log")]
    )

    if not chunk_files:
        print("No log chunks found in the folder. Exiting.")
        exit(0)

    # Process each chunk sequentially
    for chunk_file in chunk_files:
        chunk_data = read_chunk(chunk_file)
        process_chunk(chunk_data)

    print("Processing complete.")
