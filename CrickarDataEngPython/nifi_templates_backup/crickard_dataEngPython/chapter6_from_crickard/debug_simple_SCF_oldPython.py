import urllib
import urllib2
import json

# Function to fetch paginated data
def fetch_page_data(url):
    try:
        rawreply = urllib2.urlopen(url).read()
        reply = json.loads(rawreply)
        return reply
    except Exception as e:
        raise RuntimeError("Error fetching data from URL {}: {}".format(url, e))

# Initial API parameters
param = {'place_url': 'bernalillo-county', 'per_page': '100'}
base_url = 'https://seeclickfix.com/api/v2/issues?'
first_page_url = base_url + urllib.urlencode(param)

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

    # Print only the first 5 issues
    print("Fetched {} issues. Showing the first 5:".format(len(all_issues)))
    print(json.dumps(all_issues[:5], indent=4))  # Slice the list to print only the first 5 issues

except Exception as e:
    print("Error occurred: {}".format(e))
