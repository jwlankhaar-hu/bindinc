"""Module that governs all project settings."""

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class _Settings:
    """Settings class. To be instantiated only once.
    """
    base_dir = Path.cwd()
    data_dir = base_dir / 'data'
    secrets_dir = base_dir / 'secure'
    
    bindinc_api_key_file = secrets_dir / 'bindinc_api_key'
    bindinc_api_options = {
        'url': 'http://bvodclcpreview.bindinc.nl/customer/api/content',
        'headers': {
            'Authorization': f'Bearer {bindinc_api_key_file.read_text()}'
        },
        'parameters': {
            'source': 1,
            'limit': 250
        }
    }
    request_max_num_of_tries = 5

    # Maximum number of iterations. If None, all data will be retrieved.
    num_of_iterations = 1   
    
    ndjson_options = {
        'file': data_dir / 'binge.ndjson',
        
        # Append ('at') or overwrite ('wt') existing NDJSON file.
        'file_mode': 'wt',   # append: "at", overwrite: "wt"
        
        # Fields to export (use dots for nested fields).
        'export_fields' : [
            'available.from',
            'available.to',
            'available.channel',
            'available.channel.code',
            'typology.genres',
            'production.countries',
            'production.year',
            'production.original_length',
            'title.title',
            'title.series.title'            
        ]
    }
    
    csv_options = {
        'file': data_dir / 'binge.csv',
        
        # Append ('at') or overwrite ('wt') existing CSV file.
        'file_mode': 'at', 
        
        # CSV export specification.
        'format_options' : {
            'delimiter': ',', 
            'quotechar': '"', 
            'quoting': csv.QUOTE_ALL, 
            'lineterminator': '\n'
        },
        
        # Delimiter character for concatenated values 
        # of a multi-value NDJSON field.
        'multivalue_delimiter': '|'
    }
    
    
# In other modules, import the object, not the class.
settings = _Settings()