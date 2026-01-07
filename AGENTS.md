# AGENTS.md - Agent Operating System for Prompt Library

This file serves as the operating system for AI coding agents working in this repository. It contains all necessary information about build commands, testing, linting, code style guidelines, and project conventions.

## Project Overview

This is a **Prompt Library** - a curated collection of high-quality AI prompts organized by domain (analysis, trading, development, utilities, content). The repository uses structured YAML front matter for prompt metadata and includes Python tooling for validation and indexing.

**Core Technologies:**
- Python 3.9+
- uv for package management
- ruff for linting/formatting
- PyYAML for metadata parsing

## Build, Lint, and Test Commands

### General Setup
- **Install dependencies:** `uv pip install -r requirements.txt`
- **Python version:** 3.9+ (check requirements.txt for specific version)

### Linting and Formatting
- **Lint:** `uv run ruff check --select E,F,I,UP,B,SIM --ignore E501 --line-length 120`
- **Format:** `uv run ruff format`
- **Type check:** `uv run mypy --ignore-missing-imports` (if mypy is installed)

### Testing
- **Run all tests:** No dedicated test framework configured yet
- **Run single test:** No test files currently exist; manual testing via scripts
- **Integration testing:** Use custom test scripts when available (e.g., `python testcalls.py`)

### Build Commands
- **Index generation:** `uv run python scripts/prompt_manager.py index`
- **Create new prompt:** `uv run python scripts/prompt_manager.py new-prompt`
- **Search prompts:** `uv run python scripts/prompt_manager.py search <query>`

### Verification Commands
After making changes, always run:
1. `uv run ruff check --select E,F,I,UP,B,SIM --ignore E501 --line-length 120`
2. `uv run ruff format`
3. `uv run python scripts/prompt_manager.py index` (if prompt files were modified)

## Code Style Guidelines

### Python Version and Imports
- **Version:** Python 3.9+ required
- **Import Order:**
  1. Standard library imports
  2. Third-party imports
  3. Local imports
- **Style:** Absolute imports preferred; avoid relative imports unless necessary
- **Formatting:** One import per line
- **Type imports:** `from typing import List, Dict, Optional` for generics

**Example:**
```python
import logging
import uuid
import time
import json
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from models import ChatMessage, ChatCompletionRequest
```

### Naming Conventions
- **Variables and Functions:** `snake_case` (e.g., `conversation_id`, `chat_with_duckduckgo`)
- **Classes:** `PascalCase` (e.g., `ChatCompletionRequest`, `TTSEngine`)
- **Constants:** `UPPER_CASE` (e.g., `MODEL_MAPPING`, `VOICES`)
- **Private Methods/Variables:** Leading underscore (e.g., `_instance`)
- **Files/Modules:** `snake_case` (e.g., `server.py`, `models.py`)

### Type Hints
- **Required:** All function parameters and return types must have type hints
- **Optional Types:** Use `Optional[T]` or `T | None` for nullable types
- **Generic Types:** Use `List[T]`, `Dict[K, V]` from typing module

**Examples:**
```python
from typing import List, Dict, Optional, AsyncGenerator

async def chat_with_duckduckgo(query: str, model: str, conversation_history: List[ChatMessage]) -> AsyncGenerator[str, None]:
    pass

def get_next_user_agent() -> str:
    pass

conversations: Dict[str, List[ChatMessage]] = {}
```

### Async/Await Patterns
- **HTTP Requests:** Always use `httpx.AsyncClient` for async HTTP operations
- **Streaming:** Use `client.stream()` for streaming responses
- **Context Managers:** Use `async with` for client sessions and resource management

**Example:**
```python
async with httpx.AsyncClient() as client:
    async with client.stream('POST', url, json=payload, headers=headers) as response:
        async for line in response.aiter_lines():
            # Process streaming data
            yield line
```

### Error Handling
- **HTTP Exceptions:** Use `HTTPException` from FastAPI for API errors
- **Logging:** Log errors with appropriate levels (INFO, WARNING, ERROR); include `exc_info=True` for detailed traces
- **Exception Chaining:** Use `raise ValueError(f"Failed: {e}") from e`

