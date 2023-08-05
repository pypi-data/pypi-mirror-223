# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'RegistriesResult',
    'AwaitableRegistriesResult',
    'registries',
    'registries_output',
]

@pulumi.output_type
class RegistriesResult:
    """
    A collection of values returned by Registries.
    """
    def __init__(__self__, id=None, names=None, output_file=None, registries=None, statuses=None, total_count=None, types=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if registries and not isinstance(registries, list):
            raise TypeError("Expected argument 'registries' to be a list")
        pulumi.set(__self__, "registries", registries)
        if statuses and not isinstance(statuses, list):
            raise TypeError("Expected argument 'statuses' to be a list")
        pulumi.set(__self__, "statuses", statuses)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)
        if types and not isinstance(types, list):
            raise TypeError("Expected argument 'types' to be a list")
        pulumi.set(__self__, "types", types)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def names(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def registries(self) -> Sequence['outputs.RegistriesRegistryResult']:
        """
        The collection of registry query.
        """
        return pulumi.get(self, "registries")

    @property
    @pulumi.getter
    def statuses(self) -> Optional[Sequence['outputs.RegistriesStatusResult']]:
        return pulumi.get(self, "statuses")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of registry query.
        """
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter
    def types(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "types")


class AwaitableRegistriesResult(RegistriesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return RegistriesResult(
            id=self.id,
            names=self.names,
            output_file=self.output_file,
            registries=self.registries,
            statuses=self.statuses,
            total_count=self.total_count,
            types=self.types)


def registries(names: Optional[Sequence[str]] = None,
               output_file: Optional[str] = None,
               statuses: Optional[Sequence[pulumi.InputType['RegistriesStatusArgs']]] = None,
               types: Optional[Sequence[str]] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableRegistriesResult:
    """
    Use this data source to query detailed information of cr registries
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.cr.registries(statuses=[volcengine.cr.RegistriesStatusArgs(
        condition="Ok",
        phase="Running",
    )])
    ```


    :param Sequence[str] names: The list of registry names to query.
    :param str output_file: File name where to save data source results.
    :param Sequence[pulumi.InputType['RegistriesStatusArgs']] statuses: The list of registry statuses.
    :param Sequence[str] types: The list of registry types to query.
    """
    __args__ = dict()
    __args__['names'] = names
    __args__['outputFile'] = output_file
    __args__['statuses'] = statuses
    __args__['types'] = types
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:cr/registries:Registries', __args__, opts=opts, typ=RegistriesResult).value

    return AwaitableRegistriesResult(
        id=__ret__.id,
        names=__ret__.names,
        output_file=__ret__.output_file,
        registries=__ret__.registries,
        statuses=__ret__.statuses,
        total_count=__ret__.total_count,
        types=__ret__.types)


@_utilities.lift_output_func(registries)
def registries_output(names: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                      output_file: Optional[pulumi.Input[Optional[str]]] = None,
                      statuses: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['RegistriesStatusArgs']]]]] = None,
                      types: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[RegistriesResult]:
    """
    Use this data source to query detailed information of cr registries
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.cr.registries(statuses=[volcengine.cr.RegistriesStatusArgs(
        condition="Ok",
        phase="Running",
    )])
    ```


    :param Sequence[str] names: The list of registry names to query.
    :param str output_file: File name where to save data source results.
    :param Sequence[pulumi.InputType['RegistriesStatusArgs']] statuses: The list of registry statuses.
    :param Sequence[str] types: The list of registry types to query.
    """
    ...
