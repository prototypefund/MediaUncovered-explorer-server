import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from newsAnalysis.Model import Model


def create_app(model_path=None):
    app = Flask(__name__)
    CORS(app)

    if model_path is None:
        model_path = os.path.abspath("./models/model")

    app.model = Model(name="model", modelType="fasttext", model_path=model_path)
    app.model.load()

    @app.route('/query/<string:word>')
    def query(word):
        count = int(request.args.get('count', 10))

        similarWords = app.model.word_embedding.wv.similar_by_word(word, topn=count)
        body = [{"label": result[0], "value": result[1]} for result in similarWords]

        return jsonify(body)

    return app
