import serial
from time import sleep
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

class LerPorta(Resource):
    def get(self):
        ser = serial.Serial(
            port='COM3',\
            baudrate=9600,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
                timeout=0)

        print("connected to: " + ser.portstr)

        cw = [0x05]

        ser.write(serial.to_bytes(cw))
        sleep(1)
        peso = ser.readline()
        s1=slice(1,6)
        pesoleft = peso[s1]
        encoding = 'utf-8'
        strPeso = str(pesoleft, encoding)
        result =  "{'" + "Peso" + "':'" + strPeso + "'}"
        print(result)
        ser.close()
        return result

api.add_resource(LerPorta, '/LerPorta') 

if __name__ == '__main__':
     app.run(port='5002')