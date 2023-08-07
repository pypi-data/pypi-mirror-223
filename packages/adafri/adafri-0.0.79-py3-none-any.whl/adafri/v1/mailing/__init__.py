
import os
from sendgrid.helpers.mail import Email, Personalization
from sendgrid import SendGridAPIClient, Mail as SendGridMail
import urllib.parse

from datetime import datetime
from adafri.v1.user import User
from adafri.utils import generate_random_code, ResponseStatus, ApiResponse, Error, StatusCode
from adafri.v1.auth.oauth import Code
from adafri.utils import Object, boolean

VALIDATION_FIELD = '_emailValidationSendDate'
STATUS_FIELD = 'status'

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY');
REGISTRATION_TEMPLATE_ID = os.environ.get('REGISTRATION_TEMPLATE_ID')
PAYMENT_TEMPLATE_ID = os.environ.get('PAYMENT_TEMPLATE_ID')
EMAIL_VERIFICATION_TEMPLATE_ID = os.environ.get('EMAIL_VERIFICATION_TEMPLATE_ID')
try:
    os_value = os.environ.get('DEFAULT_EMAIL_TIME_TO_RESEND');
    if os_value is None:
        DEFAULT_EMAIL_TIME_TO_RESEND = 10
    else:
        DEFAULT_EMAIL_TIME_TO_RESEND = int(str(os_value))
except:
    DEFAULT_EMAIL_TIME_TO_RESEND = 10;



def compareTimes(date_string: str):
    date_format = "%Y-%m-%d, %H:%M:%S"
    date = datetime.strptime(date_string, date_format);
    now = datetime.now();
    difference = now - date;
    days, seconds = difference.days, difference.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if minutes >= DEFAULT_EMAIL_TIME_TO_RESEND:
        return {"status": "ok", "difference": minutes};
    return {"status": "error", "difference": minutes};


def setTimeSended(user: User):
    try:
        date_format = "%Y-%m-%d, %H:%M:%S"
        now = datetime.now()
        date_obj = datetime.strftime(now, date_format)
        update_value = {};
        update_value[VALIDATION_FIELD] = date_obj
        update = user.document_reference().set(update_value, merge=True)
        return update_value
    except:
        return None;

def getTimeSended(user: User):
    statement = {};
    if user is None:
        statement[STATUS_FIELD]='error'
        statement[VALIDATION_FIELD]=None
        return statement
    validation = getattr(user, VALIDATION_FIELD, None)
    if validation is not None:
        statement[STATUS_FIELD]='ok'
        statement[VALIDATION_FIELD]=validation
        return statement
    else:
        statement[STATUS_FIELD]='ok'
        statement[VALIDATION_FIELD]='now'
        return statement
    


