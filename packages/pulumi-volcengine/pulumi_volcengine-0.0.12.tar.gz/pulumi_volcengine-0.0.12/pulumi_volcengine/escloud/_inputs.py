# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'InstanceInstanceConfigurationArgs',
    'InstanceInstanceConfigurationNodeSpecsAssignArgs',
]

@pulumi.input_type
class InstanceInstanceConfigurationArgs:
    def __init__(__self__, *,
                 admin_password: pulumi.Input[str],
                 admin_user_name: pulumi.Input[str],
                 charge_type: pulumi.Input[str],
                 configuration_code: pulumi.Input[str],
                 enable_https: pulumi.Input[bool],
                 enable_pure_master: pulumi.Input[bool],
                 node_specs_assigns: pulumi.Input[Sequence[pulumi.Input['InstanceInstanceConfigurationNodeSpecsAssignArgs']]],
                 subnet_id: pulumi.Input[str],
                 version: pulumi.Input[str],
                 zone_number: pulumi.Input[int],
                 force_restart_after_scale: Optional[pulumi.Input[bool]] = None,
                 instance_name: Optional[pulumi.Input[str]] = None,
                 maintenance_days: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 maintenance_time: Optional[pulumi.Input[str]] = None,
                 project_name: Optional[pulumi.Input[str]] = None,
                 region_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] admin_password: The password of administrator account. When importing resources, this attribute will not be imported. If this attribute is set, please use lifecycle and ignore_changes ignore changes in fields.
        :param pulumi.Input[str] admin_user_name: The name of administrator account(should be admin).
        :param pulumi.Input[str] charge_type: The charge type of ESCloud instance, the value can be PostPaid or PrePaid.
        :param pulumi.Input[str] configuration_code: Configuration code used for billing.
        :param pulumi.Input[bool] enable_https: Whether Https access is enabled.
        :param pulumi.Input[bool] enable_pure_master: Whether the Master node is independent.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceInstanceConfigurationNodeSpecsAssignArgs']]] node_specs_assigns: The number and configuration of various ESCloud instance node. Kibana NodeSpecsAssign should not be modified.
        :param pulumi.Input[str] subnet_id: The ID of subnet, the subnet must belong to the AZ selected.
        :param pulumi.Input[str] version: The version of ESCloud instance, the value is V6_7 or V7_10.
        :param pulumi.Input[int] zone_number: The zone count of the ESCloud instance used.
        :param pulumi.Input[bool] force_restart_after_scale: Whether to force restart when changes are made. If true, it means that the cluster will be forced to restart without paying attention to instance availability. Works only on modified the node_specs_assigns field.
        :param pulumi.Input[str] instance_name: The name of ESCloud instance.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] maintenance_days: The maintainable date for the instance. Works only on modified scenes.
        :param pulumi.Input[str] maintenance_time: The maintainable time period for the instance. Works only on modified scenes.
        :param pulumi.Input[str] project_name: The project name  to which the ESCloud instance belongs.
        :param pulumi.Input[str] region_id: The region ID of ESCloud instance.
        :param pulumi.Input[str] zone_id: The available zone ID of ESCloud instance.
        """
        pulumi.set(__self__, "admin_password", admin_password)
        pulumi.set(__self__, "admin_user_name", admin_user_name)
        pulumi.set(__self__, "charge_type", charge_type)
        pulumi.set(__self__, "configuration_code", configuration_code)
        pulumi.set(__self__, "enable_https", enable_https)
        pulumi.set(__self__, "enable_pure_master", enable_pure_master)
        pulumi.set(__self__, "node_specs_assigns", node_specs_assigns)
        pulumi.set(__self__, "subnet_id", subnet_id)
        pulumi.set(__self__, "version", version)
        pulumi.set(__self__, "zone_number", zone_number)
        if force_restart_after_scale is not None:
            pulumi.set(__self__, "force_restart_after_scale", force_restart_after_scale)
        if instance_name is not None:
            pulumi.set(__self__, "instance_name", instance_name)
        if maintenance_days is not None:
            pulumi.set(__self__, "maintenance_days", maintenance_days)
        if maintenance_time is not None:
            pulumi.set(__self__, "maintenance_time", maintenance_time)
        if project_name is not None:
            pulumi.set(__self__, "project_name", project_name)
        if region_id is not None:
            pulumi.set(__self__, "region_id", region_id)
        if zone_id is not None:
            pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> pulumi.Input[str]:
        """
        The password of administrator account. When importing resources, this attribute will not be imported. If this attribute is set, please use lifecycle and ignore_changes ignore changes in fields.
        """
        return pulumi.get(self, "admin_password")

    @admin_password.setter
    def admin_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_password", value)

    @property
    @pulumi.getter(name="adminUserName")
    def admin_user_name(self) -> pulumi.Input[str]:
        """
        The name of administrator account(should be admin).
        """
        return pulumi.get(self, "admin_user_name")

    @admin_user_name.setter
    def admin_user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_user_name", value)

    @property
    @pulumi.getter(name="chargeType")
    def charge_type(self) -> pulumi.Input[str]:
        """
        The charge type of ESCloud instance, the value can be PostPaid or PrePaid.
        """
        return pulumi.get(self, "charge_type")

    @charge_type.setter
    def charge_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "charge_type", value)

    @property
    @pulumi.getter(name="configurationCode")
    def configuration_code(self) -> pulumi.Input[str]:
        """
        Configuration code used for billing.
        """
        return pulumi.get(self, "configuration_code")

    @configuration_code.setter
    def configuration_code(self, value: pulumi.Input[str]):
        pulumi.set(self, "configuration_code", value)

    @property
    @pulumi.getter(name="enableHttps")
    def enable_https(self) -> pulumi.Input[bool]:
        """
        Whether Https access is enabled.
        """
        return pulumi.get(self, "enable_https")

    @enable_https.setter
    def enable_https(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable_https", value)

    @property
    @pulumi.getter(name="enablePureMaster")
    def enable_pure_master(self) -> pulumi.Input[bool]:
        """
        Whether the Master node is independent.
        """
        return pulumi.get(self, "enable_pure_master")

    @enable_pure_master.setter
    def enable_pure_master(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable_pure_master", value)

    @property
    @pulumi.getter(name="nodeSpecsAssigns")
    def node_specs_assigns(self) -> pulumi.Input[Sequence[pulumi.Input['InstanceInstanceConfigurationNodeSpecsAssignArgs']]]:
        """
        The number and configuration of various ESCloud instance node. Kibana NodeSpecsAssign should not be modified.
        """
        return pulumi.get(self, "node_specs_assigns")

    @node_specs_assigns.setter
    def node_specs_assigns(self, value: pulumi.Input[Sequence[pulumi.Input['InstanceInstanceConfigurationNodeSpecsAssignArgs']]]):
        pulumi.set(self, "node_specs_assigns", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The ID of subnet, the subnet must belong to the AZ selected.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        """
        The version of ESCloud instance, the value is V6_7 or V7_10.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter(name="zoneNumber")
    def zone_number(self) -> pulumi.Input[int]:
        """
        The zone count of the ESCloud instance used.
        """
        return pulumi.get(self, "zone_number")

    @zone_number.setter
    def zone_number(self, value: pulumi.Input[int]):
        pulumi.set(self, "zone_number", value)

    @property
    @pulumi.getter(name="forceRestartAfterScale")
    def force_restart_after_scale(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to force restart when changes are made. If true, it means that the cluster will be forced to restart without paying attention to instance availability. Works only on modified the node_specs_assigns field.
        """
        return pulumi.get(self, "force_restart_after_scale")

    @force_restart_after_scale.setter
    def force_restart_after_scale(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_restart_after_scale", value)

    @property
    @pulumi.getter(name="instanceName")
    def instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of ESCloud instance.
        """
        return pulumi.get(self, "instance_name")

    @instance_name.setter
    def instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_name", value)

    @property
    @pulumi.getter(name="maintenanceDays")
    def maintenance_days(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The maintainable date for the instance. Works only on modified scenes.
        """
        return pulumi.get(self, "maintenance_days")

    @maintenance_days.setter
    def maintenance_days(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "maintenance_days", value)

    @property
    @pulumi.getter(name="maintenanceTime")
    def maintenance_time(self) -> Optional[pulumi.Input[str]]:
        """
        The maintainable time period for the instance. Works only on modified scenes.
        """
        return pulumi.get(self, "maintenance_time")

    @maintenance_time.setter
    def maintenance_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maintenance_time", value)

    @property
    @pulumi.getter(name="projectName")
    def project_name(self) -> Optional[pulumi.Input[str]]:
        """
        The project name  to which the ESCloud instance belongs.
        """
        return pulumi.get(self, "project_name")

    @project_name.setter
    def project_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_name", value)

    @property
    @pulumi.getter(name="regionId")
    def region_id(self) -> Optional[pulumi.Input[str]]:
        """
        The region ID of ESCloud instance.
        """
        return pulumi.get(self, "region_id")

    @region_id.setter
    def region_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region_id", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The available zone ID of ESCloud instance.
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone_id", value)


@pulumi.input_type
class InstanceInstanceConfigurationNodeSpecsAssignArgs:
    def __init__(__self__, *,
                 number: pulumi.Input[int],
                 resource_spec_name: pulumi.Input[str],
                 type: pulumi.Input[str],
                 storage_size: Optional[pulumi.Input[int]] = None,
                 storage_spec_name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[int] number: The number of node.
        :param pulumi.Input[str] resource_spec_name: The name of compute resource spec, the value is `kibana.x2.small` or `es.x4.medium` or `es.x4.large` or `es.x4.xlarge` or `es.x2.2xlarge` or `es.x4.2xlarge` or `es.x2.3xlarge`.
        :param pulumi.Input[str] type: The type of node, the value is `Master` or `Hot` or `Kibana`.
        :param pulumi.Input[int] storage_size: The size of storage. Kibana NodeSpecsAssign should not specify this field.
        :param pulumi.Input[str] storage_spec_name: The name of storage spec. Kibana NodeSpecsAssign should not specify this field.
        """
        pulumi.set(__self__, "number", number)
        pulumi.set(__self__, "resource_spec_name", resource_spec_name)
        pulumi.set(__self__, "type", type)
        if storage_size is not None:
            pulumi.set(__self__, "storage_size", storage_size)
        if storage_spec_name is not None:
            pulumi.set(__self__, "storage_spec_name", storage_spec_name)

    @property
    @pulumi.getter
    def number(self) -> pulumi.Input[int]:
        """
        The number of node.
        """
        return pulumi.get(self, "number")

    @number.setter
    def number(self, value: pulumi.Input[int]):
        pulumi.set(self, "number", value)

    @property
    @pulumi.getter(name="resourceSpecName")
    def resource_spec_name(self) -> pulumi.Input[str]:
        """
        The name of compute resource spec, the value is `kibana.x2.small` or `es.x4.medium` or `es.x4.large` or `es.x4.xlarge` or `es.x2.2xlarge` or `es.x4.2xlarge` or `es.x2.3xlarge`.
        """
        return pulumi.get(self, "resource_spec_name")

    @resource_spec_name.setter
    def resource_spec_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_spec_name", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of node, the value is `Master` or `Hot` or `Kibana`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="storageSize")
    def storage_size(self) -> Optional[pulumi.Input[int]]:
        """
        The size of storage. Kibana NodeSpecsAssign should not specify this field.
        """
        return pulumi.get(self, "storage_size")

    @storage_size.setter
    def storage_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "storage_size", value)

    @property
    @pulumi.getter(name="storageSpecName")
    def storage_spec_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of storage spec. Kibana NodeSpecsAssign should not specify this field.
        """
        return pulumi.get(self, "storage_spec_name")

    @storage_spec_name.setter
    def storage_spec_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_spec_name", value)


