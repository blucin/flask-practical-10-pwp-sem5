from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app) # Init db
ma = Marshmallow(app) # Init ma
migration = Migrate(app, db) # Init migration

# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

# User Schema (for marshmallow)
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Post handler
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Get handler
@app.route('/user', methods=['GET'])
def get_users():
    id = request.args.get('id')
    if id:
        user = User.query.get(id)
        return user_schema.jsonify(user)
    else:
        return jsonify({'message': 'No user found'})

@app.route('/user/all', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    if all_users:
        result = users_schema.dump(all_users)
        return jsonify(result)
    else:
        return jsonify({'message': 'No users found'})

# Run server
if __name__ == '__main__':
    app.run(debug=True)