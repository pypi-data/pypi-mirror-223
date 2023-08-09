# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from humanloop.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    PROJECTS = "Projects"
    EXPERIMENTS = "Experiments"
    COMPLETIONS = "Completions"
    CHATS = "Chats"
    LOGS = "Logs"
    SESSIONS = "Sessions"
    EVALUATIONS = "Evaluations"
    FEEDBACK = "Feedback"
    MODEL_CONFIGURATIONS = "Model Configurations"
    TRACES = "Traces"
    AUTHENTICATION = "Authentication"
