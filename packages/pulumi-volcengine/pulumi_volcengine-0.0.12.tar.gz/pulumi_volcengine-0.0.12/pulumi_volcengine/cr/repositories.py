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
    'RepositoriesResult',
    'AwaitableRepositoriesResult',
    'repositories',
    'repositories_output',
]

@pulumi.output_type
class RepositoriesResult:
    """
    A collection of values returned by Repositories.
    """
    def __init__(__self__, access_levels=None, id=None, names=None, namespaces=None, output_file=None, registry=None, repositories=None, total_count=None):
        if access_levels and not isinstance(access_levels, list):
            raise TypeError("Expected argument 'access_levels' to be a list")
        pulumi.set(__self__, "access_levels", access_levels)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if namespaces and not isinstance(namespaces, list):
            raise TypeError("Expected argument 'namespaces' to be a list")
        pulumi.set(__self__, "namespaces", namespaces)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if registry and not isinstance(registry, str):
            raise TypeError("Expected argument 'registry' to be a str")
        pulumi.set(__self__, "registry", registry)
        if repositories and not isinstance(repositories, list):
            raise TypeError("Expected argument 'repositories' to be a list")
        pulumi.set(__self__, "repositories", repositories)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)

    @property
    @pulumi.getter(name="accessLevels")
    def access_levels(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "access_levels")

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
    @pulumi.getter
    def namespaces(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "namespaces")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def registry(self) -> str:
        return pulumi.get(self, "registry")

    @property
    @pulumi.getter
    def repositories(self) -> Sequence['outputs.RepositoriesRepositoryResult']:
        """
        The collection of repository query.
        """
        return pulumi.get(self, "repositories")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of instance query.
        """
        return pulumi.get(self, "total_count")


class AwaitableRepositoriesResult(RepositoriesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return RepositoriesResult(
            access_levels=self.access_levels,
            id=self.id,
            names=self.names,
            namespaces=self.namespaces,
            output_file=self.output_file,
            registry=self.registry,
            repositories=self.repositories,
            total_count=self.total_count)


def repositories(access_levels: Optional[Sequence[str]] = None,
                 names: Optional[Sequence[str]] = None,
                 namespaces: Optional[Sequence[str]] = None,
                 output_file: Optional[str] = None,
                 registry: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableRepositoriesResult:
    """
    Use this data source to query detailed information of cr repositories
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.cr.repositories(names=["repo*"],
        registry="tf-1")
    ```


    :param Sequence[str] access_levels: The list of instance access level.
    :param Sequence[str] names: The list of instance names.
    :param Sequence[str] namespaces: The list of instance namespace.
    :param str output_file: File name where to save data source results.
    :param str registry: The CR instance name.
    """
    __args__ = dict()
    __args__['accessLevels'] = access_levels
    __args__['names'] = names
    __args__['namespaces'] = namespaces
    __args__['outputFile'] = output_file
    __args__['registry'] = registry
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:cr/repositories:Repositories', __args__, opts=opts, typ=RepositoriesResult).value

    return AwaitableRepositoriesResult(
        access_levels=__ret__.access_levels,
        id=__ret__.id,
        names=__ret__.names,
        namespaces=__ret__.namespaces,
        output_file=__ret__.output_file,
        registry=__ret__.registry,
        repositories=__ret__.repositories,
        total_count=__ret__.total_count)


@_utilities.lift_output_func(repositories)
def repositories_output(access_levels: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        names: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        namespaces: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                        registry: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[RepositoriesResult]:
    """
    Use this data source to query detailed information of cr repositories
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.cr.repositories(names=["repo*"],
        registry="tf-1")
    ```


    :param Sequence[str] access_levels: The list of instance access level.
    :param Sequence[str] names: The list of instance names.
    :param Sequence[str] namespaces: The list of instance namespace.
    :param str output_file: File name where to save data source results.
    :param str registry: The CR instance name.
    """
    ...
