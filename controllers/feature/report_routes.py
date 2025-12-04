from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, send_file
from models.MongoConference import MongoConference
from models.MongoSession import MongoSession
from models.MongoUser import MongoUser
from models.MongoAttendee import MongoAttendee
from datetime import datetime
import io
import csv
import uuid
import json

report_bp = Blueprint('report', __name__, url_prefix='/reports')

# GENERATE CONFERENCE REPORT
@report_bp.route('/conference/<conference_id>', methods=['GET', 'POST'])
def conference_report(conference_id):
    """Generate report for a conference"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        # Verify authorization (organizer only)
        if conference.organizer_id != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get conference data
        total_sessions = MongoSession.objects(conference_id=conference_id).count()
        total_attendees = len(conference.attendees)
        
        sessions = MongoSession.objects(conference_id=conference_id)
        
        report_data = {
            'conference_name': conference.name,
            'conference_id': conference.id,
            'description': conference.description,
            'location': conference.location,
            'start_date': conference.start_date.isoformat(),
            'end_date': conference.end_date.isoformat(),
            'total_sessions': total_sessions,
            'total_attendees': total_attendees,
            'max_attendees': conference.max_attendees,
            'registration_fee': conference.registration_fee,
            'status': conference.status,
            'sessions': [s.to_dict() for s in sessions],
            'generated_at': datetime.utcnow().isoformat()
        }
        
        report_format = request.args.get('format', 'json')
        
        if report_format == 'csv':
            return generate_csv_report(report_data, conference.name)
        elif report_format == 'html':
            return render_template('reports/conference_report.html', report=report_data)
        else:
            return jsonify(report_data), 200
        
    except Exception as e:
        print(f"Error generating conference report: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500

# GENERATE ATTENDEE REPORT
@report_bp.route('/attendees/<conference_id>', methods=['GET'])
def attendees_report(conference_id):
    """Generate attendee report for a conference"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        # Verify authorization
        if conference.organizer_id != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get attendee information
        attendees_data = []
        for attendee_id in conference.attendees:
            user = MongoUser.objects(id=attendee_id).first()
            if user:
                attendees_data.append({
                    'name': user.full_name,
                    'email': user.email,
                    'username': user.username,
                    'joined_date': user.created_at.isoformat() if user.created_at else ''
                })
        
        report = {
            'conference_name': conference.name,
            'total_attendees': len(attendees_data),
            'attendees': attendees_data,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        report_format = request.args.get('format', 'json')
        
        if report_format == 'csv':
            return generate_attendees_csv(report, conference.name)
        else:
            return jsonify(report), 200
        
    except Exception as e:
        print(f"Error generating attendee report: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500

# GENERATE SESSION REPORT
@report_bp.route('/sessions/<conference_id>', methods=['GET'])
def sessions_report(conference_id):
    """Generate sessions report for a conference"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        # Verify authorization
        if conference.organizer_id != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        sessions = MongoSession.objects(conference_id=conference_id).order_by('start_time')
        
        sessions_data = []
        for sess in sessions:
            sessions_data.append({
                'title': sess.title,
                'speaker': sess.speaker,
                'location': sess.location,
                'start_time': sess.start_time.isoformat(),
                'end_time': sess.end_time.isoformat(),
                'registered_attendees': len(sess.attendees),
                'capacity': sess.capacity
            })
        
        report = {
            'conference_name': conference.name,
            'total_sessions': len(sessions_data),
            'sessions': sessions_data,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return jsonify(report), 200
        
    except Exception as e:
        print(f"Error generating sessions report: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500

# DOWNLOAD REPORT
@report_bp.route('/download/<report_type>/<conference_id>', methods=['GET'])
def download_report(report_type, conference_id):
    """Download report in various formats"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        if conference.organizer_id != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        file_format = request.args.get('format', 'pdf')
        
        if report_type == 'conference':
            if file_format == 'csv':
                report_data = {
                    'conference_name': conference.name,
                    'total_sessions': MongoSession.objects(conference_id=conference_id).count(),
                    'total_attendees': len(conference.attendees)
                }
                return generate_csv_report(report_data, conference.name)
        
        return jsonify({'error': 'Invalid report type or format'}), 400
        
    except Exception as e:
        print(f"Error downloading report: {str(e)}")
        return jsonify({'error': 'Failed to download report'}), 500

# HELPER FUNCTIONS
def generate_csv_report(data, filename):
    """Generate CSV report"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Conference Report'])
        writer.writerow(['Generated at', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # Write conference details
        writer.writerow(['Conference Name', data.get('conference_name', '')])
        writer.writerow(['Total Sessions', data.get('total_sessions', 0)])
        writer.writerow(['Total Attendees', data.get('total_attendees', 0)])
        writer.writerow([])
        
        # Write sessions if available
        if 'sessions' in data:
            writer.writerow(['Sessions'])
            writer.writerow(['Title', 'Speaker', 'Location', 'Start Time', 'End Time'])
            for session in data['sessions']:
                writer.writerow([
                    session.get('title', ''),
                    session.get('speaker', ''),
                    session.get('location', ''),
                    session.get('start_time', ''),
                    session.get('end_time', '')
                ])
        
        # Create response
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{filename}_report_{datetime.utcnow().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        print(f"CSV generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate CSV'}), 500

def generate_attendees_csv(report, filename):
    """Generate attendees CSV"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Attendees Report'])
        writer.writerow(['Conference', report.get('conference_name', '')])
        writer.writerow(['Total Attendees', report.get('total_attendees', 0)])
        writer.writerow([])
        writer.writerow(['Name', 'Email', 'Username', 'Joined Date'])
        
        for attendee in report.get('attendees', []):
            writer.writerow([
                attendee.get('name', ''),
                attendee.get('email', ''),
                attendee.get('username', ''),
                attendee.get('joined_date', '')
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{filename}_attendees_{datetime.utcnow().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        print(f"Attendees CSV generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate CSV'}), 500
