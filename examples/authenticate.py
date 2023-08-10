import rave

# Create a Rave client instance
client = rave.Client()

# Prompt the user to enter their email for verification
email_input = input("Enter your email: ")

# Initiate the authentication process by sending a verification request to the provided email
# Once the email is verified, the function will return an authentication token
authentication_result = client.authenticate(email_input)

# Extract the token from the authentication result and print it (excluding the first two characters)
print("Your authentication token is:", authentication_result.token[2:])
