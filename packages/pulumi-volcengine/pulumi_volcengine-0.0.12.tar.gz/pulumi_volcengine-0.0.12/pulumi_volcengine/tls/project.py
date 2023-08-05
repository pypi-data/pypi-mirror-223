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

__all__ = ['ProjectArgs', 'Project']

@pulumi.input_type
class ProjectArgs:
    def __init__(__self__, *,
                 project_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 iam_project_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]]] = None):
        """
        The set of arguments for constructing a Project resource.
        :param pulumi.Input[str] project_name: The name of the tls project.
        :param pulumi.Input[str] description: The description of the tls project.
        :param pulumi.Input[str] iam_project_name: The IAM project name of the tls project.
        :param pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]] tags: Tags.
        """
        pulumi.set(__self__, "project_name", project_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if iam_project_name is not None:
            pulumi.set(__self__, "iam_project_name", iam_project_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="projectName")
    def project_name(self) -> pulumi.Input[str]:
        """
        The name of the tls project.
        """
        return pulumi.get(self, "project_name")

    @project_name.setter
    def project_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the tls project.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="iamProjectName")
    def iam_project_name(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM project name of the tls project.
        """
        return pulumi.get(self, "iam_project_name")

    @iam_project_name.setter
    def iam_project_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "iam_project_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]]]:
        """
        Tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ProjectState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 iam_project_name: Optional[pulumi.Input[str]] = None,
                 inner_net_domain: Optional[pulumi.Input[str]] = None,
                 project_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]]] = None,
                 topic_count: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Project resources.
        :param pulumi.Input[str] create_time: The create time of the tls project.
        :param pulumi.Input[str] description: The description of the tls project.
        :param pulumi.Input[str] iam_project_name: The IAM project name of the tls project.
        :param pulumi.Input[str] inner_net_domain: The inner net domain of the tls project.
        :param pulumi.Input[str] project_name: The name of the tls project.
        :param pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]] tags: Tags.
        :param pulumi.Input[int] topic_count: The count of topics in the tls project.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if iam_project_name is not None:
            pulumi.set(__self__, "iam_project_name", iam_project_name)
        if inner_net_domain is not None:
            pulumi.set(__self__, "inner_net_domain", inner_net_domain)
        if project_name is not None:
            pulumi.set(__self__, "project_name", project_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if topic_count is not None:
            pulumi.set(__self__, "topic_count", topic_count)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        The create time of the tls project.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the tls project.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="iamProjectName")
    def iam_project_name(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM project name of the tls project.
        """
        return pulumi.get(self, "iam_project_name")

    @iam_project_name.setter
    def iam_project_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "iam_project_name", value)

    @property
    @pulumi.getter(name="innerNetDomain")
    def inner_net_domain(self) -> Optional[pulumi.Input[str]]:
        """
        The inner net domain of the tls project.
        """
        return pulumi.get(self, "inner_net_domain")

    @inner_net_domain.setter
    def inner_net_domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "inner_net_domain", value)

    @property
    @pulumi.getter(name="projectName")
    def project_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the tls project.
        """
        return pulumi.get(self, "project_name")

    @project_name.setter
    def project_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]]]:
        """
        Tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ProjectTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="topicCount")
    def topic_count(self) -> Optional[pulumi.Input[int]]:
        """
        The count of topics in the tls project.
        """
        return pulumi.get(self, "topic_count")

    @topic_count.setter
    def topic_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "topic_count", value)


class Project(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 iam_project_name: Optional[pulumi.Input[str]] = None,
                 project_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProjectTagArgs']]]]] = None,
                 __props__=None):
        """
        Provides a resource to manage tls project
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.tls.Project("foo",
            description="tf-desc",
            iam_project_name="default",
            project_name="tf-test",
            tags=[volcengine.tls.ProjectTagArgs(
                key="k1",
                value="v1",
            )])
        ```

        ## Import

        Tls Project can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:tls/project:Project default e020c978-4f05-40e1-9167-0113d3ef****
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the tls project.
        :param pulumi.Input[str] iam_project_name: The IAM project name of the tls project.
        :param pulumi.Input[str] project_name: The name of the tls project.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProjectTagArgs']]]] tags: Tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProjectArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage tls project
        ## Example Usage

        ```python
        import pulumi
        import pulumi_volcengine as volcengine

        foo = volcengine.tls.Project("foo",
            description="tf-desc",
            iam_project_name="default",
            project_name="tf-test",
            tags=[volcengine.tls.ProjectTagArgs(
                key="k1",
                value="v1",
            )])
        ```

        ## Import

        Tls Project can be imported using the id, e.g.

        ```sh
         $ pulumi import volcengine:tls/project:Project default e020c978-4f05-40e1-9167-0113d3ef****
        ```

        :param str resource_name: The name of the resource.
        :param ProjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 iam_project_name: Optional[pulumi.Input[str]] = None,
                 project_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProjectTagArgs']]]]] = None,
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
            __props__ = ProjectArgs.__new__(ProjectArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["iam_project_name"] = iam_project_name
            if project_name is None and not opts.urn:
                raise TypeError("Missing required property 'project_name'")
            __props__.__dict__["project_name"] = project_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["create_time"] = None
            __props__.__dict__["inner_net_domain"] = None
            __props__.__dict__["topic_count"] = None
        super(Project, __self__).__init__(
            'volcengine:tls/project:Project',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            iam_project_name: Optional[pulumi.Input[str]] = None,
            inner_net_domain: Optional[pulumi.Input[str]] = None,
            project_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProjectTagArgs']]]]] = None,
            topic_count: Optional[pulumi.Input[int]] = None) -> 'Project':
        """
        Get an existing Project resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: The create time of the tls project.
        :param pulumi.Input[str] description: The description of the tls project.
        :param pulumi.Input[str] iam_project_name: The IAM project name of the tls project.
        :param pulumi.Input[str] inner_net_domain: The inner net domain of the tls project.
        :param pulumi.Input[str] project_name: The name of the tls project.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProjectTagArgs']]]] tags: Tags.
        :param pulumi.Input[int] topic_count: The count of topics in the tls project.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectState.__new__(_ProjectState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["iam_project_name"] = iam_project_name
        __props__.__dict__["inner_net_domain"] = inner_net_domain
        __props__.__dict__["project_name"] = project_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["topic_count"] = topic_count
        return Project(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The create time of the tls project.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        The description of the tls project.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="iamProjectName")
    def iam_project_name(self) -> pulumi.Output[str]:
        """
        The IAM project name of the tls project.
        """
        return pulumi.get(self, "iam_project_name")

    @property
    @pulumi.getter(name="innerNetDomain")
    def inner_net_domain(self) -> pulumi.Output[str]:
        """
        The inner net domain of the tls project.
        """
        return pulumi.get(self, "inner_net_domain")

    @property
    @pulumi.getter(name="projectName")
    def project_name(self) -> pulumi.Output[str]:
        """
        The name of the tls project.
        """
        return pulumi.get(self, "project_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.ProjectTag']]]:
        """
        Tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="topicCount")
    def topic_count(self) -> pulumi.Output[int]:
        """
        The count of topics in the tls project.
        """
        return pulumi.get(self, "topic_count")

