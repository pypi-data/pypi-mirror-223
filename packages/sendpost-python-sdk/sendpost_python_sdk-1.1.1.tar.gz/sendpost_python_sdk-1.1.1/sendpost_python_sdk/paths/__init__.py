# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from sendpost_python_sdk.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    SUBACCOUNT_EMAIL_ = "/subaccount/email/"
    SUBACCOUNT_EMAIL_TEMPLATE = "/subaccount/email/template"
    SUBACCOUNT_SUPPRESSION_ = "/subaccount/suppression/"
    SUBACCOUNT_SUPPRESSION_COUNT = "/subaccount/suppression/count"
