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

__all__ = ['CloudServerArgs', 'CloudServer']

@pulumi.input_type
class CloudServerArgs:
    def __init__(__self__, *,
                 cloudserver_name: pulumi.Input[str],
                 default_area_name: pulumi.Input[str],
                 default_isp: pulumi.Input[str],
                 image_id: pulumi.Input[str],
                 network_config: pulumi.Input['CloudServerNetworkConfigArgs'],
                 schedule_strategy: pulumi.Input['CloudServerScheduleStrategyArgs'],
                 secret_type: pulumi.Input[str],
                 server_area_level: pulumi.Input[str],
                 spec_name: pulumi.Input[str],
                 storage_config: pulumi.Input['CloudServerStorageConfigArgs'],
                 billing_config: Optional[pulumi.Input['CloudServerBillingConfigArgs']] = None,
                 custom_data: Optional[pulumi.Input['CloudServerCustomDataArgs']] = None,
                 default_cluster_name: Optional[pulumi.Input[str]] = None,
                 secret_data: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CloudServer resource.
        :param pulumi.Input[str] cloudserver_name: The name of cloud server.
        :param pulumi.Input[str] default_area_name: The name of default area.
        :param pulumi.Input[str] default_isp: The default isp info.
        :param pulumi.Input[str] image_id: The image id of cloud server.
        :param pulumi.Input['CloudServerNetworkConfigArgs'] network_config: The config of the network.
        :param pulumi.Input['CloudServerScheduleStrategyArgs'] schedule_strategy: The schedule strategy.
        :param pulumi.Input[str] secret_type: The type of secret. The value can be `KeyPair` or `Password`.
        :param pulumi.Input[str] server_area_level: The server area level. The value can be `region` or `city`.
        :param pulumi.Input[str] spec_name: The spec name of cloud server.
        :param pulumi.Input['CloudServerStorageConfigArgs'] storage_config: The config of the storage.
        :param pulumi.Input['CloudServerBillingConfigArgs'] billing_config: The config of the billing.
        :param pulumi.Input['CloudServerCustomDataArgs'] custom_data: The custom data.
        :param pulumi.Input[str] default_cluster_name: The name of default cluster.
        :param pulumi.Input[str] secret_data: The data of secret. The value can be Password or KeyPair ID.
        """
        pulumi.set(__self__, "cloudserver_name", cloudserver_name)
        pulumi.set(__self__, "default_area_name", default_area_name)
        pulumi.set(__self__, "default_isp", default_isp)
        pulumi.set(__self__, "image_id", image_id)
        pulumi.set(__self__, "network_config", network_config)
        pulumi.set(__self__, "schedule_strategy", schedule_strategy)
        pulumi.set(__self__, "secret_type", secret_type)
        pulumi.set(__self__, "server_area_level", server_area_level)
        pulumi.set(__self__, "spec_name", spec_name)
        pulumi.set(__self__, "storage_config", storage_config)
        if billing_config is not None:
            pulumi.set(__self__, "billing_config", billing_config)
        if custom_data is not None:
            pulumi.set(__self__, "custom_data", custom_data)
        if default_cluster_name is not None:
            pulumi.set(__self__, "default_cluster_name", default_cluster_name)
        if secret_data is not None:
            pulumi.set(__self__, "secret_data", secret_data)

    @property
    @pulumi.getter(name="cloudserverName")
    def cloudserver_name(self) -> pulumi.Input[str]:
        """
        The name of cloud server.
        """
        return pulumi.get(self, "cloudserver_name")

    @cloudserver_name.setter
    def cloudserver_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cloudserver_name", value)

    @property
    @pulumi.getter(name="defaultAreaName")
    def default_area_name(self) -> pulumi.Input[str]:
        """
        The name of default area.
        """
        return pulumi.get(self, "default_area_name")

    @default_area_name.setter
    def default_area_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_area_name", value)

    @property
    @pulumi.getter(name="defaultIsp")
    def default_isp(self) -> pulumi.Input[str]:
        """
        The default isp info.
        """
        return pulumi.get(self, "default_isp")

    @default_isp.setter
    def default_isp(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_isp", value)

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> pulumi.Input[str]:
        """
        The image id of cloud server.
        """
        return pulumi.get(self, "image_id")

    @image_id.setter
    def image_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "image_id", value)

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> pulumi.Input['CloudServerNetworkConfigArgs']:
        """
        The config of the network.
        """
        return pulumi.get(self, "network_config")

    @network_config.setter
    def network_config(self, value: pulumi.Input['CloudServerNetworkConfigArgs']):
        pulumi.set(self, "network_config", value)

    @property
    @pulumi.getter(name="scheduleStrategy")
    def schedule_strategy(self) -> pulumi.Input['CloudServerScheduleStrategyArgs']:
        """
        The schedule strategy.
        """
        return pulumi.get(self, "schedule_strategy")

    @schedule_strategy.setter
    def schedule_strategy(self, value: pulumi.Input['CloudServerScheduleStrategyArgs']):
        pulumi.set(self, "schedule_strategy", value)

    @property
    @pulumi.getter(name="secretType")
    def secret_type(self) -> pulumi.Input[str]:
        """
        The type of secret. The value can be `KeyPair` or `Password`.
        """
        return pulumi.get(self, "secret_type")

    @secret_type.setter
    def secret_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "secret_type", value)

    @property
    @pulumi.getter(name="serverAreaLevel")
    def server_area_level(self) -> pulumi.Input[str]:
        """
        The server area level. The value can be `region` or `city`.
        """
        return pulumi.get(self, "server_area_level")

    @server_area_level.setter
    def server_area_level(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_area_level", value)

    @property
    @pulumi.getter(name="specName")
    def spec_name(self) -> pulumi.Input[str]:
        """
        The spec name of cloud server.
        """
        return pulumi.get(self, "spec_name")

    @spec_name.setter
    def spec_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "spec_name", value)

    @property
    @pulumi.getter(name="storageConfig")
    def storage_config(self) -> pulumi.Input['CloudServerStorageConfigArgs']:
        """
        The config of the storage.
        """
        return pulumi.get(self, "storage_config")

    @storage_config.setter
    def storage_config(self, value: pulumi.Input['CloudServerStorageConfigArgs']):
        pulumi.set(self, "storage_config", value)

    @property
    @pulumi.getter(name="billingConfig")
    def billing_config(self) -> Optional[pulumi.Input['CloudServerBillingConfigArgs']]:
        """
        The config of the billing.
        """
        return pulumi.get(self, "billing_config")

    @billing_config.setter
    def billing_config(self, value: Optional[pulumi.Input['CloudServerBillingConfigArgs']]):
        pulumi.set(self, "billing_config", value)

    @property
    @pulumi.getter(name="customData")
    def custom_data(self) -> Optional[pulumi.Input['CloudServerCustomDataArgs']]:
        """
        The custom data.
        """
        return pulumi.get(self, "custom_data")

    @custom_data.setter
    def custom_data(self, value: Optional[pulumi.Input['CloudServerCustomDataArgs']]):
        pulumi.set(self, "custom_data", value)

    @property
    @pulumi.getter(name="defaultClusterName")
    def default_cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of default cluster.
        """
        return pulumi.get(self, "default_cluster_name")

    @default_cluster_name.setter
    def default_cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_cluster_name", value)

    @property
    @pulumi.getter(name="secretData")
    def secret_data(self) -> Optional[pulumi.Input[str]]:
        """
        The data of secret. The value can be Password or KeyPair ID.
        """
        return pulumi.get(self, "secret_data")

    @secret_data.setter
    def secret_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_data", value)


@pulumi.input_type
class _CloudServerState:
    def __init__(__self__, *,
                 billing_config: Optional[pulumi.Input['CloudServerBillingConfigArgs']] = None,
                 cloudserver_name: Optional[pulumi.Input[str]] = None,
                 custom_data: Optional[pulumi.Input['CloudServerCustomDataArgs']] = None,
                 default_area_name: Optional[pulumi.Input[str]] = None,
                 default_cluster_name: Optional[pulumi.Input[str]] = None,
                 default_instance_id: Optional[pulumi.Input[str]] = None,
                 default_isp: Optional[pulumi.Input[str]] = None,
                 image_id: Optional[pulumi.Input[str]] = None,
                 network_config: Optional[pulumi.Input['CloudServerNetworkConfigArgs']] = None,
                 schedule_strategy: Optional[pulumi.Input['CloudServerScheduleStrategyArgs']] = None,
                 secret_data: Optional[pulumi.Input[str]] = None,
                 secret_type: Optional[pulumi.Input[str]] = None,
                 server_area_level: Optional[pulumi.Input[str]] = None,
                 spec_name: Optional[pulumi.Input[str]] = None,
                 storage_config: Optional[pulumi.Input['CloudServerStorageConfigArgs']] = None):
        """
        Input properties used for looking up and filtering CloudServer resources.
        :param pulumi.Input['CloudServerBillingConfigArgs'] billing_config: The config of the billing.
        :param pulumi.Input[str] cloudserver_name: The name of cloud server.
        :param pulumi.Input['CloudServerCustomDataArgs'] custom_data: The custom data.
        :param pulumi.Input[str] default_area_name: The name of default area.
        :param pulumi.Input[str] default_cluster_name: The name of default cluster.
        :param pulumi.Input[str] default_instance_id: The default instance id generate by cloud server.
        :param pulumi.Input[str] default_isp: The default isp info.
        :param pulumi.Input[str] image_id: The image id of cloud server.
        :param pulumi.Input['CloudServerNetworkConfigArgs'] network_config: The config of the network.
        :param pulumi.Input['CloudServerScheduleStrategyArgs'] schedule_strategy: The schedule strategy.
        :param pulumi.Input[str] secret_data: The data of secret. The value can be Password or KeyPair ID.
        :param pulumi.Input[str] secret_type: The type of secret. The value can be `KeyPair` or `Password`.
        :param pulumi.Input[str] server_area_level: The server area level. The value can be `region` or `city`.
        :param pulumi.Input[str] spec_name: The spec name of cloud server.
        :param pulumi.Input['CloudServerStorageConfigArgs'] storage_config: The config of the storage.
        """
        if billing_config is not None:
            pulumi.set(__self__, "billing_config", billing_config)
        if cloudserver_name is not None:
            pulumi.set(__self__, "cloudserver_name", cloudserver_name)
        if custom_data is not None:
            pulumi.set(__self__, "custom_data", custom_data)
        if default_area_name is not None:
            pulumi.set(__self__, "default_area_name", default_area_name)
        if default_cluster_name is not None:
            pulumi.set(__self__, "default_cluster_name", default_cluster_name)
        if default_instance_id is not None:
            pulumi.set(__self__, "default_instance_id", default_instance_id)
        if default_isp is not None:
            pulumi.set(__self__, "default_isp", default_isp)
        if image_id is not None:
            pulumi.set(__self__, "image_id", image_id)
        if network_config is not None:
            pulumi.set(__self__, "network_config", network_config)
        if schedule_strategy is not None:
            pulumi.set(__self__, "schedule_strategy", schedule_strategy)
        if secret_data is not None:
            pulumi.set(__self__, "secret_data", secret_data)
        if secret_type is not None:
            pulumi.set(__self__, "secret_type", secret_type)
        if server_area_level is not None:
            pulumi.set(__self__, "server_area_level", server_area_level)
        if spec_name is not None:
            pulumi.set(__self__, "spec_name", spec_name)
        if storage_config is not None:
            pulumi.set(__self__, "storage_config", storage_config)

    @property
    @pulumi.getter(name="billingConfig")
    def billing_config(self) -> Optional[pulumi.Input['CloudServerBillingConfigArgs']]:
        """
        The config of the billing.
        """
        return pulumi.get(self, "billing_config")

    @billing_config.setter
    def billing_config(self, value: Optional[pulumi.Input['CloudServerBillingConfigArgs']]):
        pulumi.set(self, "billing_config", value)

    @property
    @pulumi.getter(name="cloudserverName")
    def cloudserver_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of cloud server.
        """
        return pulumi.get(self, "cloudserver_name")

    @cloudserver_name.setter
    def cloudserver_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloudserver_name", value)

    @property
    @pulumi.getter(name="customData")
    def custom_data(self) -> Optional[pulumi.Input['CloudServerCustomDataArgs']]:
        """
        The custom data.
        """
        return pulumi.get(self, "custom_data")

    @custom_data.setter
    def custom_data(self, value: Optional[pulumi.Input['CloudServerCustomDataArgs']]):
        pulumi.set(self, "custom_data", value)

    @property
    @pulumi.getter(name="defaultAreaName")
    def default_area_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of default area.
        """
        return pulumi.get(self, "default_area_name")

    @default_area_name.setter
    def default_area_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_area_name", value)

    @property
    @pulumi.getter(name="defaultClusterName")
    def default_cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of default cluster.
        """
        return pulumi.get(self, "default_cluster_name")

    @default_cluster_name.setter
    def default_cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_cluster_name", value)

    @property
    @pulumi.getter(name="defaultInstanceId")
    def default_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The default instance id generate by cloud server.
        """
        return pulumi.get(self, "default_instance_id")

    @default_instance_id.setter
    def default_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_instance_id", value)

    @property
    @pulumi.getter(name="defaultIsp")
    def default_isp(self) -> Optional[pulumi.Input[str]]:
        """
        The default isp info.
        """
        return pulumi.get(self, "default_isp")

    @default_isp.setter
    def default_isp(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_isp", value)

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> Optional[pulumi.Input[str]]:
        """
        The image id of cloud server.
        """
        return pulumi.get(self, "image_id")

    @image_id.setter
    def image_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_id", value)

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> Optional[pulumi.Input['CloudServerNetworkConfigArgs']]:
        """
        The config of the network.
        """
        return pulumi.get(self, "network_config")

    @network_config.setter
    def network_config(self, value: Optional[pulumi.Input['CloudServerNetworkConfigArgs']]):
        pulumi.set(self, "network_config", value)

    @property
    @pulumi.getter(name="scheduleStrategy")
    def schedule_strategy(self) -> Optional[pulumi.Input['CloudServerScheduleStrategyArgs']]:
        """
        The schedule strategy.
        """
        return pulumi.get(self, "schedule_strategy")

    @schedule_strategy.setter
    def schedule_strategy(self, value: Optional[pulumi.Input['CloudServerScheduleStrategyArgs']]):
        pulumi.set(self, "schedule_strategy", value)

    @property
    @pulumi.getter(name="secretData")
    def secret_data(self) -> Optional[pulumi.Input[str]]:
        """
        The data of secret. The value can be Password or KeyPair ID.
        """
        return pulumi.get(self, "secret_data")

    @secret_data.setter
    def secret_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_data", value)

    @property
    @pulumi.getter(name="secretType")
    def secret_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of secret. The value can be `KeyPair` or `Password`.
        """
        return pulumi.get(self, "secret_type")

    @secret_type.setter
    def secret_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_type", value)

    @property
    @pulumi.getter(name="serverAreaLevel")
    def server_area_level(self) -> Optional[pulumi.Input[str]]:
        """
        The server area level. The value can be `region` or `city`.
        """
        return pulumi.get(self, "server_area_level")

    @server_area_level.setter
    def server_area_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_area_level", value)

    @property
    @pulumi.getter(name="specName")
    def spec_name(self) -> Optional[pulumi.Input[str]]:
        """
        The spec name of cloud server.
        """
        return pulumi.get(self, "spec_name")

    @spec_name.setter
    def spec_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spec_name", value)

    @property
    @pulumi.getter(name="storageConfig")
    def storage_config(self) -> Optional[pulumi.Input['CloudServerStorageConfigArgs']]:
        """
        The config of the storage.
        """
        return pulumi.get(self, "storage_config")

    @storage_config.setter
    def storage_config(self, value: Optional[pulumi.Input['CloudServerStorageConfigArgs']]):
        pulumi.set(self, "storage_config", value)


class CloudServer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 billing_config: Optional[pulumi.Input[pulumi.InputType['CloudServerBillingConfigArgs']]] = None,
                 cloudserver_name: Optional[pulumi.Input[str]] = None,
                 custom_data: Optional[pulumi.Input[pulumi.InputType['CloudServerCustomDataArgs']]] = None,
                 default_area_name: Optional[pulumi.Input[str]] = None,
                 default_cluster_name: Optional[pulumi.Input[str]] = None,
                 default_isp: Optional[pulumi.Input[str]] = None,
                 image_id: Optional[pulumi.Input[str]] = None,
                 network_config: Optional[pulumi.Input[pulumi.InputType['CloudServerNetworkConfigArgs']]] = None,
                 schedule_strategy: Optional[pulumi.Input[pulumi.InputType['CloudServerScheduleStrategyArgs']]] = None,
                 secret_data: Optional[pulumi.Input[str]] = None,
                 secret_type: Optional[pulumi.Input[str]] = None,
                 server_area_level: Optional[pulumi.Input[str]] = None,
                 spec_name: Optional[pulumi.Input[str]] = None,
                 storage_config: Optional[pulumi.Input[pulumi.InputType['CloudServerStorageConfigArgs']]] = None,
                 __props__=None):
        """
        Provides a resource to manage veenedge cloud server
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.veenedge.CloudServer("foo",
            billing_config=volcengine.veenedge.CloudServerBillingConfigArgs(
                bandwidth_billing_method="MonthlyP95",
                computing_billing_method="MonthlyPeak",
            ),
            cloudserver_name="tf-test",
            default_area_name="C******na",
            default_isp="CMCC",
            image_id="image*****viqm",
            network_config=volcengine.veenedge.CloudServerNetworkConfigArgs(
                bandwidth_peak="5",
            ),
            schedule_strategy=volcengine.veenedge.CloudServerScheduleStrategyArgs(
                network_strategy="region",
                price_strategy="high_priority",
                schedule_strategy="dispersion",
            ),
            secret_data="sshkey-47*****wgc",
            secret_type="KeyPair",
            server_area_level="region",
            spec_name="veEN****rge",
            storage_config=volcengine.veenedge.CloudServerStorageConfigArgs(
                data_disk_lists=[volcengine.veenedge.CloudServerStorageConfigDataDiskListArgs(
                    capacity="20",
                    storage_type="CloudBlockSSD",
                )],
                system_disk=volcengine.veenedge.CloudServerStorageConfigSystemDiskArgs(
                    capacity="40",
                    storage_type="CloudBlockSSD",
                ),
            ))
        ```

        ## Import

        CloudServer can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:veenedge/cloudServer:CloudServer default cloudserver-n769ewmjjqyqh5dv
        ```

         After the veenedge cloud server is created, a default edge instance will be created, we recommend managing this default instance as follows resource "volcengine_veenedge_instance" "foo1" {

         instance_id = volcengine_veenedge_cloud_server.foo.default_instance_id }

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['CloudServerBillingConfigArgs']] billing_config: The config of the billing.
        :param pulumi.Input[str] cloudserver_name: The name of cloud server.
        :param pulumi.Input[pulumi.InputType['CloudServerCustomDataArgs']] custom_data: The custom data.
        :param pulumi.Input[str] default_area_name: The name of default area.
        :param pulumi.Input[str] default_cluster_name: The name of default cluster.
        :param pulumi.Input[str] default_isp: The default isp info.
        :param pulumi.Input[str] image_id: The image id of cloud server.
        :param pulumi.Input[pulumi.InputType['CloudServerNetworkConfigArgs']] network_config: The config of the network.
        :param pulumi.Input[pulumi.InputType['CloudServerScheduleStrategyArgs']] schedule_strategy: The schedule strategy.
        :param pulumi.Input[str] secret_data: The data of secret. The value can be Password or KeyPair ID.
        :param pulumi.Input[str] secret_type: The type of secret. The value can be `KeyPair` or `Password`.
        :param pulumi.Input[str] server_area_level: The server area level. The value can be `region` or `city`.
        :param pulumi.Input[str] spec_name: The spec name of cloud server.
        :param pulumi.Input[pulumi.InputType['CloudServerStorageConfigArgs']] storage_config: The config of the storage.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CloudServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage veenedge cloud server
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.veenedge.CloudServer("foo",
            billing_config=volcengine.veenedge.CloudServerBillingConfigArgs(
                bandwidth_billing_method="MonthlyP95",
                computing_billing_method="MonthlyPeak",
            ),
            cloudserver_name="tf-test",
            default_area_name="C******na",
            default_isp="CMCC",
            image_id="image*****viqm",
            network_config=volcengine.veenedge.CloudServerNetworkConfigArgs(
                bandwidth_peak="5",
            ),
            schedule_strategy=volcengine.veenedge.CloudServerScheduleStrategyArgs(
                network_strategy="region",
                price_strategy="high_priority",
                schedule_strategy="dispersion",
            ),
            secret_data="sshkey-47*****wgc",
            secret_type="KeyPair",
            server_area_level="region",
            spec_name="veEN****rge",
            storage_config=volcengine.veenedge.CloudServerStorageConfigArgs(
                data_disk_lists=[volcengine.veenedge.CloudServerStorageConfigDataDiskListArgs(
                    capacity="20",
                    storage_type="CloudBlockSSD",
                )],
                system_disk=volcengine.veenedge.CloudServerStorageConfigSystemDiskArgs(
                    capacity="40",
                    storage_type="CloudBlockSSD",
                ),
            ))
        ```

        ## Import

        CloudServer can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:veenedge/cloudServer:CloudServer default cloudserver-n769ewmjjqyqh5dv
        ```

         After the veenedge cloud server is created, a default edge instance will be created, we recommend managing this default instance as follows resource "volcengine_veenedge_instance" "foo1" {

         instance_id = volcengine_veenedge_cloud_server.foo.default_instance_id }

        :param str resource_name: The name of the resource.
        :param CloudServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CloudServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 billing_config: Optional[pulumi.Input[pulumi.InputType['CloudServerBillingConfigArgs']]] = None,
                 cloudserver_name: Optional[pulumi.Input[str]] = None,
                 custom_data: Optional[pulumi.Input[pulumi.InputType['CloudServerCustomDataArgs']]] = None,
                 default_area_name: Optional[pulumi.Input[str]] = None,
                 default_cluster_name: Optional[pulumi.Input[str]] = None,
                 default_isp: Optional[pulumi.Input[str]] = None,
                 image_id: Optional[pulumi.Input[str]] = None,
                 network_config: Optional[pulumi.Input[pulumi.InputType['CloudServerNetworkConfigArgs']]] = None,
                 schedule_strategy: Optional[pulumi.Input[pulumi.InputType['CloudServerScheduleStrategyArgs']]] = None,
                 secret_data: Optional[pulumi.Input[str]] = None,
                 secret_type: Optional[pulumi.Input[str]] = None,
                 server_area_level: Optional[pulumi.Input[str]] = None,
                 spec_name: Optional[pulumi.Input[str]] = None,
                 storage_config: Optional[pulumi.Input[pulumi.InputType['CloudServerStorageConfigArgs']]] = None,
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
            __props__ = CloudServerArgs.__new__(CloudServerArgs)

            __props__.__dict__["billing_config"] = billing_config
            if cloudserver_name is None and not opts.urn:
                raise TypeError("Missing required property 'cloudserver_name'")
            __props__.__dict__["cloudserver_name"] = cloudserver_name
            __props__.__dict__["custom_data"] = custom_data
            if default_area_name is None and not opts.urn:
                raise TypeError("Missing required property 'default_area_name'")
            __props__.__dict__["default_area_name"] = default_area_name
            __props__.__dict__["default_cluster_name"] = default_cluster_name
            if default_isp is None and not opts.urn:
                raise TypeError("Missing required property 'default_isp'")
            __props__.__dict__["default_isp"] = default_isp
            if image_id is None and not opts.urn:
                raise TypeError("Missing required property 'image_id'")
            __props__.__dict__["image_id"] = image_id
            if network_config is None and not opts.urn:
                raise TypeError("Missing required property 'network_config'")
            __props__.__dict__["network_config"] = network_config
            if schedule_strategy is None and not opts.urn:
                raise TypeError("Missing required property 'schedule_strategy'")
            __props__.__dict__["schedule_strategy"] = schedule_strategy
            __props__.__dict__["secret_data"] = secret_data
            if secret_type is None and not opts.urn:
                raise TypeError("Missing required property 'secret_type'")
            __props__.__dict__["secret_type"] = secret_type
            if server_area_level is None and not opts.urn:
                raise TypeError("Missing required property 'server_area_level'")
            __props__.__dict__["server_area_level"] = server_area_level
            if spec_name is None and not opts.urn:
                raise TypeError("Missing required property 'spec_name'")
            __props__.__dict__["spec_name"] = spec_name
            if storage_config is None and not opts.urn:
                raise TypeError("Missing required property 'storage_config'")
            __props__.__dict__["storage_config"] = storage_config
            __props__.__dict__["default_instance_id"] = None
        super(CloudServer, __self__).__init__(
            'volcengine:veenedge/cloudServer:CloudServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            billing_config: Optional[pulumi.Input[pulumi.InputType['CloudServerBillingConfigArgs']]] = None,
            cloudserver_name: Optional[pulumi.Input[str]] = None,
            custom_data: Optional[pulumi.Input[pulumi.InputType['CloudServerCustomDataArgs']]] = None,
            default_area_name: Optional[pulumi.Input[str]] = None,
            default_cluster_name: Optional[pulumi.Input[str]] = None,
            default_instance_id: Optional[pulumi.Input[str]] = None,
            default_isp: Optional[pulumi.Input[str]] = None,
            image_id: Optional[pulumi.Input[str]] = None,
            network_config: Optional[pulumi.Input[pulumi.InputType['CloudServerNetworkConfigArgs']]] = None,
            schedule_strategy: Optional[pulumi.Input[pulumi.InputType['CloudServerScheduleStrategyArgs']]] = None,
            secret_data: Optional[pulumi.Input[str]] = None,
            secret_type: Optional[pulumi.Input[str]] = None,
            server_area_level: Optional[pulumi.Input[str]] = None,
            spec_name: Optional[pulumi.Input[str]] = None,
            storage_config: Optional[pulumi.Input[pulumi.InputType['CloudServerStorageConfigArgs']]] = None) -> 'CloudServer':
        """
        Get an existing CloudServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['CloudServerBillingConfigArgs']] billing_config: The config of the billing.
        :param pulumi.Input[str] cloudserver_name: The name of cloud server.
        :param pulumi.Input[pulumi.InputType['CloudServerCustomDataArgs']] custom_data: The custom data.
        :param pulumi.Input[str] default_area_name: The name of default area.
        :param pulumi.Input[str] default_cluster_name: The name of default cluster.
        :param pulumi.Input[str] default_instance_id: The default instance id generate by cloud server.
        :param pulumi.Input[str] default_isp: The default isp info.
        :param pulumi.Input[str] image_id: The image id of cloud server.
        :param pulumi.Input[pulumi.InputType['CloudServerNetworkConfigArgs']] network_config: The config of the network.
        :param pulumi.Input[pulumi.InputType['CloudServerScheduleStrategyArgs']] schedule_strategy: The schedule strategy.
        :param pulumi.Input[str] secret_data: The data of secret. The value can be Password or KeyPair ID.
        :param pulumi.Input[str] secret_type: The type of secret. The value can be `KeyPair` or `Password`.
        :param pulumi.Input[str] server_area_level: The server area level. The value can be `region` or `city`.
        :param pulumi.Input[str] spec_name: The spec name of cloud server.
        :param pulumi.Input[pulumi.InputType['CloudServerStorageConfigArgs']] storage_config: The config of the storage.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CloudServerState.__new__(_CloudServerState)

        __props__.__dict__["billing_config"] = billing_config
        __props__.__dict__["cloudserver_name"] = cloudserver_name
        __props__.__dict__["custom_data"] = custom_data
        __props__.__dict__["default_area_name"] = default_area_name
        __props__.__dict__["default_cluster_name"] = default_cluster_name
        __props__.__dict__["default_instance_id"] = default_instance_id
        __props__.__dict__["default_isp"] = default_isp
        __props__.__dict__["image_id"] = image_id
        __props__.__dict__["network_config"] = network_config
        __props__.__dict__["schedule_strategy"] = schedule_strategy
        __props__.__dict__["secret_data"] = secret_data
        __props__.__dict__["secret_type"] = secret_type
        __props__.__dict__["server_area_level"] = server_area_level
        __props__.__dict__["spec_name"] = spec_name
        __props__.__dict__["storage_config"] = storage_config
        return CloudServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="billingConfig")
    def billing_config(self) -> pulumi.Output[Optional['outputs.CloudServerBillingConfig']]:
        """
        The config of the billing.
        """
        return pulumi.get(self, "billing_config")

    @property
    @pulumi.getter(name="cloudserverName")
    def cloudserver_name(self) -> pulumi.Output[str]:
        """
        The name of cloud server.
        """
        return pulumi.get(self, "cloudserver_name")

    @property
    @pulumi.getter(name="customData")
    def custom_data(self) -> pulumi.Output['outputs.CloudServerCustomData']:
        """
        The custom data.
        """
        return pulumi.get(self, "custom_data")

    @property
    @pulumi.getter(name="defaultAreaName")
    def default_area_name(self) -> pulumi.Output[str]:
        """
        The name of default area.
        """
        return pulumi.get(self, "default_area_name")

    @property
    @pulumi.getter(name="defaultClusterName")
    def default_cluster_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of default cluster.
        """
        return pulumi.get(self, "default_cluster_name")

    @property
    @pulumi.getter(name="defaultInstanceId")
    def default_instance_id(self) -> pulumi.Output[str]:
        """
        The default instance id generate by cloud server.
        """
        return pulumi.get(self, "default_instance_id")

    @property
    @pulumi.getter(name="defaultIsp")
    def default_isp(self) -> pulumi.Output[str]:
        """
        The default isp info.
        """
        return pulumi.get(self, "default_isp")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> pulumi.Output[str]:
        """
        The image id of cloud server.
        """
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> pulumi.Output['outputs.CloudServerNetworkConfig']:
        """
        The config of the network.
        """
        return pulumi.get(self, "network_config")

    @property
    @pulumi.getter(name="scheduleStrategy")
    def schedule_strategy(self) -> pulumi.Output['outputs.CloudServerScheduleStrategy']:
        """
        The schedule strategy.
        """
        return pulumi.get(self, "schedule_strategy")

    @property
    @pulumi.getter(name="secretData")
    def secret_data(self) -> pulumi.Output[Optional[str]]:
        """
        The data of secret. The value can be Password or KeyPair ID.
        """
        return pulumi.get(self, "secret_data")

    @property
    @pulumi.getter(name="secretType")
    def secret_type(self) -> pulumi.Output[str]:
        """
        The type of secret. The value can be `KeyPair` or `Password`.
        """
        return pulumi.get(self, "secret_type")

    @property
    @pulumi.getter(name="serverAreaLevel")
    def server_area_level(self) -> pulumi.Output[str]:
        """
        The server area level. The value can be `region` or `city`.
        """
        return pulumi.get(self, "server_area_level")

    @property
    @pulumi.getter(name="specName")
    def spec_name(self) -> pulumi.Output[str]:
        """
        The spec name of cloud server.
        """
        return pulumi.get(self, "spec_name")

    @property
    @pulumi.getter(name="storageConfig")
    def storage_config(self) -> pulumi.Output['outputs.CloudServerStorageConfig']:
        """
        The config of the storage.
        """
        return pulumi.get(self, "storage_config")

