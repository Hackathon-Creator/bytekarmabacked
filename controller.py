from flask import Flask, request, jsonify
from flask_cors import CORS
import service

app = Flask(__name__)
CORS(app)
@app.route('/upload',methods = ['POST','GET'])
def upload():
    
    f = request.files['file']
    df = service.process(f)
    
    if type(df).__name__ == 'DataFrame':
        return df.to_json(orient='records')
    elif type(df).__name__ == 'str':
        return jsonify(errorMessage = df)
    
@app.route('/searchcif/<cif>',methods = ['POST','GET'])
def searchByCif(cif):
   df = service.searchCif(cif)
   
   if type(df).__name__ == 'DataFrame':
        return df.to_json(orient='records')
   else:
       if df == 'error 1':
           return jsonify( errorMessage = 'error in connection')
       elif df == 'error 2':
           return jsonify( errorMessage = 'error in search')
   
@app.route('/home',methods = ['POST','GET'])
def home():
   result = service.home()
   
   if result[0:4] != 'error':
       resultList = result.split(',')
       return jsonify(searchResult = resultList)
   else:
       if result == 'error 1':
           return jsonify( errorMessage = 'error in connection')
       elif result == 'error 2':
           return jsonify( errorMessage = 'error in search')
    

if __name__ == '__main__':
    app.run(debug=False)
    
    
#curl -i -X POST -F "file=@C:\Users\Deval\Desktop\HACKATHON\POC\test1.xlsx" http://127.0.0.1:5000/upload