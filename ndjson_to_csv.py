"""Export and NDJSON file to CSV."""

import csv
from pathlib import Path

import ndjson
from settings import settings


def parse_row(json_node, fields, multivalue_delim):
    """Parse one NDJSON row. Retrieve the value of the fields to load
    and flatten them in a single list of strings.
    """
    row = []
    for field in fields:
        row.append(get_nested_key(json_node, field, multivalue_delim))
    return row


def get_nested_key(node, key, multivalue_delim):
    """Return a value from a node. Nesting level is encoded with dots.
    Values of multi-valued nodes (i.e. lists) are delimited with a
    concatenation character.
    """
    if '.' in key:
        top_key, nested_keys = key.split('.', maxsplit=1)
        if type(node) is dict:
            if top_key in node:
                return get_nested_key(
                    node[top_key], 
                    nested_keys, 
                    multivalue_delim
                )
            else:
                return ''
        elif type(node) is list:
            return multivalue_delim.join(
                get_nested_key(item, nested_keys, multivalue_delim) 
                for item in node
            )
    else:
        if type(node) is dict:
            return node.get(key, '')
        else:
            return multivalue_delim.join(
                get_nested_key(item, key, multivalue_delim) 
                for item in node
            )
    

def main(ndjson_options, csv_options):
    """Load NDJSON file and write a selection of the fields to a CSV 
    file.
    """
    ndjson_file = ndjson_options['file']
    fields = ndjson_options['export_fields']
    csv_file = csv_options['file']
    csv_mode = csv_options['file_mode']
    csv_format = csv_options['format_options']
    multivalue_delim = csv_options['multivalue_delimiter']
    
    with (open(ndjson_file, 'rt', encoding='utf8') as f_ndjson, 
          open(csv_file, csv_mode, encoding='utf8') as f_csv):
        reader = ndjson.reader(f_ndjson, strict=False)
        writer = csv.writer(f_csv, **csv_format)
        
        # In case of new file, write column headers.
        if csv_mode == 'wt':
            writer.writerow(fields) 
        for row in reader:
            writer.writerow(parse_row(row, fields, multivalue_delim))
        

if __name__ == '__main__':
    main(settings.ndjson_options, settings.csv_options)
    