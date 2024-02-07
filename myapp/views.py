# myapp/views.py


#
# def validate_and_verify_email(email):
#     try:
#         validate_email(email)
#     except ValidationError:
#         return False, 'Invalid email format!'
#
#     domain = email.split('@')[1]
#     try:
#         records = dns.resolver.resolve(domain, 'MX')
#         mx_record = str(records[0].exchange)
#         with smtplib.SMTP(mx_record) as server:
#             server.set_debuglevel(0)
#             server.ehlo()
#             server.mail('')
#             code, message = server.rcpt(email)
#             if code == 250:
#                 return True, 'Email is valid and exists!'
#             else:
#                 return False, 'Email does not exist.'
#     except Exception as e:
#         return False, 'Error during verification.'
#
# # def validate_email_view(request):
# #     message = ''
# #     if request.method == 'POST':
# #         email = request.POST.get('email', '')
# #         success, message = validate_and_verify_email(email)
#
# #     return render(request, 'email_form.html', {'message': message})






from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import smtplib
import dns.resolver

def combined_function(request):
    message = ''

    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            message = 'Invalid email format!'
        else:
            domain = email.split('@')[1]
            try:
                records = dns.resolver.resolve(domain, 'MX')
                mx_record = str(records[0].exchange)
                with smtplib.SMTP(mx_record) as server:
                    server.set_debuglevel(0)
                    server.ehlo()
                    server.mail('')
                    code, response = server.rcpt(email)
                    if code == 250:
                        message = 'Email is valid and exists!'
                    else:
                        message = 'Email does not exist.'
            # except Exception as e:
            #     message = 'Error during verification.'
            except dns.resolver.NoAnswer:
                message = 'Domain does not exist.'
            except dns.resolver.NXDOMAIN:
                message = 'Domain does not exist.'
            except smtplib.SMTPException as e:
                message = 'SMTP error: ' + str(e)
            except Exception as e:
                message = 'Unexpected error during verification: ' + str(e)


    return render(request, 'email_form.html', {'message': message})








# 5:25 pm -> create it such that we can use it 
# instead of request, convert it into -> passing just an email id and password 
#html page not to render -> create a new function, instead of request, pass the email and password as parameters 

#time-saved

# def check_email_existence(email, password):
#     message = ''

#     try:
#         validate_email(email)
#     except ValidationError:
#         message = 'Invalid email format!'
#     else:
#         domain = email.split('@')[1]
#         try:
#             records = dns.resolver.resolve(domain, 'MX')
#             mx_record = str(records[0].exchange)
#             with smtplib.SMTP(mx_record) as server:
#                 server.set_debuglevel(0)
#                 server.starttls()
#                 server.login(email, password)
#                 server.ehlo()
#                 server.mail('')
#                 code, response = server.rcpt(email)
#                 if code == 250:
#                     message = 'Email is valid and exists!'
#                 else:
#                     message = 'Email does not exist.'
#         except dns.resolver.NoAnswer:
#             message = 'Domain does not exist.'
#         except dns.resolver.NXDOMAIN:
#             message = 'Domain does not exist.'
#         except smtplib.SMTPAuthenticationError:
#             message = 'Authentication failed.'
#         except smtplib.SMTPException as e:
#             message = 'SMTP error: ' + str(e)
#         except Exception as e:
#             message = 'Unexpected error during verification: ' + str(e)

#     return message




# import dns.resolver
# import smtplib
# from email_validator import validate_email, EmailNotValidError


# def check_email_existence(email, password):
#     message = ''

#     try:
#         validate_email(email)
#     except EmailNotValidError:
#         message = 'Invalid email format!'
#     else:
#         domain = email.split('@')[1]
#         try:
#             records = dns.resolver.resolve(domain, 'MX')
#             mx_record = str(records[0].exchange)
#             with smtplib.SMTP(mx_record) as server:
#                 server.set_debuglevel(0)
#                 server.connect(mx_record)
#                 server.starttls()
#                 server.login(email, password)
#                 server.ehlo()
#                 server.mail('')
#                 code, response = server.rcpt(email)
#                 if code == 250:
#                     message = 'Email is valid and exists!'
#                 else:
#                     message = 'Email does not exist.'
#         except dns.resolver.NoAnswer:
#             message = 'Domain does not exist.'
#         except dns.resolver.NXDOMAIN:
#             message = 'Domain does not exist.'
#         except smtplib.SMTPAuthenticationError:
#             message = 'Authentication failed.'
#         except smtplib.SMTPException as e:
#             message = 'SMTP error: ' + str(e)
#         except Exception as e:
#             message = 'Unexpected error during verification: ' + str(e)

#     return message

# # Example usage:
# email = "example@yahoo.com"
# password = "your_password"
# print(check_email_existence(email, password))




# import dns.resolver
# import smtplib
# from email.utils import parseaddr
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from django.shortcuts import render

# def verify_email(email):
#     try:
#         validate_email(email)
#     except ValidationError:
#         return 'Invalid email format!'

