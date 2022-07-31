from ast import Index
import numpy as np
from flask import Flask, request, render_template
import pickle
import ee
import collections
import math

app = Flask(__name__)
model = pickle.load(open('model','rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/',methods=['POST'])
def getLocation():

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

    m1 = (0.00002 * b1) + (-0.1)
    m2 = (0.00002 * b2) + (-0.1)
    m3 = (0.00002 * b3) + (-0.1)
    m4 = (0.00002 * b4) + (-0.1)
    m5 = (0.00002 * b5) + (-0.1)
    m6 = (0.00002 * b6) + (-0.1)
    m7 = (0.00002 * b7) + (-0.1)
    m8 = (0.00002 * b8) + (-0.1)
    m9 = (0.00002 * b9) + (-0.1)
    m10 = (0.00002 * b10) + (-0.1)
    m11 = (0.00002 * b11) + (-0.1)


    sun = im1.get('SUN_ELEVATION').getInfo()
    
    s1 = math.sin(sun)
    v1 = m1 / s1;
    v2 = m2 / s1;
    v3 = m3 / s1;
    v4 = m4 / s1;
    v5 = m5 / s1;
    v6 = m6 / s1;
    v7 = m7 / s1;
    v8 = m8 / s1;
    v9 = m9 / s1;
    v10 = m10 / s1;
    v11 = m11 / s1;

    NDVI = (b5 - b4) / (b5 + b4);
    SAVIvalue = ((b5 - b4) / (b5 + b4)) * (1.5);
    EVI1 = (b5 - b4);
    EVI2 = (b5 + 6) * (b4 - 7.5) * (b2 + 1.5);
    EVI = (EVI1 / EVI2) * 2.5;

    return render_template('index.html',NDVI=NDVI,SAVI=SAVIvalue,EVI=EVI,b1=b1,b2=b2,b3=b3,b4=b4,b5=b5,b6=b6,b7=b7,b9=b9,b10=b10,b11=b11,rm1=m1,rm2=m2,rm3=m3,rm4=m4,rm5=m5,rm6=m6,rm7=m7,rm8=m7,rm9=m9,rm10=m10,rm11=m11,sun=sun,v1 =v1,v2=v2,v3=v3,v4=v4,v5=v5,v6=v6,v7=v7,v8=v8,v9=v9,v10=v10,v11=v11)

@app.route('/getprediction',methods=['POST'])
def getprediction():    

    input = [float(x) for x in request.form.values()]
    final_input = [np.array(input)]
    prediction = model.predict(final_input)

    return render_template('Output.html', output='Your Soil Type is :{}'.format(prediction))
   

if __name__ == "__main__":
    app.run(debug=True)