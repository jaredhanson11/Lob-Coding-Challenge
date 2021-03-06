# Mailgov
A command line tool used to send a message directly to your governor, using API's from Lob and Google Civic Information.

Before using:

    1) Make sure dependencies are installed:
        # pip install -r path/to/requirements.txt
    2) Make sure api keys have been set.
        Create account with the Google api and obtain google civic enabled api key.
        Create account with lob and obtain api_key

        Options:
            - copy api keys into mailgov.py at line 93 and line 97
            - set environment variables:
                # export google_api_key=<your google api key>
                # export lob_api_key=<your lob api key>
                (optional)
                # export lob_api_version=<your lob api version>
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

    If using -m, the input file must be a valid json file with the inputs in a dictionary.
    The dictionary can have the keys:
        'message', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip_code'
