from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize CORS and Migrate with the app
CORS(app)
migrate = Migrate(app, db)

# Initialize the database with the app
db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    # Fetch all messages from the database ordered by 'created_at' in ascending order
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:message_id>', methods=['PATCH'])
def update_message(message_id):
    data = request.get_json()
    message = Message.query.get(message_id)
    if message:
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict()), 200
    else:
        return jsonify({'error': 'Message not found'}), 404


@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted'}), 200
    else:
        return jsonify({'error': 'Message not found'}), 404
        

if __name__ == '__main__':
    # Run the app on port 5555
    app.run(port=5555)


