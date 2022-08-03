import os
from flask import Flask, send_file, request, render_template, redirect, url_for, send_from_directory
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from werkzeug.utils import secure_filename
from datetime import datetime
from mbk1 import process_excel


ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
api = Api(app)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
            # save_location = os.path.join('input', new_filename)
            # file.save(save_location)
            df = pd.read_csv(file, encoding = 'unicode_escape')
            process_excel(df)
            print(type(df))
            file_name = "conviction.csv"
            return send_file(path_or_file=file_name, as_attachment=True, download_name=file_name)

            
    return render_template('upload.html')



class Users(Resource):
    def get(self):
        data = pd.read_csv('conviction.csv')  # read my CSV
        data = data.to_dict()  # will convert dataframe to dictionary
        file_name = "conviction.csv"
        return send_file(path_or_file=file_name, as_attachment=True, download_name=file_name)
    pass


api.add_resource(Users, '/users')
   

if __name__ == '__main__':
    app.run(debug=True)  