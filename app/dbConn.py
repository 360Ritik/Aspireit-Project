from flask_pymongo import PyMongo


from run import app

app.config["MONGO_URI"] = "mongodb+srv://USERNAME:PASSWORD@cluster0.e1pgcys.mongodb.net/DATABASE-NAME?retryWrites=true&w=majority&appName=Cluster0"
db = PyMongo(app).db


