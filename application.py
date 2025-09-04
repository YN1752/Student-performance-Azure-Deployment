from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.logger import logging

application = Flask(__name__)
app = application

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('index.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))
        )

        pred_df=data.get_data_as_data_frame()

        predict_pipeline=PredictPipeline()
        results= round(predict_pipeline.predict(pred_df)[0])

        if results < 0:
            results = 0
        elif results > 100:
            results = 100

        data_dict = pred_df.to_dict(orient='list')

        return render_template('results.html', data_dict=data_dict, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)