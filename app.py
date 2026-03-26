import os
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import requests

app = Flask(__name__)

# ===========================
# DOWNLOAD MODEL FUNCTION
# ===========================
def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)

# ===========================
# 🔽 ADD YOUR GOOGLE DRIVE DIRECT LINKS HERE
# ===========================
fertilizer_url = "PASTE_YOUR_FERTILIZER_MODEL_LINK_HERE"
yield_url = "PASTE_YOUR_YIELD_MODEL_LINK_HERE"

# Download models if not present
download_file(fertilizer_url, "Fertilizer.pkl")
download_file(yield_url, "yield.pkl")

# Load models safely
try:
    Fertilizer = pickle.load(open("Fertilizer.pkl", "rb"))
    yields = pickle.load(open("yield.pkl", "rb"))
except Exception as e:
    print("Model loading error:", e)
    Fertilizer = None
    yields = None

# ===========================
# ROUTES
# ===========================

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/preview', methods=["POST"])
def preview():
    dataset = request.files['datasetfile']
    df = pd.read_csv(dataset, encoding='unicode_escape')
    df.set_index('Id', inplace=True)
    return render_template("preview.html", df_view=df)

@app.route('/logins')
def logins():
    return render_template('logins.html')

@app.route('/uploads')
def uploads():
    return render_template('uploads.html')

@app.route('/previews', methods=["POST"])
def previews():
    dataset = request.files['datasetfile']
    df = pd.read_csv(dataset, encoding='unicode_escape')
    df.set_index('Id', inplace=True)
    return render_template("previews.html", df_view=df)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    return render_template('prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if Fertilizer is None:
            return "Model not loaded"

        int_feature = [float(x) for x in request.form.values()]
        final_features = [np.array(int_feature)]

        result = Fertilizer.predict(final_features)
        output = result[0]

        return render_template('prediction.html', prediction_text=output)

    except Exception as e:
        return f"Error: {e}"

@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    return render_template('predictions.html')

@app.route('/predicts', methods=['POST'])
def predicts():
    try:
        if yields is None:
            return "Model not loaded"

        state = request.form['State_Name']
        season = request.form['Season']
        crop = request.form['Crop']
        area = float(request.form['Area'])

        int_feature = [state, season, crop, area]
        final_features = [np.array(int_feature)]

        result = yields.predict(final_features)
        pred = int(result[0])
        results = pred / area

        return render_template('predictions.html',
                               prod=pred,
                               prediction_text=results)

    except Exception as e:
        return f"Error: {e}"

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

# ===========================
# MAIN (IMPORTANT FOR RENDER)
# ===========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
