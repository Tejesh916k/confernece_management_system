from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.MongoConference import MongoConference
from datetime import datetime
import uuid

conference_bp = Blueprint('conference', __name__, url_prefix='/conferences')

def login_required(f):
    """Check if user is logged in"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@conference_bp.route('/')
@login_required
def list_conferences():
    """List all conferences"""
    try:
        conferences = MongoConference.objects()
        return render_template('conferences.html', conferences=conferences)
    except Exception as e:
        print(f"Error listing conferences: {e}")
        return render_template('conferences.html', conferences=[])

@conference_bp.route('/api/all', methods=['GET'])
@login_required
def get_all_conferences():
    """Get all conferences as JSON"""
    try:
        conferences = MongoConference.objects()
        return jsonify({
            'success': True,
            'data': [conf.to_dict() for conf in conferences],
            'count': conferences.count()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@conference_bp.route('/api/create', methods=['POST'])
@login_required
def create_conference():
    """Create a new conference"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'description', 'location', 'start_date', 'end_date']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if conference name already exists
        if MongoConference.objects(name=data['name']).first():
            return jsonify({'error': 'Conference name already exists'}), 409
        
        # Parse dates
        try:
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except:
            return jsonify({'error': 'Invalid date format'}), 400
        
        # Create conference
        conference = MongoConference(
            id=str(uuid.uuid4()),
            name=data['name'],
            description=data['description'],
            location=data['location'],
            start_date=start_date,
            end_date=end_date
        )
        conference.save()
        
        print(f"✓ Conference created: {data['name']}")
        
        return jsonify({
            'success': True,
            'message': 'Conference created successfully',
            'data': conference.to_dict()
        }), 201
        
    except Exception as e:
        print(f"Create conference error: {e}")
        return jsonify({'error': str(e)}), 500

@conference_bp.route('/api/<conference_id>', methods=['GET'])
@login_required
def get_conference(conference_id):
    """Get single conference"""
    try:
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        return jsonify({
            'success': True,
            'data': conference.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@conference_bp.route('/api/<conference_id>', methods=['PUT'])
@login_required
def update_conference(conference_id):
    """Update conference"""
    try:
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            # Check if new name already exists
            existing = MongoConference.objects(name=data['name']).first()
            if existing and existing.id != conference_id:
                return jsonify({'error': 'Conference name already exists'}), 409
            conference.name = data['name']
        
        if 'description' in data:
            conference.description = data['description']
        
        if 'location' in data:
            conference.location = data['location']
        
        if 'start_date' in data:
            conference.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        
        if 'end_date' in data:
            conference.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        conference.updated_at = datetime.utcnow()
        conference.save()
        
        print(f"✓ Conference updated: {conference_id}")
        
        return jsonify({
            'success': True,
            'message': 'Conference updated successfully',
            'data': conference.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@conference_bp.route('/api/<conference_id>', methods=['DELETE'])
@login_required
def delete_conference(conference_id):
    """Delete conference"""
    try:
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        conference_name = conference.name
        conference.delete()
        
        print(f"✓ Conference deleted: {conference_name}")
        
        return jsonify({
            'success': True,
            'message': 'Conference deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
