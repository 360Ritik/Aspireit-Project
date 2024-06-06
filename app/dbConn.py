from flask_pymongo import PyMongo


from run import app

app.config["MONGO_URI"] = "mongodb+srv://Ritik360:ritik810@cluster0.e1pgcys.mongodb.net/aspireit?retryWrites=true&w=majority&appName=Cluster0"
db = PyMongo(app).db


