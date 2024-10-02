from flask import Flask, request, jsonify

import pyttsx3

app = Flask(__name__)

# Initialize the TTS engine globally
engine = pyttsx3.init()

# Set up some default properties for the engine
engine.setProperty('rate', 150)    # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can change the voice index here

# Define an API endpoint to accept text input and trigger TTS
@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text', '')
    
    if text:
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        return jsonify({"message": "Speech completed"}), 200
    else:
        return jsonify({"error": "No text provided"}), 400

# Serve the HTML page on the root URL
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Themed Text-to-Speech</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #1a1a2e;
                color: #f5f5f5;
                font-family: 'Orbitron', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                text-align: center;
                background: #162447;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.7);
            }

            h1 {
                font-size: 2.5rem;
                margin-bottom: 20px;
                color: #00d9ff;
                text-shadow: 0px 4px 10px rgba(0, 217, 255, 0.5);
            }

            textarea {
                width: 100%;
                padding: 15px;
                border-radius: 8px;
                border: none;
                outline: none;
                font-size: 1rem;
                margin-bottom: 20px;
                background-color: #e0e0e0;
                color: #333;
            }

            button {
                padding: 10px 20px;
                font-size: 1.2rem;
                background: linear-gradient(90deg, #00d9ff, #00f260);
                border: none;
                color: white;
                border-radius: 10px;
                cursor: pointer;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }

            button:hover {
                background: linear-gradient(90deg, #00f260, #00d9ff);
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.5);
            }

            .footer {
                margin-top: 20px;
                font-size: 0.8rem;
                color: #7d7d7d;
            }

            /* Animation */
            @keyframes glow {
                0% { text-shadow: 0 0 10px #00d9ff, 0 0 20px #00d9ff, 0 0 30px #00f260, 0 0 40px #00f260; }
                100% { text-shadow: 0 0 20px #00f260, 0 0 30px #00d9ff, 0 0 40px #00d9ff, 0 0 50px #00f260; }
            }

            h1 {
                animation: glow 1.5s infinite alternate;
            }

        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Text-to-Speech</h1>
            <textarea id="text" rows="5" cols="40" placeholder="Enter text here..."></textarea><br><br>
            <button onclick="convertToSpeech()">Speak</button>
            <div class="footer">Powered by YnT</div>
        </div>

        <script>
            function convertToSpeech() {
                const text = document.getElementById("text").value;
                fetch('/speak', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: text })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        </script>
    </body>
    </html>
    '''
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)