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
    'InstanceParameterLogsResult',
    'AwaitableInstanceParameterLogsResult',
    'instance_parameter_logs',
    'instance_parameter_logs_output',
]

@pulumi.output_type
class InstanceParameterLogsResult:
    """
    A collection of values returned by InstanceParameterLogs.
    """
    def __init__(__self__, end_time=None, id=None, instance_id=None, output_file=None, parameter_change_logs=None, start_time=None, total_count=None):
        if end_time and not isinstance(end_time, str):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, "end_time", end_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if parameter_change_logs and not isinstance(parameter_change_logs, dict):
            raise TypeError("Expected argument 'parameter_change_logs' to be a dict")
        pulumi.set(__self__, "parameter_change_logs", parameter_change_logs)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> str:
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> str:
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="parameterChangeLogs")
    def parameter_change_logs(self) -> 'outputs.InstanceParameterLogsParameterChangeLogsResult':
        """
        The collection of parameter change log query.
        """
        return pulumi.get(self, "parameter_change_logs")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of mongodb instance parameter log query.
        """
        return pulumi.get(self, "total_count")


class AwaitableInstanceParameterLogsResult(InstanceParameterLogsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return InstanceParameterLogsResult(
            end_time=self.end_time,
            id=self.id,
            instance_id=self.instance_id,
            output_file=self.output_file,
            parameter_change_logs=self.parameter_change_logs,
            start_time=self.start_time,
            total_count=self.total_count)


def instance_parameter_logs(end_time: Optional[str] = None,
                            instance_id: Optional[str] = None,
                            output_file: Optional[str] = None,
                            start_time: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableInstanceParameterLogsResult:
    """
    Use this data source to query detailed information of mongodb instance parameter logs
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.mongodb.instance_parameter_logs(end_time="2023-11-14 18:15Z",
        instance_id="mongo-replica-f16e9298b121",
        start_time="2022-11-14 00:00Z")
    ```


    :param str end_time: The end time to query.
    :param str instance_id: The instance ID to query.
    :param str output_file: File name where to save data source results.
    :param str start_time: The start time to query.
    """
    __args__ = dict()
    __args__['endTime'] = end_time
    __args__['instanceId'] = instance_id
    __args__['outputFile'] = output_file
    __args__['startTime'] = start_time
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:mongodb/instanceParameterLogs:InstanceParameterLogs', __args__, opts=opts, typ=InstanceParameterLogsResult).value

    return AwaitableInstanceParameterLogsResult(
        end_time=__ret__.end_time,
        id=__ret__.id,
        instance_id=__ret__.instance_id,
        output_file=__ret__.output_file,
        parameter_change_logs=__ret__.parameter_change_logs,
        start_time=__ret__.start_time,
        total_count=__ret__.total_count)


@_utilities.lift_output_func(instance_parameter_logs)
def instance_parameter_logs_output(end_time: Optional[pulumi.Input[str]] = None,
                                   instance_id: Optional[pulumi.Input[str]] = None,
                                   output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                   start_time: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[InstanceParameterLogsResult]:
    """
    Use this data source to query detailed information of mongodb instance parameter logs
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    foo = volcengine.mongodb.instance_parameter_logs(end_time="2023-11-14 18:15Z",
        instance_id="mongo-replica-f16e9298b121",
        start_time="2022-11-14 00:00Z")
    ```


    :param str end_time: The end time to query.
    :param str instance_id: The instance ID to query.
    :param str output_file: File name where to save data source results.
    :param str start_time: The start time to query.
    """
    ...
