from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.services.twilio_service import TwilioService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_sid = request.form.get('account_sid')
        auth_token = request.form.get('auth_token')
        
        if not account_sid or not auth_token:
            flash('টুইলিও অ্যাকাউন্ট SID এবং অথ টোকেন প্রয়োজন', 'error')
            return render_template('login.html')
        
        # Validate credentials
        twilio_service = TwilioService(account_sid, auth_token)
        if twilio_service.validate_credentials():
            # Store credentials in session
            session['account_sid'] = account_sid
            session['auth_token'] = auth_token
            return redirect(url_for('numbers.dashboard'))
        else:
            flash('অবৈধ টুইলিও ক্রেডেনশিয়াল। আবার চেষ্টা করুন।', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Clear session
    session.clear()
    flash('আপনি সফলভাবে লগআউট করেছেন', 'success')
    return redirect(url_for('auth.login'))
