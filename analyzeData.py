import duckdb
import os
from flask import Flask, request, jsonify
from flask_caching import Cache
from pandasai import SmartDataframe
from pandasai.llm import OpenAI


def check_file_permissions(file_path):
    try:
        # Get file permissions as a string
        permissions = oct(os.stat(file_path).st_mode)[-3:]
        print(f"File permissions for {file_path}: {permissions}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")


def modify_file_permissions(file_path, new_permissions):
    try:
        # Convert octal string to integer
        new_permissions = int(new_permissions, 8)

        # Set the new file permissions
        os.chmod(file_path, new_permissions)
        print(f"File permissions for {file_path} modified to {oct(os.stat(file_path).st_mode)[-3:]}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except ValueError:
        print("Invalid permissions format. Use octal representation, e.g., '755'.")


app = Flask(__name__)
llm = OpenAI(api_token="")
db_file_path = ""

check_file_permissions(db_file_path)
try:
    os.remove(db_file_path)
except FileNotFoundError:
    pass
duckdb.connect(db_file_path)
modify_file_permissions(db_file_path, "777")
df = SmartDataframe("output.csv", config={"llm": llm, "cache": {"backend": "duckdb", "cache_file": db_file_path}})


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data['query']

        response = df.chat(query)
        df_dict = response.to_dict()
        return jsonify({'response': df_dict})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
