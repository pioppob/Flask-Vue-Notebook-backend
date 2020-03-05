from flask import Flask, request, jsonify
import sqlalchemy as sa
from datetime import datetime 
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
DATABASE_URI = os.environ.get('DATABASE_URI')

@app.route('/')
def index():
    return 'Hello!'

@app.route('/api/entry', methods=['GET', 'POST'])
def entry_list():

    if request.method == 'GET':
        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entries = conn.execute(
            'SELECT * FROM learning_logs_entry ORDER BY date_added DESC'
        )

        return jsonify({ 'entries': [dict(row) for row in entries.fetchall()] })


    elif request.method == 'POST':
        data = request.get_json()
        topic_id = data['topic_id']
        text = data['text']
        date_added = datetime.now().strftime('%a, %b %m %Y %H:%M:%S GMT')

        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entry = conn.execute(
            f"INSERT INTO learning_logs_entry (date_added, text, topic_id) VALUES ('{date_added}', '{text}', '{topic_id}');"
        )
        response = conn.execute(
            'SELECT * FROM learning_logs_entry ORDER BY date_added DESC LIMIT 1'
        )
        return jsonify({'entries': [dict(row) for row in response.fetchall()]})


@app.route('/api/entry/<entry_id>', methods=['GET', 'PUT', 'DELETE'])
def single_entry(entry_id):

    if request.method == 'GET':
        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entry = conn.execute(
            f'SELECT * FROM learning_logs_entry WHERE id = {entry_id};'
        )
        return jsonify({ 'entries': [dict(row) for row in entry.fetchall()] })

    if request.method == 'PUT':
        data = request.get_json()
        text = data['text']
        text = text.replace("\'", "\'\'")

        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entry = conn.execute(
            f"UPDATE learning_logs_entry SET text = '{text}' WHERE id = {entry_id};"
        )
        return f'Entry updated successfully!'

    if request.method == 'DELETE':
        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entry = conn.execute(
            f'DELETE FROM learning_logs_entry WHERE id = {entry_id};'
        )
        return f'Entry deleted successfully!'


@app.route('/api/topic', methods=['GET', 'POST'])
def topic_list():

    if request.method == 'GET':
        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        topics = conn.execute(
            'SELECT * FROM learning_logs_topic WHERE owner_id = 2;'
        )
        return jsonify({ 'topics': [dict(row) for row in topics.fetchall()] })
        

    elif request.method == 'POST':
        data = request.get_json()
        owner_id = data['owner_id']
        text = data['text']
        date_added = datetime.utcnow().strftime('%a, %b %m %Y %H:%M:%S GMT')

        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        topics = conn.execute(
            f"INSERT INTO learning_logs_topic (date_added, owner_id, text) VALUES ('{date_added}', '{owner_id}', '{text}');"
        )
        return f'New topic added successfully!'

    
@app.route('/api/topic/<topic_id>', methods=['GET', 'PUT', 'DELETE'])
def single_topic(topic_id):

    if request.method == 'GET':
        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entry = conn.execute(
            f'SELECT * FROM learning_logs_topic WHERE id = {topic_id};'
        )
        return jsonify({ 'entries': [dict(row) for row in entry.fetchall()] })

    if request.method == 'PUT':
        data = request.get_json()
        text = data['text']
        text = text.replace("\'", "\'\'")
        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entry = conn.execute(
            f"UPDATE learning_logs_topic SET text = '{text}' WHERE id = {topic_id};"
        )
        return f'Topic updated successfully!'

    if request.method == 'DELETE':
        engine = sa.create_engine(DATABASE_URI)
        conn = engine.connect()
        entry = conn.execute(
            f'DELETE FROM learning_logs_topic WHERE id = {topic_id};'
        )
        return f'Topic deleted successfully!'

