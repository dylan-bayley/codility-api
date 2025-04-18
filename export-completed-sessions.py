"""
Interactive script to export completed Codility test sessions to CSV.

This script lists all available tests, prompts for a test name, finds its ID,
retrieves sessions for that test, filters those that have completed (end_time present),
and writes each candidate's first name, last name, email, all session data fields,
and all similarity result fields into a CSV file. Nested structures are JSON-encoded.

Usage:
    export CODILITY_API_KEY="your_api_key"
    python export_completed_sessions.py
"""
import os
import csv
import sys
import json
from codility_api_client import CodilityAPIClient


def flatten_data(session_data: dict, similarity_data: dict) -> dict:
    """
    Flatten session and similarity dicts into a single-level dict,
    prefixing keys to avoid collisions and JSON-encoding nested structures.
    """
    record = {}
    # Session fields (excluding candidate)
    for key, value in session_data.items():
        if key == 'candidate':
            continue
        record[f"session_{key}"] = json.dumps(value) if isinstance(value, (dict, list)) else value

    # Similarity fields
    for key, value in similarity_data.items():
        record[f"similarity_{key}"] = json.dumps(value) if isinstance(value, (dict, list)) else value

    return record


def main():
    api_key = os.getenv("CODILITY_API_KEY")
    if not api_key:
        print("Error: Please set the CODILITY_API_KEY environment variable.")
        sys.exit(1)

    client = CodilityAPIClient(api_key=api_key)

    # List available tests
    tests_resp = client.list_tests()
    tests = tests_resp.get('tests', [])
    if not tests:
        print("No tests found in your account.")
        sys.exit(0)

    print("Available tests:")
    for t in tests:
        name = t.get('title') or t.get('name') or '<unnamed>'
        print(f"  {t['id']}: {name}")

    test_name = input("\nEnter the exact name of the test to export: ").strip()
    matches = [t for t in tests if (t.get('title') == test_name) or (t.get('name') == test_name)]
    if not matches:
        print(f"No test found with name '{test_name}'")
        sys.exit(1)
    test_id = matches[0]['id']

    # Retrieve all sessions for the selected test
    sessions_resp = client.list_test_sessions(test_id)
    sessions = sessions_resp.get('sessions', [])

    completed_records = []
    for sess in sessions:
        session_id = sess.get('id')
        data = client.get_session_data(session_id)
        # Only include sessions with an end_time (completed)
        if not data.get('end_time'):
            continue

        similarity = client.get_similarity_results(session_id)
        candidate = data.get('candidate', {})

        # Flatten
        record = flatten_data(data, similarity)
        # Add candidate fields
        record['first_name'] = candidate.get('firstName', '')
        record['last_name'] = candidate.get('lastName', '')
        record['email'] = candidate.get('email', '')

        completed_records.append(record)

    if not completed_records:
        print("No completed sessions found for this test.")
        sys.exit(0)

    # Determine CSV columns from record keys
    fieldnames = sorted(completed_records[0].keys())

    # Safe filename
    safe_name = test_name.replace(' ', '_')
    filename = f"{safe_name}_completed_sessions.csv"

    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(completed_records)

    print(f"Exported {len(completed_records)} records to '{filename}'")


if __name__ == '__main__':
    main()
