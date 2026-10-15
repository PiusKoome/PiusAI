import ollama

def generate_response(prompt: str) -> str:
    """Sends a prompt to the local Llama 3.2 model and returns the response."""
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"