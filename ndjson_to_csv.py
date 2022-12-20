"""Export and NDJSON file to CSV."""

import csv

from jsonpath import JSONPath

import ndjson
from settings import settings


def parse_row(json_node, field_specifications, delim):
    """Parse one NDJSON row. Retrieve the value of the fields to load
    and flatten them in a single list of strings.
    """
    row = []
    for spec in field_specifications:
        value = delim.join(str(v) for v in JSONPath(spec).parse(json_node))
        row.append(value)
    return row


def main(ndjson_options, csv_options):
    """Load NDJSON file and write a selection of the fields to a CSV
    file.
    """
    ndjson_file = ndjson_options['file']
    field_specs = ndjson_options['export_field_specifications']
    csv_file = csv_options['file']
    csv_mode = csv_options['file_mode']
    csv_format = csv_options['format_options']
    delim = csv_options['multivalue_delimiter']
    
    is_new_csv = not csv_file.exists()
    with (open(ndjson_file, 'rt', encoding='utf8') as f_ndjson,
          open(csv_file, csv_mode, encoding='utf8') as f_csv):
        reader = ndjson.reader(f_ndjson, strict=False)
        writer = csv.writer(f_csv, **csv_format)
        
        # In case of new file, write column headers.
        if is_new_csv:
            writer.writerow(field_specs.keys())
        for row in reader:
            writer.writerow(parse_row(row, field_specs.values(), delim))
        

if __name__ == '__main__':
    main(settings.ndjson_options, settings.csv_options)
    