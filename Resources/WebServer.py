from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/PixelData', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':

        data = open("Resources/PixelData/BadApple.txt",'r').read()
        print("SENT")
        #print("SENT >>", data)
        return data

    print("RECEIVED >>",list(request.form))
    return render_template('index.html')

app.run(host='0.0.0.0',port='1111',debug=False)