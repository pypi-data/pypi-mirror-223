# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['TopicPermissionsArgs', 'TopicPermissions']

@pulumi.input_type
class TopicPermissionsArgs:
    def __init__(__self__, *,
                 permissions: pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]],
                 user: pulumi.Input[str],
                 vhost: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TopicPermissions resource.
        :param pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]] permissions: The settings of the permissions. The structure is
               described below.
        :param pulumi.Input[str] user: The user to apply the permissions to.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        """
        pulumi.set(__self__, "permissions", permissions)
        pulumi.set(__self__, "user", user)
        if vhost is not None:
            pulumi.set(__self__, "vhost", vhost)

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]]:
        """
        The settings of the permissions. The structure is
        described below.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter
    def user(self) -> pulumi.Input[str]:
        """
        The user to apply the permissions to.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: pulumi.Input[str]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter
    def vhost(self) -> Optional[pulumi.Input[str]]:
        """
        The vhost to create the resource in.
        """
        return pulumi.get(self, "vhost")

    @vhost.setter
    def vhost(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vhost", value)


@pulumi.input_type
class _TopicPermissionsState:
    def __init__(__self__, *,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 vhost: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TopicPermissions resources.
        :param pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]] permissions: The settings of the permissions. The structure is
               described below.
        :param pulumi.Input[str] user: The user to apply the permissions to.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        """
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)
        if user is not None:
            pulumi.set(__self__, "user", user)
        if vhost is not None:
            pulumi.set(__self__, "vhost", vhost)

    @property
    @pulumi.getter
    def permissions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]]]:
        """
        The settings of the permissions. The structure is
        described below.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TopicPermissionsPermissionArgs']]]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        The user to apply the permissions to.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter
    def vhost(self) -> Optional[pulumi.Input[str]]:
        """
        The vhost to create the resource in.
        """
        return pulumi.get(self, "vhost")

    @vhost.setter
    def vhost(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vhost", value)


class TopicPermissions(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TopicPermissionsPermissionArgs']]]]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 vhost: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ``TopicPermissions`` resource creates and manages a user's set of
        topic permissions.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_rabbitmq as rabbitmq

        test_v_host = rabbitmq.VHost("testVHost")
        test_user = rabbitmq.User("testUser",
            password="foobar",
            tags=["administrator"])
        test_topic_permissions = rabbitmq.TopicPermissions("testTopicPermissions",
            permissions=[rabbitmq.TopicPermissionsPermissionArgs(
                exchange="amq.topic",
                read=".*",
                write=".*",
            )],
            user=test_user.name,
            vhost=test_v_host.name)
        ```

        ## Import

        Permissions can be imported using the `id` which is composed of

        `user@vhost`. E.g.

        ```sh
         $ pulumi import rabbitmq:index/topicPermissions:TopicPermissions test user@vhost
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TopicPermissionsPermissionArgs']]]] permissions: The settings of the permissions. The structure is
               described below.
        :param pulumi.Input[str] user: The user to apply the permissions to.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TopicPermissionsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``TopicPermissions`` resource creates and manages a user's set of
        topic permissions.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_rabbitmq as rabbitmq

        test_v_host = rabbitmq.VHost("testVHost")
        test_user = rabbitmq.User("testUser",
            password="foobar",
            tags=["administrator"])
        test_topic_permissions = rabbitmq.TopicPermissions("testTopicPermissions",
            permissions=[rabbitmq.TopicPermissionsPermissionArgs(
                exchange="amq.topic",
                read=".*",
                write=".*",
            )],
            user=test_user.name,
            vhost=test_v_host.name)
        ```

        ## Import

        Permissions can be imported using the `id` which is composed of

        `user@vhost`. E.g.

        ```sh
         $ pulumi import rabbitmq:index/topicPermissions:TopicPermissions test user@vhost
        ```

        :param str resource_name: The name of the resource.
        :param TopicPermissionsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TopicPermissionsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TopicPermissionsPermissionArgs']]]]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 vhost: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TopicPermissionsArgs.__new__(TopicPermissionsArgs)

            if permissions is None and not opts.urn:
                raise TypeError("Missing required property 'permissions'")
            __props__.__dict__["permissions"] = permissions
            if user is None and not opts.urn:
                raise TypeError("Missing required property 'user'")
            __props__.__dict__["user"] = user
            __props__.__dict__["vhost"] = vhost
        super(TopicPermissions, __self__).__init__(
            'rabbitmq:index/topicPermissions:TopicPermissions',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            permissions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TopicPermissionsPermissionArgs']]]]] = None,
            user: Optional[pulumi.Input[str]] = None,
            vhost: Optional[pulumi.Input[str]] = None) -> 'TopicPermissions':
        """
        Get an existing TopicPermissions resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TopicPermissionsPermissionArgs']]]] permissions: The settings of the permissions. The structure is
               described below.
        :param pulumi.Input[str] user: The user to apply the permissions to.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TopicPermissionsState.__new__(_TopicPermissionsState)

        __props__.__dict__["permissions"] = permissions
        __props__.__dict__["user"] = user
        __props__.__dict__["vhost"] = vhost
        return TopicPermissions(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Output[Sequence['outputs.TopicPermissionsPermission']]:
        """
        The settings of the permissions. The structure is
        described below.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        The user to apply the permissions to.
        """
        return pulumi.get(self, "user")

    @property
    @pulumi.getter
    def vhost(self) -> pulumi.Output[Optional[str]]:
        """
        The vhost to create the resource in.
        """
        return pulumi.get(self, "vhost")

