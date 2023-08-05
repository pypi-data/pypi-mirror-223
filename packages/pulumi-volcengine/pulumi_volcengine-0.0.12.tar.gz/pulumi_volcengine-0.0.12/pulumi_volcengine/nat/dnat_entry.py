# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DnatEntryArgs', 'DnatEntry']

@pulumi.input_type
class DnatEntryArgs:
    def __init__(__self__, *,
                 external_ip: pulumi.Input[str],
                 external_port: pulumi.Input[str],
                 internal_ip: pulumi.Input[str],
                 internal_port: pulumi.Input[str],
                 nat_gateway_id: pulumi.Input[str],
                 protocol: pulumi.Input[str],
                 dnat_entry_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DnatEntry resource.
        :param pulumi.Input[str] external_ip: Provides the public IP address for public network access.
        :param pulumi.Input[str] external_port: The port or port segment that receives requests from the public network. If InternalPort is passed into the port segment, ExternalPort must also be passed into the port segment.
        :param pulumi.Input[str] internal_ip: Provides the internal IP address.
        :param pulumi.Input[str] internal_port: The port or port segment on which the cloud server instance provides services to the public network.
        :param pulumi.Input[str] nat_gateway_id: The id of the nat gateway to which the entry belongs.
        :param pulumi.Input[str] protocol: The network protocol.
        :param pulumi.Input[str] dnat_entry_name: The name of the DNAT rule.
        """
        pulumi.set(__self__, "external_ip", external_ip)
        pulumi.set(__self__, "external_port", external_port)
        pulumi.set(__self__, "internal_ip", internal_ip)
        pulumi.set(__self__, "internal_port", internal_port)
        pulumi.set(__self__, "nat_gateway_id", nat_gateway_id)
        pulumi.set(__self__, "protocol", protocol)
        if dnat_entry_name is not None:
            pulumi.set(__self__, "dnat_entry_name", dnat_entry_name)

    @property
    @pulumi.getter(name="externalIp")
    def external_ip(self) -> pulumi.Input[str]:
        """
        Provides the public IP address for public network access.
        """
        return pulumi.get(self, "external_ip")

    @external_ip.setter
    def external_ip(self, value: pulumi.Input[str]):
        pulumi.set(self, "external_ip", value)

    @property
    @pulumi.getter(name="externalPort")
    def external_port(self) -> pulumi.Input[str]:
        """
        The port or port segment that receives requests from the public network. If InternalPort is passed into the port segment, ExternalPort must also be passed into the port segment.
        """
        return pulumi.get(self, "external_port")

    @external_port.setter
    def external_port(self, value: pulumi.Input[str]):
        pulumi.set(self, "external_port", value)

    @property
    @pulumi.getter(name="internalIp")
    def internal_ip(self) -> pulumi.Input[str]:
        """
        Provides the internal IP address.
        """
        return pulumi.get(self, "internal_ip")

    @internal_ip.setter
    def internal_ip(self, value: pulumi.Input[str]):
        pulumi.set(self, "internal_ip", value)

    @property
    @pulumi.getter(name="internalPort")
    def internal_port(self) -> pulumi.Input[str]:
        """
        The port or port segment on which the cloud server instance provides services to the public network.
        """
        return pulumi.get(self, "internal_port")

    @internal_port.setter
    def internal_port(self, value: pulumi.Input[str]):
        pulumi.set(self, "internal_port", value)

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> pulumi.Input[str]:
        """
        The id of the nat gateway to which the entry belongs.
        """
        return pulumi.get(self, "nat_gateway_id")

    @nat_gateway_id.setter
    def nat_gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "nat_gateway_id", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input[str]:
        """
        The network protocol.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="dnatEntryName")
    def dnat_entry_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the DNAT rule.
        """
        return pulumi.get(self, "dnat_entry_name")

    @dnat_entry_name.setter
    def dnat_entry_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dnat_entry_name", value)


@pulumi.input_type
class _DnatEntryState:
    def __init__(__self__, *,
                 dnat_entry_id: Optional[pulumi.Input[str]] = None,
                 dnat_entry_name: Optional[pulumi.Input[str]] = None,
                 external_ip: Optional[pulumi.Input[str]] = None,
                 external_port: Optional[pulumi.Input[str]] = None,
                 internal_ip: Optional[pulumi.Input[str]] = None,
                 internal_port: Optional[pulumi.Input[str]] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DnatEntry resources.
        :param pulumi.Input[str] dnat_entry_id: The id of the DNAT rule.
        :param pulumi.Input[str] dnat_entry_name: The name of the DNAT rule.
        :param pulumi.Input[str] external_ip: Provides the public IP address for public network access.
        :param pulumi.Input[str] external_port: The port or port segment that receives requests from the public network. If InternalPort is passed into the port segment, ExternalPort must also be passed into the port segment.
        :param pulumi.Input[str] internal_ip: Provides the internal IP address.
        :param pulumi.Input[str] internal_port: The port or port segment on which the cloud server instance provides services to the public network.
        :param pulumi.Input[str] nat_gateway_id: The id of the nat gateway to which the entry belongs.
        :param pulumi.Input[str] protocol: The network protocol.
        """
        if dnat_entry_id is not None:
            pulumi.set(__self__, "dnat_entry_id", dnat_entry_id)
        if dnat_entry_name is not None:
            pulumi.set(__self__, "dnat_entry_name", dnat_entry_name)
        if external_ip is not None:
            pulumi.set(__self__, "external_ip", external_ip)
        if external_port is not None:
            pulumi.set(__self__, "external_port", external_port)
        if internal_ip is not None:
            pulumi.set(__self__, "internal_ip", internal_ip)
        if internal_port is not None:
            pulumi.set(__self__, "internal_port", internal_port)
        if nat_gateway_id is not None:
            pulumi.set(__self__, "nat_gateway_id", nat_gateway_id)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)

    @property
    @pulumi.getter(name="dnatEntryId")
    def dnat_entry_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the DNAT rule.
        """
        return pulumi.get(self, "dnat_entry_id")

    @dnat_entry_id.setter
    def dnat_entry_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dnat_entry_id", value)

    @property
    @pulumi.getter(name="dnatEntryName")
    def dnat_entry_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the DNAT rule.
        """
        return pulumi.get(self, "dnat_entry_name")

    @dnat_entry_name.setter
    def dnat_entry_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dnat_entry_name", value)

    @property
    @pulumi.getter(name="externalIp")
    def external_ip(self) -> Optional[pulumi.Input[str]]:
        """
        Provides the public IP address for public network access.
        """
        return pulumi.get(self, "external_ip")

    @external_ip.setter
    def external_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_ip", value)

    @property
    @pulumi.getter(name="externalPort")
    def external_port(self) -> Optional[pulumi.Input[str]]:
        """
        The port or port segment that receives requests from the public network. If InternalPort is passed into the port segment, ExternalPort must also be passed into the port segment.
        """
        return pulumi.get(self, "external_port")

    @external_port.setter
    def external_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_port", value)

    @property
    @pulumi.getter(name="internalIp")
    def internal_ip(self) -> Optional[pulumi.Input[str]]:
        """
        Provides the internal IP address.
        """
        return pulumi.get(self, "internal_ip")

    @internal_ip.setter
    def internal_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "internal_ip", value)

    @property
    @pulumi.getter(name="internalPort")
    def internal_port(self) -> Optional[pulumi.Input[str]]:
        """
        The port or port segment on which the cloud server instance provides services to the public network.
        """
        return pulumi.get(self, "internal_port")

    @internal_port.setter
    def internal_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "internal_port", value)

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the nat gateway to which the entry belongs.
        """
        return pulumi.get(self, "nat_gateway_id")

    @nat_gateway_id.setter
    def nat_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nat_gateway_id", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The network protocol.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)


class DnatEntry(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dnat_entry_name: Optional[pulumi.Input[str]] = None,
                 external_ip: Optional[pulumi.Input[str]] = None,
                 external_port: Optional[pulumi.Input[str]] = None,
                 internal_ip: Optional[pulumi.Input[str]] = None,
                 internal_port: Optional[pulumi.Input[str]] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage dnat entry
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.nat.DnatEntry("foo",
            dnat_entry_name="terraform-test2",
            external_ip="10.249.186.68",
            external_port="23",
            internal_ip="193.168.1.1",
            internal_port="24",
            nat_gateway_id="ngw-imw3aej7e96o8gbssxkfbybv",
            protocol="tcp")
        ```

        ## Import

        Dnat entry can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:nat/dnatEntry:DnatEntry default dnat-3fvhk47kf56****
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dnat_entry_name: The name of the DNAT rule.
        :param pulumi.Input[str] external_ip: Provides the public IP address for public network access.
        :param pulumi.Input[str] external_port: The port or port segment that receives requests from the public network. If InternalPort is passed into the port segment, ExternalPort must also be passed into the port segment.
        :param pulumi.Input[str] internal_ip: Provides the internal IP address.
        :param pulumi.Input[str] internal_port: The port or port segment on which the cloud server instance provides services to the public network.
        :param pulumi.Input[str] nat_gateway_id: The id of the nat gateway to which the entry belongs.
        :param pulumi.Input[str] protocol: The network protocol.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DnatEntryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage dnat entry
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.nat.DnatEntry("foo",
            dnat_entry_name="terraform-test2",
            external_ip="10.249.186.68",
            external_port="23",
            internal_ip="193.168.1.1",
            internal_port="24",
            nat_gateway_id="ngw-imw3aej7e96o8gbssxkfbybv",
            protocol="tcp")
        ```

        ## Import

        Dnat entry can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:nat/dnatEntry:DnatEntry default dnat-3fvhk47kf56****
        ```

        :param str resource_name: The name of the resource.
        :param DnatEntryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DnatEntryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dnat_entry_name: Optional[pulumi.Input[str]] = None,
                 external_ip: Optional[pulumi.Input[str]] = None,
                 external_port: Optional[pulumi.Input[str]] = None,
                 internal_ip: Optional[pulumi.Input[str]] = None,
                 internal_port: Optional[pulumi.Input[str]] = None,
                 nat_gateway_id: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DnatEntryArgs.__new__(DnatEntryArgs)

            __props__.__dict__["dnat_entry_name"] = dnat_entry_name
            if external_ip is None and not opts.urn:
                raise TypeError("Missing required property 'external_ip'")
            __props__.__dict__["external_ip"] = external_ip
            if external_port is None and not opts.urn:
                raise TypeError("Missing required property 'external_port'")
            __props__.__dict__["external_port"] = external_port
            if internal_ip is None and not opts.urn:
                raise TypeError("Missing required property 'internal_ip'")
            __props__.__dict__["internal_ip"] = internal_ip
            if internal_port is None and not opts.urn:
                raise TypeError("Missing required property 'internal_port'")
            __props__.__dict__["internal_port"] = internal_port
            if nat_gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'nat_gateway_id'")
            __props__.__dict__["nat_gateway_id"] = nat_gateway_id
            if protocol is None and not opts.urn:
                raise TypeError("Missing required property 'protocol'")
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["dnat_entry_id"] = None
        super(DnatEntry, __self__).__init__(
            'volcengine:nat/dnatEntry:DnatEntry',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            dnat_entry_id: Optional[pulumi.Input[str]] = None,
            dnat_entry_name: Optional[pulumi.Input[str]] = None,
            external_ip: Optional[pulumi.Input[str]] = None,
            external_port: Optional[pulumi.Input[str]] = None,
            internal_ip: Optional[pulumi.Input[str]] = None,
            internal_port: Optional[pulumi.Input[str]] = None,
            nat_gateway_id: Optional[pulumi.Input[str]] = None,
            protocol: Optional[pulumi.Input[str]] = None) -> 'DnatEntry':
        """
        Get an existing DnatEntry resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dnat_entry_id: The id of the DNAT rule.
        :param pulumi.Input[str] dnat_entry_name: The name of the DNAT rule.
        :param pulumi.Input[str] external_ip: Provides the public IP address for public network access.
        :param pulumi.Input[str] external_port: The port or port segment that receives requests from the public network. If InternalPort is passed into the port segment, ExternalPort must also be passed into the port segment.
        :param pulumi.Input[str] internal_ip: Provides the internal IP address.
        :param pulumi.Input[str] internal_port: The port or port segment on which the cloud server instance provides services to the public network.
        :param pulumi.Input[str] nat_gateway_id: The id of the nat gateway to which the entry belongs.
        :param pulumi.Input[str] protocol: The network protocol.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DnatEntryState.__new__(_DnatEntryState)

        __props__.__dict__["dnat_entry_id"] = dnat_entry_id
        __props__.__dict__["dnat_entry_name"] = dnat_entry_name
        __props__.__dict__["external_ip"] = external_ip
        __props__.__dict__["external_port"] = external_port
        __props__.__dict__["internal_ip"] = internal_ip
        __props__.__dict__["internal_port"] = internal_port
        __props__.__dict__["nat_gateway_id"] = nat_gateway_id
        __props__.__dict__["protocol"] = protocol
        return DnatEntry(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dnatEntryId")
    def dnat_entry_id(self) -> pulumi.Output[str]:
        """
        The id of the DNAT rule.
        """
        return pulumi.get(self, "dnat_entry_id")

    @property
    @pulumi.getter(name="dnatEntryName")
    def dnat_entry_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the DNAT rule.
        """
        return pulumi.get(self, "dnat_entry_name")

    @property
    @pulumi.getter(name="externalIp")
    def external_ip(self) -> pulumi.Output[str]:
        """
        Provides the public IP address for public network access.
        """
        return pulumi.get(self, "external_ip")

    @property
    @pulumi.getter(name="externalPort")
    def external_port(self) -> pulumi.Output[str]:
        """
        The port or port segment that receives requests from the public network. If InternalPort is passed into the port segment, ExternalPort must also be passed into the port segment.
        """
        return pulumi.get(self, "external_port")

    @property
    @pulumi.getter(name="internalIp")
    def internal_ip(self) -> pulumi.Output[str]:
        """
        Provides the internal IP address.
        """
        return pulumi.get(self, "internal_ip")

    @property
    @pulumi.getter(name="internalPort")
    def internal_port(self) -> pulumi.Output[str]:
        """
        The port or port segment on which the cloud server instance provides services to the public network.
        """
        return pulumi.get(self, "internal_port")

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> pulumi.Output[str]:
        """
        The id of the nat gateway to which the entry belongs.
        """
        return pulumi.get(self, "nat_gateway_id")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        The network protocol.
        """
        return pulumi.get(self, "protocol")

