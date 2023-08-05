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

__all__ = ['InstanceArgs', 'Instance']

@pulumi.input_type
class InstanceArgs:
    def __init__(__self__, *,
                 instance_configuration: pulumi.Input['InstanceInstanceConfigurationArgs']):
        """
        The set of arguments for constructing a Instance resource.
        :param pulumi.Input['InstanceInstanceConfigurationArgs'] instance_configuration: The configuration of ESCloud instance.
        """
        pulumi.set(__self__, "instance_configuration", instance_configuration)

    @property
    @pulumi.getter(name="instanceConfiguration")
    def instance_configuration(self) -> pulumi.Input['InstanceInstanceConfigurationArgs']:
        """
        The configuration of ESCloud instance.
        """
        return pulumi.get(self, "instance_configuration")

    @instance_configuration.setter
    def instance_configuration(self, value: pulumi.Input['InstanceInstanceConfigurationArgs']):
        pulumi.set(self, "instance_configuration", value)


@pulumi.input_type
class _InstanceState:
    def __init__(__self__, *,
                 instance_configuration: Optional[pulumi.Input['InstanceInstanceConfigurationArgs']] = None):
        """
        Input properties used for looking up and filtering Instance resources.
        :param pulumi.Input['InstanceInstanceConfigurationArgs'] instance_configuration: The configuration of ESCloud instance.
        """
        if instance_configuration is not None:
            pulumi.set(__self__, "instance_configuration", instance_configuration)

    @property
    @pulumi.getter(name="instanceConfiguration")
    def instance_configuration(self) -> Optional[pulumi.Input['InstanceInstanceConfigurationArgs']]:
        """
        The configuration of ESCloud instance.
        """
        return pulumi.get(self, "instance_configuration")

    @instance_configuration.setter
    def instance_configuration(self, value: Optional[pulumi.Input['InstanceInstanceConfigurationArgs']]):
        pulumi.set(self, "instance_configuration", value)


class Instance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_configuration: Optional[pulumi.Input[pulumi.InputType['InstanceInstanceConfigurationArgs']]] = None,
                 __props__=None):
        """
        Provides a resource to manage escloud instance
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.escloud.Instance("foo", instance_configuration=volcengine.escloud.InstanceInstanceConfigurationArgs(
            admin_password="xxxx",
            admin_user_name="admin",
            charge_type="PostPaid",
            configuration_code="es.standard",
            enable_https=True,
            enable_pure_master=True,
            force_restart_after_scale=False,
            instance_name="from-tf4",
            node_specs_assigns=[
                volcengine.escloud.InstanceInstanceConfigurationNodeSpecsAssignArgs(
                    number=3,
                    resource_spec_name="es.x4.medium",
                    storage_size=100,
                    storage_spec_name="es.volume.essd.pl0",
                    type="Master",
                ),
                volcengine.escloud.InstanceInstanceConfigurationNodeSpecsAssignArgs(
                    number=2,
                    resource_spec_name="es.x4.large",
                    storage_size=100,
                    storage_spec_name="es.volume.essd.pl0",
                    type="Hot",
                ),
                volcengine.escloud.InstanceInstanceConfigurationNodeSpecsAssignArgs(
                    number=1,
                    resource_spec_name="kibana.x2.small",
                    type="Kibana",
                ),
            ],
            project_name="default",
            subnet_id="subnet-2bz9vxrixqigw2dx0eextz50p",
            version="V6_7",
            zone_number=1,
        ))
        ```

        ## Import

        ESCloud Instance can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:escloud/instance:Instance default n769ewmjjqyqh5dv
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['InstanceInstanceConfigurationArgs']] instance_configuration: The configuration of ESCloud instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage escloud instance
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.escloud.Instance("foo", instance_configuration=volcengine.escloud.InstanceInstanceConfigurationArgs(
            admin_password="xxxx",
            admin_user_name="admin",
            charge_type="PostPaid",
            configuration_code="es.standard",
            enable_https=True,
            enable_pure_master=True,
            force_restart_after_scale=False,
            instance_name="from-tf4",
            node_specs_assigns=[
                volcengine.escloud.InstanceInstanceConfigurationNodeSpecsAssignArgs(
                    number=3,
                    resource_spec_name="es.x4.medium",
                    storage_size=100,
                    storage_spec_name="es.volume.essd.pl0",
                    type="Master",
                ),
                volcengine.escloud.InstanceInstanceConfigurationNodeSpecsAssignArgs(
                    number=2,
                    resource_spec_name="es.x4.large",
                    storage_size=100,
                    storage_spec_name="es.volume.essd.pl0",
                    type="Hot",
                ),
                volcengine.escloud.InstanceInstanceConfigurationNodeSpecsAssignArgs(
                    number=1,
                    resource_spec_name="kibana.x2.small",
                    type="Kibana",
                ),
            ],
            project_name="default",
            subnet_id="subnet-2bz9vxrixqigw2dx0eextz50p",
            version="V6_7",
            zone_number=1,
        ))
        ```

        ## Import

        ESCloud Instance can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:escloud/instance:Instance default n769ewmjjqyqh5dv
        ```

        :param str resource_name: The name of the resource.
        :param InstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_configuration: Optional[pulumi.Input[pulumi.InputType['InstanceInstanceConfigurationArgs']]] = None,
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
            __props__ = InstanceArgs.__new__(InstanceArgs)

            if instance_configuration is None and not opts.urn:
                raise TypeError("Missing required property 'instance_configuration'")
            __props__.__dict__["instance_configuration"] = instance_configuration
        super(Instance, __self__).__init__(
            'volcengine:escloud/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_configuration: Optional[pulumi.Input[pulumi.InputType['InstanceInstanceConfigurationArgs']]] = None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['InstanceInstanceConfigurationArgs']] instance_configuration: The configuration of ESCloud instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceState.__new__(_InstanceState)

        __props__.__dict__["instance_configuration"] = instance_configuration
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceConfiguration")
    def instance_configuration(self) -> pulumi.Output['outputs.InstanceInstanceConfiguration']:
        """
        The configuration of ESCloud instance.
        """
        return pulumi.get(self, "instance_configuration")

