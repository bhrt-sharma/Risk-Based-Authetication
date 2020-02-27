import os
# from app import app
from flask import Flask, flash, request, redirect, render_template,  jsonify
from sklearn.externals import joblib
from flask_material import Material
import numpy as np
from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm

# from sklearn.externals import joblib

# And now to load...


scaler_filename = "scaler.save"
scaler = joblib.load(scaler_filename)


app = Flask(__name__)

#Loading the model


@app.route('/', methods=['GET'])
def idk():
    return jsonify('Welcome')

@app.route('/predict', methods=['POST'])
def analyze():
	# Retreive query parameters related to this request.
	status = {
		'eCode': None,
		'll': None,
		'Score' : None,
		'Correct' : None,
		'Wrong' : None,
		'User_as_per_Score':None
	}
	if request.method == 'POST':

		#print(hey)
        user_id = int(request.form["user_id"])
		Date_and_time = int(request.form["Date_and_time"])
		Device_ip = int(request.form["Device_ip"])
		Transaction_ammount = int(request.form["Transaction_ammount"])
		Typing_speed = int(request.form["Typing_speed"])
		board = int(request.form['board'])
		bootloader = int(request.form['bootloader'])
		brand = int(request.form['brand'])
		device = int(request.form['device'])
		display= int(request.form['display'])
		fingerprint= int(request.form['fingerprint'])
		host= int(request.form['host'])
		id= float(request.form['id'])
		latitude= float(request.form['latitude'])
        longitude= float(request.form['longitude'])
		manufacturer= int(request.form['manufacturer'])
		model= int(request.form['model'])
		Device_velocity= float(request.form['Device_velocity'])
		inclined= float(request.form['inclined'])

		features = [[Date_and_time,
         Device_ip, Transaction_ammount,
         Typing_speed,board,bootloader,brand,device,display,fingerprint,host,id,
         latitude,longitude,manufacturer,model,Device_velocity,inclined]]

		pkl_list = []
		import os
		for file in os.listdir(os.getcwd()):
		    if file.endswith(".pkl"):
		#         print(os.path.join("", file))
		        pkl_list.append(os.path.join("", file))


#########if user_id in file then don't build the model

		c= str(user_id)+'.pkl'

		if(c in pkl_list) :

			MODEL = joblib.load(c)
			#print(features)

			features = np.array(features)
			#features = scaler.transform(features)
			label_index = MODEL.predict(features)
			#print(features)
			#print(hey)
			if (label_index != 2):
				label = "Bad user"
			else:
				label= "Good user"

###############otherwise do this
		else :

			X_train = pd.read_csv("new_rba.csv")

            Y= []
            for index, value in y.items():
            if value !="vikram@blue-bricks.com":
                Y.append(1)
            else:
                Y.append(2)

            Y= pd.Series(Y)
            tttrain_y = Y.to_numpy()

            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X_train, tttrain_y, test_size=0.33, random_state=42)

# SVC

            model = SVC(kernel='rbf', C=1E10, class_weight='balanced', verbose=1, gamma=0.05)
            model.fit(X_train, y_train)

            print("Train ACC : {}\nTest ACC : {}".format(model.score(X_train, y_train), model.score(X_test, y_test)))


            features = [[]]
			label_index = model.predict(features)
			#print(features)
			#print(hey)
			if (label_index != 2):
				label = "Bad user"
			else:
				label= "Good user"



			import pickle
			c= str(id)+'.pkl'
			output = open(c, 'wb')
			pickle.dump(clf, output)
			output.close()

############ yaha se aage kar ANshaj

################this part is to describe which features are not matched !
		Whole_data = pd.read_csv("hey13.csv")
		X_train=Whole_data[Whole_data['user_id'] == user_id]

		X_train = X_train[['user_id', "location_browser_lang", "config_browser_engine", "config_browser_name",
		"config_device_brand", "config_device_model", "config_os" , "config_os_version",
		"config_resolution", "location_city", "location_country", "location_longitude",'location_latitude']]

		X_train = pd.DataFrame(X_train)

		x = np.cos(X_train['location_latitude']) * np.sin(X_train['location_longitude'])
		y = np.cos(X_train['location_latitude']) * np.sin(X_train['location_longitude'])
		z = np.sin(X_train['location_latitude'])


		X_train['x'] = pd.Series(x)

		X_train['y'] = y

		X_train['z'] = z


		del X_train['location_longitude']
		del X_train['location_latitude']


		an=X_train[X_train['user_id'] == user_id]

		columns = an.columns


		count=0
		nott=0



#############HERE WE CAN PROCESS THE WEIGHTS !!
		thisdict =	{
	  "user_id": 0,
	  "location_browser_lang": 2,
	  "config_browser_engine":1,
	  "config_browser_name": 1,
	  "config_device_brand": 5,
	  "config_device_model": 5,
	  "config_os": 0,
	  "config_os_version": 1,
	  "config_resolution": 1,
	  "location_city": 4,
	  "location_country": 8,
	  "location_longitude":4,
	   "location_latitude" :4
		}
		score = 0
		for i in range(0,12):
		    col = columns[i]
		    if features[0][i] in an[col].unique():
		        count=count+1
		        score= thisdict[columns[i]] + score

		    else:
		        nott=nott+1

		if(score  > 31):
		    User_as_per_Score = "Risk Level Low - Ask for password only"
		elif(score > 25 ):
			User_as_per_Score = "Risk Level 2 - Ask for password and OTP both"
		elif(score > 18) :
			User_as_per_Score = "Risk Level 3 - Ask for password and OTP and Facial password"
		else:
			User_as_per_Score = "Risk Level 4 - Very High Risk"




		#print(label_index)
		status['eCode'] = "Inside"

		status['ll'] = label

		status['Score'] =score
		status['Correct']=count
		status['Wrong']=nott
		status['User_as_per_Score'] = User_as_per_Score

		return jsonify(status)



	return jsonify(status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
