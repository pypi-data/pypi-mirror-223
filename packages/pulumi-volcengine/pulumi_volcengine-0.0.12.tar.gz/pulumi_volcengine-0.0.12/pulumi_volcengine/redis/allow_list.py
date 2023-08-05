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

__all__ = ['AllowListArgs', 'AllowList']

@pulumi.input_type
class AllowListArgs:
    def __init__(__self__, *,
                 allow_list_name: pulumi.Input[str],
                 allow_lists: pulumi.Input[Sequence[pulumi.Input[str]]],
                 allow_list_desc: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AllowList resource.
        :param pulumi.Input[str] allow_list_name: Name of allow list.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow_lists: Ip list of allow list.
        :param pulumi.Input[str] allow_list_desc: Description of allow list.
        """
        pulumi.set(__self__, "allow_list_name", allow_list_name)
        pulumi.set(__self__, "allow_lists", allow_lists)
        if allow_list_desc is not None:
            pulumi.set(__self__, "allow_list_desc", allow_list_desc)

    @property
    @pulumi.getter(name="allowListName")
    def allow_list_name(self) -> pulumi.Input[str]:
        """
        Name of allow list.
        """
        return pulumi.get(self, "allow_list_name")

    @allow_list_name.setter
    def allow_list_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "allow_list_name", value)

    @property
    @pulumi.getter(name="allowLists")
    def allow_lists(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Ip list of allow list.
        """
        return pulumi.get(self, "allow_lists")

    @allow_lists.setter
    def allow_lists(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allow_lists", value)

    @property
    @pulumi.getter(name="allowListDesc")
    def allow_list_desc(self) -> Optional[pulumi.Input[str]]:
        """
        Description of allow list.
        """
        return pulumi.get(self, "allow_list_desc")

    @allow_list_desc.setter
    def allow_list_desc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_list_desc", value)


@pulumi.input_type
class _AllowListState:
    def __init__(__self__, *,
                 allow_list_desc: Optional[pulumi.Input[str]] = None,
                 allow_list_id: Optional[pulumi.Input[str]] = None,
                 allow_list_ip_num: Optional[pulumi.Input[int]] = None,
                 allow_list_name: Optional[pulumi.Input[str]] = None,
                 allow_list_type: Optional[pulumi.Input[str]] = None,
                 allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 associated_instance_num: Optional[pulumi.Input[int]] = None,
                 associated_instances: Optional[pulumi.Input[Sequence[pulumi.Input['AllowListAssociatedInstanceArgs']]]] = None):
        """
        Input properties used for looking up and filtering AllowList resources.
        :param pulumi.Input[str] allow_list_desc: Description of allow list.
        :param pulumi.Input[str] allow_list_id: Id of allow list.
        :param pulumi.Input[int] allow_list_ip_num: The IP number of allow list.
        :param pulumi.Input[str] allow_list_name: Name of allow list.
        :param pulumi.Input[str] allow_list_type: Type of allow list.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow_lists: Ip list of allow list.
        :param pulumi.Input[int] associated_instance_num: The number of instance that associated to allow list.
        :param pulumi.Input[Sequence[pulumi.Input['AllowListAssociatedInstanceArgs']]] associated_instances: Instances associated by this allow list.
        """
        if allow_list_desc is not None:
            pulumi.set(__self__, "allow_list_desc", allow_list_desc)
        if allow_list_id is not None:
            pulumi.set(__self__, "allow_list_id", allow_list_id)
        if allow_list_ip_num is not None:
            pulumi.set(__self__, "allow_list_ip_num", allow_list_ip_num)
        if allow_list_name is not None:
            pulumi.set(__self__, "allow_list_name", allow_list_name)
        if allow_list_type is not None:
            pulumi.set(__self__, "allow_list_type", allow_list_type)
        if allow_lists is not None:
            pulumi.set(__self__, "allow_lists", allow_lists)
        if associated_instance_num is not None:
            pulumi.set(__self__, "associated_instance_num", associated_instance_num)
        if associated_instances is not None:
            pulumi.set(__self__, "associated_instances", associated_instances)

    @property
    @pulumi.getter(name="allowListDesc")
    def allow_list_desc(self) -> Optional[pulumi.Input[str]]:
        """
        Description of allow list.
        """
        return pulumi.get(self, "allow_list_desc")

    @allow_list_desc.setter
    def allow_list_desc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_list_desc", value)

    @property
    @pulumi.getter(name="allowListId")
    def allow_list_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of allow list.
        """
        return pulumi.get(self, "allow_list_id")

    @allow_list_id.setter
    def allow_list_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_list_id", value)

    @property
    @pulumi.getter(name="allowListIpNum")
    def allow_list_ip_num(self) -> Optional[pulumi.Input[int]]:
        """
        The IP number of allow list.
        """
        return pulumi.get(self, "allow_list_ip_num")

    @allow_list_ip_num.setter
    def allow_list_ip_num(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "allow_list_ip_num", value)

    @property
    @pulumi.getter(name="allowListName")
    def allow_list_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of allow list.
        """
        return pulumi.get(self, "allow_list_name")

    @allow_list_name.setter
    def allow_list_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_list_name", value)

    @property
    @pulumi.getter(name="allowListType")
    def allow_list_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of allow list.
        """
        return pulumi.get(self, "allow_list_type")

    @allow_list_type.setter
    def allow_list_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_list_type", value)

    @property
    @pulumi.getter(name="allowLists")
    def allow_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Ip list of allow list.
        """
        return pulumi.get(self, "allow_lists")

    @allow_lists.setter
    def allow_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allow_lists", value)

    @property
    @pulumi.getter(name="associatedInstanceNum")
    def associated_instance_num(self) -> Optional[pulumi.Input[int]]:
        """
        The number of instance that associated to allow list.
        """
        return pulumi.get(self, "associated_instance_num")

    @associated_instance_num.setter
    def associated_instance_num(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "associated_instance_num", value)

    @property
    @pulumi.getter(name="associatedInstances")
    def associated_instances(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AllowListAssociatedInstanceArgs']]]]:
        """
        Instances associated by this allow list.
        """
        return pulumi.get(self, "associated_instances")

    @associated_instances.setter
    def associated_instances(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AllowListAssociatedInstanceArgs']]]]):
        pulumi.set(self, "associated_instances", value)


class AllowList(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_list_desc: Optional[pulumi.Input[str]] = None,
                 allow_list_name: Optional[pulumi.Input[str]] = None,
                 allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a resource to manage redis allow list
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.redis.AllowList("foo",
            allow_lists=[
                "0.0.0.0/0",
                "192.168.0.0/24",
                "192.168.1.1",
                "192.168.2.22",
            ],
            allow_list_desc="renxin terraform测试白xxxxxxx",
            allow_list_name="rx_test_tf_allowlist_create")
        ```

        ## Import

        Redis AllowList can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:redis/allowList:AllowList default acl-cn03wk541s55c376xxxx
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allow_list_desc: Description of allow list.
        :param pulumi.Input[str] allow_list_name: Name of allow list.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow_lists: Ip list of allow list.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AllowListArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage redis allow list
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.redis.AllowList("foo",
            allow_lists=[
                "0.0.0.0/0",
                "192.168.0.0/24",
                "192.168.1.1",
                "192.168.2.22",
            ],
            allow_list_desc="renxin terraform测试白xxxxxxx",
            allow_list_name="rx_test_tf_allowlist_create")
        ```

        ## Import

        Redis AllowList can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:redis/allowList:AllowList default acl-cn03wk541s55c376xxxx
        ```

        :param str resource_name: The name of the resource.
        :param AllowListArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AllowListArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_list_desc: Optional[pulumi.Input[str]] = None,
                 allow_list_name: Optional[pulumi.Input[str]] = None,
                 allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = AllowListArgs.__new__(AllowListArgs)

            __props__.__dict__["allow_list_desc"] = allow_list_desc
            if allow_list_name is None and not opts.urn:
                raise TypeError("Missing required property 'allow_list_name'")
            __props__.__dict__["allow_list_name"] = allow_list_name
            if allow_lists is None and not opts.urn:
                raise TypeError("Missing required property 'allow_lists'")
            __props__.__dict__["allow_lists"] = allow_lists
            __props__.__dict__["allow_list_id"] = None
            __props__.__dict__["allow_list_ip_num"] = None
            __props__.__dict__["allow_list_type"] = None
            __props__.__dict__["associated_instance_num"] = None
            __props__.__dict__["associated_instances"] = None
        super(AllowList, __self__).__init__(
            'volcengine:redis/allowList:AllowList',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allow_list_desc: Optional[pulumi.Input[str]] = None,
            allow_list_id: Optional[pulumi.Input[str]] = None,
            allow_list_ip_num: Optional[pulumi.Input[int]] = None,
            allow_list_name: Optional[pulumi.Input[str]] = None,
            allow_list_type: Optional[pulumi.Input[str]] = None,
            allow_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            associated_instance_num: Optional[pulumi.Input[int]] = None,
            associated_instances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AllowListAssociatedInstanceArgs']]]]] = None) -> 'AllowList':
        """
        Get an existing AllowList resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allow_list_desc: Description of allow list.
        :param pulumi.Input[str] allow_list_id: Id of allow list.
        :param pulumi.Input[int] allow_list_ip_num: The IP number of allow list.
        :param pulumi.Input[str] allow_list_name: Name of allow list.
        :param pulumi.Input[str] allow_list_type: Type of allow list.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow_lists: Ip list of allow list.
        :param pulumi.Input[int] associated_instance_num: The number of instance that associated to allow list.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AllowListAssociatedInstanceArgs']]]] associated_instances: Instances associated by this allow list.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AllowListState.__new__(_AllowListState)

        __props__.__dict__["allow_list_desc"] = allow_list_desc
        __props__.__dict__["allow_list_id"] = allow_list_id
        __props__.__dict__["allow_list_ip_num"] = allow_list_ip_num
        __props__.__dict__["allow_list_name"] = allow_list_name
        __props__.__dict__["allow_list_type"] = allow_list_type
        __props__.__dict__["allow_lists"] = allow_lists
        __props__.__dict__["associated_instance_num"] = associated_instance_num
        __props__.__dict__["associated_instances"] = associated_instances
        return AllowList(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowListDesc")
    def allow_list_desc(self) -> pulumi.Output[Optional[str]]:
        """
        Description of allow list.
        """
        return pulumi.get(self, "allow_list_desc")

    @property
    @pulumi.getter(name="allowListId")
    def allow_list_id(self) -> pulumi.Output[str]:
        """
        Id of allow list.
        """
        return pulumi.get(self, "allow_list_id")

    @property
    @pulumi.getter(name="allowListIpNum")
    def allow_list_ip_num(self) -> pulumi.Output[int]:
        """
        The IP number of allow list.
        """
        return pulumi.get(self, "allow_list_ip_num")

    @property
    @pulumi.getter(name="allowListName")
    def allow_list_name(self) -> pulumi.Output[str]:
        """
        Name of allow list.
        """
        return pulumi.get(self, "allow_list_name")

    @property
    @pulumi.getter(name="allowListType")
    def allow_list_type(self) -> pulumi.Output[str]:
        """
        Type of allow list.
        """
        return pulumi.get(self, "allow_list_type")

    @property
    @pulumi.getter(name="allowLists")
    def allow_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        Ip list of allow list.
        """
        return pulumi.get(self, "allow_lists")

    @property
    @pulumi.getter(name="associatedInstanceNum")
    def associated_instance_num(self) -> pulumi.Output[int]:
        """
        The number of instance that associated to allow list.
        """
        return pulumi.get(self, "associated_instance_num")

    @property
    @pulumi.getter(name="associatedInstances")
    def associated_instances(self) -> pulumi.Output[Sequence['outputs.AllowListAssociatedInstance']]:
        """
        Instances associated by this allow list.
        """
        return pulumi.get(self, "associated_instances")

