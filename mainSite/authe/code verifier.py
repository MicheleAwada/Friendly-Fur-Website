import random
import string
import base64
import hashlib
import pyperclip

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
print(code_verifier)
print(code_challenge)
# import random
# import string
# import base64
# import hashlib
#
# code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
# code_verifier_bytes = code_verifier.encode('utf-8')
#
# # Use base64.urlsafe_b64encode() to get a bytes object
# code_verifier_encoded = base64.urlsafe_b64encode(code_verifier_bytes)
#
# # Decode the bytes to get the expected string representation
# code_verifier_str = code_verifier_encoded.decode('utf-8')
#
# # Print the code verifier
# print(code_verifier_str)
#
# # Calculate the code challenge
# code_challenge_bytes = hashlib.sha256(code_verifier_bytes).digest()
# code_challenge_encoded = base64.urlsafe_b64encode(code_challenge_bytes)
# code_challenge_str = code_challenge_encoded.decode('utf-8').replace('=', '')
#
# # Print the code challenge
# print(code_challenge_str)