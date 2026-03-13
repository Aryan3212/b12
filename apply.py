import os
import json
import hmac
import hashlib
from datetime import datetime, timezone
import requests

def main():
    # Use environment variables for the application details
    # This allows flexibility and keeps secrets safe
    name = os.getenv("APP_NAME", "Aryan Rahman")
    email = os.getenv("APP_EMAIL", "57558971+Aryan3212@users.noreply.github.com")
    
    # GitHub Action default environment variables
    server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    repository = os.getenv("GITHUB_REPOSITORY", "Aryan3212/b12") # Updated repository name
    run_id = os.getenv("GITHUB_RUN_ID", "local")
    
    repository_link = f"{server_url}/{repository}"
    action_run_link = f"{repository_link}/actions/runs/{run_id}"
    
    # Resume filename found in the repo
    resume_filename = "aryan rahman resume.md"
    # Assuming main branch, we encode the filename for the URL
    resume_link = f"https://github.com/Aryan3212/b12/blob/main/aryan%20rahman%20resume.md"

    # Current ISO 8601 timestamp in UTC
    timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")

    payload_dict = {
        "action_run_link": action_run_link,
        "email": email,
        "name": name,
        "repository_link": repository_link,
        "resume_link": resume_link,
        "timestamp": timestamp
    }

    # Canonicalize the JSON: 
    # - keys sorted alphabetically
    # - no extra whitespace (compact separators)
    # - UTF-8 encoded
    payload_json = json.dumps(payload_dict, sort_keys=True, separators=(',', ':'))
    payload_bytes = payload_json.encode('utf-8')

    # Signing secret
    signing_secret = "hello-there-from-b12"
    
    # Calculate HMAC-SHA256
    signature_digest = hmac.new(
        signing_secret.encode('utf-8'),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature_digest}"
    }

    print(f"Submitting payload: {payload_json}")
    
    response = requests.post(
        "https://b12.io/apply/submission",
        data=payload_bytes,
        headers=headers
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        try:
            res_json = response.json()
            if res_json.get("success"):
                print(f"Submission successful! Receipt: {res_json.get('receipt')}")
            else:
                print("Submission failed according to response body.")
        except Exception as e:
            print(f"Error parsing response: {e}")
    else:
        print(f"Request failed with status {response.status_code}")

if __name__ == "__main__":
    main()
