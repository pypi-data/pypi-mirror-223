# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['MysqlUserArgs', 'MysqlUser']

@pulumi.input_type
class MysqlUserArgs:
    def __init__(__self__, *,
                 project: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 username: pulumi.Input[str],
                 authentication: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MysqlUser resource.
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] username: The actual name of the MySQL User. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] authentication: Authentication details. The possible values are `caching_sha2_password` and `mysql_native_password`.
        :param pulumi.Input[str] password: The password of the MySQL User ( not applicable for all services ).
        """
        pulumi.set(__self__, "project", project)
        pulumi.set(__self__, "service_name", service_name)
        pulumi.set(__self__, "username", username)
        if authentication is not None:
            pulumi.set(__self__, "authentication", authentication)
        if password is not None:
            pulumi.set(__self__, "password", password)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The actual name of the MySQL User. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter
    def authentication(self) -> Optional[pulumi.Input[str]]:
        """
        Authentication details. The possible values are `caching_sha2_password` and `mysql_native_password`.
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the MySQL User ( not applicable for all services ).
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)


@pulumi.input_type
class _MysqlUserState:
    def __init__(__self__, *,
                 access_cert: Optional[pulumi.Input[str]] = None,
                 access_key: Optional[pulumi.Input[str]] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MysqlUser resources.
        :param pulumi.Input[str] access_cert: Access certificate for the user
        :param pulumi.Input[str] access_key: Access certificate key for the user
        :param pulumi.Input[str] authentication: Authentication details. The possible values are `caching_sha2_password` and `mysql_native_password`.
        :param pulumi.Input[str] password: The password of the MySQL User ( not applicable for all services ).
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] type: Type of the user account. Tells whether the user is the primary account or a regular account.
        :param pulumi.Input[str] username: The actual name of the MySQL User. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        if access_cert is not None:
            pulumi.set(__self__, "access_cert", access_cert)
        if access_key is not None:
            pulumi.set(__self__, "access_key", access_key)
        if authentication is not None:
            pulumi.set(__self__, "authentication", authentication)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if service_name is not None:
            pulumi.set(__self__, "service_name", service_name)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="accessCert")
    def access_cert(self) -> Optional[pulumi.Input[str]]:
        """
        Access certificate for the user
        """
        return pulumi.get(self, "access_cert")

    @access_cert.setter
    def access_cert(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_cert", value)

    @property
    @pulumi.getter(name="accessKey")
    def access_key(self) -> Optional[pulumi.Input[str]]:
        """
        Access certificate key for the user
        """
        return pulumi.get(self, "access_key")

    @access_key.setter
    def access_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_key", value)

    @property
    @pulumi.getter
    def authentication(self) -> Optional[pulumi.Input[str]]:
        """
        Authentication details. The possible values are `caching_sha2_password` and `mysql_native_password`.
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the MySQL User ( not applicable for all services ).
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the user account. Tells whether the user is the primary account or a regular account.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The actual name of the MySQL User. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class MysqlUser(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The MySQL User resource allows the creation and management of Aiven MySQL Users.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        foo = aiven.MysqlUser("foo",
            service_name=aiven_mysql["bar"]["service_name"],
            project="my-project",
            username="user-1",
            password="Test$1234")
        ```

        ## Import

        ```sh
         $ pulumi import aiven:index/mysqlUser:MysqlUser foo project/service_name/username
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication: Authentication details. The possible values are `caching_sha2_password` and `mysql_native_password`.
        :param pulumi.Input[str] password: The password of the MySQL User ( not applicable for all services ).
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] username: The actual name of the MySQL User. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MysqlUserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The MySQL User resource allows the creation and management of Aiven MySQL Users.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        foo = aiven.MysqlUser("foo",
            service_name=aiven_mysql["bar"]["service_name"],
            project="my-project",
            username="user-1",
            password="Test$1234")
        ```

        ## Import

        ```sh
         $ pulumi import aiven:index/mysqlUser:MysqlUser foo project/service_name/username
        ```

        :param str resource_name: The name of the resource.
        :param MysqlUserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MysqlUserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MysqlUserArgs.__new__(MysqlUserArgs)

            __props__.__dict__["authentication"] = authentication
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
            __props__.__dict__["access_cert"] = None
            __props__.__dict__["access_key"] = None
            __props__.__dict__["type"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["accessCert", "accessKey", "password"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(MysqlUser, __self__).__init__(
            'aiven:index/mysqlUser:MysqlUser',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_cert: Optional[pulumi.Input[str]] = None,
            access_key: Optional[pulumi.Input[str]] = None,
            authentication: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            service_name: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'MysqlUser':
        """
        Get an existing MysqlUser resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_cert: Access certificate for the user
        :param pulumi.Input[str] access_key: Access certificate key for the user
        :param pulumi.Input[str] authentication: Authentication details. The possible values are `caching_sha2_password` and `mysql_native_password`.
        :param pulumi.Input[str] password: The password of the MySQL User ( not applicable for all services ).
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        :param pulumi.Input[str] type: Type of the user account. Tells whether the user is the primary account or a regular account.
        :param pulumi.Input[str] username: The actual name of the MySQL User. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MysqlUserState.__new__(_MysqlUserState)

        __props__.__dict__["access_cert"] = access_cert
        __props__.__dict__["access_key"] = access_key
        __props__.__dict__["authentication"] = authentication
        __props__.__dict__["password"] = password
        __props__.__dict__["project"] = project
        __props__.__dict__["service_name"] = service_name
        __props__.__dict__["type"] = type
        __props__.__dict__["username"] = username
        return MysqlUser(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessCert")
    def access_cert(self) -> pulumi.Output[str]:
        """
        Access certificate for the user
        """
        return pulumi.get(self, "access_cert")

    @property
    @pulumi.getter(name="accessKey")
    def access_key(self) -> pulumi.Output[str]:
        """
        Access certificate key for the user
        """
        return pulumi.get(self, "access_key")

    @property
    @pulumi.getter
    def authentication(self) -> pulumi.Output[Optional[str]]:
        """
        Authentication details. The possible values are `caching_sha2_password` and `mysql_native_password`.
        """
        return pulumi.get(self, "authentication")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        The password of the MySQL User ( not applicable for all services ).
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the user account. Tells whether the user is the primary account or a regular account.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        The actual name of the MySQL User. To set up proper dependencies please refer to this variable as a reference. This property cannot be changed, doing so forces recreation of the resource.
        """
        return pulumi.get(self, "username")

