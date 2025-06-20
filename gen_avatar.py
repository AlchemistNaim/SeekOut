from hashlib import md5

email = input ()
email = email.strip().lower()  # normalize the email
email_hash = md5(email.encode('utf-8')).hexdigest()
gravatar_url = 'https://www.gravatar.com/avatar/' + email_hash

print(gravatar_url)

