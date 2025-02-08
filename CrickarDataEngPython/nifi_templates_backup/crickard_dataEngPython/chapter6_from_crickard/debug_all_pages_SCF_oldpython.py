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
    # Fetch all pages
    current_page_url = first_page_url
    all_issues = []
    total_entries = 0  # To track total entries from metadata
    total_pages = 0    # To track total pages from metadata

    while current_page_url:
        # Fetch the current page
        data = fetch_page_data(current_page_url)
        issues = data.get('issues', [])
        all_issues.extend(issues)

        # Extract pagination metadata
        if 'metadata' in data and 'pagination' in data['metadata']:
            pagination = data['metadata']['pagination']
            if total_entries == 0:
                total_entries = pagination['entries']
                total_pages = pagination['pages']
                print("Total entries available: {}".format(total_entries))
                print("Total pages available: {}".format(total_pages))

            print("Processing page {} of {}".format(pagination['page'], total_pages))
            current_page_url = pagination.get('next_page_url')
        else:
            break

    # Validate the total fetched issues
    print("Fetched {} issues out of {} expected.".format(len(all_issues), total_entries))

    # Print only the first 5 issues for inspection
    print("Showing the first 5 issues:")
    print(json.dumps(all_issues[:5], indent=4))  # Slice the list to print only the first 5 issues

except Exception as e:
    print("Error occurred: {}".format(e))
