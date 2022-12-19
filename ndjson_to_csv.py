"""Export and NDJSON file to CSV."""

import csv
import re
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
        if isinstance(node, dict):
            if top_key in node:
                return get_nested_key(
                    node[top_key],
                    nested_keys,
                    multivalue_delim
                )
            else:
                return ''
        elif isinstance(node, list):
            if '[' in key:
                k, filter_dict = parse_node_filter_spec(key)
                matching_nodes = [n for n in node
                                  if k in n and node_contains(n, filter_dict)]
                return multivalue_delim.join(str(n[k]) for n in matching_nodes)
            return multivalue_delim.join(
                get_nested_key(item, nested_keys, multivalue_delim)
                for item in node
            )
    elif isinstance(node, dict):
        return str(node.get(key, ''))
    else:
        return multivalue_delim.join(
            get_nested_key(item, key, multivalue_delim)
            for item in node
        )


def parse_node_filter_spec(filter_spec):
    """Parse the filter specification and return a tuple of the form
    (key, filter_dict) that contains the key of interest and a
    dictionary that should be contained in the node to be filtered.

    Example:
        filter_spec = 'identifiers.id[source="Binge",level="program"]'
        parse_node_filter_spec(filter_spec)
        > ('identifiers', {'source': 'Binge', 'level': 'program'})
    """
    # Get key and filter string.
    pattern = re.compile(r'([^\]]+)\[([^\]]+)\]')  # https://regex101.com/r/b9yZtr/1
    m = pattern.match(filter_spec)
    key = m.group(1)
    filter_string = m.group(2)

    # Get key-value pairs in the filter string.
    pattern_kv = re.compile(r'([^\=]+)\="([^"]+)",?') # https://regex101.com/r/DzjSEc/1
    filter_dict = dict(pattern_kv.findall(filter_string))

    return (key, filter_dict)


def node_contains(node, partial_node):
    """Return True if all keys and values of partial_node match
    those in node.
    """
    return all(k in node and node[k] == v
               for k, v in partial_node.items())


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
    
    is_new_csv = not csv_file.exists()
    with (open(ndjson_file, 'rt', encoding='utf8') as f_ndjson,
          open(csv_file, csv_mode, encoding='utf8') as f_csv):
        reader = ndjson.reader(f_ndjson, strict=False)
        writer = csv.writer(f_csv, **csv_format)
        
        # In case of new file, write column headers.
        if is_new_csv:
            writer.writerow(fields)
        for row in reader:
            writer.writerow(parse_row(row, fields, multivalue_delim))
        

if __name__ == '__main__':
    main(settings.ndjson_options, settings.csv_options)
    