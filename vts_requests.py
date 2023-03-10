import secrets
import string


def gen_id():
    return secrets.token_hex(32)


def gen_status_check_request(req_id: string = gen_id()):
    status_check: dict = {}
    status_check["apiName"] = "VTubeStudioPublicAPI"
    status_check["apiVersion"] = "1.0"
    status_check["requestID"] = req_id
    status_check["messageType"] = "APIStateRequest"
    return status_check


def gen_auth_token_request(req_id: string = gen_id()):
    token_request: dict = {}
    token_request["apiName"] = "VTubeStudioPublicAPI"
    token_request["apiVersion"] = "1.0"
    token_request["requestID"] = req_id
    token_request["messageType"] = "AuthenticationTokenRequest"
    token_request["data"] = {}
    token_request["data"]["pluginName"] = "Plugin Name"
    token_request["data"]["pluginDeveloper"] = "My Name"
    token_request["data"]["pluginIcon"] = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAACl0lEQVR4nO3c0VLrMAxFUZf//+fwBMOEJo1tWUrO2ev91rdoWx0opTUAAAAAAODiteRRt7adnLjmTAyJG8bZ0I9PJ4Zi8wMYGfz//wUhFPma+tcRw498HHQbu3krB8Y2SNW/AVbfVrZBqrmXADxeXwBZt5MtkOZ6ANlDIYIUvASYuxZA1W1kCyzHBjBHAOY+B1C9hqvPF8cGMEcA5gjAHAGYIwBzBGDucwDV789Xny+ODWCOAMxdC6BqDbP+l2MDmLseQPZt5Pan6NsAWUNh+Gl4CTDXH8Dq28ntTzX3xY58r57Bl5h7CYgaGsMvw6eDzfH3AQAAAAAA8GH5PfnWjn9O8TL7mtg82bOhH3GIQf4Jjgx+TzkE6d8HiBh+5OPckWTZKwemtg3kNsDq26q2DeQCQB+pALJup9IWkAkgeygqEcgEgDESAVTdRoUtIBEAxhGAuccHUL2Gq8+f9fgAMIcAzBGAOQIwRwDmCMDc4wOofn+++vxZjw8AcwjAnEQAVWv46eu/NZEAME4mgOzbqHD7WxMKoLW8oagMvzWxANBPLoDVt1Pp9rcm9mT2It+rVxv8D7kN8FfU0FSH35rwE9vj08HvyT/Bd/j7AAAAAAAAU3zPe0vbyQ+tXqEzI4DbOBv6kfkYCKDcyOD3xkOQfjPo/iKGP/c4bIASUYN/p28bsAHSrRx+/+MTgDkCSLX69vefQwBpsobfdx4BmCOAFNm3//q5BGCOAMwRwHJV6//a+QRgjgDMEYA5AjBHAOYIwBwBLBf7O3zR5xOAOQIwRwApql4GPp9LAOYIIE32Frh2HgGkyorg+jkEYI4A0q3eAn2PzwdDSkX+rsBYWGyAUlHbYPxx2AC3waeD8Svv7wMAAAAAAKx8Ayb6crJm3XwXAAAAAElFTkSuQmCC"
    return token_request


def gen_auth_request(auth_token: string, req_id: string = gen_id()):
    token_request: dict = {}
    token_request["apiName"] = "VTubeStudioPublicAPI"
    token_request["apiVersion"] = "1.0"
    token_request["requestID"] = req_id
    token_request["messageType"] = "AuthenticationRequest"
    token_request["data"] = {}
    token_request["data"]["pluginName"] = "Plugin Name"
    token_request["data"]["pluginDeveloper"] = "My Name"
    token_request["data"]["authenticationToken"] = auth_token
    return token_request

def gen_vts_stats_request(req_id: string = gen_id()):
    vts_stats: dict = {}
    vts_stats["apiName"] = "VTubeStudioPublicAPI"
    vts_stats["apiVersion"] = "1.0"
    vts_stats["requestID"] = req_id
    vts_stats["messageType"] = "StatisticsRequest"
    return vts_stats


def gen_loaded_model_stats_request(req_id: string = gen_id()):
    loaded_model_status: dict = {}
    loaded_model_status["apiName"] = "VTubeStudioPublicAPI"
    loaded_model_status["apiVersion"] = "1.0"
    loaded_model_status["requestID"] = req_id
    loaded_model_status["messageType"] = "CurrentModelRequest"
    return loaded_model_status


def gen_reload_current_model_request(model_id, req_id: string = gen_id()):
    reload_current_model_request = {}
    reload_current_model_request["apiName"] = "VTubeStudioPublicAPI"
    reload_current_model_request["apiVersion"] = "1.0"
    reload_current_model_request["requestID"] = req_id
    reload_current_model_request["messageType"] = "ModelLoadRequest"
    reload_current_model_request["data"] = {}
    reload_current_model_request["data"]["modelID"] = model_id
    return reload_current_model_request