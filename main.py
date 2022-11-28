import serial
from time import sleep
from flask import Flask
from flask_restful import Resource, Api, request
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
api = Api(app)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

class Config(Resource):
    def post(self):
        parser = request.get_json()
        jsonStr = json.dumps(parser, indent=4, sort_keys=True)
        parsed_json = json.loads(jsonStr)
        conn = sqlite3.connect("balanca.db")
        conn.execute("""DELETE FROM PortConfig;""")
        conn.commit()
        Port = parsed_json["Port"]
        BaudRate = str(parsed_json["BaudRate"])
        Parity = parsed_json["Parity"] 
        StopBits = parsed_json["StopBits"] 
        ByteSize = parsed_json["ByteSize"]
        Timeout = str(parsed_json["Timeout"])
        queryInsert = "INSERT INTO PortConfig ('Port','BaudRate', 'Parity', 'StopBits', 'ByteSyze', 'Timeout') VALUES ('" + Port + "','" + BaudRate + "','" + Parity + "','" + StopBits + "','" + ByteSize + "','" + Timeout + "');"
        conn.execute(queryInsert)
        conn.commit()
        return "{'" + "Message" + "':'" + "Sucesso" + "'}"


class LerPorta(Resource):
    def get(self):
        conn = sqlite3.connect("balanca.db")
        connect = conn.cursor()
        connect.execute("""SELECT * FROM PortConfig;""")
        records = connect.fetchall()

        ser = serial.Serial(
            port=records[0][0],\
            baudrate=records[0][1],\
            parity=eval(f"serial.{records[0][2]}"),\
            stopbits=eval(f"serial.{records[0][3]}"),\
            bytesize=eval(f"serial.{records[0][4]}"),\
                timeout=records[0][5])

        print("connected to: " + ser.portstr)

        total_de_tentativas = 180

        while (total_de_tentativas > 0):

            cw = [0x05]

            ser.write(serial.to_bytes(cw))
            sleep(1)
            peso = ser.readline()
            s1=slice(1,6)
            pesoleft = peso[s1]
            encoding = 'utf-8'
            strPeso = str(pesoleft, encoding)
            if strPeso:
                total_de_tentativas = 0 
            else:
                total_de_tentativas = total_de_tentativas - 1
                
            
        result =  "{'" + "Peso" + "':'" + strPeso + "'}"
        print(result)
        ser.close()
        return result

api.add_resource(LerPorta, '/LerPorta') 
api.add_resource(Config, '/Config')

if __name__ == '__main__':
     app.run(port='5002')