from flask import Flask, jsonify,render_template,request,make_response
import pickle
import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import mfcc
from flask_cors import CORS,cross_origin
import base64


loaded_model = pickle.load(open("model2.pkl", "rb"))



def mean_matrix_extractor(path):
            (rate, sig) = wav.read(path)
            mfcc_feat = mfcc(sig, rate, winlen = 0.020, appendEnergy=False)
            mean_matrix = mfcc_feat.mean(0)
            return mean_matrix

def extract(path):
  f1=mean_matrix_extractor(path)
  f=f1.reshape(1,-1)
  return f


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route("/hello", methods=["GET"])
def say_hello():
    return jsonify({"msg": "Hello from Flask"})

@app.route('/',methods=['GET'])
def home():
    return render_template("index.html")



@app.route('/',methods=['POST'])
def prediction():
    audiofile= request.files['audioFile']
    audioPath="./audio/" + audiofile.filename
    audiofile.save(audioPath)
    f=extract(audioPath)
    predictionValue = loaded_model.predict(f)[0]

    return render_template("index.html",prediction=predictionValue)





@app.route('/music', methods=['POST'])
def predict64():
    d={"1":"reggae",
"2":"metal",
"3":"country",
"4":"hiphop",
"5":"pop",
"6":"disco",
"7":"jazz",
"8":"blues",
"9":"rock",
"10":"classical"}
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        wav_file = open("temp.wav", "wb")
        b64_string=json["music"]
        extra="data:audio/wav;base64,"
        music64=json["music"]
        music64=music64[len(extra):]        
        decode_string = base64.b64decode(music64)
        wav_file.write(decode_string)
        f=extract("./temp.wav")
        predictionValue = loaded_model.predict(f)[0]
        app.logger.info(d[str(predictionValue)])
        #d={}
        #d["music genre"]=str(predictionValue)
        response = make_response(d[str(predictionValue)], 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.mimetype = "text/plain"
        return response
    else:
        return 'Content-Type not supported!'

# @app.route('/postjson', methods=['POST'])
# def process_json():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.get_json()
#         wav_file = open("temp.wav", "wb")
#         decode_string = "gtg"
#         extra="data:audio/wav;base64,"
#         music64=json["music"]
#         music64=music64[len(extra):]
#         #base64.b64decode(json["music"])
#         #wav_file.write(decode_string)
#         # f=extract("./temp.wav")
#         # predictionValue = loaded_model.predict(f)[0]
#         app.logger.info(music64)
#         response = make_response(music64, 200)
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.mimetype = "text/plain"
#         return response
#     else:
#         app.logger.info('wrong')
#         return 'Content-Type not supported!'


if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)