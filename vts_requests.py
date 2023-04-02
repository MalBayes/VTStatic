import secrets
import os
import json

config_filename = "plugin_config.json"
if os.path.isfile(config_filename):
    with open(config_filename) as file_handler:
        raw_config = file_handler.read()
        try:
            plugin_config = json.loads(raw_config)
        except json.decoder.JSONDecodeError:
            # Cannot read the file
            plugin_config = None


def gen_id():
    return secrets.token_hex(32)


def initialize_request_payload(req_type: str, req_id: str = gen_id()):
    request_payload = {
        "apiName": plugin_config["apiName"],
        "apiVersion": plugin_config["apiVersion"],
        "requestID": req_id,
        "messageType": req_type,
        "data": {}
    }
    return request_payload


def gen_status_check_request():
    return initialize_request_payload("APIStateRequest")


def gen_auth_token_request():
    request_payload = initialize_request_payload("AuthenticationTokenRequest")
    request_payload["data"].update({
        "pluginName": plugin_config["pluginName"],
        "pluginDeveloper": plugin_config["pluginDeveloper"],
        "pluginIcon": plugin_config["pluginIcon"]
    })
    return request_payload


def gen_auth_request(auth_token: str):
    request_payload = initialize_request_payload("AuthenticationRequest")
    request_payload["data"].update({
        "pluginName": plugin_config["pluginName"],
        "pluginDeveloper": plugin_config["pluginDeveloper"],
        "authenticationToken": auth_token
    })
    return request_payload


def gen_vts_stats_request():
    return initialize_request_payload("StatisticsRequest")


def gen_loaded_model_stats_request():
    return initialize_request_payload("CurrentModelRequest")


def gen_reload_current_model_request(model_id: str):
    request_payload = initialize_request_payload("ModelLoadRequest")
    request_payload["data"].update({
        "modelID": model_id
    })
    return request_payload


def gen_vts_parameters_list_request():
    return initialize_request_payload("StatisticsRequest")
