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
    'ScalingConfigurationsResult',
    'AwaitableScalingConfigurationsResult',
    'scaling_configurations',
    'scaling_configurations_output',
]

@pulumi.output_type
class ScalingConfigurationsResult:
    """
    A collection of values returned by ScalingConfigurations.
    """
    def __init__(__self__, id=None, ids=None, name_regex=None, output_file=None, scaling_configuration_names=None, scaling_configurations=None, scaling_group_id=None, total_count=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if scaling_configuration_names and not isinstance(scaling_configuration_names, list):
            raise TypeError("Expected argument 'scaling_configuration_names' to be a list")
        pulumi.set(__self__, "scaling_configuration_names", scaling_configuration_names)
        if scaling_configurations and not isinstance(scaling_configurations, list):
            raise TypeError("Expected argument 'scaling_configurations' to be a list")
        pulumi.set(__self__, "scaling_configurations", scaling_configurations)
        if scaling_group_id and not isinstance(scaling_group_id, str):
            raise TypeError("Expected argument 'scaling_group_id' to be a str")
        pulumi.set(__self__, "scaling_group_id", scaling_group_id)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="scalingConfigurationNames")
    def scaling_configuration_names(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "scaling_configuration_names")

    @property
    @pulumi.getter(name="scalingConfigurations")
    def scaling_configurations(self) -> Sequence['outputs.ScalingConfigurationsScalingConfigurationResult']:
        """
        The collection of scaling configuration query.
        """
        return pulumi.get(self, "scaling_configurations")

    @property
    @pulumi.getter(name="scalingGroupId")
    def scaling_group_id(self) -> Optional[str]:
        """
        The id of the scaling group to which the scaling configuration belongs.
        """
        return pulumi.get(self, "scaling_group_id")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of scaling configuration query.
        """
        return pulumi.get(self, "total_count")


class AwaitableScalingConfigurationsResult(ScalingConfigurationsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ScalingConfigurationsResult(
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            output_file=self.output_file,
            scaling_configuration_names=self.scaling_configuration_names,
            scaling_configurations=self.scaling_configurations,
            scaling_group_id=self.scaling_group_id,
            total_count=self.total_count)


def scaling_configurations(ids: Optional[Sequence[str]] = None,
                           name_regex: Optional[str] = None,
                           output_file: Optional[str] = None,
                           scaling_configuration_names: Optional[Sequence[str]] = None,
                           scaling_group_id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableScalingConfigurationsResult:
    """
    Use this data source to query detailed information of scaling configurations
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.autoscaling.scaling_configurations(ids=["scc-ybrurj4uw6gh9zecj327"])
    ```


    :param Sequence[str] ids: A list of scaling configuration ids.
    :param str name_regex: A Name Regex of scaling configuration.
    :param str output_file: File name where to save data source results.
    :param Sequence[str] scaling_configuration_names: A list of scaling configuration names.
    :param str scaling_group_id: An id of scaling group.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['scalingConfigurationNames'] = scaling_configuration_names
    __args__['scalingGroupId'] = scaling_group_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:autoscaling/scalingConfigurations:ScalingConfigurations', __args__, opts=opts, typ=ScalingConfigurationsResult).value

    return AwaitableScalingConfigurationsResult(
        id=__ret__.id,
        ids=__ret__.ids,
        name_regex=__ret__.name_regex,
        output_file=__ret__.output_file,
        scaling_configuration_names=__ret__.scaling_configuration_names,
        scaling_configurations=__ret__.scaling_configurations,
        scaling_group_id=__ret__.scaling_group_id,
        total_count=__ret__.total_count)


@_utilities.lift_output_func(scaling_configurations)
def scaling_configurations_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                  name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                                  output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                  scaling_configuration_names: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                  scaling_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ScalingConfigurationsResult]:
    """
    Use this data source to query detailed information of scaling configurations
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.autoscaling.scaling_configurations(ids=["scc-ybrurj4uw6gh9zecj327"])
    ```


    :param Sequence[str] ids: A list of scaling configuration ids.
    :param str name_regex: A Name Regex of scaling configuration.
    :param str output_file: File name where to save data source results.
    :param Sequence[str] scaling_configuration_names: A list of scaling configuration names.
    :param str scaling_group_id: An id of scaling group.
    """
    ...
