from flask import Flask, request, render_template
from flask_cors import cross_origin
from datetime import date
import sklearn
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
model = pickle.load(open("model.pkl","rb"))

@app.route("/")
@cross_origin()
def home():
	return render_template("index.html")


@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
	if request.method == "POST":

		#Seller Type
		seller_type = request.form["Seller_type"]
		if seller_type == 'Individual':
			Individual = 1
			Trustmark_dealer = 0
		else:
			Individual = 0
			Trustmark_dealer = 1

		#Mileage
		Mileage = request.form["Mileage"]

		#Seats
		Seats = request.form["Seats"]

		#Year bought
		Year = request.form["Year"]
		age = np.log(2022 - int(Year))

		#Distance driven
		distance = float(request.form["kms_driven"])
		kms_driven = np.log(distance)

		#Engine power
		Engine = float(request.form["Engine"])
		engine = np.log(Engine)

		#Max Power
		MaxPower = float(request.form["Max_power"])
		max_power = np.log(MaxPower)

		#Fuel Type
		fuel = {'LPG':1,'CNG':2,'Petrol':3,'Diesel':4,'Electric':5}
		FuelType = request.form["Fuel_type"]
		fuel_type = fuel[FuelType]

		#Transmission Type
		transmission = {'Manual':1, 'Automatic':2}
		TransmissionType = request.form["Transmission_type"]
		transmission_type = transmission[TransmissionType]


		prediction = model.predict([[Individual, Trustmark_dealer, Mileage,Seats, age, kms_driven, engine, max_power, fuel_type, transmission_type]])

		output = round(np.exp(prediction[0]),2)

		return render_template('index.html',prediction_text = "Your Car Price is Rs. {}".format(output))

	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug = True)

