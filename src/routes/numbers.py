from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from src.services.twilio_service import TwilioService

numbers_bp = Blueprint('numbers', __name__)

def get_twilio_service():
    """Helper function to get Twilio service from session credentials"""
    if 'account_sid' not in session or 'auth_token' not in session:
        return None
    return TwilioService(session['account_sid'], session['auth_token'])

@numbers_bp.route('/dashboard')
def dashboard():
    if 'account_sid' not in session or 'auth_token' not in session:
        flash('আপনাকে প্রথমে লগইন করতে হবে', 'error')
        return redirect(url_for('auth.login'))
    
    twilio_service = get_twilio_service()
    result = twilio_service.get_phone_numbers()
    
    if not result['success']:
        flash(f'নাম্বার লোড করতে সমস্যা: {result["message"]}', 'error')
        numbers = []
    else:
        numbers = result['numbers']
    
    return render_template('dashboard.html', numbers=numbers)

@numbers_bp.route('/buy', methods=['POST'])
def buy_number():
    if 'account_sid' not in session or 'auth_token' not in session:
        return jsonify({'success': False, 'message': 'আপনাকে প্রথমে লগইন করতে হবে'})
    
    twilio_service = get_twilio_service()
    area_code = request.form.get('area_code')
    
    # If random area code is requested, pass None to use random Canadian area code
    if request.form.get('random_area_code') == 'true':
        area_code = None
    
    result = twilio_service.buy_phone_number(area_code)
    return jsonify(result)

@numbers_bp.route('/remove', methods=['POST'])
def remove_number():
    if 'account_sid' not in session or 'auth_token' not in session:
        return jsonify({'success': False, 'message': 'আপনাকে প্রথমে লগইন করতে হবে'})
    
    twilio_service = get_twilio_service()
    number_sid = request.form.get('number_sid')
    
    if not number_sid:
        return jsonify({'success': False, 'message': 'নাম্বার SID প্রয়োজন'})
    
    result = twilio_service.remove_phone_number(number_sid)
    return jsonify(result)
