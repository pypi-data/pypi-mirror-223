# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AccountArgs', 'Account']

@pulumi.input_type
class AccountArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 primary_billing_group_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Account resource.
        :param pulumi.Input[str] name: Account name
        :param pulumi.Input[str] primary_billing_group_id: Billing group id
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if primary_billing_group_id is not None:
            warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
            pulumi.log.warn("""primary_billing_group_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")
        if primary_billing_group_id is not None:
            pulumi.set(__self__, "primary_billing_group_id", primary_billing_group_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Account name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="primaryBillingGroupId")
    def primary_billing_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        Billing group id
        """
        warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
        pulumi.log.warn("""primary_billing_group_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")

        return pulumi.get(self, "primary_billing_group_id")

    @primary_billing_group_id.setter
    def primary_billing_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_billing_group_id", value)


@pulumi.input_type
class _AccountState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 is_account_owner: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner_team_id: Optional[pulumi.Input[str]] = None,
                 primary_billing_group_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Account resources.
        :param pulumi.Input[str] account_id: Account id
        :param pulumi.Input[str] create_time: Time of creation
        :param pulumi.Input[bool] is_account_owner: If true, user is part of the owners team for this account
        :param pulumi.Input[str] name: Account name
        :param pulumi.Input[str] owner_team_id: Owner team id
        :param pulumi.Input[str] primary_billing_group_id: Billing group id
        :param pulumi.Input[str] tenant_id: Tenant id
        :param pulumi.Input[str] update_time: Time of last update
        """
        if account_id is not None:
            warnings.warn("""The new aiven_organization resource won't have it, use the built-in ID field instead.""", DeprecationWarning)
            pulumi.log.warn("""account_id is deprecated: The new aiven_organization resource won't have it, use the built-in ID field instead.""")
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if is_account_owner is not None:
            warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
            pulumi.log.warn("""is_account_owner is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")
        if is_account_owner is not None:
            pulumi.set(__self__, "is_account_owner", is_account_owner)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if owner_team_id is not None:
            warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
            pulumi.log.warn("""owner_team_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")
        if owner_team_id is not None:
            pulumi.set(__self__, "owner_team_id", owner_team_id)
        if primary_billing_group_id is not None:
            warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
            pulumi.log.warn("""primary_billing_group_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")
        if primary_billing_group_id is not None:
            pulumi.set(__self__, "primary_billing_group_id", primary_billing_group_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        Account id
        """
        warnings.warn("""The new aiven_organization resource won't have it, use the built-in ID field instead.""", DeprecationWarning)
        pulumi.log.warn("""account_id is deprecated: The new aiven_organization resource won't have it, use the built-in ID field instead.""")

        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time of creation
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="isAccountOwner")
    def is_account_owner(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, user is part of the owners team for this account
        """
        warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
        pulumi.log.warn("""is_account_owner is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")

        return pulumi.get(self, "is_account_owner")

    @is_account_owner.setter
    def is_account_owner(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_account_owner", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Account name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="ownerTeamId")
    def owner_team_id(self) -> Optional[pulumi.Input[str]]:
        """
        Owner team id
        """
        warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
        pulumi.log.warn("""owner_team_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")

        return pulumi.get(self, "owner_team_id")

    @owner_team_id.setter
    def owner_team_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_team_id", value)

    @property
    @pulumi.getter(name="primaryBillingGroupId")
    def primary_billing_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        Billing group id
        """
        warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
        pulumi.log.warn("""primary_billing_group_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")

        return pulumi.get(self, "primary_billing_group_id")

    @primary_billing_group_id.setter
    def primary_billing_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_billing_group_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        Tenant id
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time of last update
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class Account(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 primary_billing_group_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The Account resource allows the creation and management of an Aiven Account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        account1 = aiven.Account("account1")
        ```

        ## Import

        ```sh
         $ pulumi import aiven:index/account:Account account1 account_id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Account name
        :param pulumi.Input[str] primary_billing_group_id: Billing group id
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AccountArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Account resource allows the creation and management of an Aiven Account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        account1 = aiven.Account("account1")
        ```

        ## Import

        ```sh
         $ pulumi import aiven:index/account:Account account1 account_id
        ```

        :param str resource_name: The name of the resource.
        :param AccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 primary_billing_group_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountArgs.__new__(AccountArgs)

            __props__.__dict__["name"] = name
            if primary_billing_group_id is not None and not opts.urn:
                warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
                pulumi.log.warn("""primary_billing_group_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")
            __props__.__dict__["primary_billing_group_id"] = primary_billing_group_id
            __props__.__dict__["account_id"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["is_account_owner"] = None
            __props__.__dict__["owner_team_id"] = None
            __props__.__dict__["tenant_id"] = None
            __props__.__dict__["update_time"] = None
        super(Account, __self__).__init__(
            'aiven:index/account:Account',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            is_account_owner: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            owner_team_id: Optional[pulumi.Input[str]] = None,
            primary_billing_group_id: Optional[pulumi.Input[str]] = None,
            tenant_id: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'Account':
        """
        Get an existing Account resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: Account id
        :param pulumi.Input[str] create_time: Time of creation
        :param pulumi.Input[bool] is_account_owner: If true, user is part of the owners team for this account
        :param pulumi.Input[str] name: Account name
        :param pulumi.Input[str] owner_team_id: Owner team id
        :param pulumi.Input[str] primary_billing_group_id: Billing group id
        :param pulumi.Input[str] tenant_id: Tenant id
        :param pulumi.Input[str] update_time: Time of last update
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountState.__new__(_AccountState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["is_account_owner"] = is_account_owner
        __props__.__dict__["name"] = name
        __props__.__dict__["owner_team_id"] = owner_team_id
        __props__.__dict__["primary_billing_group_id"] = primary_billing_group_id
        __props__.__dict__["tenant_id"] = tenant_id
        __props__.__dict__["update_time"] = update_time
        return Account(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        Account id
        """
        warnings.warn("""The new aiven_organization resource won't have it, use the built-in ID field instead.""", DeprecationWarning)
        pulumi.log.warn("""account_id is deprecated: The new aiven_organization resource won't have it, use the built-in ID field instead.""")

        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time of creation
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="isAccountOwner")
    def is_account_owner(self) -> pulumi.Output[bool]:
        """
        If true, user is part of the owners team for this account
        """
        warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
        pulumi.log.warn("""is_account_owner is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")

        return pulumi.get(self, "is_account_owner")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Account name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ownerTeamId")
    def owner_team_id(self) -> pulumi.Output[str]:
        """
        Owner team id
        """
        warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
        pulumi.log.warn("""owner_team_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")

        return pulumi.get(self, "owner_team_id")

    @property
    @pulumi.getter(name="primaryBillingGroupId")
    def primary_billing_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        Billing group id
        """
        warnings.warn("""The new aiven_organization resource won't have it, and will not have a replacement.""", DeprecationWarning)
        pulumi.log.warn("""primary_billing_group_id is deprecated: The new aiven_organization resource won't have it, and will not have a replacement.""")

        return pulumi.get(self, "primary_billing_group_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        Tenant id
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Time of last update
        """
        return pulumi.get(self, "update_time")

