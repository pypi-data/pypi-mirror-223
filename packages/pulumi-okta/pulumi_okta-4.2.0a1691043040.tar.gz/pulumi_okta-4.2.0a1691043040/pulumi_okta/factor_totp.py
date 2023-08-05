# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['FactorTotpArgs', 'FactorTotp']

@pulumi.input_type
class FactorTotpArgs:
    def __init__(__self__, *,
                 clock_drift_interval: Optional[pulumi.Input[int]] = None,
                 hmac_algorithm: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 otp_length: Optional[pulumi.Input[int]] = None,
                 shared_secret_encoding: Optional[pulumi.Input[str]] = None,
                 time_step: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a FactorTotp resource.
        :param pulumi.Input[int] clock_drift_interval: Clock drift interval. This setting allows you to build in tolerance for any
               drift between the token's current time and the server's current time. Valid values: `3`, `5`, `10`. Default is `3`.
        :param pulumi.Input[str] hmac_algorithm: HMAC Algorithm. Valid values: `"HMacSHA1"`, `"HMacSHA256"`, `"HMacSHA512"`. Default
               is `"HMacSHA512"`.
        :param pulumi.Input[str] name: The TOTP name.
        :param pulumi.Input[int] otp_length: Length of the password. Default is `6`.
        :param pulumi.Input[str] shared_secret_encoding: Shared secret encoding. Valid values: `"base32"`, `"base64"`, `"hexadecimal"`.
               Default is `"base32"`.
        :param pulumi.Input[int] time_step: Time step in seconds. Valid values: `15`, `30`, `60`. Default is `15`.
        """
        if clock_drift_interval is not None:
            pulumi.set(__self__, "clock_drift_interval", clock_drift_interval)
        if hmac_algorithm is not None:
            pulumi.set(__self__, "hmac_algorithm", hmac_algorithm)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if otp_length is not None:
            pulumi.set(__self__, "otp_length", otp_length)
        if shared_secret_encoding is not None:
            pulumi.set(__self__, "shared_secret_encoding", shared_secret_encoding)
        if time_step is not None:
            pulumi.set(__self__, "time_step", time_step)

    @property
    @pulumi.getter(name="clockDriftInterval")
    def clock_drift_interval(self) -> Optional[pulumi.Input[int]]:
        """
        Clock drift interval. This setting allows you to build in tolerance for any
        drift between the token's current time and the server's current time. Valid values: `3`, `5`, `10`. Default is `3`.
        """
        return pulumi.get(self, "clock_drift_interval")

    @clock_drift_interval.setter
    def clock_drift_interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "clock_drift_interval", value)

    @property
    @pulumi.getter(name="hmacAlgorithm")
    def hmac_algorithm(self) -> Optional[pulumi.Input[str]]:
        """
        HMAC Algorithm. Valid values: `"HMacSHA1"`, `"HMacSHA256"`, `"HMacSHA512"`. Default
        is `"HMacSHA512"`.
        """
        return pulumi.get(self, "hmac_algorithm")

    @hmac_algorithm.setter
    def hmac_algorithm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hmac_algorithm", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The TOTP name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="otpLength")
    def otp_length(self) -> Optional[pulumi.Input[int]]:
        """
        Length of the password. Default is `6`.
        """
        return pulumi.get(self, "otp_length")

    @otp_length.setter
    def otp_length(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "otp_length", value)

    @property
    @pulumi.getter(name="sharedSecretEncoding")
    def shared_secret_encoding(self) -> Optional[pulumi.Input[str]]:
        """
        Shared secret encoding. Valid values: `"base32"`, `"base64"`, `"hexadecimal"`.
        Default is `"base32"`.
        """
        return pulumi.get(self, "shared_secret_encoding")

    @shared_secret_encoding.setter
    def shared_secret_encoding(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "shared_secret_encoding", value)

    @property
    @pulumi.getter(name="timeStep")
    def time_step(self) -> Optional[pulumi.Input[int]]:
        """
        Time step in seconds. Valid values: `15`, `30`, `60`. Default is `15`.
        """
        return pulumi.get(self, "time_step")

    @time_step.setter
    def time_step(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "time_step", value)


@pulumi.input_type
class _FactorTotpState:
    def __init__(__self__, *,
                 clock_drift_interval: Optional[pulumi.Input[int]] = None,
                 hmac_algorithm: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 otp_length: Optional[pulumi.Input[int]] = None,
                 shared_secret_encoding: Optional[pulumi.Input[str]] = None,
                 time_step: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering FactorTotp resources.
        :param pulumi.Input[int] clock_drift_interval: Clock drift interval. This setting allows you to build in tolerance for any
               drift between the token's current time and the server's current time. Valid values: `3`, `5`, `10`. Default is `3`.
        :param pulumi.Input[str] hmac_algorithm: HMAC Algorithm. Valid values: `"HMacSHA1"`, `"HMacSHA256"`, `"HMacSHA512"`. Default
               is `"HMacSHA512"`.
        :param pulumi.Input[str] name: The TOTP name.
        :param pulumi.Input[int] otp_length: Length of the password. Default is `6`.
        :param pulumi.Input[str] shared_secret_encoding: Shared secret encoding. Valid values: `"base32"`, `"base64"`, `"hexadecimal"`.
               Default is `"base32"`.
        :param pulumi.Input[int] time_step: Time step in seconds. Valid values: `15`, `30`, `60`. Default is `15`.
        """
        if clock_drift_interval is not None:
            pulumi.set(__self__, "clock_drift_interval", clock_drift_interval)
        if hmac_algorithm is not None:
            pulumi.set(__self__, "hmac_algorithm", hmac_algorithm)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if otp_length is not None:
            pulumi.set(__self__, "otp_length", otp_length)
        if shared_secret_encoding is not None:
            pulumi.set(__self__, "shared_secret_encoding", shared_secret_encoding)
        if time_step is not None:
            pulumi.set(__self__, "time_step", time_step)

    @property
    @pulumi.getter(name="clockDriftInterval")
    def clock_drift_interval(self) -> Optional[pulumi.Input[int]]:
        """
        Clock drift interval. This setting allows you to build in tolerance for any
        drift between the token's current time and the server's current time. Valid values: `3`, `5`, `10`. Default is `3`.
        """
        return pulumi.get(self, "clock_drift_interval")

    @clock_drift_interval.setter
    def clock_drift_interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "clock_drift_interval", value)

    @property
    @pulumi.getter(name="hmacAlgorithm")
    def hmac_algorithm(self) -> Optional[pulumi.Input[str]]:
        """
        HMAC Algorithm. Valid values: `"HMacSHA1"`, `"HMacSHA256"`, `"HMacSHA512"`. Default
        is `"HMacSHA512"`.
        """
        return pulumi.get(self, "hmac_algorithm")

    @hmac_algorithm.setter
    def hmac_algorithm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hmac_algorithm", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The TOTP name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="otpLength")
    def otp_length(self) -> Optional[pulumi.Input[int]]:
        """
        Length of the password. Default is `6`.
        """
        return pulumi.get(self, "otp_length")

    @otp_length.setter
    def otp_length(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "otp_length", value)

    @property
    @pulumi.getter(name="sharedSecretEncoding")
    def shared_secret_encoding(self) -> Optional[pulumi.Input[str]]:
        """
        Shared secret encoding. Valid values: `"base32"`, `"base64"`, `"hexadecimal"`.
        Default is `"base32"`.
        """
        return pulumi.get(self, "shared_secret_encoding")

    @shared_secret_encoding.setter
    def shared_secret_encoding(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "shared_secret_encoding", value)

    @property
    @pulumi.getter(name="timeStep")
    def time_step(self) -> Optional[pulumi.Input[int]]:
        """
        Time step in seconds. Valid values: `15`, `30`, `60`. Default is `15`.
        """
        return pulumi.get(self, "time_step")

    @time_step.setter
    def time_step(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "time_step", value)


