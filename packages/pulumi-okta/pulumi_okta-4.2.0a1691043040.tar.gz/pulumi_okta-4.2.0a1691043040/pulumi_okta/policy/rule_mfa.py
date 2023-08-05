# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['RuleMfaArgs', 'RuleMfa']

@pulumi.input_type
class RuleMfaArgs:
    def __init__(__self__, *,
                 app_excludes: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]]] = None,
                 app_includes: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]]] = None,
                 enroll: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_connection: Optional[pulumi.Input[str]] = None,
                 network_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network_includes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 users_excludeds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a RuleMfa resource.
        :param pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]] app_excludes: Applications to exclude
        :param pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]] app_includes: Applications to include in discovery rule. **IMPORTANT**: this field is only available in Classic Organizations.
        :param pulumi.Input[str] enroll: When a user should be prompted for MFA. It can be `"CHALLENGE"`, `"LOGIN"`, or `"NEVER"`.
        :param pulumi.Input[str] name: Use if the `type` is `"APP_TYPE"` to indicate the type of application(s) to include in instances where an entire group (i.e. `yahoo_mail`) of applications should be included.
        :param pulumi.Input[str] network_connection: Network selection mode: `"ANYWHERE"`, `"ZONE"`, `"ON_NETWORK"`, or `"OFF_NETWORK"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_excludes: The network zones to exclude. Conflicts with `network_includes`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_includes: The network zones to include. Conflicts with `network_excludes`.
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[int] priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.
        :param pulumi.Input[str] status: Policy Rule Status: `"ACTIVE"` or `"INACTIVE"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users_excludeds: Set of User IDs to Exclude
        """
        if app_excludes is not None:
            pulumi.set(__self__, "app_excludes", app_excludes)
        if app_includes is not None:
            pulumi.set(__self__, "app_includes", app_includes)
        if enroll is not None:
            pulumi.set(__self__, "enroll", enroll)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network_connection is not None:
            pulumi.set(__self__, "network_connection", network_connection)
        if network_excludes is not None:
            pulumi.set(__self__, "network_excludes", network_excludes)
        if network_includes is not None:
            pulumi.set(__self__, "network_includes", network_includes)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if users_excludeds is not None:
            pulumi.set(__self__, "users_excludeds", users_excludeds)

    @property
    @pulumi.getter(name="appExcludes")
    def app_excludes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]]]:
        """
        Applications to exclude
        """
        return pulumi.get(self, "app_excludes")

    @app_excludes.setter
    def app_excludes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]]]):
        pulumi.set(self, "app_excludes", value)

    @property
    @pulumi.getter(name="appIncludes")
    def app_includes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]]]:
        """
        Applications to include in discovery rule. **IMPORTANT**: this field is only available in Classic Organizations.
        """
        return pulumi.get(self, "app_includes")

    @app_includes.setter
    def app_includes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]]]):
        pulumi.set(self, "app_includes", value)

    @property
    @pulumi.getter
    def enroll(self) -> Optional[pulumi.Input[str]]:
        """
        When a user should be prompted for MFA. It can be `"CHALLENGE"`, `"LOGIN"`, or `"NEVER"`.
        """
        return pulumi.get(self, "enroll")

    @enroll.setter
    def enroll(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enroll", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Use if the `type` is `"APP_TYPE"` to indicate the type of application(s) to include in instances where an entire group (i.e. `yahoo_mail`) of applications should be included.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="networkConnection")
    def network_connection(self) -> Optional[pulumi.Input[str]]:
        """
        Network selection mode: `"ANYWHERE"`, `"ZONE"`, `"ON_NETWORK"`, or `"OFF_NETWORK"`.
        """
        return pulumi.get(self, "network_connection")

    @network_connection.setter
    def network_connection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_connection", value)

    @property
    @pulumi.getter(name="networkExcludes")
    def network_excludes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The network zones to exclude. Conflicts with `network_includes`.
        """
        return pulumi.get(self, "network_excludes")

    @network_excludes.setter
    def network_excludes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "network_excludes", value)

    @property
    @pulumi.getter(name="networkIncludes")
    def network_includes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The network zones to include. Conflicts with `network_excludes`.
        """
        return pulumi.get(self, "network_includes")

    @network_includes.setter
    def network_includes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "network_includes", value)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        Policy ID.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Policy Rule Status: `"ACTIVE"` or `"INACTIVE"`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="usersExcludeds")
    def users_excludeds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of User IDs to Exclude
        """
        return pulumi.get(self, "users_excludeds")

    @users_excludeds.setter
    def users_excludeds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "users_excludeds", value)


