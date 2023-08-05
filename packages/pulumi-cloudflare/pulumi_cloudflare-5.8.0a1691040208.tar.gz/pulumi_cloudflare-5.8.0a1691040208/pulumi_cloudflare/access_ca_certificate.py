# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AccessCaCertificateArgs', 'AccessCaCertificate']

@pulumi.input_type
class AccessCaCertificateArgs:
    def __init__(__self__, *,
                 application_id: pulumi.Input[str],
                 account_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AccessCaCertificate resource.
        :param pulumi.Input[str] application_id: The Access Application ID to associate with the CA certificate.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource. Conflicts with `zone_id`.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. Conflicts with `account_id`.
        """
        pulumi.set(__self__, "application_id", application_id)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if zone_id is not None:
            pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Input[str]:
        """
        The Access Application ID to associate with the CA certificate.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account identifier to target for the resource. Conflicts with `zone_id`.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The zone identifier to target for the resource. Conflicts with `account_id`.
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone_id", value)


@pulumi.input_type
class _AccessCaCertificateState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 aud: Optional[pulumi.Input[str]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccessCaCertificate resources.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource. Conflicts with `zone_id`.
        :param pulumi.Input[str] application_id: The Access Application ID to associate with the CA certificate.
        :param pulumi.Input[str] aud: Application Audience (AUD) Tag of the CA certificate.
        :param pulumi.Input[str] public_key: Cryptographic public key of the generated CA certificate.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. Conflicts with `account_id`.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if aud is not None:
            pulumi.set(__self__, "aud", aud)
        if public_key is not None:
            pulumi.set(__self__, "public_key", public_key)
        if zone_id is not None:
            pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account identifier to target for the resource. Conflicts with `zone_id`.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Access Application ID to associate with the CA certificate.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter
    def aud(self) -> Optional[pulumi.Input[str]]:
        """
        Application Audience (AUD) Tag of the CA certificate.
        """
        return pulumi.get(self, "aud")

    @aud.setter
    def aud(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aud", value)

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> Optional[pulumi.Input[str]]:
        """
        Cryptographic public key of the generated CA certificate.
        """
        return pulumi.get(self, "public_key")

    @public_key.setter
    def public_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_key", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The zone identifier to target for the resource. Conflicts with `account_id`.
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone_id", value)


class AccessCaCertificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Cloudflare Access can replace traditional SSH key models with
        short-lived certificates issued to your users based on the token
        generated by their Access login.

        > It's required that an `account_id` or `zone_id` is provided and in
        most cases using either is fine. However, if you're using a scoped
        access token, you must provide the argument that matches the token's
        scope. For example, an access token that is scoped to the "example.com"
        zone needs to use the `zone_id` argument.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        # account level
        example = cloudflare.AccessCaCertificate("example",
            account_id="f037e56e89293a057740de681ac9abbe",
            application_id="6cd6cea3-3ef2-4542-9aea-85a0bbcd5414")
        # zone level
        another_example = cloudflare.AccessCaCertificate("anotherExample",
            application_id="fe2be0ff-7f13-4350-8c8e-a9b9795fe3c2",
            zone_id="0da42c8d2132a9ddaf714f9e7c920711")
        ```

        ## Import

        Account level CA certificate import.

        ```sh
         $ pulumi import cloudflare:index/accessCaCertificate:AccessCaCertificate example account/<account_id>/<application_id>
        ```

         Zone level CA certificate import.

        ```sh
         $ pulumi import cloudflare:index/accessCaCertificate:AccessCaCertificate example account/<zone_id>/<application_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource. Conflicts with `zone_id`.
        :param pulumi.Input[str] application_id: The Access Application ID to associate with the CA certificate.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. Conflicts with `account_id`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccessCaCertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Cloudflare Access can replace traditional SSH key models with
        short-lived certificates issued to your users based on the token
        generated by their Access login.

        > It's required that an `account_id` or `zone_id` is provided and in
        most cases using either is fine. However, if you're using a scoped
        access token, you must provide the argument that matches the token's
        scope. For example, an access token that is scoped to the "example.com"
        zone needs to use the `zone_id` argument.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        # account level
        example = cloudflare.AccessCaCertificate("example",
            account_id="f037e56e89293a057740de681ac9abbe",
            application_id="6cd6cea3-3ef2-4542-9aea-85a0bbcd5414")
        # zone level
        another_example = cloudflare.AccessCaCertificate("anotherExample",
            application_id="fe2be0ff-7f13-4350-8c8e-a9b9795fe3c2",
            zone_id="0da42c8d2132a9ddaf714f9e7c920711")
        ```

        ## Import

        Account level CA certificate import.

        ```sh
         $ pulumi import cloudflare:index/accessCaCertificate:AccessCaCertificate example account/<account_id>/<application_id>
        ```

         Zone level CA certificate import.

        ```sh
         $ pulumi import cloudflare:index/accessCaCertificate:AccessCaCertificate example account/<zone_id>/<application_id>
        ```

        :param str resource_name: The name of the resource.
        :param AccessCaCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessCaCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccessCaCertificateArgs.__new__(AccessCaCertificateArgs)

            __props__.__dict__["account_id"] = account_id
            if application_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_id'")
            __props__.__dict__["application_id"] = application_id
            __props__.__dict__["zone_id"] = zone_id
            __props__.__dict__["aud"] = None
            __props__.__dict__["public_key"] = None
        super(AccessCaCertificate, __self__).__init__(
            'cloudflare:index/accessCaCertificate:AccessCaCertificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            application_id: Optional[pulumi.Input[str]] = None,
            aud: Optional[pulumi.Input[str]] = None,
            public_key: Optional[pulumi.Input[str]] = None,
            zone_id: Optional[pulumi.Input[str]] = None) -> 'AccessCaCertificate':
        """
        Get an existing AccessCaCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource. Conflicts with `zone_id`.
        :param pulumi.Input[str] application_id: The Access Application ID to associate with the CA certificate.
        :param pulumi.Input[str] aud: Application Audience (AUD) Tag of the CA certificate.
        :param pulumi.Input[str] public_key: Cryptographic public key of the generated CA certificate.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. Conflicts with `account_id`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccessCaCertificateState.__new__(_AccessCaCertificateState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["application_id"] = application_id
        __props__.__dict__["aud"] = aud
        __props__.__dict__["public_key"] = public_key
        __props__.__dict__["zone_id"] = zone_id
        return AccessCaCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        The account identifier to target for the resource. Conflicts with `zone_id`.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Output[str]:
        """
        The Access Application ID to associate with the CA certificate.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter
    def aud(self) -> pulumi.Output[str]:
        """
        Application Audience (AUD) Tag of the CA certificate.
        """
        return pulumi.get(self, "aud")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> pulumi.Output[str]:
        """
        Cryptographic public key of the generated CA certificate.
        """
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Output[str]:
        """
        The zone identifier to target for the resource. Conflicts with `account_id`.
        """
        return pulumi.get(self, "zone_id")

