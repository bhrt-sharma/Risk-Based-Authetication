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
    status = {
		'eCode': None,
		'll': None,
		'Score' : None,
		'Correct' : None,
		'Wrong' : None,
		'User_as_per_Score':None
	}
	# Retreive query parameters related to this request.


    if request.method == "POST":

		#print(hey)
        user_id = int(request.json["user_id"])
        Date_and_time = int(request.json["Date_and_time"])
        Device_ip = int(request.json["Device_ip"])
        Transaction_ammount = int(request.json["Transaction_ammount"])
        Typing_speed = int(request.json["Typing_speed"])
        board = int(request.json['board'])
        bootloader = int(request.json['bootloader'])
        brand = int(request.json['brand'])
        device = int(request.json['device'])
        display= int(request.json['display'])
        fingerprint= int(request.json['fingerprint'])
        host= int(request.json['host'])
        id= float(request.json['id'])
        latitude= float(request.json['latitude'])
        longitude= float(request.json['longitude'])
        manufacturer= int(request.json['manufacturer'])
        model= int(request.json['model'])
        Device_velocity= float(request.json['Device_velocity'])
        inclined= float(request.json['inclined'])

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

        c= str(1)+'.pkl'
        from sklearn.externals import joblib
        if(c in pkl_list) :


            MODEL = joblib.load(c)
        	#print(features)
            scc = joblib.load("scaler.save")

            features = np.array(features)
            X_test = pd.DataFrame(features)
            X_test = scc.transform(X_test)
            bharat_test = pd.DataFrame(X_test)
            bharat_test_series = bharat_test.ix[:,:]

        	#features = scaler.transform(features)
            label_index = MODEL.predict(bharat_test_series)
            #print(features)
            #print(hey)
            if (label_index != 2):
                label = "Bad user"
            else:
                label= "Good user"

############### otherwise do this
		      ######## XYZ

################ this part is to describe which features are not matched !
        Whole_data_19 = pd.read_csv("without_normalised_rba.csv")

        Y= []
        y = Whole_data_19.iloc[:, 4]

        for index, value in y.items():
            if value !="vikram@blue-bricks.com":
                Y.append("others")
            else:
                Y.append("vikram@blue-bricks.com")

        Y= pd.Series(Y)
        y = Y.astype('category').cat.codes
        tttrain_y = y.to_numpy()

        sub_df=Whole_data_19.drop(labels="User name",axis=1)

        sub_df['Target'] = y
        sub_df= sub_df[sub_df['Target']==1]
        sub_df = sub_df.drop(labels='Target',axis=1)

#############HERE WE CAN PROCESS THE WEIGHTS !!
        thisdict = {
            "Date_and_time" : 1,
            "Device_ip": 4,
            "Transaction_ammount" : 4,
            "Typing_speed" : 4,
            "board" : 4,
            "bootloader" : 4,
            "brand" :4 ,
            "device" : 4,
            "display" :4 ,
            "fingerprint" :4 ,
            "host" : 4,
            "id" : 4,
            "latitude" : 5,
            "longitude" : 5,
            "manufacturer" :4 ,
            "model" : 4,
            "Device_velocity" :1 ,
            "inclined" : 1
            }
        score = 0
        i=0
        count=0
        nott=0

        for (columnName, columnData) in sub_df.iteritems():
        #     print('Colunm Name : ', columnName)
            x=columnData.values

            tofind=features[0][i]

            if( np.any(x[:] == tofind) ):
                count=count+1
                score= thisdict[str(list(thisdict)[i])] + score
            else:
                print(tofind)
                nott=nott+1
            i=i+1

        print(str('matched'), str(count))
        print(str('NOT_matched'), str(nott))

        if(score  > 36):
            User_as_per_Score = "Risk Level Low - Ask for password only"
        elif(score > 28 ):
        	User_as_per_Score = "Risk Level 2 - Ask for password and OTP both"
        elif(score > 20) :
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
