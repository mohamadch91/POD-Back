from kavenegar import *
import json

def send_otp(otp):
    try:
        api = KavenegarAPI("444E6C6378534967385758394B41572B57434F7A4C644D664558485631704464")
        params = {
            'sender': '0018018949161',
            'receptor': otp.receiver,
             'template': 'verify',
            'token': otp.password,
            'type': 'sms'
        }   
        response = api.verify_lookup(params)
    except APIException as e: 
        print (str(e))
    except HTTPException as e: 
        print (str(e))