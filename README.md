# Celebrity Jet Usage Analyzer

A python analyzer that looks for correlations between celebrity jet usage, influence
and carbon impact on the planet. 

## Requirements

This project runs in Python 3.1x. Please ensure that you have an appropriate 
version of python installed.

The requirements.txt file contains all the dependencies to run this project. To
install all the requirements, we will be using pip. Usually, pip comes preinstalled
with python. To check that you have pip run:

```
pip --version
``` 

in BASH shells (MacOS/Linux) or:

```
python -m pip --version
```

in Windows. On the off chance that you have python and not pip, please follow
[this guide from the pip documentation](https://pip.pypa.io/en/stable/installation/).

Once you have pip installed you can run
```
pip install -r requirements.txt
```
in BASH shells (MaxOS/Linux) or:
```
pip install --upgrade -r requirements.txt
```

## API Key

An API key from [api-ninjas.com](https://www.api-ninjas.com/) is required to run this 
project. You need to create an account to create your own API key. If you do not
already have an account you can create it [here](https://www.api-ninjas.com/register).

NOTE: The api key from api-ninjas has a max calls of 10000 per month. This essay uses
~70 every time it runs so consider changing 
```
GATHER_API_DATA = False
```
in order to stop calling the api after you've run it the first time.

Once you have your account you need to retrieve your key and place it within the 
keys.py file.

First, retrieve your key by copying it from the [api-ninjas profile page](https://www.api-ninjas.com/profile).
You will have to click 'Show API Key' to see and copy your key in the profile page.

Next, open the keys.py file and and paste your key in between the quotation marks,
replacing YOUR API KEY HERE with your key. It should go from this:
```
def get_ninja_key():
    return "YOUR API KEY HERE"
```
to something like this:
```
def get_ninja_key():
    return "ABC1234xyz7890-FAKEKEY0987654321"
```

### You are now ready to run the computational essay