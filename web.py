import os
from flask import Flask, render_template_string
import pandas as pd
from main import main as run_predictions

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Football Score Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="mb-4">Football Score Predictions</h1>
    {% if table %}
        {{ table|safe }}
    {% else %}
        <div class="alert alert-warning">No predictions available for tomorrow.</div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route("/")
def index():
    run_predictions()
    if not os.path.exists("tomorrow_predictions.html"):
        return render_template_string(HTML_TEMPLATE, table=None)
    df = pd.read_html("tomorrow_predictions.html")[0]
    table = df.to_html(classes="table table-striped", index=False)
    return render_template_string(HTML_TEMPLATE, table=table)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
