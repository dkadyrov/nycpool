from flask import Flask
from flask import render_template
from database import Database, Pool

app = Flask(__name__)

db = Database("pools.db")

@app.route("/")
def home():
    pools = db.session.query(Pool).order_by(Pool.name).all()

    return render_template('home.html', pools=pools)

@app.route("/<int:pool_id>")
def pool_page(pool_id):
    pool = db.session.get(Pool, pool_id)

    return render_template('pool.html', pool=pool)
