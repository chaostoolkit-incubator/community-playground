from flask import Flask
from flask import abort
from flask import jsonify, request, render_template
import json

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Flask inside Docker!!"

@app.route("/")
def index():
     #return render_template("index.html")
     return render_template('index.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


@app.route("/dummy")
def dummy():
     #return render_template("index.html")
     return render_template('dummydata.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


@app.route('/menu/api/v1.0/menus', methods=['GET'])
def get_menus():
    with app.open_resource('data.json') as f:
        data = json.load(f)
        return jsonify(data)


@app.route('/menu/api/v1.0/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    with app.open_resource('data.json') as f:
        data = json.load(f)
        # print (data)
        print (data['data'])
        # print (data['data']['1'])
        menu_item = [menu_item for menu_item in data['data'] if menu_item['id'] == item_id]
        if len(menu_item) == 0:
            abort(404)
        return jsonify(menu_item)
        #return jsonify({'task': menu_item[0]})


@app.route("/health")
def health():
    return "", 200


@app.route("/live")
def live():
    return "", 200

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
