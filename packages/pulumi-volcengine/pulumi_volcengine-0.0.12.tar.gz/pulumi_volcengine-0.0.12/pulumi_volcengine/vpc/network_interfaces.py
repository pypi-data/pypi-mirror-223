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
    'NetworkInterfacesResult',
    'AwaitableNetworkInterfacesResult',
    'network_interfaces',
    'network_interfaces_output',
]

@pulumi.output_type
class NetworkInterfacesResult:
    """
    A collection of values returned by NetworkInterfaces.
    """
    def __init__(__self__, id=None, ids=None, instance_id=None, network_interface_ids=None, network_interface_name=None, network_interfaces=None, output_file=None, primary_ip_addresses=None, private_ip_addresses=None, project_name=None, security_group_id=None, status=None, subnet_id=None, tags=None, total_count=None, type=None, vpc_id=None, zone_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if network_interface_ids and not isinstance(network_interface_ids, list):
            raise TypeError("Expected argument 'network_interface_ids' to be a list")
        pulumi.set(__self__, "network_interface_ids", network_interface_ids)
        if network_interface_name and not isinstance(network_interface_name, str):
            raise TypeError("Expected argument 'network_interface_name' to be a str")
        pulumi.set(__self__, "network_interface_name", network_interface_name)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if primary_ip_addresses and not isinstance(primary_ip_addresses, list):
            raise TypeError("Expected argument 'primary_ip_addresses' to be a list")
        pulumi.set(__self__, "primary_ip_addresses", primary_ip_addresses)
        if private_ip_addresses and not isinstance(private_ip_addresses, list):
            raise TypeError("Expected argument 'private_ip_addresses' to be a list")
        pulumi.set(__self__, "private_ip_addresses", private_ip_addresses)
        if project_name and not isinstance(project_name, str):
            raise TypeError("Expected argument 'project_name' to be a str")
        pulumi.set(__self__, "project_name", project_name)
        if security_group_id and not isinstance(security_group_id, str):
            raise TypeError("Expected argument 'security_group_id' to be a str")
        pulumi.set(__self__, "security_group_id", security_group_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)
        if zone_id and not isinstance(zone_id, str):
            raise TypeError("Expected argument 'zone_id' to be a str")
        pulumi.set(__self__, "zone_id", zone_id)

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
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[str]:
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="networkInterfaceIds")
    def network_interface_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "network_interface_ids")

    @property
    @pulumi.getter(name="networkInterfaceName")
    def network_interface_name(self) -> Optional[str]:
        """
        The name of the ENI.
        """
        return pulumi.get(self, "network_interface_name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Sequence['outputs.NetworkInterfacesNetworkInterfaceResult']:
        """
        The collection of ENI.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="primaryIpAddresses")
    def primary_ip_addresses(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "primary_ip_addresses")

    @property
    @pulumi.getter(name="privateIpAddresses")
    def private_ip_addresses(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "private_ip_addresses")

    @property
    @pulumi.getter(name="projectName")
    def project_name(self) -> Optional[str]:
        """
        The ProjectName of the ENI.
        """
        return pulumi.get(self, "project_name")

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> Optional[str]:
        return pulumi.get(self, "security_group_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the ENI.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        The id of the subnet to which the ENI is connected.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.NetworkInterfacesTagResult']]:
        """
        Tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of ENI query.
        """
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the ENI.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        The id of the virtual private cloud (VPC) to which the ENI belongs.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[str]:
        """
        The zone id of the ENI.
        """
        return pulumi.get(self, "zone_id")


class AwaitableNetworkInterfacesResult(NetworkInterfacesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return NetworkInterfacesResult(
            id=self.id,
            ids=self.ids,
            instance_id=self.instance_id,
            network_interface_ids=self.network_interface_ids,
            network_interface_name=self.network_interface_name,
            network_interfaces=self.network_interfaces,
            output_file=self.output_file,
            primary_ip_addresses=self.primary_ip_addresses,
            private_ip_addresses=self.private_ip_addresses,
            project_name=self.project_name,
            security_group_id=self.security_group_id,
            status=self.status,
            subnet_id=self.subnet_id,
            tags=self.tags,
            total_count=self.total_count,
            type=self.type,
            vpc_id=self.vpc_id,
            zone_id=self.zone_id)


def network_interfaces(ids: Optional[Sequence[str]] = None,
                       instance_id: Optional[str] = None,
                       network_interface_ids: Optional[Sequence[str]] = None,
                       network_interface_name: Optional[str] = None,
                       output_file: Optional[str] = None,
                       primary_ip_addresses: Optional[Sequence[str]] = None,
                       private_ip_addresses: Optional[Sequence[str]] = None,
                       project_name: Optional[str] = None,
                       security_group_id: Optional[str] = None,
                       status: Optional[str] = None,
                       subnet_id: Optional[str] = None,
                       tags: Optional[Sequence[pulumi.InputType['NetworkInterfacesTagArgs']]] = None,
                       type: Optional[str] = None,
                       vpc_id: Optional[str] = None,
                       zone_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableNetworkInterfacesResult:
    """
    Use this data source to query detailed information of network interfaces
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.vpc.network_interfaces(ids=["eni-2744htx2w0j5s7fap8t3ivwze"])
    ```


    :param Sequence[str] ids: A list of ENI ids.
    :param str instance_id: An id of the instance to which the ENI is bound.
    :param Sequence[str] network_interface_ids: A list of network interface ids.
    :param str network_interface_name: A name of ENI.
    :param str output_file: File name where to save data source results.
    :param Sequence[str] primary_ip_addresses: A list of primary IP address of ENI.
    :param Sequence[str] private_ip_addresses: A list of private IP addresses.
    :param str project_name: The ProjectName of the ENI.
    :param str security_group_id: An id of the security group to which the secondary ENI belongs.
    :param str status: A status of ENI, Optional choice contains `Creating`, `Available`, `Attaching`, `InUse`, `Detaching`, `Deleting`.
    :param str subnet_id: An id of the subnet to which the ENI is connected.
    :param Sequence[pulumi.InputType['NetworkInterfacesTagArgs']] tags: Tags.
    :param str type: A type of ENI, Optional choice contains `primary`, `secondary`.
    :param str vpc_id: An id of the virtual private cloud (VPC) to which the ENI belongs.
    :param str zone_id: The zone ID.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['instanceId'] = instance_id
    __args__['networkInterfaceIds'] = network_interface_ids
    __args__['networkInterfaceName'] = network_interface_name
    __args__['outputFile'] = output_file
    __args__['primaryIpAddresses'] = primary_ip_addresses
    __args__['privateIpAddresses'] = private_ip_addresses
    __args__['projectName'] = project_name
    __args__['securityGroupId'] = security_group_id
    __args__['status'] = status
    __args__['subnetId'] = subnet_id
    __args__['tags'] = tags
    __args__['type'] = type
    __args__['vpcId'] = vpc_id
    __args__['zoneId'] = zone_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:vpc/networkInterfaces:NetworkInterfaces', __args__, opts=opts, typ=NetworkInterfacesResult).value

    return AwaitableNetworkInterfacesResult(
        id=__ret__.id,
        ids=__ret__.ids,
        instance_id=__ret__.instance_id,
        network_interface_ids=__ret__.network_interface_ids,
        network_interface_name=__ret__.network_interface_name,
        network_interfaces=__ret__.network_interfaces,
        output_file=__ret__.output_file,
        primary_ip_addresses=__ret__.primary_ip_addresses,
        private_ip_addresses=__ret__.private_ip_addresses,
        project_name=__ret__.project_name,
        security_group_id=__ret__.security_group_id,
        status=__ret__.status,
        subnet_id=__ret__.subnet_id,
        tags=__ret__.tags,
        total_count=__ret__.total_count,
        type=__ret__.type,
        vpc_id=__ret__.vpc_id,
        zone_id=__ret__.zone_id)


@_utilities.lift_output_func(network_interfaces)
def network_interfaces_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              instance_id: Optional[pulumi.Input[Optional[str]]] = None,
                              network_interface_ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              network_interface_name: Optional[pulumi.Input[Optional[str]]] = None,
                              output_file: Optional[pulumi.Input[Optional[str]]] = None,
                              primary_ip_addresses: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              private_ip_addresses: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              project_name: Optional[pulumi.Input[Optional[str]]] = None,
                              security_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                              status: Optional[pulumi.Input[Optional[str]]] = None,
                              subnet_id: Optional[pulumi.Input[Optional[str]]] = None,
                              tags: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['NetworkInterfacesTagArgs']]]]] = None,
                              type: Optional[pulumi.Input[Optional[str]]] = None,
                              vpc_id: Optional[pulumi.Input[Optional[str]]] = None,
                              zone_id: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[NetworkInterfacesResult]:
    """
    Use this data source to query detailed information of network interfaces
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.vpc.network_interfaces(ids=["eni-2744htx2w0j5s7fap8t3ivwze"])
    ```


    :param Sequence[str] ids: A list of ENI ids.
    :param str instance_id: An id of the instance to which the ENI is bound.
    :param Sequence[str] network_interface_ids: A list of network interface ids.
    :param str network_interface_name: A name of ENI.
    :param str output_file: File name where to save data source results.
    :param Sequence[str] primary_ip_addresses: A list of primary IP address of ENI.
    :param Sequence[str] private_ip_addresses: A list of private IP addresses.
    :param str project_name: The ProjectName of the ENI.
    :param str security_group_id: An id of the security group to which the secondary ENI belongs.
    :param str status: A status of ENI, Optional choice contains `Creating`, `Available`, `Attaching`, `InUse`, `Detaching`, `Deleting`.
    :param str subnet_id: An id of the subnet to which the ENI is connected.
    :param Sequence[pulumi.InputType['NetworkInterfacesTagArgs']] tags: Tags.
    :param str type: A type of ENI, Optional choice contains `primary`, `secondary`.
    :param str vpc_id: An id of the virtual private cloud (VPC) to which the ENI belongs.
    :param str zone_id: The zone ID.
    """
    ...
