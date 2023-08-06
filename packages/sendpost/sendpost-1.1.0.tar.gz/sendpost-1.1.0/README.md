# sendpost
Email API and SMTP relay to not just send and measure email sending, but also alert and optimise. We provide you with tools, expertise and support needed to reliably deliver emails to your customers inboxes on time, every time.

## Requirements.

Python &gt;&#x3D;3.7


## Installation & Usage
### pip install

```sh
pip install sendpost
```

Or you can install directly from git using:

```sh
pip install git+https://github.com/sendpost/sendpost_python_sdk.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/sendpost/sendpost_python_sdk.git`)

Then import the package:
```python
import sendpost_python_sdk
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import sendpost_python_sdk
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import sendpost_python_sdk
from pprint import pprint
from sendpost_python_sdk.apis.tags import email_api

# Enter a context with an instance of the API client
with sendpost_python_sdk.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = email_api.EmailApi(api_client)
    x_sub_account_api_key = "your_api_key" # str | Sub-Account API Key
    email = {
      "from": {
            "email": "richard@piedpiper.com",
      },
      "to": [
        {
          "email": "gavin@hooli.com",
        }
      ],
      "subject": "Hello World",
      "htmlBody": "<strong>it works!</strong>",
      "ippool": "PiedPiper",
    }
    try:
        api_response = api_instance.send_email(header_params={ 'X-SubAccount-ApiKey': x_sub_account_api_key}, body=email)
        pprint(api_response)
    except sendpost_python_sdk.ApiException as e:
        print("Exception when calling EmailApi->send_email: %s\n" % e)
```

Example with cc, bcc and template:

```python

import sendpost_python_sdk
from pprint import pprint
from sendpost_python_sdk.apis.tags import email_api

# Enter a context with an instance of the API client
with sendpost_python_sdk.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = email_api.EmailApi(api_client)
    x_sub_account_api_key = "your_api_key" # str | Sub-Account API Key
    email = {
      "from": {
            "email": "richard@piedpiper.com",
      },
      "to": [
        {
          "email": "gavin@hooli.com",
          "cc": [{ "email": "dinesh@bachmanity.com" }],
          "bcc": [{ "email": "jian@bachmanity.com" }],
        }
      ],
      "template": "Welcome Mail",
      "subject": "Hello World",
      "htmlBody": "<strong>it works!</strong>",
      "ippool": "PiedPiper",
    }
    try:
        api_response = api_instance.send_email_with_template(header_params={ 'X-SubAccount-ApiKey': x_sub_account_api_key}, body=email)
        pprint(api_response)
    except sendpost_python_sdk.ApiException as e:
        print("Exception when calling EmailApi->send_email: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.sendpost.io/api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*EmailApi* | [**send_email**](docs/apis/tags/EmailApi.md#send_email) | **post** /subaccount/email/ | 
*EmailApi* | [**send_email_with_template**](docs/apis/tags/EmailApi.md#send_email_with_template) | **post** /subaccount/email/template | 
*SuppressionApi* | [**count**](docs/apis/tags/SuppressionApi.md#count) | **get** /subaccount/suppression/count | 
*SuppressionApi* | [**create_suppressions**](docs/apis/tags/SuppressionApi.md#create_suppressions) | **post** /subaccount/suppression/ | 
*SuppressionApi* | [**delete_suppression**](docs/apis/tags/SuppressionApi.md#delete_suppression) | **delete** /subaccount/suppression/ | 
*SuppressionApi* | [**get_suppressions**](docs/apis/tags/SuppressionApi.md#get_suppressions) | **get** /subaccount/suppression/ | 

## Documentation For Models

 - [Attachment](docs/models/Attachment.md)
 - [City](docs/models/City.md)
 - [CopyTo](docs/models/CopyTo.md)
 - [CountStat](docs/models/CountStat.md)
 - [DeleteResponse](docs/models/DeleteResponse.md)
 - [Device](docs/models/Device.md)
 - [EmailMessage](docs/models/EmailMessage.md)
 - [EmailResponse](docs/models/EmailResponse.md)
 - [EventMetadata](docs/models/EventMetadata.md)
 - [ModelFrom](docs/models/ModelFrom.md)
 - [Os](docs/models/Os.md)
 - [QEmailMessage](docs/models/QEmailMessage.md)
 - [QEvent](docs/models/QEvent.md)
 - [RDSuppression](docs/models/RDSuppression.md)
 - [RSuppression](docs/models/RSuppression.md)
 - [ReplyTo](docs/models/ReplyTo.md)
 - [Suppression](docs/models/Suppression.md)
 - [SuppressionEmail](docs/models/SuppressionEmail.md)
 - [To](docs/models/To.md)
 - [UserAgent](docs/models/UserAgent.md)
 - [WebhookEvent](docs/models/WebhookEvent.md)

## Documentation For Authorization

 Endpoints do not require authorization.


## Author

dev@sendpost.io

```