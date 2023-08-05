# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['BootstrapArgs', 'Bootstrap']

@pulumi.input_type
class BootstrapArgs:
    def __init__(__self__, *,
                 initial_password: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 telemetry: Optional[pulumi.Input[bool]] = None,
                 token_ttl: Optional[pulumi.Input[int]] = None,
                 token_update: Optional[pulumi.Input[bool]] = None,
                 ui_default_landing: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Bootstrap resource.
        :param pulumi.Input[str] initial_password: Initial password for Admin user. Default: `admin` (string)
        :param pulumi.Input[str] password: Password for Admin user or random generated if empty (string)
        :param pulumi.Input[bool] telemetry: Send telemetry anonymous data. Default: `false` (bool)
        :param pulumi.Input[int] token_ttl: TTL in seconds for generated admin token. Default: `0`  (int)
        :param pulumi.Input[bool] token_update: Regenerate admin token. Default: `false` (bool)
        :param pulumi.Input[str] ui_default_landing: Default UI landing for k8s clusters. Available options: `ember` (cluster manager ui)  and `vue` (cluster explorer ui). Default: `ember` (string)
        """
        if initial_password is not None:
            pulumi.set(__self__, "initial_password", initial_password)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if telemetry is not None:
            pulumi.set(__self__, "telemetry", telemetry)
        if token_ttl is not None:
            pulumi.set(__self__, "token_ttl", token_ttl)
        if token_update is not None:
            pulumi.set(__self__, "token_update", token_update)
        if ui_default_landing is not None:
            pulumi.set(__self__, "ui_default_landing", ui_default_landing)

    @property
    @pulumi.getter(name="initialPassword")
    def initial_password(self) -> Optional[pulumi.Input[str]]:
        """
        Initial password for Admin user. Default: `admin` (string)
        """
        return pulumi.get(self, "initial_password")

    @initial_password.setter
    def initial_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "initial_password", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for Admin user or random generated if empty (string)
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def telemetry(self) -> Optional[pulumi.Input[bool]]:
        """
        Send telemetry anonymous data. Default: `false` (bool)
        """
        return pulumi.get(self, "telemetry")

    @telemetry.setter
    def telemetry(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "telemetry", value)

    @property
    @pulumi.getter(name="tokenTtl")
    def token_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        TTL in seconds for generated admin token. Default: `0`  (int)
        """
        return pulumi.get(self, "token_ttl")

    @token_ttl.setter
    def token_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "token_ttl", value)

    @property
    @pulumi.getter(name="tokenUpdate")
    def token_update(self) -> Optional[pulumi.Input[bool]]:
        """
        Regenerate admin token. Default: `false` (bool)
        """
        return pulumi.get(self, "token_update")

    @token_update.setter
    def token_update(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "token_update", value)

    @property
    @pulumi.getter(name="uiDefaultLanding")
    def ui_default_landing(self) -> Optional[pulumi.Input[str]]:
        """
        Default UI landing for k8s clusters. Available options: `ember` (cluster manager ui)  and `vue` (cluster explorer ui). Default: `ember` (string)
        """
        return pulumi.get(self, "ui_default_landing")

    @ui_default_landing.setter
    def ui_default_landing(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ui_default_landing", value)


@pulumi.input_type
class _BootstrapState:
    def __init__(__self__, *,
                 current_password: Optional[pulumi.Input[str]] = None,
                 initial_password: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 telemetry: Optional[pulumi.Input[bool]] = None,
                 temp_token: Optional[pulumi.Input[str]] = None,
                 temp_token_id: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 token_id: Optional[pulumi.Input[str]] = None,
                 token_ttl: Optional[pulumi.Input[int]] = None,
                 token_update: Optional[pulumi.Input[bool]] = None,
                 ui_default_landing: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Bootstrap resources.
        :param pulumi.Input[str] current_password: (Computed/Sensitive) Current password for Admin user (string)
        :param pulumi.Input[str] initial_password: Initial password for Admin user. Default: `admin` (string)
        :param pulumi.Input[str] password: Password for Admin user or random generated if empty (string)
        :param pulumi.Input[bool] telemetry: Send telemetry anonymous data. Default: `false` (bool)
        :param pulumi.Input[str] temp_token: (Computed) Generated API temporary token as helper. Should be empty (string)
        :param pulumi.Input[str] temp_token_id: (Computed) Generated API temporary token id as helper. Should be empty (string)
        :param pulumi.Input[str] token: (Computed) Generated API token for Admin User (string)
        :param pulumi.Input[str] token_id: (Computed) Generated API token id for Admin User (string)
        :param pulumi.Input[int] token_ttl: TTL in seconds for generated admin token. Default: `0`  (int)
        :param pulumi.Input[bool] token_update: Regenerate admin token. Default: `false` (bool)
        :param pulumi.Input[str] ui_default_landing: Default UI landing for k8s clusters. Available options: `ember` (cluster manager ui)  and `vue` (cluster explorer ui). Default: `ember` (string)
        :param pulumi.Input[str] url: (Computed) URL set as server-url (string)
        :param pulumi.Input[str] user: (Computed) Admin username (string)
        """
        if current_password is not None:
            pulumi.set(__self__, "current_password", current_password)
        if initial_password is not None:
            pulumi.set(__self__, "initial_password", initial_password)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if telemetry is not None:
            pulumi.set(__self__, "telemetry", telemetry)
        if temp_token is not None:
            pulumi.set(__self__, "temp_token", temp_token)
        if temp_token_id is not None:
            pulumi.set(__self__, "temp_token_id", temp_token_id)
        if token is not None:
            pulumi.set(__self__, "token", token)
        if token_id is not None:
            pulumi.set(__self__, "token_id", token_id)
        if token_ttl is not None:
            pulumi.set(__self__, "token_ttl", token_ttl)
        if token_update is not None:
            pulumi.set(__self__, "token_update", token_update)
        if ui_default_landing is not None:
            pulumi.set(__self__, "ui_default_landing", ui_default_landing)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter(name="currentPassword")
    def current_password(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed/Sensitive) Current password for Admin user (string)
        """
        return pulumi.get(self, "current_password")

    @current_password.setter
    def current_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "current_password", value)

    @property
    @pulumi.getter(name="initialPassword")
    def initial_password(self) -> Optional[pulumi.Input[str]]:
        """
        Initial password for Admin user. Default: `admin` (string)
        """
        return pulumi.get(self, "initial_password")

    @initial_password.setter
    def initial_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "initial_password", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for Admin user or random generated if empty (string)
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def telemetry(self) -> Optional[pulumi.Input[bool]]:
        """
        Send telemetry anonymous data. Default: `false` (bool)
        """
        return pulumi.get(self, "telemetry")

    @telemetry.setter
    def telemetry(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "telemetry", value)

    @property
    @pulumi.getter(name="tempToken")
    def temp_token(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) Generated API temporary token as helper. Should be empty (string)
        """
        return pulumi.get(self, "temp_token")

    @temp_token.setter
    def temp_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "temp_token", value)

    @property
    @pulumi.getter(name="tempTokenId")
    def temp_token_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) Generated API temporary token id as helper. Should be empty (string)
        """
        return pulumi.get(self, "temp_token_id")

    @temp_token_id.setter
    def temp_token_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "temp_token_id", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) Generated API token for Admin User (string)
        """
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)

    @property
    @pulumi.getter(name="tokenId")
    def token_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) Generated API token id for Admin User (string)
        """
        return pulumi.get(self, "token_id")

    @token_id.setter
    def token_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_id", value)

    @property
    @pulumi.getter(name="tokenTtl")
    def token_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        TTL in seconds for generated admin token. Default: `0`  (int)
        """
        return pulumi.get(self, "token_ttl")

    @token_ttl.setter
    def token_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "token_ttl", value)

    @property
    @pulumi.getter(name="tokenUpdate")
    def token_update(self) -> Optional[pulumi.Input[bool]]:
        """
        Regenerate admin token. Default: `false` (bool)
        """
        return pulumi.get(self, "token_update")

    @token_update.setter
    def token_update(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "token_update", value)

    @property
    @pulumi.getter(name="uiDefaultLanding")
    def ui_default_landing(self) -> Optional[pulumi.Input[str]]:
        """
        Default UI landing for k8s clusters. Available options: `ember` (cluster manager ui)  and `vue` (cluster explorer ui). Default: `ember` (string)
        """
        return pulumi.get(self, "ui_default_landing")

    @ui_default_landing.setter
    def ui_default_landing(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ui_default_landing", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) URL set as server-url (string)
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) Admin username (string)
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


class Bootstrap(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 initial_password: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 telemetry: Optional[pulumi.Input[bool]] = None,
                 token_ttl: Optional[pulumi.Input[int]] = None,
                 token_update: Optional[pulumi.Input[bool]] = None,
                 ui_default_landing: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Create a new rancher2_bootstrap
        admin = rancher2.Bootstrap("admin",
            password="blahblah",
            telemetry=True)
        ```

        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Create a new rancher2_bootstrap for Rancher v2.6.0 and above
        admin = rancher2.Bootstrap("admin",
            initial_password="<INSTALL_PASSWORD>",
            password="blahblah",
            telemetry=True)
        ```

        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Provider bootstrap config with alias
        bootstrap = rancher2.Provider("bootstrap",
            api_url="https://rancher.my-domain.com",
            bootstrap=True)
        # Create a new rancher2_bootstrap using bootstrap provider config
        admin = rancher2.Bootstrap("admin",
            password="blahblah",
            telemetry=True,
            opts=pulumi.ResourceOptions(provider="rancher2.bootstrap"))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] initial_password: Initial password for Admin user. Default: `admin` (string)
        :param pulumi.Input[str] password: Password for Admin user or random generated if empty (string)
        :param pulumi.Input[bool] telemetry: Send telemetry anonymous data. Default: `false` (bool)
        :param pulumi.Input[int] token_ttl: TTL in seconds for generated admin token. Default: `0`  (int)
        :param pulumi.Input[bool] token_update: Regenerate admin token. Default: `false` (bool)
        :param pulumi.Input[str] ui_default_landing: Default UI landing for k8s clusters. Available options: `ember` (cluster manager ui)  and `vue` (cluster explorer ui). Default: `ember` (string)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[BootstrapArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Create a new rancher2_bootstrap
        admin = rancher2.Bootstrap("admin",
            password="blahblah",
            telemetry=True)
        ```

        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Create a new rancher2_bootstrap for Rancher v2.6.0 and above
        admin = rancher2.Bootstrap("admin",
            initial_password="<INSTALL_PASSWORD>",
            password="blahblah",
            telemetry=True)
        ```

        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Provider bootstrap config with alias
        bootstrap = rancher2.Provider("bootstrap",
            api_url="https://rancher.my-domain.com",
            bootstrap=True)
        # Create a new rancher2_bootstrap using bootstrap provider config
        admin = rancher2.Bootstrap("admin",
            password="blahblah",
            telemetry=True,
            opts=pulumi.ResourceOptions(provider="rancher2.bootstrap"))
        ```

        :param str resource_name: The name of the resource.
        :param BootstrapArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BootstrapArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 initial_password: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 telemetry: Optional[pulumi.Input[bool]] = None,
                 token_ttl: Optional[pulumi.Input[int]] = None,
                 token_update: Optional[pulumi.Input[bool]] = None,
                 ui_default_landing: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BootstrapArgs.__new__(BootstrapArgs)

            __props__.__dict__["initial_password"] = None if initial_password is None else pulumi.Output.secret(initial_password)
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            __props__.__dict__["telemetry"] = telemetry
            __props__.__dict__["token_ttl"] = token_ttl
            __props__.__dict__["token_update"] = token_update
            __props__.__dict__["ui_default_landing"] = ui_default_landing
            __props__.__dict__["current_password"] = None
            __props__.__dict__["temp_token"] = None
            __props__.__dict__["temp_token_id"] = None
            __props__.__dict__["token"] = None
            __props__.__dict__["token_id"] = None
            __props__.__dict__["url"] = None
            __props__.__dict__["user"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["currentPassword", "initialPassword", "password", "tempToken", "token"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Bootstrap, __self__).__init__(
            'rancher2:index/bootstrap:Bootstrap',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            current_password: Optional[pulumi.Input[str]] = None,
            initial_password: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            telemetry: Optional[pulumi.Input[bool]] = None,
            temp_token: Optional[pulumi.Input[str]] = None,
            temp_token_id: Optional[pulumi.Input[str]] = None,
            token: Optional[pulumi.Input[str]] = None,
            token_id: Optional[pulumi.Input[str]] = None,
            token_ttl: Optional[pulumi.Input[int]] = None,
            token_update: Optional[pulumi.Input[bool]] = None,
            ui_default_landing: Optional[pulumi.Input[str]] = None,
            url: Optional[pulumi.Input[str]] = None,
            user: Optional[pulumi.Input[str]] = None) -> 'Bootstrap':
        """
        Get an existing Bootstrap resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] current_password: (Computed/Sensitive) Current password for Admin user (string)
        :param pulumi.Input[str] initial_password: Initial password for Admin user. Default: `admin` (string)
        :param pulumi.Input[str] password: Password for Admin user or random generated if empty (string)
        :param pulumi.Input[bool] telemetry: Send telemetry anonymous data. Default: `false` (bool)
        :param pulumi.Input[str] temp_token: (Computed) Generated API temporary token as helper. Should be empty (string)
        :param pulumi.Input[str] temp_token_id: (Computed) Generated API temporary token id as helper. Should be empty (string)
        :param pulumi.Input[str] token: (Computed) Generated API token for Admin User (string)
        :param pulumi.Input[str] token_id: (Computed) Generated API token id for Admin User (string)
        :param pulumi.Input[int] token_ttl: TTL in seconds for generated admin token. Default: `0`  (int)
        :param pulumi.Input[bool] token_update: Regenerate admin token. Default: `false` (bool)
        :param pulumi.Input[str] ui_default_landing: Default UI landing for k8s clusters. Available options: `ember` (cluster manager ui)  and `vue` (cluster explorer ui). Default: `ember` (string)
        :param pulumi.Input[str] url: (Computed) URL set as server-url (string)
        :param pulumi.Input[str] user: (Computed) Admin username (string)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BootstrapState.__new__(_BootstrapState)

        __props__.__dict__["current_password"] = current_password
        __props__.__dict__["initial_password"] = initial_password
        __props__.__dict__["password"] = password
        __props__.__dict__["telemetry"] = telemetry
        __props__.__dict__["temp_token"] = temp_token
        __props__.__dict__["temp_token_id"] = temp_token_id
        __props__.__dict__["token"] = token
        __props__.__dict__["token_id"] = token_id
        __props__.__dict__["token_ttl"] = token_ttl
        __props__.__dict__["token_update"] = token_update
        __props__.__dict__["ui_default_landing"] = ui_default_landing
        __props__.__dict__["url"] = url
        __props__.__dict__["user"] = user
        return Bootstrap(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="currentPassword")
    def current_password(self) -> pulumi.Output[str]:
        """
        (Computed/Sensitive) Current password for Admin user (string)
        """
        return pulumi.get(self, "current_password")

    @property
    @pulumi.getter(name="initialPassword")
    def initial_password(self) -> pulumi.Output[Optional[str]]:
        """
        Initial password for Admin user. Default: `admin` (string)
        """
        return pulumi.get(self, "initial_password")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        Password for Admin user or random generated if empty (string)
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def telemetry(self) -> pulumi.Output[Optional[bool]]:
        """
        Send telemetry anonymous data. Default: `false` (bool)
        """
        return pulumi.get(self, "telemetry")

    @property
    @pulumi.getter(name="tempToken")
    def temp_token(self) -> pulumi.Output[str]:
        """
        (Computed) Generated API temporary token as helper. Should be empty (string)
        """
        return pulumi.get(self, "temp_token")

    @property
    @pulumi.getter(name="tempTokenId")
    def temp_token_id(self) -> pulumi.Output[str]:
        """
        (Computed) Generated API temporary token id as helper. Should be empty (string)
        """
        return pulumi.get(self, "temp_token_id")

    @property
    @pulumi.getter
    def token(self) -> pulumi.Output[str]:
        """
        (Computed) Generated API token for Admin User (string)
        """
        return pulumi.get(self, "token")

    @property
    @pulumi.getter(name="tokenId")
    def token_id(self) -> pulumi.Output[str]:
        """
        (Computed) Generated API token id for Admin User (string)
        """
        return pulumi.get(self, "token_id")

    @property
    @pulumi.getter(name="tokenTtl")
    def token_ttl(self) -> pulumi.Output[Optional[int]]:
        """
        TTL in seconds for generated admin token. Default: `0`  (int)
        """
        return pulumi.get(self, "token_ttl")

    @property
    @pulumi.getter(name="tokenUpdate")
    def token_update(self) -> pulumi.Output[Optional[bool]]:
        """
        Regenerate admin token. Default: `false` (bool)
        """
        return pulumi.get(self, "token_update")

    @property
    @pulumi.getter(name="uiDefaultLanding")
    def ui_default_landing(self) -> pulumi.Output[Optional[str]]:
        """
        Default UI landing for k8s clusters. Available options: `ember` (cluster manager ui)  and `vue` (cluster explorer ui). Default: `ember` (string)
        """
        return pulumi.get(self, "ui_default_landing")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        (Computed) URL set as server-url (string)
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        (Computed) Admin username (string)
        """
        return pulumi.get(self, "user")

