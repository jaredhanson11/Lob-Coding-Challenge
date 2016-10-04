import sys
import os
import json

import requests
from googleapiclient.discovery import build, HttpError
import lob

help_message = \
'''
Mailgov:
Send a message directly to your governor.

Before using:

    1) Make sure dependencies are installed:
        # pip install -r path/to/requirements.txt
    2) Make sure api keys have been set.
        Create account with the Google api and obtain google civic enabled api key.
        Create account with lob and obtain api_key

        Options:
            - copy api keys into mailgov.py at line 93 and line 97
            - set environment variables:
                # export google_api_key='<your google api key>'
                # export lob_api_key='<your lob api key>'
                (optional)
                # export lob_api_version='<your lob api version>'
    3) (Optional) Set mailgov alias.
        # alias mailgov='python full/path/to/mailgov.py'
        Note:
            Make sure to include the full path from root to mailgov.py when setting alias.

Usage:

    if alias is set, then run:
        # mailgov [tag] [path/to/inputs.json]

    if alias is not set, then run:
        # python path/to/mailgov.py [tag] [path/to/inputs.json]

    possible tags:
        -h : show help
        -m : use inputs from json file

    If using -m, the input file must be a valid json file with the inputs in a dictionary. The dictionary can have the keys, 'message', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip_code'
'''

def main():

    if len(sys.argv) != 1:
        if sys.argv[1] == '-h':
            print help_message
            return

        elif sys.argv[1] == '-m':
            if len(sys.argv) != 3:
                print_err('Invalid inputs')
                return
            try:
                user_inputs = json.load(open(sys.argv[2]))
            except:
                print_err('Invalid file name, file type, and/or file content.')
                return

            name = user_inputs.get('name', '')
            address_line1 = user_inputs.get('address_line1', '')
            address_line2 = user_inputs.get('address_line2', '')
            city = user_inputs.get('city', '')
            state = user_inputs.get('state', '')
            zip_code = user_inputs.get('zip_code', '')
            message = user_inputs.get('message', '')

        else:
            print_err('Invalid Inputs')
            print help_message
            return
    else:
        name = raw_input('Enter your full name: ')
        address_line1 = raw_input('Enter your address line1: ')
        address_line2 = raw_input('Enter your address line2: ')
        city = raw_input('Enter your city: ')
        state = raw_input('Enter your state: ')
        zip_code = raw_input('Enter your zip: ')
        message = raw_input('Enter a message to your governor: ')

    if message == '':
        error = 'The message is missing or invalid.'
        print_err(error)
        return

    address = ' '.join((address_line1, address_line2, city, state, zip_code))

    # Set up lob api
    lob.api_version = os.environ.get('lob_api_version', '2016-06-30')
    lob.api_key = os.environ.get('lob_api_key', None)
    # lob.api_key = ### YOUR API KEY HERE, IF NOT IN ENVIRONMENT ###

    # Set up google civic information api client
    google_api_key = os.environ.get('google_api_key', None)
    # google_api_key = ### YOUR API KEY HERE, IF NOT IN ENVIRONMENT ###

    if lob.api_key is None or google_api_key is None:
        error = 'An api key is not set.'
        print_err(error)
        return

    service = build('civicinfo', 'v2', developerKey=google_api_key)

    try:
        query = service.representatives().representativeInfoByAddress(
            levels='administrativeArea1',
            roles='headOfGovernment',
            address=address
        ).execute()

    except HttpError, e:
        err_info = json.loads(e.__dict__['content'])
        print err_info
        error = 'code: %s -- %s' % (err_info['error']['code'], err_info['error']['message'])
        print '\n'
        print_err(error)
        return

    for official in query.get('offices', []):
        if official['name'] == 'Governor':
            gov_index = official['officialIndices'][0]
            governor = query['officials'][gov_index]
            break
    else:
        # Only gets here if governor isn't an option, then return error.
        error = 'There is no Governor for the given address.'
        print '\n'
        print_err(error)
        return

    from_address = {
        'name': name,
        'address_line1': query['normalizedInput']['line1'],
        'address_line2': query['normalizedInput'].get('line2', ''),
        'address_city': query['normalizedInput']['city'],
        'address_state': query['normalizedInput']['state'],
        'address_zip': query['normalizedInput']['zip'],
        'address_country': 'US'
    }

    to_address = {
        'name': governor['name'],
        'address_line1': governor['address'][0]['line1'],
        'address_city': governor['address'][0]['city'],
        'address_state': governor['address'][0]['state'],
        'address_zip': governor['address'][0]['zip'],
        'address_country': 'US'
    }

    try:
        response = lob.Letter.create(
            description = 'Letter to Governor',
            to_address = to_address,
            from_address = from_address,
            file = open('letter.html').read(),
            data = {
                'message': message,
                'gov_name': governor['name'],
                'name': name
            },
            color = True
        )
    except lob.error.InvalidRequestError, e:
        error = 'Address line 1 is missing or incorrect.'
        print_err(error)
        return


    print '\n'
    print_success(governor['name'],response['url'])
    return

def print_err(error):
    '''Prints the error to the user.'''
    print 'There was an error: '
    print '\t%s\n' % error
    print 'For more help on the error:\n\t# mailgov -h'

def print_success(gov_name, url):
    print 'Your message was sent to %s. Check out the letter at:'
    print '\t%s\n' % url


main()
