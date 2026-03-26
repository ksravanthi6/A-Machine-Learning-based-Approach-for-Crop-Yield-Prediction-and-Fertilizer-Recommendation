import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle

import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle
import numpy as np
import pandas as pd

 

app = Flask(__name__) #Initialize the flask App
Fertilizer = pickle.load(open('Fertilizer.pkl','rb'))
yields = pickle.load(open('yield.pkl', 'rb'))
@app.route('/')

@app.route('/index')
def index():
	return render_template('index.html')
 

#@app.route('/future')
#def future():
#	return render_template('future.html')    

@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/upload')
def upload():
    return render_template('upload.html')  
@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df)	

@app.route('/logins')
def logins():
	return render_template('logins.html')
@app.route('/uploads')
def uploads():
    return render_template('uploads.html')  
@app.route('/previews',methods=["POST"])
def previews():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("previews.html",df_view = df)	

#@app.route('/home')
#def home():
 #   return render_template('home.html')

@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
    return render_template('prediction.html')


#@app.route('/upload')
#def upload_file():
#   return render_template('BatchPredict.html')



@app.route('/predict',methods=['POST'])
def predict():
	int_feature = [float(x) for x in request.form.values()]
	print(int_feature) 
	final_features = [np.array(int_feature)]
     
	result=Fertilizer.predict(final_features)
	#if result == 1:
			#result = "liver disease"
	#else:
		#result = 'No disease'
	for i in result:
	    print(i, end="")
	return render_template('prediction.html', prediction_text= i)

@app.route('/predictions', methods = ['GET', 'POST'])
def predictions():
    return render_template('predictions.html')


#@app.route('/upload')
#def upload_file():
#   return render_template('BatchPredict.html')



@app.route('/predicts',methods=['POST'])
def predicts():
	if request.method == 'POST':
		state = request.form['State_Name'] 
		season = request.form['Season']
		crop = request.form['Crop'] 
		area = request.form['Area']          
		int_feature =[state,season,crop,area]
         
		final_features = [np.array(int_feature)]
 
		result=yields.predict(final_features)
		pred = int(result)
		results = pred/float(area)
	return render_template('predictions.html',prod = pred, prediction_text= results)
    
@app.route('/performance')
def performance():
	return render_template('performance.html')
    
@app.route('/chart')
def chart():
	return render_template('chart.html')    
    
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
