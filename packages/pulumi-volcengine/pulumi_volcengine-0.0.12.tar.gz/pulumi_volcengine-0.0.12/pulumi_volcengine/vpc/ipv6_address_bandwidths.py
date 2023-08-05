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
    'Ipv6AddressBandwidthsResult',
    'AwaitableIpv6AddressBandwidthsResult',
    'ipv6_address_bandwidths',
    'ipv6_address_bandwidths_output',
]

@pulumi.output_type
class Ipv6AddressBandwidthsResult:
    """
    A collection of values returned by Ipv6AddressBandwidths.
    """
    def __init__(__self__, associated_instance_id=None, associated_instance_type=None, id=None, ids=None, ipv6_address_bandwidths=None, ipv6_addresses=None, isp=None, network_type=None, output_file=None, total_count=None, vpc_id=None):
        if associated_instance_id and not isinstance(associated_instance_id, str):
            raise TypeError("Expected argument 'associated_instance_id' to be a str")
        pulumi.set(__self__, "associated_instance_id", associated_instance_id)
        if associated_instance_type and not isinstance(associated_instance_type, str):
            raise TypeError("Expected argument 'associated_instance_type' to be a str")
        pulumi.set(__self__, "associated_instance_type", associated_instance_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if ipv6_address_bandwidths and not isinstance(ipv6_address_bandwidths, list):
            raise TypeError("Expected argument 'ipv6_address_bandwidths' to be a list")
        pulumi.set(__self__, "ipv6_address_bandwidths", ipv6_address_bandwidths)
        if ipv6_addresses and not isinstance(ipv6_addresses, list):
            raise TypeError("Expected argument 'ipv6_addresses' to be a list")
        pulumi.set(__self__, "ipv6_addresses", ipv6_addresses)
        if isp and not isinstance(isp, str):
            raise TypeError("Expected argument 'isp' to be a str")
        pulumi.set(__self__, "isp", isp)
        if network_type and not isinstance(network_type, str):
            raise TypeError("Expected argument 'network_type' to be a str")
        pulumi.set(__self__, "network_type", network_type)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="associatedInstanceId")
    def associated_instance_id(self) -> Optional[str]:
        return pulumi.get(self, "associated_instance_id")

    @property
    @pulumi.getter(name="associatedInstanceType")
    def associated_instance_type(self) -> Optional[str]:
        return pulumi.get(self, "associated_instance_type")

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
    @pulumi.getter(name="ipv6AddressBandwidths")
    def ipv6_address_bandwidths(self) -> Sequence['outputs.Ipv6AddressBandwidthsIpv6AddressBandwidthResult']:
        """
        The collection of Ipv6AddressBandwidth query.
        """
        return pulumi.get(self, "ipv6_address_bandwidths")

    @property
    @pulumi.getter(name="ipv6Addresses")
    def ipv6_addresses(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "ipv6_addresses")

    @property
    @pulumi.getter
    def isp(self) -> Optional[str]:
        """
        The ISP of the Ipv6AddressBandwidth.
        """
        return pulumi.get(self, "isp")

    @property
    @pulumi.getter(name="networkType")
    def network_type(self) -> Optional[str]:
        """
        The network type of the Ipv6AddressBandwidth.
        """
        return pulumi.get(self, "network_type")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        The total count of Ipv6AddressBandwidth query.
        """
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        return pulumi.get(self, "vpc_id")


class AwaitableIpv6AddressBandwidthsResult(Ipv6AddressBandwidthsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return Ipv6AddressBandwidthsResult(
            associated_instance_id=self.associated_instance_id,
            associated_instance_type=self.associated_instance_type,
            id=self.id,
            ids=self.ids,
            ipv6_address_bandwidths=self.ipv6_address_bandwidths,
            ipv6_addresses=self.ipv6_addresses,
            isp=self.isp,
            network_type=self.network_type,
            output_file=self.output_file,
            total_count=self.total_count,
            vpc_id=self.vpc_id)


def ipv6_address_bandwidths(associated_instance_id: Optional[str] = None,
                            associated_instance_type: Optional[str] = None,
                            ids: Optional[Sequence[str]] = None,
                            ipv6_addresses: Optional[Sequence[str]] = None,
                            isp: Optional[str] = None,
                            network_type: Optional[str] = None,
                            output_file: Optional[str] = None,
                            vpc_id: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableIpv6AddressBandwidthsResult:
    """
    Use this data source to query detailed information of vpc ipv6 address bandwidths
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.vpc.ipv6_address_bandwidths(ids=["eip-in2y2duvtlhc8gbssyfnhfre"])
    ```


    :param str associated_instance_id: The ID of the associated instance.
    :param str associated_instance_type: The type of the associated instance.
    :param Sequence[str] ids: Allocation IDs of the Ipv6 address width.
    :param Sequence[str] ipv6_addresses: The ipv6 addresses.
    :param str isp: ISP of the ipv6 address.
    :param str network_type: The network type of the ipv6 address.
    :param str output_file: File name where to save data source results.
    :param str vpc_id: The ID of Vpc the ipv6 address in.
    """
    __args__ = dict()
    __args__['associatedInstanceId'] = associated_instance_id
    __args__['associatedInstanceType'] = associated_instance_type
    __args__['ids'] = ids
    __args__['ipv6Addresses'] = ipv6_addresses
    __args__['isp'] = isp
    __args__['networkType'] = network_type
    __args__['outputFile'] = output_file
    __args__['vpcId'] = vpc_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
    __ret__ = pulumi.runtime.invoke('volcengine:vpc/ipv6AddressBandwidths:Ipv6AddressBandwidths', __args__, opts=opts, typ=Ipv6AddressBandwidthsResult).value

    return AwaitableIpv6AddressBandwidthsResult(
        associated_instance_id=__ret__.associated_instance_id,
        associated_instance_type=__ret__.associated_instance_type,
        id=__ret__.id,
        ids=__ret__.ids,
        ipv6_address_bandwidths=__ret__.ipv6_address_bandwidths,
        ipv6_addresses=__ret__.ipv6_addresses,
        isp=__ret__.isp,
        network_type=__ret__.network_type,
        output_file=__ret__.output_file,
        total_count=__ret__.total_count,
        vpc_id=__ret__.vpc_id)


@_utilities.lift_output_func(ipv6_address_bandwidths)
def ipv6_address_bandwidths_output(associated_instance_id: Optional[pulumi.Input[Optional[str]]] = None,
                                   associated_instance_type: Optional[pulumi.Input[Optional[str]]] = None,
                                   ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                   ipv6_addresses: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                   isp: Optional[pulumi.Input[Optional[str]]] = None,
                                   network_type: Optional[pulumi.Input[Optional[str]]] = None,
                                   output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                   vpc_id: Optional[pulumi.Input[Optional[str]]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[Ipv6AddressBandwidthsResult]:
    """
    Use this data source to query detailed information of vpc ipv6 address bandwidths
    ## Example Usage

    ```python
    import pulumi
    import pulumi_volcengine as volcengine

    default = volcengine.vpc.ipv6_address_bandwidths(ids=["eip-in2y2duvtlhc8gbssyfnhfre"])
    ```


    :param str associated_instance_id: The ID of the associated instance.
    :param str associated_instance_type: The type of the associated instance.
    :param Sequence[str] ids: Allocation IDs of the Ipv6 address width.
    :param Sequence[str] ipv6_addresses: The ipv6 addresses.
    :param str isp: ISP of the ipv6 address.
    :param str network_type: The network type of the ipv6 address.
    :param str output_file: File name where to save data source results.
    :param str vpc_id: The ID of Vpc the ipv6 address in.
    """
    ...
