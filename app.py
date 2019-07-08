import os
# from app import app
from flask import Flask, flash, request, redirect, render_template,  jsonify
from sklearn.externals import joblib
from flask_material import Material

from sklearn import metrics
import pandas as pd

app = Flask(__name__)

#Loading the model
MODEL = joblib.load("osvm.pkl")

@app.route('/', methods=['GET'])
def idk():
    return jsonify('Welcome')

@app.route('/predict', methods=['POST'])
def analyze():
	# Retreive query parameters related to this request.
	status = {
		'eCode': None
	}
	print(request.method)
	if request.method == 'POST':
		print(request.form)
		user_id = request.form["user_id"].astype(np.int)
		location_browser_lang = request.form["location_browser_lang"].astype(np.int)
		config_browser_engine = request.form["config_browser_engine"].astype(np.int)
		config_browser_name = request.form["config_browser_name"].astype(np.int)
		config_device_brand=request.form['config_device_brand'].astype(np.int)
		config_device_model=request.form['config_device_model'].astype(np.int)
		config_os=request.form['config_os'].astype(np.int)
		config_os_version=request.form['config_os_version'].astype(np.int)
		config_resolution=request.form['config_resolution'].astype(np.int)
		location_city=request.form['location_city'].astype(np.int)
		location_country=request.form['location_country'].astype(np.int)
		location_longitude=request.form['location_longitude'].astype(np.int)

		# features = [[user_id,location_browser_lang,config_browser_engine,config_browser_name,config_device_brand,config_device_model, config_os , config_os_version,config_resolution,location_city,location_country,location_longitude]]
		
		# features = pd.DataFrame(features)

		# label_index = MODEL.predict(features)
		# print(label_index)
		# if (label_index == -1):

		# 	label = "Bad user"
		# else:
		# 	label= "Good user"
		status['eCode'] = "Inside"	
		return jsonify(status)

	return jsonify(status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)