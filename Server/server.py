from flask import Flask, request
from flask_cors import CORS
from pynput.mouse import Button, Controller

mouse_c = Controller()

app = Flask(__name__)
CORS(app)


@app.route('/mouse', methods=['POST'])
def mouse():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    mouse_c.move(x*10, y* -10)
    print(x)
    
    # Puoi aggiungere ulteriore elaborazione qui
    return 'Dati ricevuti correttamente', 200

@app.route('/mouse_click', methods=['POST'])
def click_funct():
    
    print('CLICK')
    mouse_c.click(Button.left, 1)
    
    return 'Dati ricevuti correttamente', 200

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.44',ssl_context=('/home/HoloOS/GUI_TK/Server/cert.pem', '/home/HoloOS/GUI_TK/Server/key.pem'))



