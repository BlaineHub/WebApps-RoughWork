from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from matplotlib.pyplot import text
from sqlalchemy.sql import func
import pandas as pd
from werkzeug.utils import secure_filename,send_file
from geopy.geocoders import Nominatim
import datetime as dt

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
        if request.method=='POST':
            try:
                global filename
                file=request.files['file']
                df = pd.read_csv(file)
                df = df.set_index('ID')
                pd.set_option('display.colheader_justify', 'center')
                address = list(df['Address'])
                lat = []
                lon = []
                for x in address:
                    if str(x) == 'nan':
                        lat.append('None')
                        lon.append('None')
                    else:
                        geolocator = Nominatim(user_agent="MyApp")
                        location = geolocator.geocode(x)
                        lat.append(location.latitude)
                        lon.append(location.longitude)
                df['Latitude'] = lat
                df['Longitude'] = lon
                html = df.to_html()
                text_file = open('templates/dataframe.html','w')
                text_file.write(html)
                text_file.close()
                filename=dt.datetime.now().strftime('uploads/%Y-%m-%d-%H-%M-%S'+'.csv')
                df.to_csv(filename)
                return render_template('index.html', text='file uploaded successfully')
            except:
                return render_template('index.html', text='file error')
        else:
            return render_template('index.html')

@app.route('/download')
def download():
    return send_file(filename, download_name=filename[8:], as_attachment=True, environ=request.environ)        

if __name__ == '__main__':
    app.debug=True
    app.run()