# Aspire App

## Introduction

Aspire App is a Flask-based web application designed to provide various functionalities such as user registration, authentication, file upload, user profile management, text analysis, and more.

[Watch the App Demonstration [aspire-demo.webm](..%2F..%2FVideos%2FScreencasts%2Faspire-demo.webm)Video](https://www.youtube.com/watch?v=your_video_id)

## Features

- User registration and login
- Token-based authentication
- File upload and management (supports image, video, and PDF)
- Text analysis using TextBlob
- User profile management (including updating email and password)
- Access control based on user roles
- Secure storage of files using MongoDB GridFS

## Installation

1. Clone the repository:

git clone https://github.com/your-username/aspire-app.git

2. Navigate to the project directory:
- cd aspire-app


4. Set up the MongoDB database:

- Install MongoDB and start the MongoDB service.
- Create a new database named `aspireit`.

## Configuration

To connect the app with your MongoDB configuration, update the `dbConn.py` file with your personal MongoDB connection details.

## Usage

1. Start the Flask server:
- python run.py



2. Access the application in your web browser at `http://localhost:5000`.

## API Endpoints

### User Registration and Authentication

- **POST /register**: Register a new user.
- **POST /login**: Authenticate and log in a user.

### File Upload and Management

- **POST /upload/image**: Upload an image file.
- **POST /upload/video**: Upload a video file.
- **POST /upload/pdf**: Upload a PDF file.
- **GET /file/:file_type**: Retrieve a file by type (image, video, or PDF).

### Text Analysis

- **POST /analyze/text**: Analyze text using TextBlob.

### User Profile Management

- **GET /user/profile**: Get the user's profile information.
- **PUT /user/profile**: Update the user's profile information (email and password).

## Authentication and Authorization

- User authentication is implemented using JWT (JSON Web Tokens).
- Token-based authentication is required for accessing protected routes.
- Certain routes are protected and require a valid JWT token in the request headers.

## File Storage

- Files uploaded by users are stored securely using MongoDB's GridFS.
- GridFS is used for storing large files that exceed the BSON document size limit.
- Each file is associated with the user who uploaded it.

## Contributing

Contributions to the Aspire App are welcome! To contribute:

## License

This project is licensed under the [MIT License](LICENSE).



