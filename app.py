from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def flatten_cookies(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # Load JSON from file

    flat_list = []

    if "tokens" in data:
        for domain, cookies in data["tokens"].items():
            for name, attributes in cookies.items():
                flat_list.append({
                    "domain": domain.lstrip("."),
                    "name": attributes.get("Name", ""),
                    "path": attributes.get("Path", "/"),
                    "value": attributes.get("Value", ""),
                    "httpOnly": attributes.get("HttpOnly", False)
                })
    return flat_list


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        flat_json = flatten_cookies(file_path)
        return jsonify(flat_json)

    return '''
    <!doctype html>
    <html>
    <body>
        <h2>Upload JSON File</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
