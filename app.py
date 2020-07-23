from flask import Flask, abort, request
from dotenv import load_dotenv, find_dotenv
import requests, os, re
app = Flask(__name__)

load_dotenv(dotenv_path=".env")
api_key = os.getenv("HACKNEY")
regex = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})"

@app.route('/get_address')
def get_address():
    postcode = request.args.get('postcode')
    if not postcode:
        abort(400)    
    if not validate_postcode(postcode):
        abort(400)
    return get_api_request(postcode)

# Helper functions

def validate_postcode(postcode):
    pattern = re.compile(regex)
    if pattern.fullmatch(postcode):
        return True
    return False

def get_api_request(postcode):
    r = requests.get('https://ndws9fa08d.execute-api.eu-west-2.amazonaws.com/development/api/v1/addresses/', 
        params={"postcode": postcode},
        headers={"x-api-key": api_key}
    )

    print(r.request.headers)
    print(r.status_code)


    return r.json()

def get_static_data(postcode):
    with open("mock.json", "r") as file:
        return file.read()


app.run(debug=True)