class Mail:
    def __init__(self, from_text=None, destination=None, subject=None, custom_data=None, link=None):
        self.from_text = from_text;
        self.destination = destination;
        self.subject = subject;
        self.custom_data = custom_data;
        self.link = link;
    
    def sendgrid_client(self, _api_key=None):
        api_key = _api_key;
        if api_key is None:
            api_key = SENDGRID_API_KEY;
        return SendGridAPIClient(api_key);

    def check_time_send(self, check=True):
        user_model = User().query([{"key": "email", "value": self.destination, "comp": "=="}], True);
        if user_model is not None and user_model.uid is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error('User not exist', 'USER_NOT_EXIST'))
        if check:
            time_sended = getTimeSended(user_model);
            if time_sended['status']=='error':
                return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error('User not exist', 'USER_NOT_EXIST'))
            if time_sended[VALIDATION_FIELD]!='now':
                compare = compareTimes(time_sended[VALIDATION_FIELD]);
                if compare['status'] == 'error':
                    minutes = DEFAULT_EMAIL_TIME_TO_RESEND - compare['difference']
                    return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, {"minutes": minutes}, Error(f"Please wait {minutes} minutes and retry", 'WAIT_FEW_MINUTES'))

        return ApiResponse(ResponseStatus.OK, StatusCode.status_200, user_model, None)
    
    def sendMailRegistration(self, domain, _api_key=None, _template_id=None, bccs=[]):
        if domain is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error('Invalid domain', 'INVALID_REQUEST'))
        result = None
        template_id = _template_id;
        if template_id is None:
            template_id = REGISTRATION_TEMPLATE_ID
        message = Mail(
            from_email=self.from_text+'@'+domain,
            to_emails=[self.destination],
            )
        try:
            message.template_id = template_id
            personalization = Personalization()
            for bcc in bccs:
                personalization.add_bcc(Email(bcc))
            message.add_personalization(personalization)
            response = self.sendgrid_client(_api_key=_api_key).send(message)
            if response.status_code==200 or response.status_code==202:
                result = ApiResponse(ResponseStatus.OK, response.status_code, {"message": "Email sent successfully"}, None)
                print(result)
            else:
                result = ApiResponse(ResponseStatus.ERROR, response.status_code, None, Error('An error occurated', 'INVALID_REQUEST'))
        except Exception as e:
            print(e)
            result = ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(str(e), 'INVALID_REQUEST'))
        
        return result
    
    def sendMailPaymentSuccess(self, domain, _api_key=None, _template_id=None, bccs=[]):
        if domain is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error('Invalid domain', 'INVALID_REQUEST'))
        result = None
        message = SendGridMail()
        try:
            template_id = _template_id;
            if template_id is None:
                template_id = PAYMENT_TEMPLATE_ID
            message.from_email = self.from_text+'@'+domain
            message.template_id = template_id
            personalization = Personalization()
            personalization.dynamic_template_data = self.custom_data
            personalization.add_to(Email(self.destination))
            personalization.subject = self.subject
            for bcc in bccs:
                personalization.add_bcc(Email(bcc))
            message.add_personalization(personalization)
        
            response = self.sendgrid_client(_api_key).send(message) 
            if response.status_code==200 or response.status_code==202:
                result = ApiResponse(ResponseStatus.OK, response.status_code, {"message": "Email sent successfully"}, None)
            else:
                result = ApiResponse(ResponseStatus.ERROR, response.status_code, None, Error('An error occurated', 'INVALID_REQUEST'))
        except Exception as e:
            print(e)
            result = ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(str(e), 'INVALID_REQUEST'))
        
        return result
    
    def sendMailEmailVerfication(self, domain, _api_key=None, _template_id=None, bccs=[], check=False) -> 'ApiResponse':
        if domain is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error('Invalid domain', 'INVALID_REQUEST'))
        result = None
        message = SendGridMail()
        time_sended = self.check_time_send(check);
        if time_sended.status==ResponseStatus.ERROR:
            return time_sended
        user_model = User(time_sended.data)
        try:
            template_id = _template_id;
            if template_id is None:
                template_id = os.environ.get('EMAIL_VERIFICATION_TEMPLATE_ID')
            custom_data = self.custom_data;
            if self.link is not None:
                c_data = {'link': urllib.parse.unquote(self.link)}
                if custom_data is not None:
                    custom_data = {**custom_data, **c_data}
                else:
                    custom_data = c_data
            message.from_email = self.from_text+'@'+domain
            message.template_id = template_id
            personalization = Personalization()
            if self.custom_data is not None:
                personalization.dynamic_template_data = custom_data
            personalization.add_to(Email(self.destination))
            personalization.subject = self.subject
            for bcc in bccs:
                personalization.add_bcc(Email(bcc))
            message.add_personalization(personalization)
            email_test_mode = boolean(os.environ.get('EMAIL_TEST_MODE'))
            if email_test_mode is None or email_test_mode is True:
                response = Object(status_code=200, message="success")
            else:
                response = self.sendgrid_client(_api_key).send(message) 
            if response.status_code==200 or response.status_code==202:
                setTimeSended(user_model);
                result = ApiResponse(ResponseStatus.OK, response.status_code, {"message": "Email sent successfully"}, None)
            else:
                result = ApiResponse(ResponseStatus.ERROR, response.status_code, None, Error('An error occurated that\'s why your email were not sent', 'EMAIL_NOT_SENT', 1))
        except Exception as e:
            print(e)
            result = ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(str(e), 'INVALID_REQUEST'))
        
        return result
    

class MailSetting(Mail):
    DEFAULT_CODE_VALIDATION_BODY = "Vous êtes prêts pour commencer. Saisissez le code ci dessous pour valider votre email."
    CODE_VALIDATION_TEMPLATE_ID = os.environ.get('CODE_VALIDATION_TEMPLATE_ID')
    def __init__(self, from_text=None, destination=None, subject=None, custom_data=None, link=None):
        super().__init__(from_text, destination, subject, custom_data, link);
    
    def generate_email_validation_code(self, domain=None, bccs=[], template_id=CODE_VALIDATION_TEMPLATE_ID, _body=None):
        time_sended = self.check_time_send();
        if time_sended.status==ResponseStatus.ERROR:
            return time_sended
        user_model = User(time_sended.data)
        uid = user_model.uid;
        code = str(generate_random_code());
        model_ = {
            "target": uid,
            "code_type": "email_validation",
            "code": code
        }
        id = Code(Code.generate(**model_).data).id
        code_model = Code();
        code_model.id = id;
        code_model.code = code;
        code_model.code_type = 'email_validation'
        code_model.expires_in = 600
        code_model.target = uid;
        code = code_model.getCode();
        if code is None or code.is_expired():
            create = Code().create(**code_model.to_json());
            if create.status == ResponseStatus.OK:
                code = Code(create.data)
            else:
                return create
            
        if code is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error('An error occurrated', 'INVALID_REQUEST'))
        body = _body;
        if body is None:
            body = self.DEFAULT_CODE_VALIDATION_BODY
        self.custom_data = {"code": code.code, "body": body}
        # return ApiResponse(ResponseStatus.OK, StatusCode.status_200, code.to_json(), None)
        return self.sendMailEmailVerfication(domain=domain, _template_id=template_id, bccs=bccs, check=False)