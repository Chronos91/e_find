from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def flatten_json(data):
    """ Function to flatten JSON by extracting only cookies. """
    if isinstance(data, list):
        return [{"cookies": item.get("cookies", [])} for item in data]
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        if "file" not in request.files:
            return "No file part", 400
        
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            
            # Read and process the file
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)  # Load JSON data
                    flattened_result = flatten_json(data)
            except json.JSONDecodeError:
                return "Invalid JSON file", 400
            
            return render_template("index.html", result=flattened_result)
    
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
