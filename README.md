# AI Agent

This project uses a pre-trained LLM to create an AI agent that assists with coding tasks. Users can provide command-line instructions for the program to analyze a codebase, identify issues, and apply corrections.

**Project Demo:**

<img src="./public/ai-agent-demo.gif" alt="Demonstration of using program to inspect files in a directory." width="80%">

## Tech Stack

* **Frontend:** n/a
* **Backend:** Python, Google Gemini 2.5 Flash

## Project Structure

``` bash
ai-agent/
├── public/                     # Media assets
├── calculator/                 # Calculator app logic
│   ├── calculator.py           # Implements calculator class functionality
│   └── render.py               # Handles output rendering of expressions and results
├── functions/                  # Contains files with helper functions for AI agent to
├── .gitignore                  # Git ignore rules
├── .env                        # Environmental variables
├── main.py                     # Entry point for CLI agent
├── tests.py                    # Test scripts for call functions
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock
├── README.md

# Before running this project locally, ensure you have the following installed:
- IDE (VS Code, PyCharm, etc.)
- Install Python 3.10+ version > visit python.org/downloads/

# Install dependencies
- uv project/package manager > docs.astral.sh/uv/getting-started/installation/
- Environmental variables > uv add python-dotenv==1.1.0
- Google Gemini API > uv add google-genai==1.12.1
```

## Quick Start

This repo will later be, if not already, saved as a subfolder. Be sure to only clone relevant files. Then, do the following:

### Virtual Environment Setup

- All-in-one command to create project: `uv init project-name && cd project-name`
- Create virtual environment: `uv venv`
- Use uv's project environment and avoid pyenv/global mismatches: `uv add requests && uv run python main.py`
- Activate virtual environment: `source .venv/bin/activate`

### Environmental Variables Setup

Create a `.env` file with the following contents:

```bash
GEMINI_API_KEY=""
AI_MODEL="gemini-2.5-flash"
MAX_CHAR_LIMIT=1000
SYSTEM_PROMPT=""
WORKING_DIR=""
MAX_ITERATIONS=20
```

This project used Google Gemini 2.5 Flash. At the time of this writing a free tier existed. Regardless of the AI provider you choose, you should set values for each variable shown.

### API Key Setup

