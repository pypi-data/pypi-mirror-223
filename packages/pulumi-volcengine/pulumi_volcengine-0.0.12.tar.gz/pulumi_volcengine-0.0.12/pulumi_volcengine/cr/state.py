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

__all__ = ['StateArgs', 'State']

@pulumi.input_type
class StateArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a State resource.
        :param pulumi.Input[str] action: Start cr instance action,the value must be `Start`.
        :param pulumi.Input[str] name: The cr instance id.
        """
        pulumi.set(__self__, "action", action)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        Start cr instance action,the value must be `Start`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The cr instance id.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _StateState:
    def __init__(__self__, *,
                 action: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['StateStatusArgs']] = None):
        """
        Input properties used for looking up and filtering State resources.
        :param pulumi.Input[str] action: Start cr instance action,the value must be `Start`.
        :param pulumi.Input[str] name: The cr instance id.
        :param pulumi.Input['StateStatusArgs'] status: The status of cr instance.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[str]]:
        """
        Start cr instance action,the value must be `Start`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The cr instance id.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input['StateStatusArgs']]:
        """
        The status of cr instance.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input['StateStatusArgs']]):
        pulumi.set(self, "status", value)


class State(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage cr registry state
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.cr.State("foo", action="Start")
        ```

        ## Import

        CR registry state can be imported using the state:registry_name, e.g.

        ```sh
         $ pulumi import volcengine:cr/state:State default state:cr-basic
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: Start cr instance action,the value must be `Start`.
        :param pulumi.Input[str] name: The cr instance id.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage cr registry state
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.cr.State("foo", action="Start")
        ```

        ## Import

        CR registry state can be imported using the state:registry_name, e.g.

        ```sh
         $ pulumi import volcengine:cr/state:State default state:cr-basic
        ```

        :param str resource_name: The name of the resource.
        :param StateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
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
            __props__ = StateArgs.__new__(StateArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["name"] = name
            __props__.__dict__["status"] = None
        super(State, __self__).__init__(
            'volcengine:cr/state:State',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[pulumi.InputType['StateStatusArgs']]] = None) -> 'State':
        """
        Get an existing State resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: Start cr instance action,the value must be `Start`.
        :param pulumi.Input[str] name: The cr instance id.
        :param pulumi.Input[pulumi.InputType['StateStatusArgs']] status: The status of cr instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StateState.__new__(_StateState)

        __props__.__dict__["action"] = action
        __props__.__dict__["name"] = name
        __props__.__dict__["status"] = status
        return State(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        Start cr instance action,the value must be `Start`.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The cr instance id.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.StateStatus']:
        """
        The status of cr instance.
        """
        return pulumi.get(self, "status")

