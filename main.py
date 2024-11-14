import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier


def get_listener_count(url):
    # Fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {url}: status code {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table with class 'btable'
    table = soup.find("table", {"class": "btable"})
    if not table:
        print("Could not find table with class 'btable'")
        return None

    # Get all the rows in the table
    rows = table.find_all("tr")
    if len(rows) < 2:
        print("Table does not contain enough rows")
        return None

    # Get the header row and data row
    header_row = rows[0]
    data_row = rows[1]

    # Find the index of the 'Listeners' column
    headers = header_row.find_all("th")
    header_texts = [header.get_text(strip=True) for header in headers]
    try:
        listener_index = header_texts.index("Listeners")
    except ValueError:
        print("Could not find 'Listeners' column")
        return None

    # Get the listener count from the data row
    data_cells = data_row.find_all("td")
    if len(data_cells) <= listener_index:
        print("Data row does not contain enough cells")
        return None
    listener_cell = data_cells[listener_index]
    listener_count = listener_cell.get_text(strip=True)
    return listener_count


def send_notification(listener_count):
    # Create a ToastNotifier object
    notifier = ToastNotifier()
    # Display the notification
    notifier.show_toast(
        "Newton PD Listener Count",
        f"Current listeners: {listener_count}",
        duration=10,
    )


# Main function
if __name__ == "__main__":
    url = "https://www.broadcastify.com/listen/feed/32397"
    listener_count = get_listener_count(url)

    if listener_count:
        print(f"Current listeners: {listener_count}")
        send_notification(listener_count)
    else:
        print("Failed to retrieve listener count.")
