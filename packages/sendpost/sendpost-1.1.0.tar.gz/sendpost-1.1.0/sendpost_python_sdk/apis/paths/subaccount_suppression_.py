from sendpost_python_sdk.paths.subaccount_suppression_.get import ApiForget
from sendpost_python_sdk.paths.subaccount_suppression_.post import ApiForpost
from sendpost_python_sdk.paths.subaccount_suppression_.delete import ApiFordelete


class SubaccountSuppression(
    ApiForget,
    ApiForpost,
    ApiFordelete,
):
    pass
