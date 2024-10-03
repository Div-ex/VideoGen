from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import ollama


# Initialize Flask app
app = Flask(__name__)
CORS(app)

def get_ollama_response(prompt):
    try:
        # result = subprocess.run(
        #     ["ollama", "run", "llama3.2:1b", "p", prompt],
        #     capture_output=True,
        #     text=True
        # )
        
        # # Check if the command executed successfully
        # if result.returncode == 0:
        #     return result.stdout.strip()  # Model response
        # else:
        #     return f"Error running model: {result.stderr}"  # Error message
        
        result = ollama.chat(model='llama3.2:1b', messages=[
  {
    'role': 'system',
    'content': 'Give an answer in one line',
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

# Define an endpoint to accept prompts
@app.route("/api/prompt", methods=["POST"])
def prompt():
    # Ensure the request has a JSON body
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data['prompt']

    # Get the response from the language model
    response = get_ollama_response(prompt)

    # Return the response as JSON
    return jsonify({"response": response})

# Run the web server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
