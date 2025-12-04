from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.MongoSession import MongoSession
from models.MongoConference import MongoConference
from datetime import datetime
import uuid

session_bp = Blueprint('session', __name__, url_prefix='/sessions')

# CREATE SESSION
@session_bp.route('/create', methods=['GET', 'POST'])
def create_session():
    """Create a new session"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['conference_id', 'title', 'speaker', 'start_time', 'end_time', 'location']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Verify conference exists
            conference = MongoConference.objects(id=data['conference_id']).first()
            if not conference:
                return jsonify({'error': 'Conference not found'}), 404
            
            # Verify user is organizer
            if conference.organizer_id != session['user_id']:
                return jsonify({'error': 'Unauthorized'}), 403
            
            # Create session
            new_session = MongoSession(
                id=str(uuid.uuid4()),
                title=data['title'],
                description=data.get('description', ''),
                speaker=data['speaker'],
                start_time=datetime.fromisoformat(data['start_time']),
                end_time=datetime.fromisoformat(data['end_time']),
                location=data['location'],
                capacity=int(data.get('capacity', 50)),
                conference_id=data['conference_id']
            )
            new_session.save()
            
            print(f"[OK] Session created: {data['title']}")
            
            return jsonify({
                'success': True,
                'message': 'Session created successfully',
                'session_id': new_session.id,
                'redirect': f'/sessions/{new_session.id}'
            }), 201
            
        except Exception as e:
            print(f"Session creation error: {str(e)}")
            return jsonify({'error': f'Failed to create session: {str(e)}'}), 500
    
    return render_template('sessions/create_session.html')

# LIST SESSIONS FOR CONFERENCE
@session_bp.route('/conference/<conference_id>', methods=['GET'])
def list_sessions(conference_id):
    """List all sessions for a conference"""
    try:
        sessions = MongoSession.objects(conference_id=conference_id).order_by('start_time')
        session_list = [s.to_dict() for s in sessions]
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'sessions': session_list}), 200
        
        return render_template('sessions/list_sessions.html', sessions=session_list, conference_id=conference_id)
    except Exception as e:
        print(f"Error listing sessions: {str(e)}")
        return jsonify({'error': 'Failed to fetch sessions'}), 500

# VIEW SESSION DETAILS
@session_bp.route('/<session_id>', methods=['GET'])
def view_session(session_id):
    """View session details"""
    try:
        sess = MongoSession.objects(id=session_id).first()
        if not sess:
            return jsonify({'error': 'Session not found'}), 404
        
        return render_template('sessions/view_session.html', session=sess.to_dict())
    except Exception as e:
        print(f"Error viewing session: {str(e)}")
        return jsonify({'error': 'Failed to fetch session'}), 500

# EDIT SESSION
@session_bp.route('/<session_id>/edit', methods=['GET', 'POST'])
def edit_session(session_id):
    """Edit session details"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        sess = MongoSession.objects(id=session_id).first()
        if not sess:
            return jsonify({'error': 'Session not found'}), 404
        
        # Verify authorization
        conference = MongoConference.objects(id=sess.conference_id).first()
        if not conference or conference.organizer_id != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        if request.method == 'POST':
            data = request.get_json()
            
            sess.title = data.get('title', sess.title)
            sess.description = data.get('description', sess.description)
            sess.speaker = data.get('speaker', sess.speaker)
            sess.location = data.get('location', sess.location)
            sess.capacity = int(data.get('capacity', sess.capacity))
            sess.start_time = datetime.fromisoformat(data['start_time'])
            sess.end_time = datetime.fromisoformat(data['end_time'])
            sess.updated_at = datetime.utcnow()
            sess.save()
            
            print(f"[OK] Session updated: {sess.title}")
            
            return jsonify({'success': True, 'message': 'Session updated'}), 200
        
        return render_template('sessions/edit_session.html', session=sess.to_dict())
    
    except Exception as e:
        print(f"Error editing session: {str(e)}")
        return jsonify({'error': 'Failed to update session'}), 500

# DELETE SESSION
@session_bp.route('/<session_id>/delete', methods=['POST'])
def delete_session(session_id):
    """Delete a session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        sess = MongoSession.objects(id=session_id).first()
        if not sess:
            return jsonify({'error': 'Session not found'}), 404
        
        # Verify authorization
        conference = MongoConference.objects(id=sess.conference_id).first()
        if not conference or conference.organizer_id != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        session_title = sess.title
        sess.delete()
        
        print(f"[OK] Session deleted: {session_title}")
        
        return jsonify({'success': True, 'message': 'Session deleted'}), 200
    
    except Exception as e:
        print(f"Error deleting session: {str(e)}")
        return jsonify({'error': 'Failed to delete session'}), 500

# REGISTER FOR SESSION
@session_bp.route('/<session_id>/register', methods=['POST'])
def register_session(session_id):
    """Register user for a session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        sess = MongoSession.objects(id=session_id).first()
        if not sess:
            return jsonify({'error': 'Session not found'}), 404
        
        user_id = session['user_id']
        
        # Check if already registered
        if user_id in sess.attendees:
            return jsonify({'error': 'Already registered for this session'}), 409
        
        # Check if session is full
        if len(sess.attendees) >= sess.capacity:
            return jsonify({'error': 'Session is full'}), 400
        
        sess.attendees.append(user_id)
        sess.save()
        
        print(f"[OK] User registered for session: {sess.title}")
        
        return jsonify({'success': True, 'message': 'Registered for session'}), 200
    
    except Exception as e:
        print(f"Error registering: {str(e)}")
        return jsonify({'error': 'Failed to register'}), 500

# UNREGISTER FROM SESSION
@session_bp.route('/<session_id>/unregister', methods=['POST'])
def unregister_session(session_id):
    """Unregister user from a session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        sess = MongoSession.objects(id=session_id).first()
        if not sess:
            return jsonify({'error': 'Session not found'}), 404
        
        user_id = session['user_id']
        
        if user_id not in sess.attendees:
            return jsonify({'error': 'Not registered for this session'}), 400
        
        sess.attendees.remove(user_id)
        sess.save()
        
        print(f"[OK] User unregistered from session: {sess.title}")
        
        return jsonify({'success': True, 'message': 'Unregistered from session'}), 200
    
    except Exception as e:
        print(f"Error unregistering: {str(e)}")
        return jsonify({'error': 'Failed to unregister'}), 500
