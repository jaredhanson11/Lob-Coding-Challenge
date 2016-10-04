# Lob-Coding-Challenge
Mailgov:
Send a message directly to your governor.

Before using:

    1) Make sure dependencies are installed:
        # pip install -r path/to/requirements.txt

    2) Make sure api keys have been set.
        Create account with the Google api and obtain google civic enabled api key.
        Create account with lob and obtain api_key
        
        Options for setting api key:
            1) copy api keys into mailgov.py at line 93 and line 97
            2) set environment variables:
                # export lob_api_key='<your lob api key>'
                # export google_api_key='<your google api key>'

    3) (Optional) Set mailgov alias.
        Inside the directory containing mailgov.py, run:
            # alias mailgov='python mailgov.py'
        for a temporary alias.

Usage:

    if alias is set:
        # mailgov [tag] [path/to/inputs.json]
    if alias is not set:
        # python path/to/mailgov.py [tag] [path/to/inputs.json]

    possible tags:
        -h : show help
        -m : use inputs from json file

    If using -m, the input file must be a valid json file with the inputs in a dictionary.
    The dictionary can have the keys:
        'message', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip_code'
