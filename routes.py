from flask import Flask, request, render_template, send_file, json, jsonify
from app.api import Api
from fastai.structured import *


app = Flask(__name__)

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    file_path = (os.path.abspath("node_modules/" + subpath))
    return send_file(file_path)

@app.route('/models', methods=["POST"])
def get_models():
    data = request.get_json() or request.values
    print ("DATA: ",data)
    api = Api()
    api.load_data()
    models = api.get_models(data["brand"])
    print(models)
    resp = jsonify(models)
    resp.status_code = 200

    return resp


@app.route('/predict', methods=["POST"])
def get_prediction():
    data = request.get_json() or request.values
    api = Api()
    df_raw = api.load_data()
    prediction = api.predict(df_raw, data)

    resp = jsonify(prediction)
    resp.status_code = 200

    return resp


@app.route('/')
def index():
    api = Api()
    df_raw = api.load_categorized_data()

    df_raw, manufacturers, now, models, fuels, volumes = api.get_options(df_raw)

    return render_template(
        'index.html',
        df=df_raw,
        manufacturers=manufacturers,
        now=now,
        models=models,
        fuels=fuels,
        volumes=volumes
    )

if __name__ == '__main__':
    app.run(debug=True)
