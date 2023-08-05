# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NetworkInterfaceAttachArgs', 'NetworkInterfaceAttach']

@pulumi.input_type
class NetworkInterfaceAttachArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 network_interface_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a NetworkInterfaceAttach resource.
        :param pulumi.Input[str] instance_id: The id of the instance to which the ENI is bound.
        :param pulumi.Input[str] network_interface_id: The id of the ENI.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "network_interface_id", network_interface_id)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The id of the instance to which the ENI is bound.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Input[str]:
        """
        The id of the ENI.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_interface_id", value)


@pulumi.input_type
class _NetworkInterfaceAttachState:
    def __init__(__self__, *,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkInterfaceAttach resources.
        :param pulumi.Input[str] instance_id: The id of the instance to which the ENI is bound.
        :param pulumi.Input[str] network_interface_id: The id of the ENI.
        """
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the instance to which the ENI is bound.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the ENI.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_interface_id", value)


class NetworkInterfaceAttach(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage network interface attach
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.vpc.NetworkInterfaceAttach("foo",
            instance_id="i-72q20hi6s082wcafdem8",
            network_interface_id="eni-274ecj646ylts7fap8t6xbba1")
        ```

        ## Import

        Network interface attach can be imported using the network_interface_id:instance_id.

        ```sh
         $ pulumi import volcengine:vpc/networkInterfaceAttach:NetworkInterfaceAttach default eni-bp1fg655nh68xyz9***:i-wijfn35c****
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: The id of the instance to which the ENI is bound.
        :param pulumi.Input[str] network_interface_id: The id of the ENI.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkInterfaceAttachArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage network interface attach
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.vpc.NetworkInterfaceAttach("foo",
            instance_id="i-72q20hi6s082wcafdem8",
            network_interface_id="eni-274ecj646ylts7fap8t6xbba1")
        ```

        ## Import

        Network interface attach can be imported using the network_interface_id:instance_id.

        ```sh
         $ pulumi import volcengine:vpc/networkInterfaceAttach:NetworkInterfaceAttach default eni-bp1fg655nh68xyz9***:i-wijfn35c****
        ```

        :param str resource_name: The name of the resource.
        :param NetworkInterfaceAttachArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkInterfaceAttachArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = NetworkInterfaceAttachArgs.__new__(NetworkInterfaceAttachArgs)

            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if network_interface_id is None and not opts.urn:
                raise TypeError("Missing required property 'network_interface_id'")
            __props__.__dict__["network_interface_id"] = network_interface_id
        super(NetworkInterfaceAttach, __self__).__init__(
            'volcengine:vpc/networkInterfaceAttach:NetworkInterfaceAttach',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            network_interface_id: Optional[pulumi.Input[str]] = None) -> 'NetworkInterfaceAttach':
        """
        Get an existing NetworkInterfaceAttach resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: The id of the instance to which the ENI is bound.
        :param pulumi.Input[str] network_interface_id: The id of the ENI.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkInterfaceAttachState.__new__(_NetworkInterfaceAttachState)

        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["network_interface_id"] = network_interface_id
        return NetworkInterfaceAttach(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The id of the instance to which the ENI is bound.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[str]:
        """
        The id of the ENI.
        """
        return pulumi.get(self, "network_interface_id")

