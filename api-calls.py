import requests

class CodilityAPIClient:
    """
    Client for Codility API.

    Usage:
        client = CodilityAPIClient(api_key='your_api_key', base_url='https://codility.com/api')
    """

    def __init__(self, api_key: str, base_url: str = 'https://codility.com/api'):
        """
        Initialize the Codility API client.

        :param api_key: Your Codility API key.
        :param base_url: Base URL for the Codility API (no trailing slash).
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        })

    def get_user_details(self) -> dict:
        """
        Retrieve user details.

        GET /account/user

        :return: JSON response with user details.
        """
        url = f"{self.base_url}/account/user"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_available_credits(self) -> dict:
        """
        Retrieve the current amount of credits available.

        GET /account/credits

        :return: JSON response with credits information.
        """
        url = f"{self.base_url}/account/credits"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_user_logins(self) -> dict:
        """
        List user login events.

        GET /account/logins

        :return: JSON response with login records.
        """
        url = f"{self.base_url}/account/logins"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    # CodeLive endpoints

    def list_codelive_templates(self) -> dict:
        """
        List all CodeLive templates.

        GET /codelive/templates

        :return: JSON response with template list.
        """
        url = f"{self.base_url}/codelive/templates"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_codelive_session(self, template_id: str, candidate_info: dict) -> dict:
        """
        Create a new CodeLive session based on a template.

        POST /codelive/sessions

        :param template_id: ID of the CodeLive template to use.
        :param candidate_info: Candidate details for the session.
        :return: JSON response with session details.
        """
        url = f"{self.base_url}/codelive/sessions"
        payload = {'template_id': template_id, **candidate_info}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def create_whiteboard(self, session_id: str) -> dict:
        """
        Create a whiteboard for an existing CodeLive session.

        POST /codelive/whiteboards

        :param session_id: ID of the CodeLive session.
        :return: JSON response with whiteboard URL/details.
        """
        url = f"{self.base_url}/codelive/whiteboards"
        payload = {'session_id': session_id}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    # Email Templates endpoints

    def list_email_templates(self) -> dict:
        """
        Retrieve all saved email templates.

        GET /email/templates

        :return: JSON response with email templates.
        """
        url = f"{self.base_url}/email/templates"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_default_email_template(self) -> dict:
        """
        Retrieve the default email template.

        GET /email/templates/default

        :return: JSON response with default template.
        """
        url = f"{self.base_url}/email/templates/default"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_email_template(self, name: str, subject: str, body: str) -> dict:
        """
        Create a new custom email template.

        POST /email/templates

        :param name: Name for the new template.
        :param subject: Email subject placeholder text.
        :param body: Email body placeholder text.
        :return: JSON response with created template details.
        """
        url = f"{self.base_url}/email/templates"
        payload = {'name': name, 'subject': subject, 'body': body}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    # Session endpoints

    def list_sessions(self) -> dict:
        """
        List all candidate sessions.

        GET /sessions

        :return: JSON response with all sessions.
        """
        url = f"{self.base_url}/sessions"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_session_data(self, session_id: str) -> dict:
        """
        Browse data for a specific candidate session.

        GET /sessions/{session_id}

        :param session_id: ID of the candidate session.
        :return: JSON response with session data.
        """
        url = f"{self.base_url}/sessions/{session_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_pdf_report(self, session_id: str) -> bytes:
        """
        Retrieve a PDF report for a session.

        GET /sessions/{session_id}/report/pdf

        :param session_id: ID of the candidate session.
        :return: Raw PDF bytes.
        """
        url = f"{self.base_url}/sessions/{session_id}/report/pdf"
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

    def get_similarity_results(self, session_id: str) -> dict:
        """
        Get similarity check results for a session.

        GET /sessions/{session_id}/similarity

        :param session_id: ID of the candidate session.
        :return: JSON response with similarity details.
        """
        url = f"{self.base_url}/sessions/{session_id}/similarity"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def email_candidates(self, session_id: str, email_template_id: str) -> dict:
        """
        Email findings to candidates for a session.

        POST /sessions/{session_id}/email

        :param session_id: ID of the candidate session.
        :param email_template_id: The email template to use.
        :return: JSON response with email status.
        """
        url = f"{self.base_url}/sessions/{session_id}/email"
        payload = {'template_id': email_template_id}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def cancel_session(self, session_id: str) -> None:
        """
        Cancel an existing candidate session.

        DELETE /sessions/{session_id}

        :param session_id: ID of the candidate session.
        """
        url = f"{self.base_url}/sessions/{session_id}"
        response = self.session.delete(url)
        response.raise_for_status()

    def embed_candidate_report(self, session_id: str) -> dict:
        """
        Get embed configuration for a candidate report.

        GET /sessions/{session_id}/embed

        :param session_id: ID of the candidate session.
        :return: JSON response with embed details.
        """
        url = f"{self.base_url}/sessions/{session_id}/embed"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    # Test endpoints

    def list_tests(self) -> dict:
        """
        Browse all available tests.

        GET /tests

        :return: JSON response with test list.
        """
        url = f"{self.base_url}/tests"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_test_details(self, test_id: str) -> dict:
        """
        Retrieve details for a specific test.

        GET /tests/{test_id}

        :param test_id: ID of the test.
        :return: JSON response with test details.
        """
        url = f"{self.base_url}/tests/{test_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_test_sessions(self, test_id: str) -> dict:
        """
        List all sessions for a specific test.

        GET /tests/{test_id}/sessions

        :param test_id: ID of the test.
        :return: JSON response with sessions for the given test.
        """
        url = f"{self.base_url}/tests/{test_id}/sessions"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def add_candidates(self, test_id: str, candidates: list) -> dict:
        """
        Add candidates to a specific test.

        POST /tests/{test_id}/candidates

        :param test_id: ID of the test.
        :param candidates: List of candidate dicts (e.g., [{'email': ..., 'name': ...}, ...]).
        :return: JSON response with invitation status.
        """
        url = f"{self.base_url}/tests/{test_id}/candidates"
        payload = {'candidates': candidates}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
