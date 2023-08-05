# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RuleArgs', 'Rule']

@pulumi.input_type
class RuleArgs:
    def __init__(__self__, *,
                 listener_id: pulumi.Input[str],
                 server_group_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Rule resource.
        :param pulumi.Input[str] listener_id: The ID of listener.
        :param pulumi.Input[str] server_group_id: Server Group Id.
        :param pulumi.Input[str] description: The description of the Rule.
        :param pulumi.Input[str] domain: The domain of Rule.
        :param pulumi.Input[str] url: The Url of Rule.
        """
        pulumi.set(__self__, "listener_id", listener_id)
        pulumi.set(__self__, "server_group_id", server_group_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Input[str]:
        """
        The ID of listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter(name="serverGroupId")
    def server_group_id(self) -> pulumi.Input[str]:
        """
        Server Group Id.
        """
        return pulumi.get(self, "server_group_id")

    @server_group_id.setter
    def server_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_group_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        The domain of Rule.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The Url of Rule.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


@pulumi.input_type
class _RuleState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 server_group_id: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Rule resources.
        :param pulumi.Input[str] description: The description of the Rule.
        :param pulumi.Input[str] domain: The domain of Rule.
        :param pulumi.Input[str] listener_id: The ID of listener.
        :param pulumi.Input[str] server_group_id: Server Group Id.
        :param pulumi.Input[str] url: The Url of Rule.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if listener_id is not None:
            pulumi.set(__self__, "listener_id", listener_id)
        if server_group_id is not None:
            pulumi.set(__self__, "server_group_id", server_group_id)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        The domain of Rule.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter(name="serverGroupId")
    def server_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        Server Group Id.
        """
        return pulumi.get(self, "server_group_id")

    @server_group_id.setter
    def server_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_group_id", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The Url of Rule.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


class Rule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 server_group_id: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage clb rule
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo_zones = volcengine.ecs.zones()
        foo_vpc = volcengine.vpc.Vpc("fooVpc",
            vpc_name="acc-test-vpc",
            cidr_block="172.16.0.0/16")
        foo_subnet = volcengine.vpc.Subnet("fooSubnet",
            subnet_name="acc-test-subnet",
            cidr_block="172.16.0.0/24",
            zone_id=foo_zones.zones[0].id,
            vpc_id=foo_vpc.id)
        foo_clb = volcengine.clb.Clb("fooClb",
            type="public",
            subnet_id=foo_subnet.id,
            load_balancer_spec="small_1",
            description="acc0Demo",
            load_balancer_name="acc-test-create",
            eip_billing_config=volcengine.clb.ClbEipBillingConfigArgs(
                isp="BGP",
                eip_billing_type="PostPaidByBandwidth",
                bandwidth=1,
            ))
        foo_server_group = volcengine.clb.ServerGroup("fooServerGroup",
            load_balancer_id=foo_clb.id,
            server_group_name="acc-test-create",
            description="hello demo11")
        foo_listener = volcengine.clb.Listener("fooListener",
            load_balancer_id=foo_clb.id,
            listener_name="acc-test-listener",
            protocol="HTTP",
            port=90,
            server_group_id=foo_server_group.id,
            health_check=volcengine.clb.ListenerHealthCheckArgs(
                enabled="on",
                interval=10,
                timeout=3,
                healthy_threshold=5,
                un_healthy_threshold=2,
                domain="volcengine.com",
                http_code="http_2xx",
                method="GET",
                uri="/",
            ),
            enabled="on")
        foo_rule = volcengine.clb.Rule("fooRule",
            listener_id=foo_listener.id,
            server_group_id=foo_server_group.id,
            domain="test-volc123.com",
            url="/tftest")
        ```

        ## Import

        Rule can be imported using the id, e.g. NoticeresourceId is ruleId, due to the lack of describeRuleAttributes in openapi, for import resources, please use ruleId:listenerId to import. we will fix this problem later.

        ```sh
         $ pulumi import volcengine:clb/rule:Rule foo rule-273zb9hzi1gqo7fap8u1k3utb:lsn-273ywvnmiu70g7fap8u2xzg9d
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the Rule.
        :param pulumi.Input[str] domain: The domain of Rule.
        :param pulumi.Input[str] listener_id: The ID of listener.
        :param pulumi.Input[str] server_group_id: Server Group Id.
        :param pulumi.Input[str] url: The Url of Rule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage clb rule
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo_zones = volcengine.ecs.zones()
        foo_vpc = volcengine.vpc.Vpc("fooVpc",
            vpc_name="acc-test-vpc",
            cidr_block="172.16.0.0/16")
        foo_subnet = volcengine.vpc.Subnet("fooSubnet",
            subnet_name="acc-test-subnet",
            cidr_block="172.16.0.0/24",
            zone_id=foo_zones.zones[0].id,
            vpc_id=foo_vpc.id)
        foo_clb = volcengine.clb.Clb("fooClb",
            type="public",
            subnet_id=foo_subnet.id,
            load_balancer_spec="small_1",
            description="acc0Demo",
            load_balancer_name="acc-test-create",
            eip_billing_config=volcengine.clb.ClbEipBillingConfigArgs(
                isp="BGP",
                eip_billing_type="PostPaidByBandwidth",
                bandwidth=1,
            ))
        foo_server_group = volcengine.clb.ServerGroup("fooServerGroup",
            load_balancer_id=foo_clb.id,
            server_group_name="acc-test-create",
            description="hello demo11")
        foo_listener = volcengine.clb.Listener("fooListener",
            load_balancer_id=foo_clb.id,
            listener_name="acc-test-listener",
            protocol="HTTP",
            port=90,
            server_group_id=foo_server_group.id,
            health_check=volcengine.clb.ListenerHealthCheckArgs(
                enabled="on",
                interval=10,
                timeout=3,
                healthy_threshold=5,
                un_healthy_threshold=2,
                domain="volcengine.com",
                http_code="http_2xx",
                method="GET",
                uri="/",
            ),
            enabled="on")
        foo_rule = volcengine.clb.Rule("fooRule",
            listener_id=foo_listener.id,
            server_group_id=foo_server_group.id,
            domain="test-volc123.com",
            url="/tftest")
        ```

        ## Import

        Rule can be imported using the id, e.g. NoticeresourceId is ruleId, due to the lack of describeRuleAttributes in openapi, for import resources, please use ruleId:listenerId to import. we will fix this problem later.

        ```sh
         $ pulumi import volcengine:clb/rule:Rule foo rule-273zb9hzi1gqo7fap8u1k3utb:lsn-273ywvnmiu70g7fap8u2xzg9d
        ```

        :param str resource_name: The name of the resource.
        :param RuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 server_group_id: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
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
            __props__ = RuleArgs.__new__(RuleArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["domain"] = domain
            if listener_id is None and not opts.urn:
                raise TypeError("Missing required property 'listener_id'")
            __props__.__dict__["listener_id"] = listener_id
            if server_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'server_group_id'")
            __props__.__dict__["server_group_id"] = server_group_id
            __props__.__dict__["url"] = url
        super(Rule, __self__).__init__(
            'volcengine:clb/rule:Rule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            domain: Optional[pulumi.Input[str]] = None,
            listener_id: Optional[pulumi.Input[str]] = None,
            server_group_id: Optional[pulumi.Input[str]] = None,
            url: Optional[pulumi.Input[str]] = None) -> 'Rule':
        """
        Get an existing Rule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the Rule.
        :param pulumi.Input[str] domain: The domain of Rule.
        :param pulumi.Input[str] listener_id: The ID of listener.
        :param pulumi.Input[str] server_group_id: Server Group Id.
        :param pulumi.Input[str] url: The Url of Rule.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RuleState.__new__(_RuleState)

        __props__.__dict__["description"] = description
        __props__.__dict__["domain"] = domain
        __props__.__dict__["listener_id"] = listener_id
        __props__.__dict__["server_group_id"] = server_group_id
        __props__.__dict__["url"] = url
        return Rule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the Rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[Optional[str]]:
        """
        The domain of Rule.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Output[str]:
        """
        The ID of listener.
        """
        return pulumi.get(self, "listener_id")

    @property
    @pulumi.getter(name="serverGroupId")
    def server_group_id(self) -> pulumi.Output[str]:
        """
        Server Group Id.
        """
        return pulumi.get(self, "server_group_id")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[Optional[str]]:
        """
        The Url of Rule.
        """
        return pulumi.get(self, "url")

