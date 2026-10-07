"""
Sample / Anonymized Company Catalog for Corporate Indemnity Form Generator.

This sample file illustrates the data schema expected by generate_all_final_forms.py
without exposing confidential corporate filings, personal identity records,
or signature assets.
"""

SAMPLE_COMPANIES = [
    {
        'name': 'ACME PACIFIC HOLDINGS (PRIVATE) LIMITED',
        'reg_no': 'PV 00123456',
        'office': 'NO. 100, GALLE ROAD, COLOMBO 03, POSTCODE: 00300',
        'instruction': 'ALL',
        'folder_name': 'ACME PACIFIC HOLDINGS (PRIVATE) LIMITED',
        'file_prefix': 'ACME PACIFIC HOLDINGS (PRIVATE) LIMITED',
        'incorp_day': '15',
        'incorp_ord': 'TH',
        'incorp_month_year': 'NOV 2022',
        'signing_day': '22',
        'signing_ord': 'nd',
        'signing_month_year': 'Nov 2022',
        'signatory_name': 'JOHN ALEXANDER DOE',
        'signatory_sig': None,  # In production: path to signature image
        'directors': [
            {
                'name': 'JOHN ALEXANDER DOE',
                'id_lines': ['Passport No: N1234567', 'Country: United Kingdom'],
                'address_paragraphs': [
                    'Local Address',
                    'No. 100, Galle Road, Colombo 03, Postcode: 00300',
                    'Foreign Address',
                    '25 High Street, Kensington, London, Zipcode: W8 5SE, United Kingdom'
                ],
                'sig_file': None
            },
            {
                'name': 'SARAH JANE SMITH',
                'id_lines': ['NIC No: 198512345678'],
                'address_paragraphs': [
                    'No. 45, Flower Road, Colombo 07, Postcode: 00700'
                ],
                'sig_file': None
            }
        ],
        'shareholders': [
            {
                'name': 'JOHN ALEXANDER DOE',
                'id_lines': ['Passport No: N1234567'],
                'address_paragraphs': [
                    'Local Address',
                    'No. 100, Galle Road, Colombo 03, Postcode: 00300',
                    'Foreign Address',
                    '25 High Street, Kensington, London, Zipcode: W8 5SE, United Kingdom'
                ],
                'sig_file': None
            },
            {
                'name': 'ACME VENTURES GLOBAL LIMITED',
                'id_lines': ['Company Reg: HE 987654'],
                'address_paragraphs': [
                    'Foreign Address',
                    '100 Wall Street, 15th Floor, New York, Zipcode: 10005, USA'
                ],
                'sig_file': None
            }
        ]
    }
]

ALL_COMPANIES = SAMPLE_COMPANIES
