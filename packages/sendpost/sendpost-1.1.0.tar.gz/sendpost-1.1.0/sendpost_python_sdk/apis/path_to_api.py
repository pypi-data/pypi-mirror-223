import typing_extensions

from sendpost_python_sdk.paths import PathValues
from sendpost_python_sdk.apis.paths.subaccount_email_ import SubaccountEmail
from sendpost_python_sdk.apis.paths.subaccount_email_template import SubaccountEmailTemplate
from sendpost_python_sdk.apis.paths.subaccount_suppression_ import SubaccountSuppression
from sendpost_python_sdk.apis.paths.subaccount_suppression_count import SubaccountSuppressionCount

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.SUBACCOUNT_EMAIL_: SubaccountEmail,
        PathValues.SUBACCOUNT_EMAIL_TEMPLATE: SubaccountEmailTemplate,
        PathValues.SUBACCOUNT_SUPPRESSION_: SubaccountSuppression,
        PathValues.SUBACCOUNT_SUPPRESSION_COUNT: SubaccountSuppressionCount,
    }
)

path_to_api = PathToApi(
    {
        PathValues.SUBACCOUNT_EMAIL_: SubaccountEmail,
        PathValues.SUBACCOUNT_EMAIL_TEMPLATE: SubaccountEmailTemplate,
        PathValues.SUBACCOUNT_SUPPRESSION_: SubaccountSuppression,
        PathValues.SUBACCOUNT_SUPPRESSION_COUNT: SubaccountSuppressionCount,
    }
)
