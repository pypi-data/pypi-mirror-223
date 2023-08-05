# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['KeyPairAssociateArgs', 'KeyPairAssociate']

@pulumi.input_type
class KeyPairAssociateArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 key_pair_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a KeyPairAssociate resource.
        :param pulumi.Input[str] instance_id: The ID of ECS Instance.
        :param pulumi.Input[str] key_pair_id: The ID of ECS KeyPair Associate.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "key_pair_id", key_pair_id)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The ID of ECS Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="keyPairId")
    def key_pair_id(self) -> pulumi.Input[str]:
        """
        The ID of ECS KeyPair Associate.
        """
        return pulumi.get(self, "key_pair_id")

    @key_pair_id.setter
    def key_pair_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_pair_id", value)


@pulumi.input_type
class _KeyPairAssociateState:
    def __init__(__self__, *,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 key_pair_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering KeyPairAssociate resources.
        :param pulumi.Input[str] instance_id: The ID of ECS Instance.
        :param pulumi.Input[str] key_pair_id: The ID of ECS KeyPair Associate.
        """
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if key_pair_id is not None:
            pulumi.set(__self__, "key_pair_id", key_pair_id)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of ECS Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="keyPairId")
    def key_pair_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of ECS KeyPair Associate.
        """
        return pulumi.get(self, "key_pair_id")

    @key_pair_id.setter
    def key_pair_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_pair_id", value)


class KeyPairAssociate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 key_pair_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage ecs key pair associate
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo_key_pair = volcengine.ecs.KeyPair("fooKeyPair",
            key_pair_name="acc-test-key-name",
            description="acc-test")
        foo_zones = volcengine.ecs.zones()
        foo_images = volcengine.ecs.images(os_type="Linux",
            visibility="public",
            instance_type_id="ecs.g1.large")
        foo_vpc = volcengine.vpc.Vpc("fooVpc",
            vpc_name="acc-test-vpc",
            cidr_block="172.16.0.0/16")
        foo_subnet = volcengine.vpc.Subnet("fooSubnet",
            subnet_name="acc-test-subnet",
            cidr_block="172.16.0.0/24",
            zone_id=foo_zones.zones[0].id,
            vpc_id=foo_vpc.id)
        foo_security_group = volcengine.vpc.SecurityGroup("fooSecurityGroup",
            vpc_id=foo_vpc.id,
            security_group_name="acc-test-security-group")
        foo_instance = volcengine.ecs.Instance("fooInstance",
            image_id=foo_images.images[0].image_id,
            instance_type="ecs.g1.large",
            instance_name="acc-test-ecs-name",
            password="your password",
            instance_charge_type="PostPaid",
            system_volume_type="ESSD_PL0",
            system_volume_size=40,
            subnet_id=foo_subnet.id,
            security_group_ids=[foo_security_group.id])
        foo_key_pair_associate = volcengine.ecs.KeyPairAssociate("fooKeyPairAssociate",
            instance_id=foo_instance.id,
            key_pair_id=foo_key_pair.id)
        ```

        ## Import

        ECS key pair associate can be imported using the id, e.g. After binding the key pair, the instance needs to be restarted for the key pair to take effect. After the key pair is bound, the password login method will automatically become invalid. If your instance has been set for password login, after the key pair is bound, you will no longer be able to use the password login method.

        ```sh
         $ pulumi import volcengine:ecs/keyPairAssociate:KeyPairAssociate default kp-ybti5tkpkv2udbfolrft:i-mizl7m1kqccg5smt1bdpijuj
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: The ID of ECS Instance.
        :param pulumi.Input[str] key_pair_id: The ID of ECS KeyPair Associate.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KeyPairAssociateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage ecs key pair associate
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo_key_pair = volcengine.ecs.KeyPair("fooKeyPair",
            key_pair_name="acc-test-key-name",
            description="acc-test")
        foo_zones = volcengine.ecs.zones()
        foo_images = volcengine.ecs.images(os_type="Linux",
            visibility="public",
            instance_type_id="ecs.g1.large")
        foo_vpc = volcengine.vpc.Vpc("fooVpc",
            vpc_name="acc-test-vpc",
            cidr_block="172.16.0.0/16")
        foo_subnet = volcengine.vpc.Subnet("fooSubnet",
            subnet_name="acc-test-subnet",
            cidr_block="172.16.0.0/24",
            zone_id=foo_zones.zones[0].id,
            vpc_id=foo_vpc.id)
        foo_security_group = volcengine.vpc.SecurityGroup("fooSecurityGroup",
            vpc_id=foo_vpc.id,
            security_group_name="acc-test-security-group")
        foo_instance = volcengine.ecs.Instance("fooInstance",
            image_id=foo_images.images[0].image_id,
            instance_type="ecs.g1.large",
            instance_name="acc-test-ecs-name",
            password="your password",
            instance_charge_type="PostPaid",
            system_volume_type="ESSD_PL0",
            system_volume_size=40,
            subnet_id=foo_subnet.id,
            security_group_ids=[foo_security_group.id])
        foo_key_pair_associate = volcengine.ecs.KeyPairAssociate("fooKeyPairAssociate",
            instance_id=foo_instance.id,
            key_pair_id=foo_key_pair.id)
        ```

        ## Import

        ECS key pair associate can be imported using the id, e.g. After binding the key pair, the instance needs to be restarted for the key pair to take effect. After the key pair is bound, the password login method will automatically become invalid. If your instance has been set for password login, after the key pair is bound, you will no longer be able to use the password login method.

        ```sh
         $ pulumi import volcengine:ecs/keyPairAssociate:KeyPairAssociate default kp-ybti5tkpkv2udbfolrft:i-mizl7m1kqccg5smt1bdpijuj
        ```

        :param str resource_name: The name of the resource.
        :param KeyPairAssociateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyPairAssociateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 key_pair_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = KeyPairAssociateArgs.__new__(KeyPairAssociateArgs)

            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if key_pair_id is None and not opts.urn:
                raise TypeError("Missing required property 'key_pair_id'")
            __props__.__dict__["key_pair_id"] = key_pair_id
        super(KeyPairAssociate, __self__).__init__(
            'volcengine:ecs/keyPairAssociate:KeyPairAssociate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            key_pair_id: Optional[pulumi.Input[str]] = None) -> 'KeyPairAssociate':
        """
        Get an existing KeyPairAssociate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: The ID of ECS Instance.
        :param pulumi.Input[str] key_pair_id: The ID of ECS KeyPair Associate.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KeyPairAssociateState.__new__(_KeyPairAssociateState)

        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["key_pair_id"] = key_pair_id
        return KeyPairAssociate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The ID of ECS Instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="keyPairId")
    def key_pair_id(self) -> pulumi.Output[str]:
        """
        The ID of ECS KeyPair Associate.
        """
        return pulumi.get(self, "key_pair_id")

