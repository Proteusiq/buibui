ollama_config = {
    "llm": {
        "model": "ollama/llama3.1",  # choices: llama3.1, llama3.1:8b, mistral
        "temperature": 0,
        "format": "json",
        "base_url": "http://localhost:11434",
    },
    "verbose": False,
    "headless": True,
}

# options

grog_config = {
    "llm": {
        "model": "groq/llama3-8b-8192",
        "temperature": 0,
    },
    "headless": True,
    "verbose": True,
}


gemini_config = {
    "llm": {
        "model": "google_genai/gemini-pro",
        "temperature": 0,
    },
    "headless": True,
    "verbose": False,
}



openai_config = {
    "llm": {
        "model": "openai/gpt-4o",
        "temperature": 0,
    },
    "verbose": False,
    "headless": True,
}
