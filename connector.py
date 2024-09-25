import hashlib
import hmac
import os
import uuid

from datetime import datetime
from flask import Flask, redirect, request, Response
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['BASE_URL'] = "https://ca-votriope.minddistrict.dev"
app.config['CAREPROVIDER_ID'] = os.getenv("CAREPROVIDER_ID")
app.config['CLIENT_ID'] = os.getenv("CLIENT_ID")
app.config['SHARED_SECRET'] = os.getenv("SHARED_SECRET")
app.config['CAREPROVIDER_USERTYPE_NAME'] = "careprovider"
app.config['CLIENT_USERTYPE_NAME'] = "client"


def generate_token(nonce, timestamp, userid, usertype):
    """
    Generate HMAC SHA-512 token based on input parameters.
    
    Args:
        nonce (str): Unique identifier.
        timestamp (str): Timestamp in ISO 8601 format.
        userid (str): User identifier.
        usertype (str): Type of user (e.g., 'careprovider').

    Returns:
        str: Generated HMAC SHA-512 token.
    """
    message = f"nonce{nonce}timestamp{timestamp}userid{userid}usertype{usertype}"
    token = hmac.new(
        app.config.get('SHARED_SECRET').encode(),
        message.encode(),
        hashlib.sha512
    ).hexdigest()
    return token


def get_user_id(usertype):
    """
    Return the user ID based on user type.

    Args:
        usertype (str): Type of user (e.g., 'client').

    Returns:
        str: Corresponding user ID.
    """
    careprovider_usertype_name = app.config.get('CAREPROVIDER_USERTYPE_NAME')
    careprovider_id, client_id = app.config.get('CAREPROVIDER_ID'), app.config.get('CLIENT_ID')
    return careprovider_id if usertype == careprovider_usertype_name else client_id


def get_sub_path(usertype):
    """
    Return the sub-path based on user type.

    Args:
        usertype (str): Type of user (e.g., 'client').

    Returns:
        str: Corresponding sub-path.
    """
    return "c" if usertype == app.config.get('CAREPROVIDER_USERTYPE_NAME') else "conversations"


@app.route('/')
def delegatedlogon():
    """
    Handle delegated logon request and redirect to the Minddistrict platform.
    
    Returns:
        Response: Redirects to the generated URL for delegated logon or a 403 error if usertype is invalid.
    """
    usertype = request.args.get('usertype', app.config.get('CAREPROVIDER_USERTYPE_NAME'))
    if usertype not in {app.config.get('CAREPROVIDER_USERTYPE_NAME'), app.config.get('CLIENT_USERTYPE_NAME')}:
        return Response("Given usertype isn't valid.", status=403)

    userid = get_user_id(usertype)
    sub_path = get_sub_path(usertype)
    nonce = uuid.uuid4()  # random (unique with each request) uuid for making url unique

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    encoded_timestamp = quote(timestamp, safe='')

    token = generate_token(nonce, timestamp, userid, usertype)
    dlo_url = (f"{app.config.get('BASE_URL')}/{sub_path}?userid={userid}&"
               f"usertype={usertype}&nonce={nonce}&timestamp={encoded_timestamp}"
               f"&token={token}")

    return redirect(dlo_url)


if __name__ == '__main__':
    app.run(debug=True)
