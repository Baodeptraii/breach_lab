# server.py
from flask import Flask, request, make_response
import gzip
import io
import random

app = Flask(__name__)

# SECRET_TOKEN = ''.join(random.choices('1234567890abcdef', k=32))
SECRET_TOKEN = '1234abcd'

@app.route('/poc/')
def poc():
    user_input = request.args.get('request_token', '')
    content = f"Welcome!\nYour request token is: {SECRET_TOKEN}\nYou submitted: {user_input}"
    
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(content.encode())

    response = make_response(buf.getvalue())
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = str(len(response.data))
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == '__main__':
    print("SECRET TOKEN:", SECRET_TOKEN)
    app.run(host='0.0.0.0', port=5000)
