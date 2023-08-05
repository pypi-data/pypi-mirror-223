# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VolumeAttachArgs', 'VolumeAttach']

@pulumi.input_type
class VolumeAttachArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 volume_id: pulumi.Input[str],
                 delete_with_instance: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a VolumeAttach resource.
        :param pulumi.Input[str] instance_id: The Id of Instance.
        :param pulumi.Input[str] volume_id: The Id of Volume.
        :param pulumi.Input[bool] delete_with_instance: Delete Volume with Attached Instance.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "volume_id", volume_id)
        if delete_with_instance is not None:
            pulumi.set(__self__, "delete_with_instance", delete_with_instance)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The Id of Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> pulumi.Input[str]:
        """
        The Id of Volume.
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "volume_id", value)

    @property
    @pulumi.getter(name="deleteWithInstance")
    def delete_with_instance(self) -> Optional[pulumi.Input[bool]]:
        """
        Delete Volume with Attached Instance.
        """
        return pulumi.get(self, "delete_with_instance")

    @delete_with_instance.setter
    def delete_with_instance(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_with_instance", value)


@pulumi.input_type
class _VolumeAttachState:
    def __init__(__self__, *,
                 created_at: Optional[pulumi.Input[str]] = None,
                 delete_with_instance: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VolumeAttach resources.
        :param pulumi.Input[str] created_at: Creation time of Volume.
        :param pulumi.Input[bool] delete_with_instance: Delete Volume with Attached Instance.
        :param pulumi.Input[str] instance_id: The Id of Instance.
        :param pulumi.Input[str] status: Status of Volume.
        :param pulumi.Input[str] updated_at: Update time of Volume.
        :param pulumi.Input[str] volume_id: The Id of Volume.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if delete_with_instance is not None:
            pulumi.set(__self__, "delete_with_instance", delete_with_instance)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)
        if volume_id is not None:
            pulumi.set(__self__, "volume_id", volume_id)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        Creation time of Volume.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="deleteWithInstance")
    def delete_with_instance(self) -> Optional[pulumi.Input[bool]]:
        """
        Delete Volume with Attached Instance.
        """
        return pulumi.get(self, "delete_with_instance")

    @delete_with_instance.setter
    def delete_with_instance(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_with_instance", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of Volume.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[str]]:
        """
        Update time of Volume.
        """
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_at", value)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of Volume.
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "volume_id", value)


class VolumeAttach(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delete_with_instance: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage volume attach
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.ebs.VolumeAttach("foo",
            instance_id="i-4ay59ww7dq8dt9c29hd4",
            volume_id="vol-3tzl52wubz3b9fciw7ev")
        ```

        ## Import

        VolumeAttach can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:ebs/volumeAttach:VolumeAttach default vol-abc12345:i-abc12345
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] delete_with_instance: Delete Volume with Attached Instance.
        :param pulumi.Input[str] instance_id: The Id of Instance.
        :param pulumi.Input[str] volume_id: The Id of Volume.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VolumeAttachArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage volume attach
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.ebs.VolumeAttach("foo",
            instance_id="i-4ay59ww7dq8dt9c29hd4",
            volume_id="vol-3tzl52wubz3b9fciw7ev")
        ```

        ## Import

        VolumeAttach can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:ebs/volumeAttach:VolumeAttach default vol-abc12345:i-abc12345
        ```

        :param str resource_name: The name of the resource.
        :param VolumeAttachArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VolumeAttachArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delete_with_instance: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = VolumeAttachArgs.__new__(VolumeAttachArgs)

            __props__.__dict__["delete_with_instance"] = delete_with_instance
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if volume_id is None and not opts.urn:
                raise TypeError("Missing required property 'volume_id'")
            __props__.__dict__["volume_id"] = volume_id
            __props__.__dict__["created_at"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["updated_at"] = None
        super(VolumeAttach, __self__).__init__(
            'volcengine:ebs/volumeAttach:VolumeAttach',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            delete_with_instance: Optional[pulumi.Input[bool]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            updated_at: Optional[pulumi.Input[str]] = None,
            volume_id: Optional[pulumi.Input[str]] = None) -> 'VolumeAttach':
        """
        Get an existing VolumeAttach resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_at: Creation time of Volume.
        :param pulumi.Input[bool] delete_with_instance: Delete Volume with Attached Instance.
        :param pulumi.Input[str] instance_id: The Id of Instance.
        :param pulumi.Input[str] status: Status of Volume.
        :param pulumi.Input[str] updated_at: Update time of Volume.
        :param pulumi.Input[str] volume_id: The Id of Volume.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VolumeAttachState.__new__(_VolumeAttachState)

        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["delete_with_instance"] = delete_with_instance
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["status"] = status
        __props__.__dict__["updated_at"] = updated_at
        __props__.__dict__["volume_id"] = volume_id
        return VolumeAttach(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Creation time of Volume.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="deleteWithInstance")
    def delete_with_instance(self) -> pulumi.Output[bool]:
        """
        Delete Volume with Attached Instance.
        """
        return pulumi.get(self, "delete_with_instance")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The Id of Instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of Volume.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        Update time of Volume.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> pulumi.Output[str]:
        """
        The Id of Volume.
        """
        return pulumi.get(self, "volume_id")

