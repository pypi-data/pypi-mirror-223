# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ServerArgs', 'Server']

@pulumi.input_type
class ServerArgs:
    def __init__(__self__, *,
                 audiences: pulumi.Input[Sequence[pulumi.Input[str]]],
                 credentials_rotation_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 issuer_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Server resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] audiences: The recipients that the tokens are intended for. This becomes the `aud` claim in an access token.
        :param pulumi.Input[str] credentials_rotation_mode: The key rotation mode for the authorization server. Can be `"AUTO"` or `"MANUAL"`.
        :param pulumi.Input[str] description: The description of the authorization server.
        :param pulumi.Input[str] issuer_mode: Allows you to use a custom issuer URL. It can be set to `"CUSTOM_URL"`,`"ORG_URL"` or `"DYNAMIC"`.
        :param pulumi.Input[str] name: The name of the authorization server.
        :param pulumi.Input[str] status: The status of the auth server. It defaults to `"ACTIVE"`
        """
        pulumi.set(__self__, "audiences", audiences)
        if credentials_rotation_mode is not None:
            pulumi.set(__self__, "credentials_rotation_mode", credentials_rotation_mode)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if issuer_mode is not None:
            pulumi.set(__self__, "issuer_mode", issuer_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def audiences(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The recipients that the tokens are intended for. This becomes the `aud` claim in an access token.
        """
        return pulumi.get(self, "audiences")

    @audiences.setter
    def audiences(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "audiences", value)

    @property
    @pulumi.getter(name="credentialsRotationMode")
    def credentials_rotation_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The key rotation mode for the authorization server. Can be `"AUTO"` or `"MANUAL"`.
        """
        return pulumi.get(self, "credentials_rotation_mode")

    @credentials_rotation_mode.setter
    def credentials_rotation_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "credentials_rotation_mode", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the authorization server.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="issuerMode")
    def issuer_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Allows you to use a custom issuer URL. It can be set to `"CUSTOM_URL"`,`"ORG_URL"` or `"DYNAMIC"`.
        """
        return pulumi.get(self, "issuer_mode")

    @issuer_mode.setter
    def issuer_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the authorization server.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the auth server. It defaults to `"ACTIVE"`
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _ServerState:
    def __init__(__self__, *,
                 audiences: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 credentials_last_rotated: Optional[pulumi.Input[str]] = None,
                 credentials_next_rotation: Optional[pulumi.Input[str]] = None,
                 credentials_rotation_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 issuer_mode: Optional[pulumi.Input[str]] = None,
                 kid: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Server resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] audiences: The recipients that the tokens are intended for. This becomes the `aud` claim in an access token.
        :param pulumi.Input[str] credentials_last_rotated: The timestamp when the authorization server started to use the `kid` for signing tokens.
        :param pulumi.Input[str] credentials_next_rotation: The timestamp when the authorization server changes the key for signing tokens. Only returned when `credentials_rotation_mode` is `"AUTO"`.
        :param pulumi.Input[str] credentials_rotation_mode: The key rotation mode for the authorization server. Can be `"AUTO"` or `"MANUAL"`.
        :param pulumi.Input[str] description: The description of the authorization server.
        :param pulumi.Input[str] issuer: The complete URL for a Custom Authorization Server. This becomes the `iss` claim in an access token.
        :param pulumi.Input[str] issuer_mode: Allows you to use a custom issuer URL. It can be set to `"CUSTOM_URL"`,`"ORG_URL"` or `"DYNAMIC"`.
        :param pulumi.Input[str] kid: The ID of the JSON Web Key used for signing tokens issued by the authorization server.
        :param pulumi.Input[str] name: The name of the authorization server.
        :param pulumi.Input[str] status: The status of the auth server. It defaults to `"ACTIVE"`
        """
        if audiences is not None:
            pulumi.set(__self__, "audiences", audiences)
        if credentials_last_rotated is not None:
            pulumi.set(__self__, "credentials_last_rotated", credentials_last_rotated)
        if credentials_next_rotation is not None:
            pulumi.set(__self__, "credentials_next_rotation", credentials_next_rotation)
        if credentials_rotation_mode is not None:
            pulumi.set(__self__, "credentials_rotation_mode", credentials_rotation_mode)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)
        if issuer_mode is not None:
            pulumi.set(__self__, "issuer_mode", issuer_mode)
        if kid is not None:
            pulumi.set(__self__, "kid", kid)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def audiences(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The recipients that the tokens are intended for. This becomes the `aud` claim in an access token.
        """
        return pulumi.get(self, "audiences")

    @audiences.setter
    def audiences(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "audiences", value)

    @property
    @pulumi.getter(name="credentialsLastRotated")
    def credentials_last_rotated(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp when the authorization server started to use the `kid` for signing tokens.
        """
        return pulumi.get(self, "credentials_last_rotated")

    @credentials_last_rotated.setter
    def credentials_last_rotated(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "credentials_last_rotated", value)

    @property
    @pulumi.getter(name="credentialsNextRotation")
    def credentials_next_rotation(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp when the authorization server changes the key for signing tokens. Only returned when `credentials_rotation_mode` is `"AUTO"`.
        """
        return pulumi.get(self, "credentials_next_rotation")

    @credentials_next_rotation.setter
    def credentials_next_rotation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "credentials_next_rotation", value)

    @property
    @pulumi.getter(name="credentialsRotationMode")
    def credentials_rotation_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The key rotation mode for the authorization server. Can be `"AUTO"` or `"MANUAL"`.
        """
        return pulumi.get(self, "credentials_rotation_mode")

    @credentials_rotation_mode.setter
    def credentials_rotation_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "credentials_rotation_mode", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the authorization server.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def issuer(self) -> Optional[pulumi.Input[str]]:
        """
        The complete URL for a Custom Authorization Server. This becomes the `iss` claim in an access token.
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer", value)

    @property
    @pulumi.getter(name="issuerMode")
    def issuer_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Allows you to use a custom issuer URL. It can be set to `"CUSTOM_URL"`,`"ORG_URL"` or `"DYNAMIC"`.
        """
        return pulumi.get(self, "issuer_mode")

    @issuer_mode.setter
    def issuer_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer_mode", value)

    @property
    @pulumi.getter
    def kid(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the JSON Web Key used for signing tokens issued by the authorization server.
        """
        return pulumi.get(self, "kid")

    @kid.setter
    def kid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kid", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the authorization server.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the auth server. It defaults to `"ACTIVE"`
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class Server(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audiences: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 credentials_rotation_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 issuer_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates an Authorization Server.

        This resource allows you to create and configure an Authorization Server.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.auth.Server("example",
            audiences=["api://example"],
            description="My Example Auth Server",
            issuer_mode="CUSTOM_URL",
            status="ACTIVE")
        ```

        ## Import

        Authorization Server can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:auth/server:Server example &#60;auth server id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] audiences: The recipients that the tokens are intended for. This becomes the `aud` claim in an access token.
        :param pulumi.Input[str] credentials_rotation_mode: The key rotation mode for the authorization server. Can be `"AUTO"` or `"MANUAL"`.
        :param pulumi.Input[str] description: The description of the authorization server.
        :param pulumi.Input[str] issuer_mode: Allows you to use a custom issuer URL. It can be set to `"CUSTOM_URL"`,`"ORG_URL"` or `"DYNAMIC"`.
        :param pulumi.Input[str] name: The name of the authorization server.
        :param pulumi.Input[str] status: The status of the auth server. It defaults to `"ACTIVE"`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates an Authorization Server.

        This resource allows you to create and configure an Authorization Server.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.auth.Server("example",
            audiences=["api://example"],
            description="My Example Auth Server",
            issuer_mode="CUSTOM_URL",
            status="ACTIVE")
        ```

        ## Import

        Authorization Server can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:auth/server:Server example &#60;auth server id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param ServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audiences: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 credentials_rotation_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 issuer_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServerArgs.__new__(ServerArgs)

            if audiences is None and not opts.urn:
                raise TypeError("Missing required property 'audiences'")
            __props__.__dict__["audiences"] = audiences
            __props__.__dict__["credentials_rotation_mode"] = credentials_rotation_mode
            __props__.__dict__["description"] = description
            __props__.__dict__["issuer_mode"] = issuer_mode
            __props__.__dict__["name"] = name
            __props__.__dict__["status"] = status
            __props__.__dict__["credentials_last_rotated"] = None
            __props__.__dict__["credentials_next_rotation"] = None
            __props__.__dict__["issuer"] = None
            __props__.__dict__["kid"] = None
        super(Server, __self__).__init__(
            'okta:auth/server:Server',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            audiences: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            credentials_last_rotated: Optional[pulumi.Input[str]] = None,
            credentials_next_rotation: Optional[pulumi.Input[str]] = None,
            credentials_rotation_mode: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            issuer: Optional[pulumi.Input[str]] = None,
            issuer_mode: Optional[pulumi.Input[str]] = None,
            kid: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'Server':
        """
        Get an existing Server resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] audiences: The recipients that the tokens are intended for. This becomes the `aud` claim in an access token.
        :param pulumi.Input[str] credentials_last_rotated: The timestamp when the authorization server started to use the `kid` for signing tokens.
        :param pulumi.Input[str] credentials_next_rotation: The timestamp when the authorization server changes the key for signing tokens. Only returned when `credentials_rotation_mode` is `"AUTO"`.
        :param pulumi.Input[str] credentials_rotation_mode: The key rotation mode for the authorization server. Can be `"AUTO"` or `"MANUAL"`.
        :param pulumi.Input[str] description: The description of the authorization server.
        :param pulumi.Input[str] issuer: The complete URL for a Custom Authorization Server. This becomes the `iss` claim in an access token.
        :param pulumi.Input[str] issuer_mode: Allows you to use a custom issuer URL. It can be set to `"CUSTOM_URL"`,`"ORG_URL"` or `"DYNAMIC"`.
        :param pulumi.Input[str] kid: The ID of the JSON Web Key used for signing tokens issued by the authorization server.
        :param pulumi.Input[str] name: The name of the authorization server.
        :param pulumi.Input[str] status: The status of the auth server. It defaults to `"ACTIVE"`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServerState.__new__(_ServerState)

        __props__.__dict__["audiences"] = audiences
        __props__.__dict__["credentials_last_rotated"] = credentials_last_rotated
        __props__.__dict__["credentials_next_rotation"] = credentials_next_rotation
        __props__.__dict__["credentials_rotation_mode"] = credentials_rotation_mode
        __props__.__dict__["description"] = description
        __props__.__dict__["issuer"] = issuer
        __props__.__dict__["issuer_mode"] = issuer_mode
        __props__.__dict__["kid"] = kid
        __props__.__dict__["name"] = name
        __props__.__dict__["status"] = status
        return Server(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def audiences(self) -> pulumi.Output[Sequence[str]]:
        """
        The recipients that the tokens are intended for. This becomes the `aud` claim in an access token.
        """
        return pulumi.get(self, "audiences")

    @property
    @pulumi.getter(name="credentialsLastRotated")
    def credentials_last_rotated(self) -> pulumi.Output[str]:
        """
        The timestamp when the authorization server started to use the `kid` for signing tokens.
        """
        return pulumi.get(self, "credentials_last_rotated")

    @property
    @pulumi.getter(name="credentialsNextRotation")
    def credentials_next_rotation(self) -> pulumi.Output[str]:
        """
        The timestamp when the authorization server changes the key for signing tokens. Only returned when `credentials_rotation_mode` is `"AUTO"`.
        """
        return pulumi.get(self, "credentials_next_rotation")

    @property
    @pulumi.getter(name="credentialsRotationMode")
    def credentials_rotation_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The key rotation mode for the authorization server. Can be `"AUTO"` or `"MANUAL"`.
        """
        return pulumi.get(self, "credentials_rotation_mode")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the authorization server.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def issuer(self) -> pulumi.Output[str]:
        """
        The complete URL for a Custom Authorization Server. This becomes the `iss` claim in an access token.
        """
        return pulumi.get(self, "issuer")

    @property
    @pulumi.getter(name="issuerMode")
    def issuer_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Allows you to use a custom issuer URL. It can be set to `"CUSTOM_URL"`,`"ORG_URL"` or `"DYNAMIC"`.
        """
        return pulumi.get(self, "issuer_mode")

    @property
    @pulumi.getter
    def kid(self) -> pulumi.Output[str]:
        """
        The ID of the JSON Web Key used for signing tokens issued by the authorization server.
        """
        return pulumi.get(self, "kid")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the authorization server.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        The status of the auth server. It defaults to `"ACTIVE"`
        """
        return pulumi.get(self, "status")

