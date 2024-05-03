from flask import Flask, render_template, request
import base64
from mods.model import Movie as ModelUser  # 匯入資料模型
from mods.model import db  # 匯入資料庫實例
from sqlalchemy import and_, or_, func

app = Flask(__name__)  # 創建 Flask 應用
app.config["DEBUG"] = True  # 啟用偵錯模式

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:passwd@ip/test'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/' ,  methods=['GET'])
def index():
    data = movie_data()
    return render_template('index.html',data=data )
def movie_data():
    rows = ModelUser.query.all()

    data = [{
        "電影名" : row.電影名,
        "海報" : base64.b64encode(row.海報).decode("utf-8"),
        "類型" : row.類型,
        "片長" : row.片長,
        "制片國家" : row.制片國家,
        "語言" : row.語言,
        "上映日期" : row.上映日期,
        "別名" : row.別名,
        "IMDb編號" : row.IMDb編號,
        "鏈接" : row.鏈接,


    } for row in rows]
    return data




if __name__ == '__main__':
    # 啟動 Flask 應用
    app.run(host='0.0.0.0', port=5004, debug=True)