#     _, domain = parseaddr(email)
#     try:
#         mx_records = dns.resolver.resolve(domain, 'MX')
#     except dns.resolver.NoAnswer:
#         return 'Domain does not have mail exchange (MX) records.'
#     except dns.resolver.NXDOMAIN:
#         return 'Domain does not exist.'
#     except dns.resolver.Timeout:
#         return 'DNS query timed out.'
#     except Exception as e:
#         return f'DNS error: {str(e)}'

#     for mx_record in mx_records:
#         mx_host = str(mx_record.exchange)
#         try:
#             with smtplib.SMTP(mx_host) as server:
#                 server.ehlo()
#                 if server.has_extn('starttls'):
#                     server.starttls()
#                     server.ehlo()
#                 code, response = server.mail('')
#                 if code == 250:
#                     code, response = server.rcpt(email)
#                     if code == 250:
#                         return 'Email is valid and exists!'
#         except smtplib.SMTPConnectError:
#             pass  # Try next MX server
#         except smtplib.SMTPResponseException:
#             pass  # Try next MX server
#         except smtplib.SMTPException as e:
#             return f'SMTP error: {str(e)}'
#         except Exception as e:
#             return f'Unexpected error during verification: {str(e)}'

#     return 'Email does not exist.'

# def combined_function(request):
#     message = ''

#     if request.method == 'POST':
#         email = request.POST.get('email', '')
#         message = verify_email(email)

#     return render(request, 'email_form.html', {'message': message})






###









# import dns.resolver
# import smtplib
# from email.utils import parseaddr
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from django.shortcuts import render

# def verify_email(email):
#     try:
#         validate_email(email)
#     except ValidationError:
#         return 'Invalid email format!'
    
#     _, domain = parseaddr(email)
#     if not domain:
#         return 'Invalid email format!'
    
#     try:
#         mx_records = dns.resolver.resolve(domain, 'MX')
#     except dns.resolver.NoAnswer:
#         return 'Domain does not have mail exchange (MX) records.'
#     except dns.resolver.NXDOMAIN:
#         return 'Domain does not exist.'
#     except dns.resolver.Timeout:
#         return 'DNS query timed out.'
#     except Exception as e:
#         return f'DNS error: {str(e)}'

#     for mx_record in sorted(mx_records, key=lambda record: record.preference):
#         mx_host = str(mx_record.exchange)
#         try:
#             with smtplib.SMTP(mx_host) as server:
#                 server.set_debuglevel(0)  # No debug messages
#                 server.ehlo()
#                 if server.has_extn('starttls'):
#                     server.starttls()
#                     server.ehlo()  # Re-identify ourselves over TLS connection
#                 server.mail('')
#                 code, response = server.rcpt(email)
#                 if code == 250:
#                     return 'Email is valid and exists!'
#         except smtplib.SMTPException as e:
#             return f'SMTP error: {str(e)}'
#         except Exception as e:
#             return f'Unexpected error during verification: {str(e)}'
    
#     return 'Email does not exist.'

# def combined_function(request):
#     message = ''

#     if request.method == 'POST':
#         email = request.POST.get('email', '')
#         message = verify_email(email)

#     return render(request, 'email_form.html', {'message': message})





# import dns.resolver
# import smtplib
# from email.utils import parseaddr
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from django.shortcuts import render

# def verify_email(email):
#     # Validate the email format.
#     try:
#         validate_email(email)
#     except ValidationError:
#         return 'Invalid email format!'
    
#     # Extract the domain from the email.
#     _, domain = parseaddr(email)
#     if not domain:
#         return 'Invalid email format!'
    
#     # Resolve the MX records for the domain.
#     try:
#         mx_records = dns.resolver.resolve(domain, 'MX')
#     except dns.resolver.NoAnswer:
#         return 'Domain does not have mail exchange (MX) records.'
#     except dns.resolver.NXDOMAIN:
#         return 'Domain does not exist.'
#     except dns.resolver.Timeout:
#         return 'DNS query timed out.'
#     except Exception as e:
#         return f'DNS error: {str(e)}'

#     # Attempt to connect to the MX server and verify the email.
#     for mx_record in sorted(mx_records, key=lambda record: record.preference):
#         mx_host = str(mx_record.exchange)
#         try:
#             with smtplib.SMTP(mx_host) as server:
#                 server.set_debuglevel(0)  # Suppress debug output
#                 server.ehlo()
#                 if server.has_extn('starttls'):
#                     server.starttls()
#                     server.ehlo()  # Re-identify after starting TLS
#                 server.mail('')
#                 code, response = server.rcpt(email)
#                 if code == 250:
#                     return 'Email is valid and exists!'
#         except smtplib.SMTPException as e:
#             return f'SMTP error: {str(e)}'
#         except Exception as e:
#             return f'Unexpected error during verification: {str(e)}'
    
#     return 'Email does not exist.'

# def combined_function(request):
#     message = ''
    
#     if request.method == 'POST':
#         email = request.POST.get('email', '')
#         message = verify_email(email)

#     return render(request, 'email_form.html', {'message': message})
