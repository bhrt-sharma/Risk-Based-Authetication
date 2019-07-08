import os
# from app import app
from flask import Flask, flash, request, redirect, render_template,  jsonify
from sklearn.externals import joblib
from flask_material import Material
import numpy as np
from sklearn import metrics
import pandas as pd

# from sklearn.externals import joblib

# And now to load...


scaler_filename = "scaler.save"
scaler = joblib.load(scaler_filename) 


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
		'eCode': None,
		'll': None
	}
	if request.method == 'POST':
	
		user_id = int(request.form["user_id"])
		location_browser_lang = int(request.form["location_browser_lang"])
		config_browser_engine = int(request.form["config_browser_engine"])
		config_browser_name = int(request.form["config_browser_name"])
		config_device_brand= int(request.form['config_device_brand'])
		config_device_model= int(request.form['config_device_model'])
		config_os= int(request.form['config_os'])
		config_os_version= int(request.form['config_os_version'])
		config_resolution= int(request.form['config_resolution'])
		location_city= int(request.form['location_city'])
		location_country= int(request.form['location_country'])
		location_longitude= int(request.form['location_longitude'])

		features = [user_id, location_browser_lang, config_browser_engine, config_browser_name, 
		config_device_brand, config_device_model, config_os , config_os_version, 
		config_resolution, location_city, location_country, location_longitude]


		features = np.array(features)
		features = scaler.transform(features)		
		label_index = MODEL.predict(features)
		# print(features)
		if (label_index == -1):
			label = "Bad user"
		else:
			label= "Good user"
		status['eCode'] = "Inside"	
	
		status['ll'] = label

		return jsonify(status)


	return jsonify(status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)