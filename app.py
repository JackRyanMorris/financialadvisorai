from flask import Flask, render_template, redirect, request

# Add our OpenAI API
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values

# Load our API_KEY
load_dotenv()

# Establish a connection with OpenAI
connection = OpenAI()

# Configure our Flask App
app = Flask(__name__)  # Directly create the Flask app instance

# Enable auto-reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Create our main route in our code, loading our index.html page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle POST
        # Start by getting our prompt and validating it
        prompt = request.form.get("prompt")
        if not prompt:
            print("Your forgot the prompt!")
            return redirect("/")
        
        # Handle sending this prompt to ChatGPT's API
        output = askAI(prompt)
        return render_template("index.html", output=output)
    else:
        # Handle GET
        return render_template("index.html")

# Handle API Requests
def askAI(prompt):
    completion = connection.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "system",
                "content": "Take the prompt and give really ironic, poor financial advice. Try to make your response use dry humor. Make sure your response is always relevant to giving poor financial advice."
            }
        ]
    )
    # Get the best response from the completion variable from the API call
    response = completion.choices[0].message.content
    return response