# Codility API Client

This repository contains a Python client (`codility_api_client.py`) for interacting with the Codility REST API. The client provides convenient methods for all publicly documented endpoints: account management, CodeLive sessions, email templates, candidate sessions, and test management.

---

## Prerequisites

- **Python 3.7+**
- [requests](https://pypi.org/project/requests/) library


## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/codility-client.git
   cd codility-client
   ```

2. **Create a virtual environment** (optional, but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # on macOS/Linux
   venv\Scripts\activate     # on Windows
   ```

3. **Install dependencies**

   ```bash
   pip install requests
   ```


## Configuration

The client uses Bearer token authentication. You need a Codility API key. You can supply it directly when instantiating the client, or set it as an environment variable and read it in your code.

```bash
export CODILITY_API_KEY="your_api_key_here"
```


## Usage

```python
from codility_api_client import CodilityAPIClient
import os

# Read API key from environment, or replace with your key
api_key = os.getenv('CODILITY_API_KEY', 'YOUR_API_KEY')

# Instantiate the client
client = CodilityAPIClient(
    api_key=api_key,
    base_url='https://codility.com/api'  # default value
)

# Example: get your account details
user = client.get_user_details()
print("Logged in as:", user['email'])

# Example: list all tests
tests = client.list_tests()
for t in tests.get('tests', []):
    print(f"Test {t['id']}: {t['title']}")
```

### Available Methods

| Category           | Method                                          | Description                                    |
|--------------------|-------------------------------------------------|------------------------------------------------|
| **Account**        | `get_user_details()`                            | Retrieve your user profile                     |
|                    | `get_available_credits()`                       | Check your current credit balance              |
|                    | `list_user_logins()`                            | List your recent login events                  |
| **CodeLive**       | `list_codelive_templates()`                     | Retrieve all CodeLive templates                |
|                    | `create_codelive_session(template_id, info)`    | Start a new CodeLive session                   |
|                    | `create_whiteboard(session_id)`                 | Generate a whiteboard for a session            |
| **Email**          | `list_email_templates()`                        | List all saved email templates                 |
|                    | `get_default_email_template()`                  | Retrieve the default email template            |
|                    | `create_email_template(name, subject, body)`    | Create a custom email template                 |
| **Sessions**       | `list_sessions()`                               | List all candidate sessions                    |
|                    | `get_session_data(session_id)`                  | Fetch details for a specific session           |
|                    | `get_pdf_report(session_id)`                    | Download a PDF report for a session            |
|                    | `get_similarity_results(session_id)`            | Retrieve code similarity results               |
|                    | `email_candidates(session_id, template_id)`     | Email report to candidates                     |
|                    | `cancel_session(session_id)`                    | Cancel a candidate session                     |
|                    | `embed_candidate_report(session_id)`            | Get embed configuration for report             |
| **Tests**          | `list_tests()`                                  | Browse all available tests                     |
|                    | `get_test_details(test_id)`                     | Retrieve metadata for a test                   |
|                    | `list_test_sessions(test_id)`                   | List sessions taken for a given test           |
|                    | `add_candidates(test_id, candidates_list)`      | Invite candidates to take a test               |


## Error Handling

All methods call `response.raise_for_status()` to raise an exception on HTTP errors (4xx and 5xx responses). Wrap your calls in `try/except` if you need to handle errors gracefully.

```python
try:
    credits = client.get_available_credits()
    print("Credits:", credits['available'])
except requests.HTTPError as e:
    print("API request failed:", e)
```


## Contributing

Contributions are welcome! Please open issues or submit pull requests on GitHub.


## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

