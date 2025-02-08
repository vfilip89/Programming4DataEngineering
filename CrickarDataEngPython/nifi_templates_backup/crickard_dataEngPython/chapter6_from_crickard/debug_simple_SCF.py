import urllib.parse
import urllib.request
import json

# Function to fetch paginated data
def fetch_page_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            rawreply = response.read()
            reply = json.loads(rawreply)
            return reply
    except Exception as e:
        raise RuntimeError(f"Error fetching data from URL {url}: {e}")

# Initial API parameters
param = {'place_url': 'bernalillo-county', 'per_page': '100'}
base_url = 'https://seeclickfix.com/api/v2/issues?'
first_page_url = base_url + urllib.parse.urlencode(param)

try:
    # Fetch the first page
    data = fetch_page_data(first_page_url)
    all_issues = data.get('issues', [])

    # Check if pagination metadata exists
    if 'metadata' in data and 'pagination' in data['metadata']:
        pagination = data['metadata']['pagination']

        # Fetch the second page only
        if pagination['page'] == 1 and 'next_page_url' in pagination:
            second_page_url = pagination['next_page_url']
            second_page_data = fetch_page_data(second_page_url)
            all_issues.extend(second_page_data.get('issues', []))
        else:
            raise ValueError("Invalid pagination state. Expected page 1 with a next_page_url.")
    else:
        raise ValueError("Pagination metadata is missing in the input JSON.")

    # Save all issues to a file
    with open('all_issues.json', 'w') as f:
        json.dump(all_issues, f, indent=4)

    print(f"Fetched and saved {len(all_issues)} issues.")

except Exception as e:
    print(f"Error occurred: {e}")
