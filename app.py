import numpy as np
from flask import Flask, request, render_template
import pickle
import ee
import collections

app = Flask(__name__)
model = pickle.load(open('model','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def getLocation():

    starting = request.form['start']
    ending = request.form['end']
    print(starting+" == "+ending)
    location = request.form['location']
    l = location.split(",")
    l1 = l[0]
    l2 = l[1]
    lat = float(l1)
    lon = float(l2)
    collections.Callable = collections.abc.Callable
    service_account = 'muhammad402ali123@ee-afzal.iam.gserviceaccount.com'
    key = 'key.json'
    credentials = ee.ServiceAccountCredentials(service_account, key)
    ee.Initialize(credentials)

    p = ee.Geometry.Point([lon, lat])
    start = '2020-06-25'
    end = '2020-07-25'
    imageCollection = ee.ImageCollection('LANDSAT/LC08/C01/T1').filterDate(start, end).filterBounds(p)
    im1 = imageCollection.sort('CLOUD_COVER', True).first()
    data_b1 = im1.select("B1").reduceRegion(ee.Reducer.mean(),p,10).get("B1")
    b1 = (data_b1.getInfo())
    data_b1 = im1.select("B2").reduceRegion(ee.Reducer.mean(),p,10).get("B2")
    b2 = (data_b1.getInfo())
    data_b1 = im1.select("B3").reduceRegion(ee.Reducer.mean(),p,10).get("B3")
    b3 = (data_b1.getInfo())
    data_b1 = im1.select("B4").reduceRegion(ee.Reducer.mean(),p,10).get("B4")
    b4 = (data_b1.getInfo())
    data_b1 = im1.select("B5").reduceRegion(ee.Reducer.mean(),p,10).get("B5")
    b5 = (data_b1.getInfo())
    data_b1 = im1.select("B6").reduceRegion(ee.Reducer.mean(),p,10).get("B6")
    b6 = (data_b1.getInfo())
    data_b1 = im1.select("B7").reduceRegion(ee.Reducer.mean(),p,10).get("B7")
    b7 = (data_b1.getInfo())
    data_b1 = im1.select("B8").reduceRegion(ee.Reducer.mean(),p,10).get("B8")
    b8 = (data_b1.getInfo())
    data_b1 = im1.select("B9").reduceRegion(ee.Reducer.mean(),p,10).get("B9")
    b9 = (data_b1.getInfo())
    data_b1 = im1.select("B10").reduceRegion(ee.Reducer.mean(),p,10).get("B10")
    b10 = (data_b1.getInfo())
    data_b1 = im1.select("B11").reduceRegion(ee.Reducer.mean(),p,10).get("B11")
    b11 = (data_b1.getInfo()) 

    rb1 = im1.get('REFLECTANCE_ADD_BAND_1').getInfo()
    rb2 = im1.get('REFLECTANCE_ADD_BAND_2').getInfo()
    rb3 = im1.get('REFLECTANCE_ADD_BAND_3').getInfo()
    rb4 = im1.get('REFLECTANCE_ADD_BAND_4').getInfo()
    rb5 = im1.get('REFLECTANCE_ADD_BAND_5').getInfo()
    rb6 = im1.get('REFLECTANCE_ADD_BAND_6').getInfo()
    rb7 = im1.get('REFLECTANCE_ADD_BAND_7').getInfo()
    rb8 = im1.get('REFLECTANCE_ADD_BAND_8').getInfo()
    rb9 = im1.get('REFLECTANCE_ADD_BAND_9').getInfo()

    rm1 = im1.get('REFLECTANCE_MULT_BAND_1').getInfo()
    rm2 = im1.get('REFLECTANCE_MULT_BAND_2').getInfo()
    rm3 = im1.get('REFLECTANCE_MULT_BAND_3').getInfo()
    rm4 = im1.get('REFLECTANCE_MULT_BAND_4').getInfo()
    rm5 = im1.get('REFLECTANCE_MULT_BAND_5').getInfo()
    rm6 = im1.get('REFLECTANCE_MULT_BAND_6').getInfo()
    rm7 = im1.get('REFLECTANCE_MULT_BAND_7').getInfo()
    rm8 = im1.get('REFLECTANCE_MULT_BAND_8').getInfo()
    rm9 = im1.get('REFLECTANCE_MULT_BAND_9').getInfo()

    sun = im1.get('SUN_ELEVATION').getInfo()
    
    crb1=rm1/sun
    crb2=rm2/sun
    crb3=rm3/sun
    crb4=rm4/sun
    crb5=rm5/sun
    crb6=rm6/sun
    crb7=rm7/sun
    crb8=rm8/sun
    crb9=rm9/sun
    crb10=rm9/sun
    crb11=rm9/sun
    NDVI = (b5 - b4) / (b5 + b4);
    SAVIvalue = ((b5 - b4) / (b5 + b4)) * (1.5);
    EVI1 = (b5 - b4);
    EVI2 = (b5 + 6) * (b4 - 7.5) * (b2 + 1.5);
    EVI = (EVI1 / EVI2) * 2.5;
    return render_template('index.html',b1=b1,b2=b2,b3=b3,b4=b4,b5=b5,b6=b6,b7=b7,b9=b9,b10=b10,b11=b11,sun=sun,rm1=rm1,rm2=rm2,rm3=rm3,rm4=rm4,rm5=rm5,rm6=rm6,rm7=rm7,rm8=rm8,rm9=rm9,crb1=crb1,crb2=crb2,crb3=crb3,crb4=crb4,crb5=crb5,crb6=crb6,crb7=crb7,crb8=crb8,crb9=crb9,crb10=crb10,crb11=crb11,ndvi=NDVI,savi=SAVIvalue,evi=EVI)

@app.route('/getprediction',methods=['POST'])
def getprediction():
    def listToString(s): 
        str1 = " "     
        for ele in s: 
            str1 += ele  
            return str1 
    print("Form Values",request.form.values())
    input = [float(x) for x in request.form.values()]
    final_input = [np.array(input)]
    prediction = model.predict(final_input)
    prediction=listToString(prediction)
    return render_template('Output.html', output=prediction)


if __name__ == "__main__":
  app.run(threaded=True, port=5000)