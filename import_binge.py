"""Import binge data from Bindinc API."""

import time
from datetime import datetime, timedelta

import requests

from settings import settings


def get_rows(api_options, max_tries, offset):
    """Make request until maximum is reached. Return the 
    fetched rows.
    """
    url = api_options['url']
    headers = api_options['headers']
    parameters = api_options['parameters']
    parameters['offset'] = offset
    
    for i in range(max_tries):
        try:
            print(f'Requesting rows (offset = {offset}, try {i+1})...')
            response = requests.get(url, headers=headers, params=parameters)
            print(f'Response status: {response.status_code}')
            response.raise_for_status()
            if response.ok:
                break
        except:
            # Wait some time for next request.
            time.sleep((i + 2)**2)
    else:
        raise SystemError('Maximum number of request retries exceeded')
    return response.text


def main(api_options, file_options, max_tries, num_of_iterations):
    """Get rows from Bindinc API until rows are exhausted."""
    
    ndjson_file = file_options['file']
    file_mode = file_options['file_mode']
    limit = api_options['parameters']['limit']
    
    with open(ndjson_file, file_mode) as f:
        offset = 0
        i = 1
        while num_of_iterations:
            rows = get_rows(api_options, max_tries, offset)
            if rows:
                f.write(rows + '\n')
                offset += limit
            else:
                print(f'Rows exhausted.\nWritten to {ndjson_file}.')
                break
            i += 1
            if num_of_iterations and i == num_of_iterations:
                print(f'Maximum number of iterations ({i - 1}) reached.\n'
                      f'Written to {ndjson_file}.')
                break


if __name__ == '__main__':
    start_time = time.time()
    print(f'{datetime.now():%Y-%m-%d %H:%M}: Getting data from Bindinc API...')
    main(
        settings.bindinc_api_options,
        settings.ndjson_options,
        settings.request_max_num_of_tries,
        settings.num_of_iterations
    )
    elapsed = time.time() - start_time
    print(f'{datetime.now():%Y-%m-%d %H:%M}: finished\n'
          f'{timedelta(seconds=elapsed)}')
