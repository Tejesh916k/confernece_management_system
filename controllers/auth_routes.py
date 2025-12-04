from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from models.MongoUser import MongoUser
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                return jsonify({'error': 'Username and password required'}), 400
            
            # Query user
            user = MongoUser.objects(username=username).first()
            
            if not user:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not user.check_password(password):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not user.is_active:
                return jsonify({'error': 'Account disabled'}), 403
            
            # Store user in session
            session['user_id'] = str(user.id)
            session['username'] = user.username
            session['email'] = user.email
            session['full_name'] = user.full_name
            session.permanent = True
            
            print(f'[OK] User logged in: {username}')
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'redirect': '/dashboard'
            }), 200
            
        except Exception as e:
            print(f'Login error: {str(e)}')
            return jsonify({'error': 'Login failed: ' + str(e)}), 500
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and handler"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            full_name = data.get('full_name', '').strip()
            
            # Validation
            if not all([username, email, password, full_name]):
                return jsonify({'error': 'All fields required'}), 400
            
            if len(password) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            
            if len(username) < 3:
                return jsonify({'error': 'Username must be at least 3 characters'}), 400
            
            if '@' not in email:
                return jsonify({'error': 'Invalid email address'}), 400
            
            # Check if username exists
            if MongoUser.objects(username=username).first():
                return jsonify({'error': 'Username already taken'}), 409
            
            # Check if email exists
            if MongoUser.objects(email=email).first():
                return jsonify({'error': 'Email already registered'}), 409
            
            # Create new user
            user = MongoUser(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                full_name=full_name,
                is_active=True
            )
            user.set_password(password)
            user.save()
            
            print(f'[OK] New user registered: {username}')
            
            return jsonify({
                'success': True,
                'message': 'Account created successfully',
                'redirect': '/login'
            }), 201
            
        except Exception as e:
            print(f'Signup error: {str(e)}')
            return jsonify({'error': 'Signup failed: ' + str(e)}), 500
    
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    if 'username' in session:
        print(f'[OK] User logged out: {session["username"]}')
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
def profile():
    """User profile"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        user = MongoUser.objects(id=session['user_id']).first()
        if user:
            return render_template('auth/profile.html', user=user.to_dict())
        return redirect(url_for('auth.login'))
    except Exception as e:
        print(f'Profile error: {e}')
        return redirect(url_for('auth.login'))
