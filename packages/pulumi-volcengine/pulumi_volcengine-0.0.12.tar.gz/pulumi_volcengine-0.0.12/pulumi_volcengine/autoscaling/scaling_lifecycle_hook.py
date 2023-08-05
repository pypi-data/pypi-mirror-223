# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ScalingLifecycleHookArgs', 'ScalingLifecycleHook']

@pulumi.input_type
class ScalingLifecycleHookArgs:
    def __init__(__self__, *,
                 lifecycle_hook_name: pulumi.Input[str],
                 lifecycle_hook_policy: pulumi.Input[str],
                 lifecycle_hook_timeout: pulumi.Input[int],
                 lifecycle_hook_type: pulumi.Input[str],
                 scaling_group_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a ScalingLifecycleHook resource.
        :param pulumi.Input[str] lifecycle_hook_name: The name of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_policy: The policy of the lifecycle hook. Valid values: CONTINUE, REJECT.
        :param pulumi.Input[int] lifecycle_hook_timeout: The timeout of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_type: The type of the lifecycle hook. Valid values: SCALE_IN, SCALE_OUT.
        :param pulumi.Input[str] scaling_group_id: The id of the scaling group.
        """
        pulumi.set(__self__, "lifecycle_hook_name", lifecycle_hook_name)
        pulumi.set(__self__, "lifecycle_hook_policy", lifecycle_hook_policy)
        pulumi.set(__self__, "lifecycle_hook_timeout", lifecycle_hook_timeout)
        pulumi.set(__self__, "lifecycle_hook_type", lifecycle_hook_type)
        pulumi.set(__self__, "scaling_group_id", scaling_group_id)

    @property
    @pulumi.getter(name="lifecycleHookName")
    def lifecycle_hook_name(self) -> pulumi.Input[str]:
        """
        The name of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_name")

    @lifecycle_hook_name.setter
    def lifecycle_hook_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "lifecycle_hook_name", value)

    @property
    @pulumi.getter(name="lifecycleHookPolicy")
    def lifecycle_hook_policy(self) -> pulumi.Input[str]:
        """
        The policy of the lifecycle hook. Valid values: CONTINUE, REJECT.
        """
        return pulumi.get(self, "lifecycle_hook_policy")

    @lifecycle_hook_policy.setter
    def lifecycle_hook_policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "lifecycle_hook_policy", value)

    @property
    @pulumi.getter(name="lifecycleHookTimeout")
    def lifecycle_hook_timeout(self) -> pulumi.Input[int]:
        """
        The timeout of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_timeout")

    @lifecycle_hook_timeout.setter
    def lifecycle_hook_timeout(self, value: pulumi.Input[int]):
        pulumi.set(self, "lifecycle_hook_timeout", value)

    @property
    @pulumi.getter(name="lifecycleHookType")
    def lifecycle_hook_type(self) -> pulumi.Input[str]:
        """
        The type of the lifecycle hook. Valid values: SCALE_IN, SCALE_OUT.
        """
        return pulumi.get(self, "lifecycle_hook_type")

    @lifecycle_hook_type.setter
    def lifecycle_hook_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "lifecycle_hook_type", value)

    @property
    @pulumi.getter(name="scalingGroupId")
    def scaling_group_id(self) -> pulumi.Input[str]:
        """
        The id of the scaling group.
        """
        return pulumi.get(self, "scaling_group_id")

    @scaling_group_id.setter
    def scaling_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "scaling_group_id", value)


@pulumi.input_type
class _ScalingLifecycleHookState:
    def __init__(__self__, *,
                 lifecycle_hook_id: Optional[pulumi.Input[str]] = None,
                 lifecycle_hook_name: Optional[pulumi.Input[str]] = None,
                 lifecycle_hook_policy: Optional[pulumi.Input[str]] = None,
                 lifecycle_hook_timeout: Optional[pulumi.Input[int]] = None,
                 lifecycle_hook_type: Optional[pulumi.Input[str]] = None,
                 scaling_group_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ScalingLifecycleHook resources.
        :param pulumi.Input[str] lifecycle_hook_id: The id of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_name: The name of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_policy: The policy of the lifecycle hook. Valid values: CONTINUE, REJECT.
        :param pulumi.Input[int] lifecycle_hook_timeout: The timeout of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_type: The type of the lifecycle hook. Valid values: SCALE_IN, SCALE_OUT.
        :param pulumi.Input[str] scaling_group_id: The id of the scaling group.
        """
        if lifecycle_hook_id is not None:
            pulumi.set(__self__, "lifecycle_hook_id", lifecycle_hook_id)
        if lifecycle_hook_name is not None:
            pulumi.set(__self__, "lifecycle_hook_name", lifecycle_hook_name)
        if lifecycle_hook_policy is not None:
            pulumi.set(__self__, "lifecycle_hook_policy", lifecycle_hook_policy)
        if lifecycle_hook_timeout is not None:
            pulumi.set(__self__, "lifecycle_hook_timeout", lifecycle_hook_timeout)
        if lifecycle_hook_type is not None:
            pulumi.set(__self__, "lifecycle_hook_type", lifecycle_hook_type)
        if scaling_group_id is not None:
            pulumi.set(__self__, "scaling_group_id", scaling_group_id)

    @property
    @pulumi.getter(name="lifecycleHookId")
    def lifecycle_hook_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_id")

    @lifecycle_hook_id.setter
    def lifecycle_hook_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lifecycle_hook_id", value)

    @property
    @pulumi.getter(name="lifecycleHookName")
    def lifecycle_hook_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_name")

    @lifecycle_hook_name.setter
    def lifecycle_hook_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lifecycle_hook_name", value)

    @property
    @pulumi.getter(name="lifecycleHookPolicy")
    def lifecycle_hook_policy(self) -> Optional[pulumi.Input[str]]:
        """
        The policy of the lifecycle hook. Valid values: CONTINUE, REJECT.
        """
        return pulumi.get(self, "lifecycle_hook_policy")

    @lifecycle_hook_policy.setter
    def lifecycle_hook_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lifecycle_hook_policy", value)

    @property
    @pulumi.getter(name="lifecycleHookTimeout")
    def lifecycle_hook_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        The timeout of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_timeout")

    @lifecycle_hook_timeout.setter
    def lifecycle_hook_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "lifecycle_hook_timeout", value)

    @property
    @pulumi.getter(name="lifecycleHookType")
    def lifecycle_hook_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the lifecycle hook. Valid values: SCALE_IN, SCALE_OUT.
        """
        return pulumi.get(self, "lifecycle_hook_type")

    @lifecycle_hook_type.setter
    def lifecycle_hook_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lifecycle_hook_type", value)

    @property
    @pulumi.getter(name="scalingGroupId")
    def scaling_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the scaling group.
        """
        return pulumi.get(self, "scaling_group_id")

    @scaling_group_id.setter
    def scaling_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scaling_group_id", value)


