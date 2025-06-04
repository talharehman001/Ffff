from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from src.services.twilio_service import TwilioService

messages_bp = Blueprint('messages', __name__)

def get_twilio_service():
    """Helper function to get Twilio service from session credentials"""
    if 'account_sid' not in session or 'auth_token' not in session:
        return None
    return TwilioService(session['account_sid'], session['auth_token'])

@messages_bp.route('/messages')
def show_messages():
    if 'account_sid' not in session or 'auth_token' not in session:
        flash('আপনাকে প্রথমে লগইন করতে হবে', 'error')
        return redirect(url_for('auth.login'))
    
    twilio_service = get_twilio_service()
    phone_number = request.args.get('phone_number')
    
    result = twilio_service.get_messages(phone_number)
    
    if not result['success']:
        flash(f'মেসেজ লোড করতে সমস্যা: {result["message"]}', 'error')
        messages = []
    else:
        messages = result['messages']
    
    # Get phone numbers for filtering
    numbers_result = twilio_service.get_phone_numbers()
    if numbers_result['success']:
        numbers = numbers_result['numbers']
    else:
        numbers = []
    
    return render_template('messages.html', messages=messages, numbers=numbers, selected_number=phone_number)

@messages_bp.route('/api/messages')
def get_messages_api():
    if 'account_sid' not in session or 'auth_token' not in session:
        return jsonify({'success': False, 'message': 'আপনাকে প্রথমে লগইন করতে হবে'})
    
    twilio_service = get_twilio_service()
    phone_number = request.args.get('phone_number')
    
    result = twilio_service.get_messages(phone_number)
    return jsonify(result)