class FactorTotp(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 clock_drift_interval: Optional[pulumi.Input[int]] = None,
                 hmac_algorithm: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 otp_length: Optional[pulumi.Input[int]] = None,
                 shared_secret_encoding: Optional[pulumi.Input[str]] = None,
                 time_step: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Allows you to manage the time-based one-time password (TOTP) factors. A time-based one-time password (TOTP) is a
        temporary passcode that is generated for user authentication. Examples of TOTP include hardware authenticators and
        mobile app authenticators.

        Once saved, the settings cannot be changed (except for the `name` field). Any other change would force resource
        recreation.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.FactorTotp("example",
            clock_drift_interval=10,
            hmac_algorithm="HMacSHA256",
            otp_length=10,
            shared_secret_encoding="hexadecimal",
            time_step=30)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] clock_drift_interval: Clock drift interval. This setting allows you to build in tolerance for any
               drift between the token's current time and the server's current time. Valid values: `3`, `5`, `10`. Default is `3`.
        :param pulumi.Input[str] hmac_algorithm: HMAC Algorithm. Valid values: `"HMacSHA1"`, `"HMacSHA256"`, `"HMacSHA512"`. Default
               is `"HMacSHA512"`.
        :param pulumi.Input[str] name: The TOTP name.
        :param pulumi.Input[int] otp_length: Length of the password. Default is `6`.
        :param pulumi.Input[str] shared_secret_encoding: Shared secret encoding. Valid values: `"base32"`, `"base64"`, `"hexadecimal"`.
               Default is `"base32"`.
        :param pulumi.Input[int] time_step: Time step in seconds. Valid values: `15`, `30`, `60`. Default is `15`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[FactorTotpArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allows you to manage the time-based one-time password (TOTP) factors. A time-based one-time password (TOTP) is a
        temporary passcode that is generated for user authentication. Examples of TOTP include hardware authenticators and
        mobile app authenticators.

        Once saved, the settings cannot be changed (except for the `name` field). Any other change would force resource
        recreation.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.FactorTotp("example",
            clock_drift_interval=10,
            hmac_algorithm="HMacSHA256",
            otp_length=10,
            shared_secret_encoding="hexadecimal",
            time_step=30)
        ```

        :param str resource_name: The name of the resource.
        :param FactorTotpArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FactorTotpArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 clock_drift_interval: Optional[pulumi.Input[int]] = None,
                 hmac_algorithm: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 otp_length: Optional[pulumi.Input[int]] = None,
                 shared_secret_encoding: Optional[pulumi.Input[str]] = None,
                 time_step: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FactorTotpArgs.__new__(FactorTotpArgs)

            __props__.__dict__["clock_drift_interval"] = clock_drift_interval
            __props__.__dict__["hmac_algorithm"] = hmac_algorithm
            __props__.__dict__["name"] = name
            __props__.__dict__["otp_length"] = otp_length
            __props__.__dict__["shared_secret_encoding"] = shared_secret_encoding
            __props__.__dict__["time_step"] = time_step
        super(FactorTotp, __self__).__init__(
            'okta:index/factorTotp:FactorTotp',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            clock_drift_interval: Optional[pulumi.Input[int]] = None,
            hmac_algorithm: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            otp_length: Optional[pulumi.Input[int]] = None,
            shared_secret_encoding: Optional[pulumi.Input[str]] = None,
            time_step: Optional[pulumi.Input[int]] = None) -> 'FactorTotp':
        """
        Get an existing FactorTotp resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] clock_drift_interval: Clock drift interval. This setting allows you to build in tolerance for any
               drift between the token's current time and the server's current time. Valid values: `3`, `5`, `10`. Default is `3`.
        :param pulumi.Input[str] hmac_algorithm: HMAC Algorithm. Valid values: `"HMacSHA1"`, `"HMacSHA256"`, `"HMacSHA512"`. Default
               is `"HMacSHA512"`.
        :param pulumi.Input[str] name: The TOTP name.
        :param pulumi.Input[int] otp_length: Length of the password. Default is `6`.
        :param pulumi.Input[str] shared_secret_encoding: Shared secret encoding. Valid values: `"base32"`, `"base64"`, `"hexadecimal"`.
               Default is `"base32"`.
        :param pulumi.Input[int] time_step: Time step in seconds. Valid values: `15`, `30`, `60`. Default is `15`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FactorTotpState.__new__(_FactorTotpState)

        __props__.__dict__["clock_drift_interval"] = clock_drift_interval
        __props__.__dict__["hmac_algorithm"] = hmac_algorithm
        __props__.__dict__["name"] = name
        __props__.__dict__["otp_length"] = otp_length
        __props__.__dict__["shared_secret_encoding"] = shared_secret_encoding
        __props__.__dict__["time_step"] = time_step
        return FactorTotp(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clockDriftInterval")
    def clock_drift_interval(self) -> pulumi.Output[Optional[int]]:
        """
        Clock drift interval. This setting allows you to build in tolerance for any
        drift between the token's current time and the server's current time. Valid values: `3`, `5`, `10`. Default is `3`.
        """
        return pulumi.get(self, "clock_drift_interval")

    @property
    @pulumi.getter(name="hmacAlgorithm")
    def hmac_algorithm(self) -> pulumi.Output[Optional[str]]:
        """
        HMAC Algorithm. Valid values: `"HMacSHA1"`, `"HMacSHA256"`, `"HMacSHA512"`. Default
        is `"HMacSHA512"`.
        """
        return pulumi.get(self, "hmac_algorithm")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The TOTP name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="otpLength")
    def otp_length(self) -> pulumi.Output[Optional[int]]:
        """
        Length of the password. Default is `6`.
        """
        return pulumi.get(self, "otp_length")

    @property
    @pulumi.getter(name="sharedSecretEncoding")
    def shared_secret_encoding(self) -> pulumi.Output[Optional[str]]:
        """
        Shared secret encoding. Valid values: `"base32"`, `"base64"`, `"hexadecimal"`.
        Default is `"base32"`.
        """
        return pulumi.get(self, "shared_secret_encoding")

    @property
    @pulumi.getter(name="timeStep")
    def time_step(self) -> pulumi.Output[Optional[int]]:
        """
        Time step in seconds. Valid values: `15`, `30`, `60`. Default is `15`.
        """
        return pulumi.get(self, "time_step")

