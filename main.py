from flask import Flask, request, jsonify
from flask_cors import CORS
from models.user import db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:DavidEbula1999@localhost:3306/taskpro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BCRYPT_LOG_ROUNDS'] = 12

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

from businesslogic import storeUser  # Updated import statement

@app.route('/register', methods=['POST'])
def registration():
    try:
        # Extract information from the request and store user
        user_data = storeUser() 

        return jsonify({'user': user_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
