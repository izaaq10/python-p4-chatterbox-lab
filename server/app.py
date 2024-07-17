from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from models import db, Message  # Assuming 'Message' is the SQLAlchemy model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.serialize() for message in messages])

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')
    
    if not body or not username:
        return jsonify({'error': 'Missing body or username'}), 400
    
    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.serialize()), 201

# Route to update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    
    body = request.json.get('body')
    if body:
        message.body = body
        message.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(message.serialize())

# Route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'}), 204

if __name__ == '__main__':
    app.run(port=5555)
