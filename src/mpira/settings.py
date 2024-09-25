ollama_config = {
    "llm": {
        "model": "ollama/mistral",  # choices: llama3.1, llama3.1:8b,
        "temperature": 0,
        "format": "json",
        "base_url": "http://localhost:11434",
    },
    "verbose": False,
    "headless": True,
}

# options

openai_config = {
    "llm": {
        "model": "openai/gpt-4o",
        "temperature": 0,
    },
    "verbose": False,
    "headless": False,
}