@pulumi.input_type
class _RuleMfaState:
    def __init__(__self__, *,
                 app_excludes: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]]] = None,
                 app_includes: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]]] = None,
                 enroll: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_connection: Optional[pulumi.Input[str]] = None,
                 network_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network_includes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 users_excludeds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering RuleMfa resources.
        :param pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]] app_excludes: Applications to exclude
        :param pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]] app_includes: Applications to include in discovery rule. **IMPORTANT**: this field is only available in Classic Organizations.
        :param pulumi.Input[str] enroll: When a user should be prompted for MFA. It can be `"CHALLENGE"`, `"LOGIN"`, or `"NEVER"`.
        :param pulumi.Input[str] name: Use if the `type` is `"APP_TYPE"` to indicate the type of application(s) to include in instances where an entire group (i.e. `yahoo_mail`) of applications should be included.
        :param pulumi.Input[str] network_connection: Network selection mode: `"ANYWHERE"`, `"ZONE"`, `"ON_NETWORK"`, or `"OFF_NETWORK"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_excludes: The network zones to exclude. Conflicts with `network_includes`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_includes: The network zones to include. Conflicts with `network_excludes`.
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[int] priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.
        :param pulumi.Input[str] status: Policy Rule Status: `"ACTIVE"` or `"INACTIVE"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users_excludeds: Set of User IDs to Exclude
        """
        if app_excludes is not None:
            pulumi.set(__self__, "app_excludes", app_excludes)
        if app_includes is not None:
            pulumi.set(__self__, "app_includes", app_includes)
        if enroll is not None:
            pulumi.set(__self__, "enroll", enroll)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network_connection is not None:
            pulumi.set(__self__, "network_connection", network_connection)
        if network_excludes is not None:
            pulumi.set(__self__, "network_excludes", network_excludes)
        if network_includes is not None:
            pulumi.set(__self__, "network_includes", network_includes)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if users_excludeds is not None:
            pulumi.set(__self__, "users_excludeds", users_excludeds)

    @property
    @pulumi.getter(name="appExcludes")
    def app_excludes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]]]:
        """
        Applications to exclude
        """
        return pulumi.get(self, "app_excludes")

    @app_excludes.setter
    def app_excludes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppExcludeArgs']]]]):
        pulumi.set(self, "app_excludes", value)

    @property
    @pulumi.getter(name="appIncludes")
    def app_includes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]]]:
        """
        Applications to include in discovery rule. **IMPORTANT**: this field is only available in Classic Organizations.
        """
        return pulumi.get(self, "app_includes")

    @app_includes.setter
    def app_includes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleMfaAppIncludeArgs']]]]):
        pulumi.set(self, "app_includes", value)

    @property
    @pulumi.getter
    def enroll(self) -> Optional[pulumi.Input[str]]:
        """
        When a user should be prompted for MFA. It can be `"CHALLENGE"`, `"LOGIN"`, or `"NEVER"`.
        """
        return pulumi.get(self, "enroll")

    @enroll.setter
    def enroll(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enroll", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Use if the `type` is `"APP_TYPE"` to indicate the type of application(s) to include in instances where an entire group (i.e. `yahoo_mail`) of applications should be included.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="networkConnection")
    def network_connection(self) -> Optional[pulumi.Input[str]]:
        """
        Network selection mode: `"ANYWHERE"`, `"ZONE"`, `"ON_NETWORK"`, or `"OFF_NETWORK"`.
        """
        return pulumi.get(self, "network_connection")

    @network_connection.setter
    def network_connection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_connection", value)

    @property
    @pulumi.getter(name="networkExcludes")
    def network_excludes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The network zones to exclude. Conflicts with `network_includes`.
        """
        return pulumi.get(self, "network_excludes")

    @network_excludes.setter
    def network_excludes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "network_excludes", value)

    @property
    @pulumi.getter(name="networkIncludes")
    def network_includes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The network zones to include. Conflicts with `network_excludes`.
        """
        return pulumi.get(self, "network_includes")

    @network_includes.setter
    def network_includes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "network_includes", value)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        Policy ID.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Policy Rule Status: `"ACTIVE"` or `"INACTIVE"`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="usersExcludeds")
    def users_excludeds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of User IDs to Exclude
        """
        return pulumi.get(self, "users_excludeds")

    @users_excludeds.setter
    def users_excludeds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "users_excludeds", value)


