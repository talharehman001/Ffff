from twilio.rest import Client
import random

class TwilioService:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)
        self.account_sid = account_sid
        self.auth_token = auth_token
        
    def validate_credentials(self):
        """Validate Twilio credentials by attempting to access the account."""
        try:
            # Try to access account info to validate credentials
            account = self.client.api.accounts(self.account_sid).fetch()
            return True
        except Exception as e:
            print(f"Validation error: {str(e)}")
            return False
    
    def buy_phone_number(self, area_code=None):
        """Buy a phone number with specified area code or random Canadian area code."""
        try:
            # Canadian area codes
            canadian_area_codes = ['204', '226', '236', '249', '250', '289', '306', '343', '365', 
                                  '403', '416', '418', '431', '437', '438', '450', '506', '514', 
                                  '519', '548', '579', '581', '587', '604', '613', '639', '647', 
                                  '705', '709', '778', '780', '782', '807', '819', '825', '867', '873', '902', '905']
            
            # If no area code provided or user wants random, select a random Canadian area code
            if not area_code:
                area_code = random.choice(canadian_area_codes)
            
            # Search for available phone numbers
            available_numbers = self.client.available_phone_numbers('CA').local.list(
                area_code=area_code,
                limit=1
            )
            
            if not available_numbers:
                return {
                    'success': False,
                    'message': f'No available phone numbers found with area code {area_code}'
                }
            
            # Buy the first available number
            number = self.client.incoming_phone_numbers.create(
                phone_number=available_numbers[0].phone_number
            )
            
            return {
                'success': True,
                'phone_number': number.phone_number,
                'sid': number.sid
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_phone_numbers(self):
        """Get all phone numbers in the account."""
        try:
            numbers = self.client.incoming_phone_numbers.list()
            return {
                'success': True,
                'numbers': [{
                    'phone_number': number.phone_number,
                    'sid': number.sid,
                    'friendly_name': number.friendly_name
                } for number in numbers]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def remove_phone_number(self, number_sid):
        """Remove a phone number by SID."""
        try:
            self.client.incoming_phone_numbers(number_sid).delete()
            return {
                'success': True,
                'message': 'Phone number removed successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_messages(self, phone_number=None):
        """Get messages for a specific phone number or all numbers."""
        try:
            if phone_number:
                # Filter messages by the To phone number
                messages = self.client.messages.list(to=phone_number)
            else:
                # Get all messages
                messages = self.client.messages.list()
            
            return {
                'success': True,
                'messages': [{
                    'sid': msg.sid,
                    'body': msg.body,
                    'from_number': msg.from_,
                    'to_number': msg.to,
                    'date_created': str(msg.date_created),
                    'status': msg.status
                } for msg in messages]
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