- Create an API Key on [Google AI Studio](https://aistudio.google.com)
- Store API Key inside `.env` file on the `GEMINI_API_KEY` environmental variable
- Add `.env` file to `.gitignore`

## Usage

### Safeguards

The program grants read _and_ write privileges to a codebase. This can be dangerous! Safeguards taken throughout this project included: (1) safely storing API keys; (2) limiting read-write privileges to a single directory; (3) protecting against directory traversal; (4) using timeout limits when running subprocesses; (5) setting an iteration limit to avoid infite agent call loops; and (6) setting a character limit for output to preserve tokens. Error handling was used, but did not cover all edge cases. 

Safegaurds (1), (2), (5), and (6) are implemented via environmental variables in the the `.env` file, which the `.gitignore` file then protects from public exposure. Safeguards (3) and (4) are implemented via files in the `./functions/` folder.

### User Prompts

After the virtual environment has been activated, users should use the following prompt format:

> `python main.py 'ENTER YOUR PROMPT HERE' [--verbose]`

The program will throw an error if a prompt is not entered after the program file name. Optionally, users can use a `--verbose` statement in the prompt for the response to report token input and output metadata.

## System Design

### 1. Requirements

**Functional Requirements:**

- User submits a **user_prompt** in command-line interface (CLI)
- For a single `WORKING_DIRECTORY`, the AI agent can inspect files, read contents, write changes, and execute Python files
- Program ends with model response that satisfies initial prompt

**Optional Requirements:**

- **Verbose mode:** if user ends initial prompt with `--verbose` tag for model response to include additional metadata
- Low latency: use timeout limits when running subprocesses
- Scalability: limiting output character length to preserve tokens (`MAX_CHAR_LIMIT` in `.env` file)
- Security: (1) safely storing API keys (`GEMINI_API_KEY` in `.env` file); (2) limit read-write privileges to a single directory (`WORKING_DIRECTORY` in `.env` file); (3) protecting against directory traversal (conditional checks in `./functions/` files); (4) setting an iteration limit to avoid infite model + function execution loops (`MAX_ITERATIONS` in `.env` file)
- CAP Theorem: prioritize consistency (read/writes must be correct) over availability

### 2. Core Entities

- **UserPrompt:** user_prompt (string), is_verbose (boolean)
- **ModelSettings:** GEMINI_API_KEY, AI_MODEL, SYSTEM_PROMPT, available_functions (function schemas), conversation_history (content messages)
- **ModelCalls:** MAX_ITERATIONS, current_iteration, model_response
- **FunctionCalls:** WORKING_DIR, function_name, arguments, function_response

### 3. API (or Interface)

**Command-Line Interface (CLI):**

> `python main.py 'user_prompt' [--verbose]`

**Model Call:**

> `call_model(model_settings, conversation_history) -> model_response(result | function_calls | error)`

**Function Calls:**

> `call_function(function_name, arguments, WORKING_DIR) -> function_response (result | error)`

_In reality, several function call files were written. However, each generally follows this convention._

### 4. Data Flow

<img src="./public/function-calling-diagram.PNG" width="80%">

I created the diagram above to illustrate [function calling with Gemini API](https://ai.google.dev/gemini-api/docs/function-calling?example=meeting). The four numbers shown correspond with the article steps outlined, which are used throughout this project for developer documentation. The overall workflow follows this order and is expanded upon in a table below:

1. **Function Declarations:** The `./functions/schemas.py` file defined all external functions to be used by the model. The `./functions/call_function.py` file bundled these functions into a `types.Tool()` object.
2. **Call Model:** The Gemini model is executed. This requires providing the model settings: `GEMINI_API_KEY`, `AI_MODEL`, `SYSTEM_PROMPT`, user prompt, conversation history, and function declarations.
3. **Call Functions:** Function calls are executed. This requires parsing the model response from step (2) to determine function names and arguments to call. The `WORKING_DIR` must be provided on each function call.
4. **Model Response:** The Gemini model is executed again within an agent loop that repeats steps (2) and (3). At the end of each cycle, the function response is parsed for content to update the conversation history. The agent loop runs at most for `MAX_ITERATIONS` and final output has a character limitation of `MAX_CHAR_LIMIT` to preserve tokens.

<img src="./public/function-calling-table.PNG" width="80%">

### 5. High Level Design

The project currently reprsents a **single-node, agent-driven architecture** without a frontend, backend server, or database. The project could be improved to be more robust in the following manner:

1. **Client:** Use HTML and JavaScript to create an **asynchronous** web application using **WebSockets** over a TCP connection. This will allow the UI to provide a real-time log of the agent's thought process after a user submits a prompt and waits for a response.
2. **API Gateway:** This is the single, centralized entry point and security perimeter to the backend services. **Security benefits** include handling authentication/authorization and rate limiting. **Scalability benefits** include horizontal load balancing and service routing.
3. **Server (Agent Orchestration):** This service runs the core agent logic (planningn and action loop). Can be implemented as a **stateless microservice** that passes user requests to an **asynchronous task queue** (e.g., Redis or Kafka). This would allow for horizontal scaling and improved client response times by allowing tasks to execute independently.
4. **Database:** May use two database types. **Relational database** may store user account information and system logs. **Vector database** may store embeddings of conversation history for retrieval-augmented generation **(RAG)**.

## Credits and Contributing

[Boot.dev](https://www.boot.dev) provided the project requirements and guidance to complete this project. Modifications were made to follow [function calling guidance from Google](https://ai.google.dev/gemini-api/docs/function-calling?example=meeting). The [Google Gen AI SDK](https://googleapis.github.io/python-genai/) for Python was used as a source of truth for development. Contributions are welcome! Feel free to report any problems.
