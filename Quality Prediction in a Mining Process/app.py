import joblib
from flask import Flask , render_template ,request
app = Flask(__name__)


model = joblib.load("model.h5")
scaling = joblib.load("scaling.h5")

Month_dummies = [0 for i in range(11)]
Day_dummies = [0 for i in range(6)]
Hour_dummies = [0 for i in range(23)]

@app.route('/' , methods = ["GET"])
def index():
  return render_template("index.html")

@app.route("/predict" , methods = ["GET"])
def predict():
  Iron_Feed = float(request.args["Iron Feed"])
  Silica_Feed = float(request.args["Silica Feed"])
  Starch_Flow = float(request.args["Starch Flow"])
  Amina_Flow = float(request.args["Amina Flow"])
  Ore_Pulp_Flow = float(request.args["Ore Pulp Flow"])
  Ore_Pulp_pH = float(request.args["Ore Pulp pH"])
  Ore_Pulp_Density = float(request.args["Ore Pulp Density"])
  Flotation_Column_01_Air_Flow = float(request.args["Flotation Column 01 Air Flow"])
  Flotation_Column_02_Air_Flow = float(request.args["Flotation Column 02 Air Flow"])
  Flotation_Column_03_Air_Flow = float(request.args["Flotation Column 03 Air Flow"])
  Flotation_Column_04_Air_Flow = float(request.args["Flotation Column 04 Air Flow"])
  Flotation_Column_05_Air_Flow = float(request.args["Flotation Column 05 Air Flow"])
  Flotation_Column_06_Air_Flow = float(request.args["Flotation Column 06 Air Flow"])
  Flotation_Column_07_Air_Flow = float(request.args["Flotation Column 07 Air Flow"])
  Flotation_Column_01_Level = float(request.args["Flotation Column 01 Level"])
  Flotation_Column_02_Level = float(request.args["Flotation Column 02 Level"])
  Flotation_Column_03_Level = float(request.args["Flotation Column 03 Level"])
  Flotation_Column_04_Level = float(request.args["Flotation Column 04 Level"])
  Flotation_Column_05_Level = float(request.args["Flotation Column 05 Level"])
  Flotation_Column_06_Level = float(request.args["Flotation Column 06 Level"])
  Flotation_Column_07_Level = float(request.args["Flotation Column 07 Level"])
  Month_Name_ID = int((request.args["Month"]))
  Day_Name_ID = int((request.args["Day"]))
  Hour_ID = int((request.args["Hour"]))

  if Month_Name_ID != -1:
    Month_dummies[Month_Name_ID] = 1

  if Day_Name_ID != -1:
    Day_dummies[Day_Name_ID] = 1

  if Hour_ID != -1:
    Hour_dummies[Hour_ID] = 1


  data = [Iron_Feed, Silica_Feed, Starch_Flow, Amina_Flow, Ore_Pulp_Flow, Ore_Pulp_pH, Ore_Pulp_Density,
          Flotation_Column_01_Air_Flow, Flotation_Column_02_Air_Flow, Flotation_Column_03_Air_Flow, Flotation_Column_04_Air_Flow,
          Flotation_Column_05_Air_Flow, Flotation_Column_06_Air_Flow, Flotation_Column_07_Air_Flow, Flotation_Column_01_Level,
          Flotation_Column_02_Level, Flotation_Column_03_Level, Flotation_Column_04_Level, Flotation_Column_05_Level,
          Flotation_Column_06_Level, Flotation_Column_07_Level] + Month_dummies + Day_dummies + Hour_dummies

  data = scaling.transform([data])
  silica_percentage = model.predict(data)[0]

  return render_template("result.html" , silica_percentage = silica_percentage)

if __name__ == "__main__":
  app.run()