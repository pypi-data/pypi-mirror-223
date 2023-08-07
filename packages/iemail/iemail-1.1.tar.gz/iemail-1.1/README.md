# IEmail

## Description

IEmail is a PyPI package that provides a simple way to get a temporary email address and receive emails anonymously. It is a wrapper for [IEmail](https://iemail.eu.org/), an online service that allows users to create temporary email addresses for free.

The project is released on [pypi.org](https://pypi.org/), and you can view it at [https://pypi.org/project/iemail/](https://pypi.org/project/iemail/).

## Installation

You can install IEmail with pip as usual.

```bash
pip3 install iemail
```

## Usage

```python
# Import the module
from iemail import Account

# Create an account
test = Account(username='test', prefix='mymail')  # Address: test@mymail.iemail.eu.org

# See the address and password
print(test.address)

# Check the email's inbox
print(a.get_message(latest=0))
# latest: 0 means the latest email, 1 means the second latest email, and so on.
# If there is no email, it will raise IndexError.

print(a.get_messages()) # Get All the emails.
```

## Contact

If you have any questions or concerns, please feel free to contact us at [i@iemail.eu.org](mailto:i@iemail.eu.org).