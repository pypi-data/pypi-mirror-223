# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RuleApplierArgs', 'RuleApplier']

@pulumi.input_type
class RuleApplierArgs:
    def __init__(__self__, *,
                 host_group_id: pulumi.Input[str],
                 rule_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a RuleApplier resource.
        :param pulumi.Input[str] host_group_id: The id of the host group.
        :param pulumi.Input[str] rule_id: The id of the rule.
        """
        pulumi.set(__self__, "host_group_id", host_group_id)
        pulumi.set(__self__, "rule_id", rule_id)

    @property
    @pulumi.getter(name="hostGroupId")
    def host_group_id(self) -> pulumi.Input[str]:
        """
        The id of the host group.
        """
        return pulumi.get(self, "host_group_id")

    @host_group_id.setter
    def host_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "host_group_id", value)

    @property
    @pulumi.getter(name="ruleId")
    def rule_id(self) -> pulumi.Input[str]:
        """
        The id of the rule.
        """
        return pulumi.get(self, "rule_id")

    @rule_id.setter
    def rule_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "rule_id", value)


@pulumi.input_type
class _RuleApplierState:
    def __init__(__self__, *,
                 host_group_id: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RuleApplier resources.
        :param pulumi.Input[str] host_group_id: The id of the host group.
        :param pulumi.Input[str] rule_id: The id of the rule.
        """
        if host_group_id is not None:
            pulumi.set(__self__, "host_group_id", host_group_id)
        if rule_id is not None:
            pulumi.set(__self__, "rule_id", rule_id)

    @property
    @pulumi.getter(name="hostGroupId")
    def host_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the host group.
        """
        return pulumi.get(self, "host_group_id")

    @host_group_id.setter
    def host_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_group_id", value)

    @property
    @pulumi.getter(name="ruleId")
    def rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the rule.
        """
        return pulumi.get(self, "rule_id")

    @rule_id.setter
    def rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_id", value)


class RuleApplier(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 host_group_id: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage tls rule applier
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.tls.RuleApplier("foo",
            host_group_id="a2a9e8c5-9835-434f-b866-2c1cfa82887d",
            rule_id="25104b0f-28b7-4a5c-8339-7f9c431d77c8")
        ```

        ## Import

        tls rule applier can be imported using the rule id and host group id, e.g.

        ```sh
         $ pulumi import volcengine:tls/ruleApplier:RuleApplier default fa************:bcb*******
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] host_group_id: The id of the host group.
        :param pulumi.Input[str] rule_id: The id of the rule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RuleApplierArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage tls rule applier
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.tls.RuleApplier("foo",
            host_group_id="a2a9e8c5-9835-434f-b866-2c1cfa82887d",
            rule_id="25104b0f-28b7-4a5c-8339-7f9c431d77c8")
        ```

        ## Import

        tls rule applier can be imported using the rule id and host group id, e.g.

        ```sh
         $ pulumi import volcengine:tls/ruleApplier:RuleApplier default fa************:bcb*******
        ```

        :param str resource_name: The name of the resource.
        :param RuleApplierArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RuleApplierArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 host_group_id: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = RuleApplierArgs.__new__(RuleApplierArgs)

            if host_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'host_group_id'")
            __props__.__dict__["host_group_id"] = host_group_id
            if rule_id is None and not opts.urn:
                raise TypeError("Missing required property 'rule_id'")
            __props__.__dict__["rule_id"] = rule_id
        super(RuleApplier, __self__).__init__(
            'volcengine:tls/ruleApplier:RuleApplier',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            host_group_id: Optional[pulumi.Input[str]] = None,
            rule_id: Optional[pulumi.Input[str]] = None) -> 'RuleApplier':
        """
        Get an existing RuleApplier resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] host_group_id: The id of the host group.
        :param pulumi.Input[str] rule_id: The id of the rule.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RuleApplierState.__new__(_RuleApplierState)

        __props__.__dict__["host_group_id"] = host_group_id
        __props__.__dict__["rule_id"] = rule_id
        return RuleApplier(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="hostGroupId")
    def host_group_id(self) -> pulumi.Output[str]:
        """
        The id of the host group.
        """
        return pulumi.get(self, "host_group_id")

    @property
    @pulumi.getter(name="ruleId")
    def rule_id(self) -> pulumi.Output[str]:
        """
        The id of the rule.
        """
        return pulumi.get(self, "rule_id")

