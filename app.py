 # Bad code

from flask import Flask, request, jsonify, render_template_string
from IPython import get_ipython

app = Flask(__name__)

def execute_cell(code):
    ipython = get_ipython()
    if ipython is None:
        from IPython.core.interactiveshell import InteractiveShell
        ipython = InteractiveShell()
    out = ipython.run_cell(code)
    return out.result

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Code Executor</title>
    </head>
    <body>
        <h2>Enter Your Code</h2>
        <form action="/execute" method="post">
            <textarea name="code" rows="10" cols="50"></textarea><br>
            <input type="submit" value="Execute">
        </form>
    </body>
    </html>
    """)

@app.route('/execute', methods=['POST'])
def execute():
    code = request.form['code']
    try:
        result = execute_cell(code)
        return render_template_string("""
        <h2>Result</h2>
        <p>{{result}}</p>
        <a href="/">Go Back</a>
        """, result=str(result))
    except Exception as e:
        return render_template_string("""
        <h2>Error</h2>
        <p>{{error}}</p>
        <a href="/">Go Back</a>
        """, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
