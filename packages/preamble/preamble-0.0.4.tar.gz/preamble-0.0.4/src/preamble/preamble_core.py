"""API for connecting to the preamble.com AI safety backend.  This file contains common functionality."""

import json, requests

# Map from policy_name to policy_id
POLICY_NAME_TO_ID = {
    # Prompt Defender [Preamble] is a policy developed in-house by Preamble to prevent jailbreaks and other types of prompt attacks.
    # This is an INPUT policy, which means it evaluates the safety of the user input.  So, you should pass the user's input (the prompt) as the text parameter.
    # The score returned ranges from 0.0 (input is a dangerous prompt attack) thru 1.0 (input is benign).
    "Prompt Defender [Preamble]": "a3451c53-a056-4a5b-9465-24b714d79981",

    # No Code Generation [Preamble] is a policy developed in-house by Preamble to prevent the generation of computer code (programming language code).
    # This is an OUTPUT policy, which means it evaluates the safety of the LLM's output.  So, you should pass the LLM's output as the text parameter.
    # The score returned ranges from 0.0 (output contains code) thru 1.0 (output does not contain code).
    "No Code Generation [Preamble]": "3ebca3e0-2c4b-45d1-8f19-0f87649c1af8",

    # No PII [Preamble] is a policy developed in-house by Preamble to prevent the outputting of certain kinds of PII (Personally Identifiable Information).
    # This is an OUTPUT policy, which means it evaluates the safety of the LLM's output.  So, you should pass the LLM's output as the text parameter.
    # The score returned ranges from 0.0 (output contains PII) thru 1.0 (output does not contain PII).
    "No PII [Preamble]": "fe02e8f3-673c-4e2f-82e5-6a1783038371",

    # No Phishing Emails [Preamble] is a policy developed in-house by Preamble to prevent the outputting of phishing emails.
    # This is an OUTPUT policy, which means it evaluates the safety of the LLM's output.  So, you should pass the LLM's output as the text parameter.
    # The score returned ranges from 0.0 (output is a phishing email) thru 1.0 (output is benign).
    "No Phishing Emails [Preamble]": "9869b569-ff70-4ecc-8e2e-e8bc2995689c",
}

INPUT_POLICY = "Input Policy" # 
OUTPUT_POLICY = "Output Policy"
POLICY_NAME_TO_POLICY_TYPE = {
    "Prompt Defender [Preamble]": INPUT_POLICY,
    "No Code Generation [Preamble]": OUTPUT_POLICY,
    "No PII [Preamble]": OUTPUT_POLICY,
    "No Phishing Emails [Preamble]": OUTPUT_POLICY,
}

POLICY_NAME_TO_EMBEDDING_MODEL = {
    "Prompt Defender [Preamble]": "text-embedding-ada-002",
    "No Code Generation [Preamble]": "text-embedding-ada-002",
    "No PII [Preamble]": "text-embedding-ada-002",
    "No Phishing Emails [Preamble]": "text-embedding-ada-002",
}

DEFAULT_THRESHOLD = 0.5
SCORE_ON_ERROR = 0.4999 # If there is an API error, treat the text's score as being slightly unsafe (err on the side of caution).
PREAMBLE_SERVER_ENDPOINT = "https://capybara-convo-dot-preamble.uc.r.appspot.com/policies/test"

_preamble_access_token = None

def set_access_token(api_key):
    """Call this once at the beginning, before using the other functions in this module.
    Also call this if your access token expired and you need to provide a new one."""
    _preamble_access_token = api_key

def eval_policy(policy_name, text):
    assert policy_name in POLICY_NAME_TO_ID
    policy_id = POLICY_NAME_TO_ID[policy_name]
    embedding_model = POLICY_NAME_TO_EMBEDDING_MODEL[policy_name]

    headers = {
        "Authorization": f"Bearer {_preamble_access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "policyId": policy_id,
        "modelId": embedding_model,
        "text": text,
    }

    response = requests.post(
        PREAMBLE_SERVER_ENDPOINT,
        headers=headers,
        json=payload,
    )

    result_json = response.text

    try:
        result_obj = json.loads(result_json)

        if "error" in result_obj and result_obj["error"] is not None:
            return SCORE_ON_ERROR
        if "confidence" not in result_obj:
            return SCORE_ON_ERROR

        return result_obj["confidence"]

    except json.JSONDecodeError:
        return SCORE_ON_ERROR

def get_threshold(policy_name):
    # In the future we should pull the per-policy threshold from the server database.  (But cache the looked-up value at runtime so we don't make multiple unnecessary calls.)
    # Our plan to call the server in the future is why this is a function instead of a constant lookup table.
    assert policy_name in POLICY_NAME_TO_ID
    return DEFAULT_THRESHOLD
