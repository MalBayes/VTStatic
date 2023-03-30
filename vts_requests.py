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
    token_request["data"]["pluginName"] = "VTStatic"
    token_request["data"]["pluginDeveloper"] = "Mal Bayes"
    token_request["data"]["pluginIcon"] = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAIAAABMXPacAAAACXBIWXMAAC4jAAAuIwF4pT92AAAH+ElEQVR4nO3abUhT3x8A8HO3q5ub5nNtupaVgUllzzNNe7KMEFJfFPlCRITIoNDyhUFREAhFjaQoFetNJaJZkA8UwWo2LUN60DTSpOkyU8GHzc25e+79v5CGbPfqHu74/378vp932zn3fL/7nt2ze88dQgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAkoiFLxQKxfbt2wmCYO1qNBo1Gg3G2MuQJEmmpKSEhISwtppMJq1Wa7Va7e/ExMRs2bLFy6CsMMbNzc0URbG2SqVSpVIZFRUllUqFQqH34fr7+7u6uhzeJBe+oCjqwoULcXFxrMebTKaCgoLm5mYv89i/f/+jR49EIhFr640bNzQajf1lRETE3bt3k5OTvQzqjGGYqqqq58+fO7y/evXqgwcPHjp0aOPGjcHBwSKRiJfqj46OnjhxYul+WVlZRqOR4fDp0yeZTOZNHitXruzq6uIaX6fTLV++3N5ZJBKp1WqKorj6e0On0zmchWFhYVeuXNHr9bxHNJvNhYWFAoFg6QKRJHnr1i2uDDDGd+7c8fgbERAQcP/+fa4sx8fHExMT7Z0JgsjPzzeZTPzWYt7Q0NCGDRsW5iaXy1+8eOGLycYYV1RUiMViV8skk8nev3/PNZzRaMzMzPSg+gKBIC8vb3Z2livLoqKihVOblJQ0ODjIeznmP8KxY8cW5ubn51dXV0fTtC/CabVauVzuXrHS0tLGx8e5Ruzp6YmKinJ3AhISEvR6PdeYz549CwwMtHeOjo5ua2vzRTlsNltZWZnDSZyRkWG1Wn0RTq/X79y5091aIaFQePnyZZvNxjooxri6upokyaUH+is0NLSxsZEry8HBwdjYWHtniUTy4MEDjDHv5aBpurGxcdmyZQ7p1dTU8B6LYRiTyZSbm8t1VTmPvYgY4/Ly8uTk5LS0NOdWgUCQk5PT0tJSX1/vSvVJkjx16tThw4dZW+fm5kpKSn78+GF/JzExUalUtre3LzKmv7//jh07WJu6urqmp6dZmyYnJ4uKihxaBQLBrl27WPtbLJafP39OTU15dvH96tWr2tpahmE8OBYhhFQqlcFg4JregYGB6OhoV8Y5cODAIgtaRUWFw4JAuEAul3P9YKampi5yoHN6UqmU9afearUWFxeHh4cLBAJXUnIxnBsIgjh79izX4kjT9MOHD5dciBQKxbt377iq393dHR4e7kFuMpmMawJSUlLcGkoqlc7MzDiPYzAYFi6M/x9BQUFPnjzhKh9FUcePH1/kcJFIdPv2ba6rC5PJlJqa6lliPE6AUCj89euX8zgzMzNZWVn+/v6eZeiiJb6/RqPx0qVLmzdvXrNmjXOrUCi8efNmW1vb0NCQcytBENnZ2Xl5eaxnIsb4+vXrWq3Ws7x5hDHu6OhwvraWSCSVlZVardZgMJjNZtcHpChqcnJyYGCgt7d3eHh4/sbWqxRzc3O5rt8ZhqmtrWXdV4iLi+vr6+M6SqPRBAQEeJwSj2cAQig7O9sXl6EWi6Wjo6OkpEQmk3n1eyAWi6urq7lWEpqmnS+2pFJpQ0MDV2Z//vyJj4/3PCG+J4AkyYaGBh/diDEM8/nz5927d3s1B0ql8uvXr1wBRkZG1q5da+9MEERxcfHc3Bxr59nZ2YKCAs9TQQjxPQEIocjIyKamJh/tOzEMo9frN23a5NVnzsjIMJvNXAGePn1qX1JUKtXo6ChrN5qmHz9+7P3+Iu8TgBASi8WFhYV9fX0URfnibGhoaHDej3PjpPDz8ysrKzt37hxXh5MnT1ZVVYWEhDQ3Ny/cVlvo+/fve/fu/f37t+txWclkMoPBwDqRqampra2tHo/s7++vUqmSk5Pj4+MVCoVEInFpFxMhhBBBEJGRkQqFgjWxsbGxPXv29Pb2epwbEolE5eXlXDNstVrPnDmj0+m4OvT09MTExHgefgFfnAF8CQ0NbW9vd06MoqicnBxvR5fL5R8/fuQqscVi4drDmZqaOnr0KB8fEKF/9gQghOrr650To2k6Pz/foaerJ5fdyMjI+fPnTSYTa6tYLGY9YTHGlZWVTU1N7ob7dxEIBMHBwenp6awrMMbY+X7CjR3NeQzDvHnzRq1WX7x40fWjdDrdtWvXuJ6+/nMoFIp79+6tWLHCs8MJgggICIiOjg4ODnZutVgsBoPBuwT/CgkJefv2LddC5GB4eJj3h7q+WIIkEklNTY0vtsHnffv2LSwsjLcSbNu2bWJiYsmo83uKrl9IuIj3CSAIorS0lOvexXsY46tXr/JZgvm7rcW/LzRN19XVBQUF8RkYIeSDCThy5Igr3yePdXR0uLh77waRSNTS0rJI1J6envXr1/McFSHE9wTExsb29/f7pvIMxvjDhw9bt271RR3QqlWrvnz5whpYr9enp6f7JCqvExAYGPjy5Utf3PpSFDU0NKRWq5VKJVd0t6+CHOj1+szMTLVavW/fPvtSYzabOzs7S0tL29ravByfC03TY2NjrDecNpvNraFOnz6dkJAwPj7OV2Jzc3MTExPd3d2vX7/WaDQDAwM0TXP19+6Z2V9+fn5JSUkqlSoiImJ6erqzs7O1tZXrXoEXJElyPa4aHBx0a/t+3bp1vPz3DSHEMIzNZpuenp6YmPD+P5wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAf9v/AJch9qzbrxl0AAAAAElFTkSuQmCC"
    return token_request


def gen_auth_request(auth_token: string, req_id: string = gen_id()):
    token_request: dict = {}
    token_request["apiName"] = "VTubeStudioPublicAPI"
    token_request["apiVersion"] = "1.0"
    token_request["requestID"] = req_id
    token_request["messageType"] = "AuthenticationRequest"
    token_request["data"] = {}
    token_request["data"]["pluginName"] = "VTStatic"
    token_request["data"]["pluginDeveloper"] = "Mal Bayes"
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

def gen_vts_parameters_list_request(req_id: string = gen_id()):
    vts_stats: dict = {}
    vts_stats["apiName"] = "VTubeStudioPublicAPI"
    vts_stats["apiVersion"] = "1.0"
    vts_stats["requestID"] = req_id
    vts_stats["messageType"] = "StatisticsRequest"
    return vts_stats
