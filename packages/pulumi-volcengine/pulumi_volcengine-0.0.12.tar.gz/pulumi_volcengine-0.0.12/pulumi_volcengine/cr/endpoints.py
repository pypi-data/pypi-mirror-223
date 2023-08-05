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
    'EndpointsResult',
    'AwaitableEndpointsResult',
    'endpoints',
    'endpoints_output',
]

@pulumi.output_type
class EndpointsResult:
    """
    A collection of values returned by Endpoints.
    """
    def __init__(__self__, endpoints=None, id=None, output_file=None, registry=None, total_count=None):
        if endpoints and not isinstance(endpoints, list):
            raise TypeError("Expected argument 'endpoints' to be a list")
        pulumi.set(__self__, "endpoints", endpoints)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if registry and not isinstance(registry, str):
            raise TypeError("Expected argument 'registry' to be a str")
        pulumi.set(__self__, "registry", registry)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)

    @property
    @pulumi.getter
    def endpoints(self) -> Sequence['outputs.EndpointsEndpointResult']:
        """
        The collection of endpoint query.
        """
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def registry(self) -> str:
        """
        The name of CR instance.
        """
        return pulumi.get(self, "registry")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of tag query.
        """
        return pulumi.get(self, "total_count")


class AwaitableEndpointsResult(EndpointsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return EndpointsResult(
            endpoints=self.endpoints,
            id=self.id,
            output_file=self.output_file,
            registry=self.registry,
            total_count=self.total_count)


def endpoints(output_file: Optional[str] = None,
              registry: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableEndpointsResult:
    """
    Use this data source to query detailed information of cr endpoints
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.cr.endpoints(registry="tf-1")
    ```


    :param str output_file: File name where to save data source results.
    :param str registry: The CR instance name.
    """
    __args__ = dict()
    __args__['outputFile'] = output_file
    __args__['registry'] = registry
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:cr/endpoints:Endpoints', __args__, opts=opts, typ=EndpointsResult).value

    return AwaitableEndpointsResult(
        endpoints=__ret__.endpoints,
        id=__ret__.id,
        output_file=__ret__.output_file,
        registry=__ret__.registry,
        total_count=__ret__.total_count)


@_utilities.lift_output_func(endpoints)
def endpoints_output(output_file: Optional[pulumi.Input[Optional[str]]] = None,
                     registry: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[EndpointsResult]:
    """
    Use this data source to query detailed information of cr endpoints
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.cr.endpoints(registry="tf-1")
    ```


    :param str output_file: File name where to save data source results.
    :param str registry: The CR instance name.
    """
    ...
