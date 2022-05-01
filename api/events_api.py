from flask import Blueprint, jsonify, request

from data.db_session import create_session
from data.__all_models import Event

blueprint = Blueprint(
    'events_api',
    __name__,
    template_folder='templates',
    static_folder='static')


@blueprint.route('/api/events')
def get_events():
    db_sess = create_session()
    event = db_sess.query(Event).all()
    return jsonify(
        {
            'event':
                [item.to_dict(only=('title', 'description', 'img'))
                 for item in event]
        }
    )


@blueprint.route('/api/events/<int:event_id>')
def get_one_event(event_id):
    db_sess = create_session()
    event = db_sess.query(Event).get(event_id)
    if not event:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'event': event.to_dict(only=('name', 'surname', 'email'))
        }
    )


@blueprint.route('/api/events', methods=['POST'])
def create_event():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'description', 'img']):
        return jsonify({'error': 'Bad request'})
    db_sess = create_session()
    event = Event()
    event.title = request.json['title']
    event.description = request.json['description']
    event.img = request.json['img']
    db_sess.add(event)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    db_sess = create_session()
    event = db_sess.query(Event).get(event_id)
    if not event:
        return jsonify({'error': 'Not found'})
    db_sess.delete(event)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/events/<int:event_id>', methods=['PUT'])
def edit_event(event_id):
    db_sess = create_session()
    event = db_sess.query(Event).get(event_id)
    if not event:
        return jsonify({'error': 'Not found'})
    if not any(key in request.json for key in
               ['title', 'description', 'img']):
        return jsonify({'error': 'Bad request'})
    event.title = request.json.get('title', event.title)
    event.description = request.json.get('description', event.description)
    event.img = request.json.get('img', event.img)
    db_sess.commit()
    return jsonify({'success': 'OK'})
