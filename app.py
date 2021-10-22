import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import pickle
import yaml

app = Flask(__name__)
model = pickle.load(open('Teaching_performance.pkl', 'rb'))


# Route for handling the login page logic

# @app.route('/')
# def home():
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/about')  
def about():
    return render_template('about.html')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    print(f'final_features={final_features}')
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)


    return render_template('index.html', 
        prediction_text='Teaching_performance is {} where low:1, medium:2 and high:3'.format(output)
        )



@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    print("reached here")
    data = request.get_json(force=True)
    print("check")
    prediction = model.predict([np.array(list(data.values()))])
    print("modle done")

    output = prediction[0]
    json_output={"output": output}
    print(json_output)

    print("modeldone1")
    return jsonify(json_output)

if __name__=="__main__":
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))
