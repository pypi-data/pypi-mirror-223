# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'UsersResult',
    'AwaitableUsersResult',
    'users',
    'users_output',
]

@pulumi.output_type
class UsersResult:
    """
    A collection of values returned by Users.
    """
    def __init__(__self__, id=None, name_regex=None, output_file=None, total_count=None, user_names=None, users=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)
        if user_names and not isinstance(user_names, list):
            raise TypeError("Expected argument 'user_names' to be a list")
        pulumi.set(__self__, "user_names", user_names)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of user query.
        """
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter(name="userNames")
    def user_names(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "user_names")

    @property
    @pulumi.getter
    def users(self) -> Sequence['outputs.UsersUserResult']:
        """
        The collection of user.
        """
        return pulumi.get(self, "users")


class AwaitableUsersResult(UsersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return UsersResult(
            id=self.id,
            name_regex=self.name_regex,
            output_file=self.output_file,
            total_count=self.total_count,
            user_names=self.user_names,
            users=self.users)


def users(name_regex: Optional[str] = None,
          output_file: Optional[str] = None,
          user_names: Optional[Sequence[str]] = None,
          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableUsersResult:
    """
    Use this data source to query detailed information of iam users
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.iam.users()
    ```


    :param str name_regex: A Name Regex of IAM.
    :param str output_file: File name where to save data source results.
    :param Sequence[str] user_names: A list of user names.
    """
    __args__ = dict()
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['userNames'] = user_names
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:iam/users:Users', __args__, opts=opts, typ=UsersResult).value

    return AwaitableUsersResult(
        id=__ret__.id,
        name_regex=__ret__.name_regex,
        output_file=__ret__.output_file,
        total_count=__ret__.total_count,
        user_names=__ret__.user_names,
        users=__ret__.users)


@_utilities.lift_output_func(users)
def users_output(name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                 output_file: Optional[pulumi.Input[Optional[str]]] = None,
                 user_names: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[UsersResult]:
    """
    Use this data source to query detailed information of iam users
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.iam.users()
    ```


    :param str name_regex: A Name Regex of IAM.
    :param str output_file: File name where to save data source results.
    :param Sequence[str] user_names: A list of user names.
    """
    ...