class RuleMfa(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppExcludeArgs']]]]] = None,
                 app_includes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppIncludeArgs']]]]] = None,
                 enroll: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_connection: Optional[pulumi.Input[str]] = None,
                 network_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network_includes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 users_excludeds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        This resource allows you to create and configure an MFA Policy Rule.

        ## Import

        A Policy Rule can be imported via the Policy and Rule ID.

        ```sh
         $ pulumi import okta:policy/ruleMfa:RuleMfa example &#60;policy id&#62;/&#60;rule id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppExcludeArgs']]]] app_excludes: Applications to exclude
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppIncludeArgs']]]] app_includes: Applications to include in discovery rule. **IMPORTANT**: this field is only available in Classic Organizations.
        :param pulumi.Input[str] enroll: When a user should be prompted for MFA. It can be `"CHALLENGE"`, `"LOGIN"`, or `"NEVER"`.
        :param pulumi.Input[str] name: Use if the `type` is `"APP_TYPE"` to indicate the type of application(s) to include in instances where an entire group (i.e. `yahoo_mail`) of applications should be included.
        :param pulumi.Input[str] network_connection: Network selection mode: `"ANYWHERE"`, `"ZONE"`, `"ON_NETWORK"`, or `"OFF_NETWORK"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_excludes: The network zones to exclude. Conflicts with `network_includes`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_includes: The network zones to include. Conflicts with `network_excludes`.
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[int] priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.
        :param pulumi.Input[str] status: Policy Rule Status: `"ACTIVE"` or `"INACTIVE"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users_excludeds: Set of User IDs to Exclude
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[RuleMfaArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows you to create and configure an MFA Policy Rule.

        ## Import

        A Policy Rule can be imported via the Policy and Rule ID.

        ```sh
         $ pulumi import okta:policy/ruleMfa:RuleMfa example &#60;policy id&#62;/&#60;rule id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param RuleMfaArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RuleMfaArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppExcludeArgs']]]]] = None,
                 app_includes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppIncludeArgs']]]]] = None,
                 enroll: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_connection: Optional[pulumi.Input[str]] = None,
                 network_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network_includes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 users_excludeds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RuleMfaArgs.__new__(RuleMfaArgs)

            __props__.__dict__["app_excludes"] = app_excludes
            __props__.__dict__["app_includes"] = app_includes
            __props__.__dict__["enroll"] = enroll
            __props__.__dict__["name"] = name
            __props__.__dict__["network_connection"] = network_connection
            __props__.__dict__["network_excludes"] = network_excludes
            __props__.__dict__["network_includes"] = network_includes
            __props__.__dict__["policy_id"] = policy_id
            __props__.__dict__["priority"] = priority
            __props__.__dict__["status"] = status
            __props__.__dict__["users_excludeds"] = users_excludeds
        super(RuleMfa, __self__).__init__(
            'okta:policy/ruleMfa:RuleMfa',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            app_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppExcludeArgs']]]]] = None,
            app_includes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppIncludeArgs']]]]] = None,
            enroll: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network_connection: Optional[pulumi.Input[str]] = None,
            network_excludes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            network_includes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            policy_id: Optional[pulumi.Input[str]] = None,
            priority: Optional[pulumi.Input[int]] = None,
            status: Optional[pulumi.Input[str]] = None,
            users_excludeds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'RuleMfa':
        """
        Get an existing RuleMfa resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppExcludeArgs']]]] app_excludes: Applications to exclude
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleMfaAppIncludeArgs']]]] app_includes: Applications to include in discovery rule. **IMPORTANT**: this field is only available in Classic Organizations.
        :param pulumi.Input[str] enroll: When a user should be prompted for MFA. It can be `"CHALLENGE"`, `"LOGIN"`, or `"NEVER"`.
        :param pulumi.Input[str] name: Use if the `type` is `"APP_TYPE"` to indicate the type of application(s) to include in instances where an entire group (i.e. `yahoo_mail`) of applications should be included.
        :param pulumi.Input[str] network_connection: Network selection mode: `"ANYWHERE"`, `"ZONE"`, `"ON_NETWORK"`, or `"OFF_NETWORK"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_excludes: The network zones to exclude. Conflicts with `network_includes`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_includes: The network zones to include. Conflicts with `network_excludes`.
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[int] priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.
        :param pulumi.Input[str] status: Policy Rule Status: `"ACTIVE"` or `"INACTIVE"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users_excludeds: Set of User IDs to Exclude
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RuleMfaState.__new__(_RuleMfaState)

        __props__.__dict__["app_excludes"] = app_excludes
        __props__.__dict__["app_includes"] = app_includes
        __props__.__dict__["enroll"] = enroll
        __props__.__dict__["name"] = name
        __props__.__dict__["network_connection"] = network_connection
        __props__.__dict__["network_excludes"] = network_excludes
        __props__.__dict__["network_includes"] = network_includes
        __props__.__dict__["policy_id"] = policy_id
        __props__.__dict__["priority"] = priority
        __props__.__dict__["status"] = status
        __props__.__dict__["users_excludeds"] = users_excludeds
        return RuleMfa(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appExcludes")
    def app_excludes(self) -> pulumi.Output[Optional[Sequence['outputs.RuleMfaAppExclude']]]:
        """
        Applications to exclude
        """
        return pulumi.get(self, "app_excludes")

    @property
    @pulumi.getter(name="appIncludes")
    def app_includes(self) -> pulumi.Output[Optional[Sequence['outputs.RuleMfaAppInclude']]]:
        """
        Applications to include in discovery rule. **IMPORTANT**: this field is only available in Classic Organizations.
        """
        return pulumi.get(self, "app_includes")

    @property
    @pulumi.getter
    def enroll(self) -> pulumi.Output[Optional[str]]:
        """
        When a user should be prompted for MFA. It can be `"CHALLENGE"`, `"LOGIN"`, or `"NEVER"`.
        """
        return pulumi.get(self, "enroll")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Use if the `type` is `"APP_TYPE"` to indicate the type of application(s) to include in instances where an entire group (i.e. `yahoo_mail`) of applications should be included.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkConnection")
    def network_connection(self) -> pulumi.Output[Optional[str]]:
        """
        Network selection mode: `"ANYWHERE"`, `"ZONE"`, `"ON_NETWORK"`, or `"OFF_NETWORK"`.
        """
        return pulumi.get(self, "network_connection")

    @property
    @pulumi.getter(name="networkExcludes")
    def network_excludes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The network zones to exclude. Conflicts with `network_includes`.
        """
        return pulumi.get(self, "network_excludes")

    @property
    @pulumi.getter(name="networkIncludes")
    def network_includes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The network zones to include. Conflicts with `network_excludes`.
        """
        return pulumi.get(self, "network_includes")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Output[Optional[str]]:
        """
        Policy ID.
        """
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[int]]:
        """
        Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Policy Rule Status: `"ACTIVE"` or `"INACTIVE"`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="usersExcludeds")
    def users_excludeds(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Set of User IDs to Exclude
        """
        return pulumi.get(self, "users_excludeds")

