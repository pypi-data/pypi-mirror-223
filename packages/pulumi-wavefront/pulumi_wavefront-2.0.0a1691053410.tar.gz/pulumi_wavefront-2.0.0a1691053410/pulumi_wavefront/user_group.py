# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UserGroupArgs', 'UserGroup']

@pulumi.input_type
class UserGroupArgs:
    def __init__(__self__, *,
                 description: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a UserGroup resource.
        :param pulumi.Input[str] description: A short description of the user group.
        :param pulumi.Input[str] name: The name of the user group.
        """
        pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        A short description of the user group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _UserGroupState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserGroup resources.
        :param pulumi.Input[str] description: A short description of the user group.
        :param pulumi.Input[str] name: The name of the user group.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A short description of the user group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class UserGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Wavefront User Group Resource. This allows user groups to be created, updated, and deleted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_wavefront as wavefront

        basic = wavefront.UserGroup("basic", description="Basic User Group for Unit Tests")
        ```

        ## Import

        User Groups can be imported by using the `id`, e.g.

        ```sh
         $ pulumi import wavefront:index/userGroup:UserGroup some_group a411c16b-3cf7-4f03-bf11-8ca05aab898d
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A short description of the user group.
        :param pulumi.Input[str] name: The name of the user group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Wavefront User Group Resource. This allows user groups to be created, updated, and deleted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_wavefront as wavefront

        basic = wavefront.UserGroup("basic", description="Basic User Group for Unit Tests")
        ```

        ## Import

        User Groups can be imported by using the `id`, e.g.

        ```sh
         $ pulumi import wavefront:index/userGroup:UserGroup some_group a411c16b-3cf7-4f03-bf11-8ca05aab898d
        ```

        :param str resource_name: The name of the resource.
        :param UserGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserGroupArgs.__new__(UserGroupArgs)

            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
        super(UserGroup, __self__).__init__(
            'wavefront:index/userGroup:UserGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'UserGroup':
        """
        Get an existing UserGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A short description of the user group.
        :param pulumi.Input[str] name: The name of the user group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserGroupState.__new__(_UserGroupState)

        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        return UserGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        A short description of the user group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the user group.
        """
        return pulumi.get(self, "name")

