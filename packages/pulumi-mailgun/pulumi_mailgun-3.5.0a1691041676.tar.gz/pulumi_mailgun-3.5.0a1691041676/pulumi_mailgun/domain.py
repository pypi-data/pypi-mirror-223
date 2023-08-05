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

__all__ = ['DomainArgs', 'Domain']

@pulumi.input_type
class DomainArgs:
    def __init__(__self__, *,
                 dkim_key_size: Optional[pulumi.Input[int]] = None,
                 dkim_selector: Optional[pulumi.Input[str]] = None,
                 force_dkim_authority: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 open_tracking: Optional[pulumi.Input[bool]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 smtp_password: Optional[pulumi.Input[str]] = None,
                 spam_action: Optional[pulumi.Input[str]] = None,
                 wildcard: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Domain resource.
        :param pulumi.Input[int] dkim_key_size: The length of your domain’s generated DKIM key. Default value is `1024`.
        :param pulumi.Input[str] dkim_selector: The name of your DKIM selector if you want to specify it whereas MailGun will make it's own choice.
        :param pulumi.Input[bool] force_dkim_authority: If set to true, the domain will be the DKIM authority for itself even if the root domain is registered on the same mailgun account. If set to false, the domain will have the same DKIM authority as the root domain registered on the same mailgun account. The default is `false`.
        :param pulumi.Input[str] name: The domain to add to Mailgun
        :param pulumi.Input[bool] open_tracking: (Enum: `yes` or `no`) The open tracking settings for the domain. Default: `no`
        :param pulumi.Input[str] region: The region where domain will be created. Default value is `us`.
        :param pulumi.Input[str] smtp_password: Password for SMTP authentication
        :param pulumi.Input[str] spam_action: `disabled` or `tag` Disable, no spam
               filtering will occur for inbound messages. Tag, messages
               will be tagged with a spam header.
        :param pulumi.Input[bool] wildcard: Boolean that determines whether
               the domain will accept email for sub-domains.
        """
        if dkim_key_size is not None:
            pulumi.set(__self__, "dkim_key_size", dkim_key_size)
        if dkim_selector is not None:
            pulumi.set(__self__, "dkim_selector", dkim_selector)
        if force_dkim_authority is not None:
            pulumi.set(__self__, "force_dkim_authority", force_dkim_authority)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if open_tracking is not None:
            pulumi.set(__self__, "open_tracking", open_tracking)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if smtp_password is not None:
            pulumi.set(__self__, "smtp_password", smtp_password)
        if spam_action is not None:
            pulumi.set(__self__, "spam_action", spam_action)
        if wildcard is not None:
            pulumi.set(__self__, "wildcard", wildcard)

    @property
    @pulumi.getter(name="dkimKeySize")
    def dkim_key_size(self) -> Optional[pulumi.Input[int]]:
        """
        The length of your domain’s generated DKIM key. Default value is `1024`.
        """
        return pulumi.get(self, "dkim_key_size")

    @dkim_key_size.setter
    def dkim_key_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "dkim_key_size", value)

    @property
    @pulumi.getter(name="dkimSelector")
    def dkim_selector(self) -> Optional[pulumi.Input[str]]:
        """
        The name of your DKIM selector if you want to specify it whereas MailGun will make it's own choice.
        """
        return pulumi.get(self, "dkim_selector")

    @dkim_selector.setter
    def dkim_selector(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dkim_selector", value)

    @property
    @pulumi.getter(name="forceDkimAuthority")
    def force_dkim_authority(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, the domain will be the DKIM authority for itself even if the root domain is registered on the same mailgun account. If set to false, the domain will have the same DKIM authority as the root domain registered on the same mailgun account. The default is `false`.
        """
        return pulumi.get(self, "force_dkim_authority")

    @force_dkim_authority.setter
    def force_dkim_authority(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_dkim_authority", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain to add to Mailgun
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="openTracking")
    def open_tracking(self) -> Optional[pulumi.Input[bool]]:
        """
        (Enum: `yes` or `no`) The open tracking settings for the domain. Default: `no`
        """
        return pulumi.get(self, "open_tracking")

    @open_tracking.setter
    def open_tracking(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "open_tracking", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region where domain will be created. Default value is `us`.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="smtpPassword")
    def smtp_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for SMTP authentication
        """
        return pulumi.get(self, "smtp_password")

    @smtp_password.setter
    def smtp_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "smtp_password", value)

    @property
    @pulumi.getter(name="spamAction")
    def spam_action(self) -> Optional[pulumi.Input[str]]:
        """
        `disabled` or `tag` Disable, no spam
        filtering will occur for inbound messages. Tag, messages
        will be tagged with a spam header.
        """
        return pulumi.get(self, "spam_action")

    @spam_action.setter
    def spam_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spam_action", value)

    @property
    @pulumi.getter
    def wildcard(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean that determines whether
        the domain will accept email for sub-domains.
        """
        return pulumi.get(self, "wildcard")

    @wildcard.setter
    def wildcard(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wildcard", value)


@pulumi.input_type
class _DomainState:
    def __init__(__self__, *,
                 dkim_key_size: Optional[pulumi.Input[int]] = None,
                 dkim_selector: Optional[pulumi.Input[str]] = None,
                 force_dkim_authority: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 open_tracking: Optional[pulumi.Input[bool]] = None,
                 receiving_records: Optional[pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordArgs']]]] = None,
                 receiving_records_sets: Optional[pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordsSetArgs']]]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 sending_records: Optional[pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordArgs']]]] = None,
                 sending_records_sets: Optional[pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordsSetArgs']]]] = None,
                 smtp_login: Optional[pulumi.Input[str]] = None,
                 smtp_password: Optional[pulumi.Input[str]] = None,
                 spam_action: Optional[pulumi.Input[str]] = None,
                 wildcard: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Domain resources.
        :param pulumi.Input[int] dkim_key_size: The length of your domain’s generated DKIM key. Default value is `1024`.
        :param pulumi.Input[str] dkim_selector: The name of your DKIM selector if you want to specify it whereas MailGun will make it's own choice.
        :param pulumi.Input[bool] force_dkim_authority: If set to true, the domain will be the DKIM authority for itself even if the root domain is registered on the same mailgun account. If set to false, the domain will have the same DKIM authority as the root domain registered on the same mailgun account. The default is `false`.
        :param pulumi.Input[str] name: The domain to add to Mailgun
        :param pulumi.Input[bool] open_tracking: (Enum: `yes` or `no`) The open tracking settings for the domain. Default: `no`
        :param pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordArgs']]] receiving_records: A list of DNS records for receiving validation.  **Deprecated** Use `receiving_records_set` instead.
        :param pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordsSetArgs']]] receiving_records_sets: A set of DNS records for receiving validation.
        :param pulumi.Input[str] region: The region where domain will be created. Default value is `us`.
        :param pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordArgs']]] sending_records: A list of DNS records for sending validation. **Deprecated** Use `sending_records_set` instead.
        :param pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordsSetArgs']]] sending_records_sets: A set of DNS records for sending validation.
        :param pulumi.Input[str] smtp_login: The login email for the SMTP server.
        :param pulumi.Input[str] smtp_password: Password for SMTP authentication
        :param pulumi.Input[str] spam_action: `disabled` or `tag` Disable, no spam
               filtering will occur for inbound messages. Tag, messages
               will be tagged with a spam header.
        :param pulumi.Input[bool] wildcard: Boolean that determines whether
               the domain will accept email for sub-domains.
        """
        if dkim_key_size is not None:
            pulumi.set(__self__, "dkim_key_size", dkim_key_size)
        if dkim_selector is not None:
            pulumi.set(__self__, "dkim_selector", dkim_selector)
        if force_dkim_authority is not None:
            pulumi.set(__self__, "force_dkim_authority", force_dkim_authority)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if open_tracking is not None:
            pulumi.set(__self__, "open_tracking", open_tracking)
        if receiving_records is not None:
            warnings.warn("""Use `receiving_records_set` instead.""", DeprecationWarning)
            pulumi.log.warn("""receiving_records is deprecated: Use `receiving_records_set` instead.""")
        if receiving_records is not None:
            pulumi.set(__self__, "receiving_records", receiving_records)
        if receiving_records_sets is not None:
            pulumi.set(__self__, "receiving_records_sets", receiving_records_sets)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if sending_records is not None:
            warnings.warn("""Use `sending_records_set` instead.""", DeprecationWarning)
            pulumi.log.warn("""sending_records is deprecated: Use `sending_records_set` instead.""")
        if sending_records is not None:
            pulumi.set(__self__, "sending_records", sending_records)
        if sending_records_sets is not None:
            pulumi.set(__self__, "sending_records_sets", sending_records_sets)
        if smtp_login is not None:
            pulumi.set(__self__, "smtp_login", smtp_login)
        if smtp_password is not None:
            pulumi.set(__self__, "smtp_password", smtp_password)
        if spam_action is not None:
            pulumi.set(__self__, "spam_action", spam_action)
        if wildcard is not None:
            pulumi.set(__self__, "wildcard", wildcard)

    @property
    @pulumi.getter(name="dkimKeySize")
    def dkim_key_size(self) -> Optional[pulumi.Input[int]]:
        """
        The length of your domain’s generated DKIM key. Default value is `1024`.
        """
        return pulumi.get(self, "dkim_key_size")

    @dkim_key_size.setter
    def dkim_key_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "dkim_key_size", value)

    @property
    @pulumi.getter(name="dkimSelector")
    def dkim_selector(self) -> Optional[pulumi.Input[str]]:
        """
        The name of your DKIM selector if you want to specify it whereas MailGun will make it's own choice.
        """
        return pulumi.get(self, "dkim_selector")

    @dkim_selector.setter
    def dkim_selector(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dkim_selector", value)

    @property
    @pulumi.getter(name="forceDkimAuthority")
    def force_dkim_authority(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, the domain will be the DKIM authority for itself even if the root domain is registered on the same mailgun account. If set to false, the domain will have the same DKIM authority as the root domain registered on the same mailgun account. The default is `false`.
        """
        return pulumi.get(self, "force_dkim_authority")

    @force_dkim_authority.setter
    def force_dkim_authority(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_dkim_authority", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain to add to Mailgun
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="openTracking")
    def open_tracking(self) -> Optional[pulumi.Input[bool]]:
        """
        (Enum: `yes` or `no`) The open tracking settings for the domain. Default: `no`
        """
        return pulumi.get(self, "open_tracking")

    @open_tracking.setter
    def open_tracking(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "open_tracking", value)

    @property
    @pulumi.getter(name="receivingRecords")
    def receiving_records(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordArgs']]]]:
        """
        A list of DNS records for receiving validation.  **Deprecated** Use `receiving_records_set` instead.
        """
        return pulumi.get(self, "receiving_records")

    @receiving_records.setter
    def receiving_records(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordArgs']]]]):
        pulumi.set(self, "receiving_records", value)

    @property
    @pulumi.getter(name="receivingRecordsSets")
    def receiving_records_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordsSetArgs']]]]:
        """
        A set of DNS records for receiving validation.
        """
        return pulumi.get(self, "receiving_records_sets")

    @receiving_records_sets.setter
    def receiving_records_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DomainReceivingRecordsSetArgs']]]]):
        pulumi.set(self, "receiving_records_sets", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region where domain will be created. Default value is `us`.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="sendingRecords")
    def sending_records(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordArgs']]]]:
        """
        A list of DNS records for sending validation. **Deprecated** Use `sending_records_set` instead.
        """
        return pulumi.get(self, "sending_records")

    @sending_records.setter
    def sending_records(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordArgs']]]]):
        pulumi.set(self, "sending_records", value)

    @property
    @pulumi.getter(name="sendingRecordsSets")
    def sending_records_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordsSetArgs']]]]:
        """
        A set of DNS records for sending validation.
        """
        return pulumi.get(self, "sending_records_sets")

    @sending_records_sets.setter
    def sending_records_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DomainSendingRecordsSetArgs']]]]):
        pulumi.set(self, "sending_records_sets", value)

    @property
    @pulumi.getter(name="smtpLogin")
    def smtp_login(self) -> Optional[pulumi.Input[str]]:
        """
        The login email for the SMTP server.
        """
        return pulumi.get(self, "smtp_login")

    @smtp_login.setter
    def smtp_login(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "smtp_login", value)

    @property
    @pulumi.getter(name="smtpPassword")
    def smtp_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for SMTP authentication
        """
        return pulumi.get(self, "smtp_password")

    @smtp_password.setter
    def smtp_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "smtp_password", value)

    @property
    @pulumi.getter(name="spamAction")
    def spam_action(self) -> Optional[pulumi.Input[str]]:
        """
        `disabled` or `tag` Disable, no spam
        filtering will occur for inbound messages. Tag, messages
        will be tagged with a spam header.
        """
        return pulumi.get(self, "spam_action")

    @spam_action.setter
    def spam_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spam_action", value)

    @property
    @pulumi.getter
    def wildcard(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean that determines whether
        the domain will accept email for sub-domains.
        """
        return pulumi.get(self, "wildcard")

    @wildcard.setter
    def wildcard(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wildcard", value)


class Domain(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dkim_key_size: Optional[pulumi.Input[int]] = None,
                 dkim_selector: Optional[pulumi.Input[str]] = None,
                 force_dkim_authority: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 open_tracking: Optional[pulumi.Input[bool]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 smtp_password: Optional[pulumi.Input[str]] = None,
                 spam_action: Optional[pulumi.Input[str]] = None,
                 wildcard: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Provides a Mailgun App resource. This can be used to
        create and manage applications on Mailgun.

        After DNS records are set, domain verification should be triggered manually using [PUT /domains/\\<domain\\>/verify](https://documentation.mailgun.com/en/latest/api-domains.html#domains)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_mailgun as mailgun

        # Create a new Mailgun domain
        default = mailgun.Domain("default",
            dkim_key_size=1024,
            region="us",
            smtp_password="supersecretpassword1234",
            spam_action="disabled")
        ```

        ## Import

        Domains can be imported using `region:domain_name` via `import` command. Region has to be chosen from `eu` or `us` (when no selection `us` is applied).

        hcl

        ```sh
         $ pulumi import mailgun:index/domain:Domain test us:example.domain.com
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] dkim_key_size: The length of your domain’s generated DKIM key. Default value is `1024`.
        :param pulumi.Input[str] dkim_selector: The name of your DKIM selector if you want to specify it whereas MailGun will make it's own choice.
        :param pulumi.Input[bool] force_dkim_authority: If set to true, the domain will be the DKIM authority for itself even if the root domain is registered on the same mailgun account. If set to false, the domain will have the same DKIM authority as the root domain registered on the same mailgun account. The default is `false`.
        :param pulumi.Input[str] name: The domain to add to Mailgun
        :param pulumi.Input[bool] open_tracking: (Enum: `yes` or `no`) The open tracking settings for the domain. Default: `no`
        :param pulumi.Input[str] region: The region where domain will be created. Default value is `us`.
        :param pulumi.Input[str] smtp_password: Password for SMTP authentication
        :param pulumi.Input[str] spam_action: `disabled` or `tag` Disable, no spam
               filtering will occur for inbound messages. Tag, messages
               will be tagged with a spam header.
        :param pulumi.Input[bool] wildcard: Boolean that determines whether
               the domain will accept email for sub-domains.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[DomainArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Mailgun App resource. This can be used to
        create and manage applications on Mailgun.

        After DNS records are set, domain verification should be triggered manually using [PUT /domains/\\<domain\\>/verify](https://documentation.mailgun.com/en/latest/api-domains.html#domains)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_mailgun as mailgun

        # Create a new Mailgun domain
        default = mailgun.Domain("default",
            dkim_key_size=1024,
            region="us",
            smtp_password="supersecretpassword1234",
            spam_action="disabled")
        ```

        ## Import

        Domains can be imported using `region:domain_name` via `import` command. Region has to be chosen from `eu` or `us` (when no selection `us` is applied).

        hcl

        ```sh
         $ pulumi import mailgun:index/domain:Domain test us:example.domain.com
        ```

        :param str resource_name: The name of the resource.
        :param DomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dkim_key_size: Optional[pulumi.Input[int]] = None,
                 dkim_selector: Optional[pulumi.Input[str]] = None,
                 force_dkim_authority: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 open_tracking: Optional[pulumi.Input[bool]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 smtp_password: Optional[pulumi.Input[str]] = None,
                 spam_action: Optional[pulumi.Input[str]] = None,
                 wildcard: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainArgs.__new__(DomainArgs)

            __props__.__dict__["dkim_key_size"] = dkim_key_size
            __props__.__dict__["dkim_selector"] = dkim_selector
            __props__.__dict__["force_dkim_authority"] = force_dkim_authority
            __props__.__dict__["name"] = name
            __props__.__dict__["open_tracking"] = open_tracking
            __props__.__dict__["region"] = region
            __props__.__dict__["smtp_password"] = None if smtp_password is None else pulumi.Output.secret(smtp_password)
            __props__.__dict__["spam_action"] = spam_action
            __props__.__dict__["wildcard"] = wildcard
            __props__.__dict__["receiving_records"] = None
            __props__.__dict__["receiving_records_sets"] = None
            __props__.__dict__["sending_records"] = None
            __props__.__dict__["sending_records_sets"] = None
            __props__.__dict__["smtp_login"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["smtpPassword"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Domain, __self__).__init__(
            'mailgun:index/domain:Domain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            dkim_key_size: Optional[pulumi.Input[int]] = None,
            dkim_selector: Optional[pulumi.Input[str]] = None,
            force_dkim_authority: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            open_tracking: Optional[pulumi.Input[bool]] = None,
            receiving_records: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainReceivingRecordArgs']]]]] = None,
            receiving_records_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainReceivingRecordsSetArgs']]]]] = None,
            region: Optional[pulumi.Input[str]] = None,
            sending_records: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainSendingRecordArgs']]]]] = None,
            sending_records_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainSendingRecordsSetArgs']]]]] = None,
            smtp_login: Optional[pulumi.Input[str]] = None,
            smtp_password: Optional[pulumi.Input[str]] = None,
            spam_action: Optional[pulumi.Input[str]] = None,
            wildcard: Optional[pulumi.Input[bool]] = None) -> 'Domain':
        """
        Get an existing Domain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] dkim_key_size: The length of your domain’s generated DKIM key. Default value is `1024`.
        :param pulumi.Input[str] dkim_selector: The name of your DKIM selector if you want to specify it whereas MailGun will make it's own choice.
        :param pulumi.Input[bool] force_dkim_authority: If set to true, the domain will be the DKIM authority for itself even if the root domain is registered on the same mailgun account. If set to false, the domain will have the same DKIM authority as the root domain registered on the same mailgun account. The default is `false`.
        :param pulumi.Input[str] name: The domain to add to Mailgun
        :param pulumi.Input[bool] open_tracking: (Enum: `yes` or `no`) The open tracking settings for the domain. Default: `no`
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainReceivingRecordArgs']]]] receiving_records: A list of DNS records for receiving validation.  **Deprecated** Use `receiving_records_set` instead.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainReceivingRecordsSetArgs']]]] receiving_records_sets: A set of DNS records for receiving validation.
        :param pulumi.Input[str] region: The region where domain will be created. Default value is `us`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainSendingRecordArgs']]]] sending_records: A list of DNS records for sending validation. **Deprecated** Use `sending_records_set` instead.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainSendingRecordsSetArgs']]]] sending_records_sets: A set of DNS records for sending validation.
        :param pulumi.Input[str] smtp_login: The login email for the SMTP server.
        :param pulumi.Input[str] smtp_password: Password for SMTP authentication
        :param pulumi.Input[str] spam_action: `disabled` or `tag` Disable, no spam
               filtering will occur for inbound messages. Tag, messages
               will be tagged with a spam header.
        :param pulumi.Input[bool] wildcard: Boolean that determines whether
               the domain will accept email for sub-domains.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DomainState.__new__(_DomainState)

        __props__.__dict__["dkim_key_size"] = dkim_key_size
        __props__.__dict__["dkim_selector"] = dkim_selector
        __props__.__dict__["force_dkim_authority"] = force_dkim_authority
        __props__.__dict__["name"] = name
        __props__.__dict__["open_tracking"] = open_tracking
        __props__.__dict__["receiving_records"] = receiving_records
        __props__.__dict__["receiving_records_sets"] = receiving_records_sets
        __props__.__dict__["region"] = region
        __props__.__dict__["sending_records"] = sending_records
        __props__.__dict__["sending_records_sets"] = sending_records_sets
        __props__.__dict__["smtp_login"] = smtp_login
        __props__.__dict__["smtp_password"] = smtp_password
        __props__.__dict__["spam_action"] = spam_action
        __props__.__dict__["wildcard"] = wildcard
        return Domain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dkimKeySize")
    def dkim_key_size(self) -> pulumi.Output[Optional[int]]:
        """
        The length of your domain’s generated DKIM key. Default value is `1024`.
        """
        return pulumi.get(self, "dkim_key_size")

    @property
    @pulumi.getter(name="dkimSelector")
    def dkim_selector(self) -> pulumi.Output[Optional[str]]:
        """
        The name of your DKIM selector if you want to specify it whereas MailGun will make it's own choice.
        """
        return pulumi.get(self, "dkim_selector")

    @property
    @pulumi.getter(name="forceDkimAuthority")
    def force_dkim_authority(self) -> pulumi.Output[Optional[bool]]:
        """
        If set to true, the domain will be the DKIM authority for itself even if the root domain is registered on the same mailgun account. If set to false, the domain will have the same DKIM authority as the root domain registered on the same mailgun account. The default is `false`.
        """
        return pulumi.get(self, "force_dkim_authority")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The domain to add to Mailgun
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="openTracking")
    def open_tracking(self) -> pulumi.Output[Optional[bool]]:
        """
        (Enum: `yes` or `no`) The open tracking settings for the domain. Default: `no`
        """
        return pulumi.get(self, "open_tracking")

    @property
    @pulumi.getter(name="receivingRecords")
    def receiving_records(self) -> pulumi.Output[Sequence['outputs.DomainReceivingRecord']]:
        """
        A list of DNS records for receiving validation.  **Deprecated** Use `receiving_records_set` instead.
        """
        return pulumi.get(self, "receiving_records")

    @property
    @pulumi.getter(name="receivingRecordsSets")
    def receiving_records_sets(self) -> pulumi.Output[Sequence['outputs.DomainReceivingRecordsSet']]:
        """
        A set of DNS records for receiving validation.
        """
        return pulumi.get(self, "receiving_records_sets")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[Optional[str]]:
        """
        The region where domain will be created. Default value is `us`.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="sendingRecords")
    def sending_records(self) -> pulumi.Output[Sequence['outputs.DomainSendingRecord']]:
        """
        A list of DNS records for sending validation. **Deprecated** Use `sending_records_set` instead.
        """
        return pulumi.get(self, "sending_records")

    @property
    @pulumi.getter(name="sendingRecordsSets")
    def sending_records_sets(self) -> pulumi.Output[Sequence['outputs.DomainSendingRecordsSet']]:
        """
        A set of DNS records for sending validation.
        """
        return pulumi.get(self, "sending_records_sets")

    @property
    @pulumi.getter(name="smtpLogin")
    def smtp_login(self) -> pulumi.Output[str]:
        """
        The login email for the SMTP server.
        """
        return pulumi.get(self, "smtp_login")

    @property
    @pulumi.getter(name="smtpPassword")
    def smtp_password(self) -> pulumi.Output[Optional[str]]:
        """
        Password for SMTP authentication
        """
        return pulumi.get(self, "smtp_password")

    @property
    @pulumi.getter(name="spamAction")
    def spam_action(self) -> pulumi.Output[Optional[str]]:
        """
        `disabled` or `tag` Disable, no spam
        filtering will occur for inbound messages. Tag, messages
        will be tagged with a spam header.
        """
        return pulumi.get(self, "spam_action")

    @property
    @pulumi.getter
    def wildcard(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean that determines whether
        the domain will accept email for sub-domains.
        """
        return pulumi.get(self, "wildcard")

