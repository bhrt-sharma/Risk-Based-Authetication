# Risk-Based-Authetication


Step 1 :  Run the RBA.ipynb file :
          It is using the new_rba.csv which has 18 features in it, this data is which is proviced by Bluebricks..
          
          
          
Step 2 :  Open POSTMAN, give the POST request to the last_api.py file running at http://0.0.0.0:5000/predict, pass the parameters.
For example:
          {
	"user_id" : 1,
        "Date_and_time" : 22,
        "Device_ip" : 6,
        "Transaction_ammount" : 14.0,
        "Typing_speed" : 4.666666666666667,
        "board" : 2,
        "bootloader" : 0,
        "brand" : 1,
        "device" : 1,
        "display" : 1,
        "fingerprint" : 1, 
        "host" : 2,
        "id" : 0,
        "latitude" : 32.0,
        "longitude" : 115.0,
        "manufacturer" : 1,
        "model" : 0,
        "Device_velocity" : -1,
        "inclined" : 13
}
