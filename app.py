import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACcf7425cafe5073ff98f5c5882eb0aba8'
    TWILIO_SYNC_SERVICE_SID = 'ISc672c6afeb771b4039a25d126c5317c1'
    TWILIO_API_KEY = 'SKfc2789184b6690b284750aa81e20a22e'
    TWILIO_API_SECRET = 'ZIungIY1TLMRpj1wSXyiWpFXaUsVNOnV'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    dataFromArea = request.form['text']

    with open('file.txt', 'w') as x:
        x.write(dataFromArea)

    WorkFile = 'file.txt'

    return send_file(WorkFile, as_attachment=True)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5001', debug=True)