**Examples:**
```python
try:
    # code
except Exception as e:
    logging.error(f"Error fetching token: {str(e)}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Data Models
- **Base Classes:** Use Pydantic `BaseModel` for all data structures
- **Optional Fields:** Use `Optional[T] = None` for nullable fields
- **Field Validation:** Leverage Pydantic's built-in validation

**Example:**
```python
from pydantic import BaseModel
from typing import List, Optional

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    conversation_id: Optional[str] = None
    temperature: Optional[float] = 1.0
```

### Logging
- **Configuration:** Use Python's logging module with format: `'%(asctime)s - %(levelname)s - %(message)s'`
- **Levels:** INFO for normal operations, WARNING for recoverable issues, ERROR for failures
- **Context:** Include relevant IDs and operation details in log messages

**Example:**
```python
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"Received request for conversation {conversation_id}")
logging.error(f"Error response from service. Status: {response.status_code}")
```

### String Formatting
- **Preferred:** F-strings for all string interpolation (e.g., `f"Error: {str(e)}"`)
- **Avoid:** `.format()` and `%` formatting

### Code Structure Patterns
- **Singleton Pattern:** Used for engines like TTSEngine (`_instance: Optional['TTSEngine'] = None`)
- **Generator Functions:** Use `async def` with `yield` for streaming responses
- **List/Dict Comprehensions:** Preferred over explicit loops for simple transformations
- **Context Managers:** Use `async with` for resource management

### Security Considerations
- **Environment Variables:** Store sensitive data (session IDs, API keys) in environment variables
- **Input Validation:** Rely on Pydantic models for automatic validation
- **Error Messages:** Avoid exposing sensitive information in error responses
- **CORS:** Configure appropriately for deployment environment

## Project Structure and Organization

### Directory Layout
```
prompt-library/
├── analysis/           # Data analysis & extraction prompts
├── content/            # Content creation (visual, text)
├── development/        # Coding & engineering prompts
├── trading/            # Financial & trading bot workflows
├── utilities/          # Meta-prompts & agent operations
├── metadata/           # Auto-generated indices (prompt_index.yaml)
└── scripts/            # Automation tools (prompt_manager.py)
```

### Prompt File Standards
Every prompt file (`.md`) MUST start with YAML front matter:

```yaml
---
id: my-prompt-id
title: My Prompt Title
description: A clear description of what this prompt does.
category: utilities
sub_category: general
tags: ["tag1", "tag2"]
version: "1.0.0"
status: "active"
llm_model_compatibility: ["gpt-4o", "claude-3-opus"]
parameters:
  - name: input_text
    type: string
    description: The text to process.
---
# My Prompt Title

## ROLE
...
```

### File Organization
- **Logical Separation:** Group related functionality (e.g., `server.py` for routes, `models.py` for data models)
- **Consistent Layout:** Maintain directory structures across projects

## API Design Patterns
- **OpenAI Compatibility:** Follow OpenAI Chat Completions API format where applicable
- **Streaming Support:** Implement Server-Sent Events for real-time responses
- **Conversation Management:** Maintain history by ID
- **Modality Support:** Support text and audio responses
- **HTTP Status Codes:** Use standard codes (200, 400, 404, 429, 500)

## Performance Considerations
- **Connection Reuse:** Use httpx.AsyncClient with context managers
- **Rate Limiting:** Handle 429 responses with exponential backoff
- **Memory Management:** Clean up resources (conversation histories)
- **Chunking:** Split long inputs for processing

## Testing Approach
- **Integration Tests:** Test actual endpoints with HTTP requests
- **Manual Testing:** Use scripts like `testcalls.py` for verification
- **Error Scenarios:** Test edge cases and failures
- **Streaming Tests:** Verify both streaming and non-streaming responses

## Deployment
- **Containerization:** Use Docker for consistent deployment
- **Environment Variables:** Configure features via env vars
- **Port Configuration:** Standard ports (e.g., 1337 for APIs)
- **Health Checks:** Consider adding endpoints for production monitoring

## User Preferences (Learned Context)
- Always use uv for Python package management
- Always use bun for Node.js package management (when applicable)

## Cursor/Copilot Rules
No Cursor rules (.cursor/rules/ or .cursorrules) or Copilot rules (.github/copilot-instructions.md) found in the repository. Follow the guidelines above for consistency.

## Agent Evolution Protocol
This file serves as a living document that should be updated based on user feedback and observed preferences. When users provide feedback like "Don't do X", "Prefer Y", or "Always Z", immediately update the relevant sections to ensure consistent behavior going forward.</content>
<parameter name="filePath">AGENTS.md