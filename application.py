from flask import Flask, request, render_template
import pickle
import pandas as pd

# Load model and scaler from models folder
ridge_model = pickle.load(open('models/ridge_reg_model.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scaler_reg.pkl', 'rb'))

app = Flask(__name__)

@app.route("/")
def index():
    # You can serve a landing page or redirect to form
    return render_template('index.html')


@app.route("/predictdata", methods=['GET', 'POST'])
def predict_data():
    if request.method == 'POST':
        try:
            # Extract inputs from form
            temp = int(request.form['Temperature'])
            rh = int(request.form['RH'])
            ws = int(request.form['Ws'])
            rain = float(request.form['Rain'])
            ffmc = float(request.form['FFMC'])
            dmc = float(request.form['DMC'])
            isi = float(request.form['ISI'])
            classes = int(request.form['Classes'])
            
            # classes can be ignored if not used for prediction

            # Prepare DataFrame for prediction (excluding 'Classes')
            input_data = pd.DataFrame([[temp, rh, ws, rain, ffmc, dmc, isi,classes]],
                                      columns=['Temperature','RH','Ws','Rain','FFMC','DMC','ISI','Classes'])

            # Scale input data
            scaled_data = standard_scaler.transform(input_data)

            # Predict
            prediction = ridge_model.predict(scaled_data)

            return render_template('home.html', results=round(prediction[0], 2))

        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)