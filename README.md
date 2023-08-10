# Unofficial Python Wrapper for Rave API ✨

Simplify interaction with the Rave API using this unofficial Python wrapper. Perform actions like retrieving project details, creating new projects, and updating existing ones.

## Installation

Install the package using pip:

```bash
pip install rave.py
```
## Usage
Here's a simple example of logging in and getting the token:
```py
import rave

# Create a Rave client instance
client = rave.Client()

# Prompt the user for their email
email_input = input("Enter your email: ")

# Initiate authentication, returning an authentication token once the email is verified
authentication_result = client.authenticate(email_input)

# Extract and print the token (excluding the first two characters)
print("Your authentication token is:", authentication_result.token[2:])
```
For more details, refer to the upcoming documentation.

## Contributing
Contributions are welcome! Report bugs or suggest features by creating GitHub issues. Contribute code by forking the repository and submitting a pull request.

## Contact
Questions or discussions about the package can be held on our [Discord community](https://discord.gg/s7qacU5YNX). Join us today!
