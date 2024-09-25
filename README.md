# Delegated Logon Connector

## Description

This project is a Flask-based web application designed to handle delegated logon requests for the Minddistrict platform using the Delegated Logon (DLO) mechanism. It generates a URL for user authentication based on the specified user type and redirects the user to the Minddistrict platform.

## Features

- Handles user logon requests and redirects users to the Minddistrict platform.
- Generates a secure token using HMAC SHA-512.
- Validates user type and handles errors gracefully.
- Configurable user IDs and shared secret using environment variables.

## Requirements

- Python 3.6 or higher
- Flask
- python-dotenv

## Setup

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

### 2. Create and Activate a Virtual Environment:

#### On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
#### After activating the virtual environment, install the required Python packages using:
```bash
pip install -r requirements.txt
```

### 4. Create a .env File
#### Create a .env file in the root directory of the project and add the following environment variables:

```env
CAREPROVIDER_ID=your_careprovider_id
CLIENT_ID=your_client_id
SHARED_SECRET=your_shared_secret
```

### 5. Run the Application
#### Once the environment is set up and the dependencies are installed, run the Flask application:
```bash
python connector.py
```

The application will be accessible at http://127.0.0.1:5000.


## Running Tests

#### Automated tests are included to ensure code quality and correct behavior of the application. To run the unit tests:

#### Run the following command:
```bash
python -m unittest discover
```
