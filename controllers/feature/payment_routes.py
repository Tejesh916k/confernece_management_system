from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.MongoConference import MongoConference
from models.MongoUser import MongoUser
from datetime import datetime
import uuid
import json
import random

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

# INITIATE PAYMENT
@payment_bp.route('/initiate', methods=['POST'])
def initiate_payment():
    """Initiate payment for conference registration"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        conference_id = data.get('conference_id')
        amount = float(data.get('amount', 0))
        
        if not conference_id or amount <= 0:
            return jsonify({'error': 'Invalid conference or amount'}), 400
        
        # Verify conference exists
        conference = MongoConference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        # Create payment session
        payment_data = {
            'payment_id': str(uuid.uuid4()),
            'user_id': session['user_id'],
            'conference_id': conference_id,
            'amount': amount,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'conference_name': conference.name,
            'user_email': session.get('email', ''),
            'full_name': session.get('full_name', '')
        }
        
        print(f"[OK] Payment initiated: {payment_data['payment_id']}")
        
        return jsonify({
            'success': True,
            'payment_id': payment_data['payment_id'],
            'amount': amount,
            'conference_name': conference.name,
            'message': 'Payment session created'
        }), 201
        
    except Exception as e:
        print(f"Payment initiation error: {str(e)}")
        return jsonify({'error': f'Failed to initiate payment: {str(e)}'}), 500

# PROCESS PAYMENT (Simulate)
@payment_bp.route('/process', methods=['POST'])
def process_payment():
    """Process payment"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        card_number = data.get('card_number')
        cvv = data.get('cvv')
        expiry = data.get('expiry')
        
        if not all([payment_id, card_number, cvv, expiry]):
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Validate card (basic validation)
        if len(card_number) != 16 or not card_number.isdigit():
            return jsonify({'error': 'Invalid card number'}), 400
        
        if len(cvv) != 3 or not cvv.isdigit():
            return jsonify({'error': 'Invalid CVV'}), 400
        
        # Simulate payment processing (70% success rate for demo)
        is_success = random.random() < 0.7
        
        if is_success:
            status = 'completed'
            message = 'Payment processed successfully'
            response_code = 200
        else:
            status = 'failed'
            message = 'Payment processing failed. Please try again.'
            response_code = 400
        
        payment_record = {
            'payment_id': payment_id,
            'status': status,
            'transaction_id': f'TXN{uuid.uuid4().hex[:12].upper()}',
            'processed_at': datetime.utcnow().isoformat(),
            'amount': data.get('amount', 0),
            'user_id': session['user_id']
        }
        
        print(f"[OK] Payment processed: {payment_id} - {status}")
        
        return jsonify({
            'success': is_success,
            'message': message,
            'payment_data': payment_record
        }), response_code
        
    except Exception as e:
        print(f"Payment processing error: {str(e)}")
        return jsonify({'error': f'Failed to process payment: {str(e)}'}), 500

# GET PAYMENT STATUS
@payment_bp.route('/status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Get payment status"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # In a real system, fetch from database
        # For now, return dummy data
        payment_data = {
            'payment_id': payment_id,
            'user_id': session['user_id'],
            'status': 'completed',  # Can be: pending, processing, completed, failed
            'amount': 299.99,
            'created_at': datetime.utcnow().isoformat(),
            'transaction_id': f'TXN{uuid.uuid4().hex[:12].upper()}'
        }
        
        return jsonify({'success': True, 'data': payment_data}), 200
        
    except Exception as e:
        print(f"Error fetching payment status: {str(e)}")
        return jsonify({'error': 'Failed to fetch payment status'}), 500

# GET USER PAYMENT HISTORY
@payment_bp.route('/history', methods=['GET'])
def payment_history():
    """Get user's payment history"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # In a real system, fetch from database
        # For now, return empty list
        history = []
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'success': True, 'payments': history, 'count': len(history)}), 200
        
        return render_template('payments/payment_history.html', payments=history)
        
    except Exception as e:
        print(f"Error fetching payment history: {str(e)}")
        return jsonify({'error': 'Failed to fetch payment history'}), 500

# PAYMENT PAGE
@payment_bp.route('/<conference_id>', methods=['GET'])
def payment_page(conference_id):
    """Payment page for conference"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        conference = Conference.objects(id=conference_id).first()
        if not conference:
            return jsonify({'error': 'Conference not found'}), 404
        
        user = MongoUser.objects(id=session['user_id']).first()
        
        return render_template(
            'payments/payment_page.html',
            conference=conference.to_dict(),
            user=user.to_dict() if user else {}
        )
    except Exception as e:
        print(f"Error loading payment page: {str(e)}")
        return redirect(url_for('conference.list_conferences'))

# REFUND REQUEST
@payment_bp.route('/refund/<payment_id>', methods=['POST'])
def request_refund(payment_id):
    """Request refund for a payment"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        reason = data.get('reason', 'No reason provided')
        
        refund_data = {
            'refund_id': str(uuid.uuid4()),
            'payment_id': payment_id,
            'user_id': session['user_id'],
            'reason': reason,
            'status': 'pending',
            'requested_at': datetime.utcnow().isoformat()
        }
        
        print(f"[OK] Refund requested: {refund_data['refund_id']}")
        
        return jsonify({
            'success': True,
            'message': 'Refund request submitted',
            'refund_id': refund_data['refund_id']
        }), 201
        
    except Exception as e:
        print(f"Refund request error: {str(e)}")
        return jsonify({'error': 'Failed to request refund'}), 500
