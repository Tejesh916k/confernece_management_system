from flask import Blueprint, render_template, jsonify, session, redirect, url_for, request
from functools import wraps
from datetime import datetime
from models.MongoConference import MongoConference
from models.MongoSession import MongoSession
from models.MongoAttendee import MongoAttendee
import uuid

main_bp = Blueprint('main', __name__)

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    """Home page - redirect to login if not authenticated, else to dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.dashboard'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html', username=session.get('username'))

@main_bp.route('/conferences')
@login_required
def conferences():
    """Conferences list page"""
    return render_template('conferences.html')

@main_bp.route('/sessions')
@login_required
def sessions():
    """Sessions list page"""
    return render_template('sessions.html')

@main_bp.route('/attendees')
@login_required
def attendees():
    """Attendees list page"""
    return render_template('attendees.html')

@main_bp.route('/api/create-conference', methods=['POST'])
@login_required
def create_conference():
    """Create a new conference"""
    try:
        data = request.get_json()
        
        # Parse dates from form (format: YYYY-MM-DD)
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')
        
        # Create new conference
        conference = MongoConference(
            name=data.get('name'),
            field=data.get('field'),
            location=data.get('location'),
            start_date=start_date,
            end_date=end_date,
            organizer_id=session.get('user_id'),
            description=f"Conference: {data.get('name')} in {data.get('location')}",
            status='upcoming'
        )
        
        conference.save()
        
        return jsonify({
            'success': True,
            'message': f"Conference '{data.get('name')}' created successfully",
            'conference_id': conference.id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@main_bp.route('/api/create-session', methods=['POST'])
@login_required
def create_session():
    """Create a new session"""
    try:
        data = request.get_json()
        
        # Parse times from form (format: HH:MM)
        start_time = datetime.strptime(data.get('start_time'), '%H:%M')
        end_time = datetime.strptime(data.get('end_time'), '%H:%M')
        
        # Create new session
        session_obj = MongoSession(
            id=str(uuid.uuid4()),
            title=data.get('title'),
            speaker=data.get('speaker'),
            location=data.get('location'),
            start_time=start_time,
            end_time=end_time,
            capacity=int(data.get('capacity', 50)),
            description=f"Session: {data.get('title')} with {data.get('speaker')}",
            conference_id=data.get('conference_id', 'general')
        )
        
        session_obj.save()
        
        return jsonify({
            'success': True,
            'message': f"Session '{data.get('title')}' added successfully",
            'session_id': session_obj.id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@main_bp.route('/api/register-attendee', methods=['POST'])
@login_required
def register_attendee():
    """Register a new attendee"""
    try:
        data = request.get_json()
        
        # Check if attendee already exists
        existing = MongoAttendee.objects(email=data.get('email')).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Attendee with this email already registered'
            }), 400
        
        # Create new attendee
        attendee = MongoAttendee(
            id=str(uuid.uuid4()),
            name=data.get('full_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            company=data.get('company')
        )
        
        attendee.save()
        
        return jsonify({
            'success': True,
            'message': f"{data.get('full_name')} has been registered successfully",
            'attendee_id': attendee.id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running'
    }), 200
