# app/routes.py
import os

import gridfs
import io
from bcrypt import hashpw, gensalt
from bson import ObjectId
from flask import request, jsonify, make_response, g, send_file
import json
from werkzeug.utils import secure_filename

from textblob import TextBlob

from app import app, db, bcrypt
from app.models import user_schema
from app.authentication import token_required
import jwt
import datetime

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'jpg', 'jpeg', 'png', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

fs = gridfs.GridFS(db)


@app.route("/upload/<file_type>", methods=["POST"])
@token_required
def upload_file(current_user, file_type):
    try:
        content_type = {
            "pdf": "application/pdf",
            "video": "video/mp4",
            "image": "image/jpeg"
        }.get(file_type)

        if not content_type:
            return jsonify({"message": f"Invalid file type: {file_type}"}), 400

        # Check if a file of the same type already exists for the user
        existing_file = fs.find_one({'contentType': content_type, 'user_id': current_user['_id']})
        if existing_file:
            # Delete the existing file
            fs.delete(existing_file._id)

        # Save the new file
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_id = fs.put(file, contentType=content_type, filename=filename, user_id=current_user['_id'])

        return jsonify({"message": f"File uploaded successfully", "file_id": str(file_id)}), 201
    except Exception as e:
        return jsonify({"message": "Failed to upload file"}), 500


@app.route("/file/<file_type>", methods=["GET"])
@token_required
def get_file(current_user, file_type):
    try:
        content_type = {
            "pdf": "application/pdf",
            "video": "video/mp4",
            "image": "image/jpeg"
        }.get(file_type)

        if not content_type:
            return jsonify({"message": f"Invalid file type: {file_type}"}), 400

        # Get the file based on the content type and user ID
        file = fs.find_one({'contentType': content_type, 'user_id': current_user['_id']})
        if not file:
            return jsonify({"message": f"No {file_type} file found for the current user"}), 404

        # Construct the response based on the file type
        response = send_file(io.BytesIO(file.read()), mimetype=file.contentType)
        response.headers["Content-Disposition"] = f"attachment; filename={file.filename}"
        return response
    except Exception as e:
        return jsonify({"message": "File not found"}), 404


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    existing_user = db.users.find_one({"username": data["username"]})
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    # Hash the password
    hashed_password = hashpw(data['password'].encode('utf-8'), gensalt())
    data['password'] = hashed_password.decode('utf-8')

    result = db.users.insert_one(data)
    if result.inserted_id:
        return jsonify({"message": "User registered successfully", "user_id": str(result.inserted_id)}), 201
    else:
        return jsonify({"message": "Failed to register user"}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    user = db.users.find_one({"username": data["username"]})
    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    token = jwt.encode({
        "username": user["username"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    # Convert token to string
    token_str = token.decode('utf-8')

    return jsonify({"token": token_str})


@app.route("/analyze/text", methods=["POST"])
@token_required
def analyze_text(current_user):
    if request.method == 'POST':
        try:
            data = request.get_json()
            text = data.get('text', '')

            if not text:
                return jsonify({'error': 'No text provided'}), 400

            # Analyze the text using TextBlob
            blob = TextBlob(text)
            sentiment = blob.sentiment

            # Construct the response data
            response_data = {
                'text': text,
                'polarity': sentiment.polarity,
                'subjectivity': sentiment.subjectivity,
                'note': {
                    'polarity': 'Polarity measures how positive or negative the text is.',
                    'subjectivity': 'Subjectivity measures how subjective or objective the text is.'
                }
            }

            return jsonify(response_data), 200
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON'}), 400
    else:
        return jsonify({'error': 'Invalid HTTP method'}), 405


@app.route("/user/profile", methods=["GET"])
@token_required
def get_user_profile(current_user):
    # Accessing username from current_user
    username = current_user["username"]
    user = db.users.find_one({"username": username})

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Construct the response data
    user_profile = {
        "username": user["username"],
        "email": user.get("email"),
        "image_url": user.get("image_url"),
        # Add more fields as needed
    }

    return jsonify({"user_profile": user_profile}), 200


@app.route("/user/profile", methods=["PUT"])
@token_required
def update_user_profile(current_user):
    # Accessing username from current_user
    username = current_user["username"]
    user = db.users.find_one({"username": username})

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    updated_fields = {}

    # Update fields based on the provided data
    if "email" in data:
        updated_fields["email"] = data["email"]
    if "password" in data:
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        updated_fields["password"] = hashed_password

    if updated_fields:
        db.users.update_one({"username": username}, {"$set": updated_fields})

    return jsonify({"message": "User profile updated successfully"}), 200