class ScalingLifecycleHook(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 lifecycle_hook_name: Optional[pulumi.Input[str]] = None,
                 lifecycle_hook_policy: Optional[pulumi.Input[str]] = None,
                 lifecycle_hook_timeout: Optional[pulumi.Input[int]] = None,
                 lifecycle_hook_type: Optional[pulumi.Input[str]] = None,
                 scaling_group_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage scaling lifecycle hook
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.autoscaling.ScalingLifecycleHook("foo",
            lifecycle_hook_name="tf-test",
            lifecycle_hook_policy="CONTINUE",
            lifecycle_hook_timeout=30,
            lifecycle_hook_type="SCALE_IN",
            scaling_group_id="scg-ybru8pazhgl8j1di4tyd")
        ```

        ## Import

        ScalingLifecycleHook can be imported using the ScalingGroupId:LifecycleHookId, e.g.

        ```sh
         $ pulumi import volcengine:autoscaling/scalingLifecycleHook:ScalingLifecycleHook default scg-yblfbfhy7agh9zn72iaz:sgh-ybqholahe4gso0ee88sd
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] lifecycle_hook_name: The name of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_policy: The policy of the lifecycle hook. Valid values: CONTINUE, REJECT.
        :param pulumi.Input[int] lifecycle_hook_timeout: The timeout of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_type: The type of the lifecycle hook. Valid values: SCALE_IN, SCALE_OUT.
        :param pulumi.Input[str] scaling_group_id: The id of the scaling group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScalingLifecycleHookArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage scaling lifecycle hook
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.autoscaling.ScalingLifecycleHook("foo",
            lifecycle_hook_name="tf-test",
            lifecycle_hook_policy="CONTINUE",
            lifecycle_hook_timeout=30,
            lifecycle_hook_type="SCALE_IN",
            scaling_group_id="scg-ybru8pazhgl8j1di4tyd")
        ```

        ## Import

        ScalingLifecycleHook can be imported using the ScalingGroupId:LifecycleHookId, e.g.

        ```sh
         $ pulumi import volcengine:autoscaling/scalingLifecycleHook:ScalingLifecycleHook default scg-yblfbfhy7agh9zn72iaz:sgh-ybqholahe4gso0ee88sd
        ```

        :param str resource_name: The name of the resource.
        :param ScalingLifecycleHookArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScalingLifecycleHookArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 lifecycle_hook_name: Optional[pulumi.Input[str]] = None,
                 lifecycle_hook_policy: Optional[pulumi.Input[str]] = None,
                 lifecycle_hook_timeout: Optional[pulumi.Input[int]] = None,
                 lifecycle_hook_type: Optional[pulumi.Input[str]] = None,
                 scaling_group_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = ScalingLifecycleHookArgs.__new__(ScalingLifecycleHookArgs)

            if lifecycle_hook_name is None and not opts.urn:
                raise TypeError("Missing required property 'lifecycle_hook_name'")
            __props__.__dict__["lifecycle_hook_name"] = lifecycle_hook_name
            if lifecycle_hook_policy is None and not opts.urn:
                raise TypeError("Missing required property 'lifecycle_hook_policy'")
            __props__.__dict__["lifecycle_hook_policy"] = lifecycle_hook_policy
            if lifecycle_hook_timeout is None and not opts.urn:
                raise TypeError("Missing required property 'lifecycle_hook_timeout'")
            __props__.__dict__["lifecycle_hook_timeout"] = lifecycle_hook_timeout
            if lifecycle_hook_type is None and not opts.urn:
                raise TypeError("Missing required property 'lifecycle_hook_type'")
            __props__.__dict__["lifecycle_hook_type"] = lifecycle_hook_type
            if scaling_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'scaling_group_id'")
            __props__.__dict__["scaling_group_id"] = scaling_group_id
            __props__.__dict__["lifecycle_hook_id"] = None
        super(ScalingLifecycleHook, __self__).__init__(
            'volcengine:autoscaling/scalingLifecycleHook:ScalingLifecycleHook',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            lifecycle_hook_id: Optional[pulumi.Input[str]] = None,
            lifecycle_hook_name: Optional[pulumi.Input[str]] = None,
            lifecycle_hook_policy: Optional[pulumi.Input[str]] = None,
            lifecycle_hook_timeout: Optional[pulumi.Input[int]] = None,
            lifecycle_hook_type: Optional[pulumi.Input[str]] = None,
            scaling_group_id: Optional[pulumi.Input[str]] = None) -> 'ScalingLifecycleHook':
        """
        Get an existing ScalingLifecycleHook resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] lifecycle_hook_id: The id of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_name: The name of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_policy: The policy of the lifecycle hook. Valid values: CONTINUE, REJECT.
        :param pulumi.Input[int] lifecycle_hook_timeout: The timeout of the lifecycle hook.
        :param pulumi.Input[str] lifecycle_hook_type: The type of the lifecycle hook. Valid values: SCALE_IN, SCALE_OUT.
        :param pulumi.Input[str] scaling_group_id: The id of the scaling group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ScalingLifecycleHookState.__new__(_ScalingLifecycleHookState)

        __props__.__dict__["lifecycle_hook_id"] = lifecycle_hook_id
        __props__.__dict__["lifecycle_hook_name"] = lifecycle_hook_name
        __props__.__dict__["lifecycle_hook_policy"] = lifecycle_hook_policy
        __props__.__dict__["lifecycle_hook_timeout"] = lifecycle_hook_timeout
        __props__.__dict__["lifecycle_hook_type"] = lifecycle_hook_type
        __props__.__dict__["scaling_group_id"] = scaling_group_id
        return ScalingLifecycleHook(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="lifecycleHookId")
    def lifecycle_hook_id(self) -> pulumi.Output[str]:
        """
        The id of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_id")

    @property
    @pulumi.getter(name="lifecycleHookName")
    def lifecycle_hook_name(self) -> pulumi.Output[str]:
        """
        The name of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_name")

    @property
    @pulumi.getter(name="lifecycleHookPolicy")
    def lifecycle_hook_policy(self) -> pulumi.Output[str]:
        """
        The policy of the lifecycle hook. Valid values: CONTINUE, REJECT.
        """
        return pulumi.get(self, "lifecycle_hook_policy")

    @property
    @pulumi.getter(name="lifecycleHookTimeout")
    def lifecycle_hook_timeout(self) -> pulumi.Output[int]:
        """
        The timeout of the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_hook_timeout")

    @property
    @pulumi.getter(name="lifecycleHookType")
    def lifecycle_hook_type(self) -> pulumi.Output[str]:
        """
        The type of the lifecycle hook. Valid values: SCALE_IN, SCALE_OUT.
        """
        return pulumi.get(self, "lifecycle_hook_type")

    @property
    @pulumi.getter(name="scalingGroupId")
    def scaling_group_id(self) -> pulumi.Output[str]:
        """
        The id of the scaling group.
        """
        return pulumi.get(self, "scaling_group_id")

