"""API for connecting to the preamble.com AI safety backend from within NeMo Guardrails projects."""

from typing import Optional
from nemoguardrails.actions import action
from preamble import preamble_core


# If you have custom catchall / wildcard flows in your application instead of using our recommended CATCHALL_FLOWS_FOR_PREAMBLE_INTEGRATION catchalls,
# then please integrate the relevant calls to execute preamble_input_policies and execute preamble_output_policies
# at the appropriate places in your catchall flows.
CATCHALL_FLOWS_FOR_PREAMBLE_INTEGRATION = """

define bot preamble_fn1
    "(remove last message)"

define bot preamble_fn2
    "I'm sorry, I can't help you with that."

define flow
    user ...
    $input_is_safe = execute preamble_input_policies
    if $input_is_safe
        bot respond
    else
        bot preamble_fn2

define flow
    bot ...
    $output_is_safe = execute preamble_output_policies
    if not $output_is_safe
        bot preamble_fn1
        bot preamble_fn2
"""


def install(app, api_key):
    """Call this once, before using the other functions in this module.
    This will set the API key -> preamble_core,
    and it will install the two required NeMo actions. (preamble_input_policies and preamble_output_policies)
    The "app" parameter should be the object you created by doing app = LLMRails(config)"""
    preamble_core.set_access_token(api_key)
    
    app.register_action(preamble_input_policies, name="preamble_input_policies")
    app.register_action(preamble_output_policies, name="preamble_output_policies")

    return True


_active_input_policies = []
_active_output_policies = []

def activate_policy(policy_name):
    assert policy_name in preamble_core.POLICY_NAME_TO_ID
    policy_type = preamble_core.POLICY_NAME_TO_POLICY_TYPE[policy_name]

    if policy_type == preamble_core.INPUT_POLICY:
        if policy_name not in _active_input_policies:
            _active_input_policies.append(policy_name)
    if policy_type == preamble_core.OUTPUT_POLICY:
        if policy_name not in _active_output_policies:
            _active_output_policies.append(policy_name)

    return True


@action()
async def preamble_input_policies(
    context: Optional[dict] = None
):
    user_message = context.get("last_user_message")
    
    input_is_safe = True
    for policy_name in _active_input_policies:
        score = preamble_core.eval_policy(policy_name, user_message)
        threshold = preamble_core.get_threshold(policy_name)
        if score < threshold:
            input_is_safe = False
            break
    return input_is_safe


@action()
async def preamble_output_policies(
    context: Optional[dict] = None
):
    bot_message = context.get("last_bot_message")
    
    output_is_safe = True
    for policy_name in _active_output_policies:
        score = preamble_core.eval_policy(policy_name, bot_message)
        threshold = preamble_core.get_threshold(policy_name)
        if score < threshold:
            output_is_safe = False
            break
    return output_is_safe
