import ollama

def get_ollama_response(prompt):
    try:
        
        result = ollama.chat(model='llama3.2:3b', messages=[
  {
    'role': 'system',
    'content': 'Give me a script for narrated 1 minute video.',
  },
  {
    'role': 'user',
    'content': prompt,
  },
])
        print(result['message']['content'])
        return result['message']['content']
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def get_ollama_images(prompt):
    try:
        result = ollama.chat(model='llama3.2:3b', messages=[
  {
    'role': 'system',
    'content': 'Generate a just a single list of keywords. Output the list only, without any introduction or numbering. Each term in a new line',
  },
  {
    'role': 'user',
    'content': prompt,
  },
])
        print(result['message']['content'])
        return result['message']['content']
    except Exception as e:
        return f"Exception occurred: {str(e)}"