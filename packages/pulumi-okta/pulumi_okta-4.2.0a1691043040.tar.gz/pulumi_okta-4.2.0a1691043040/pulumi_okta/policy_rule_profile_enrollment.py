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

__all__ = ['PolicyRuleProfileEnrollmentArgs', 'PolicyRuleProfileEnrollment']

@pulumi.input_type
class PolicyRuleProfileEnrollmentArgs:
    def __init__(__self__, *,
                 policy_id: pulumi.Input[str],
                 unknown_user_action: pulumi.Input[str],
                 access: Optional[pulumi.Input[str]] = None,
                 email_verification: Optional[pulumi.Input[bool]] = None,
                 inline_hook_id: Optional[pulumi.Input[str]] = None,
                 profile_attributes: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]] = None,
                 target_group_id: Optional[pulumi.Input[str]] = None,
                 ui_schema_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PolicyRuleProfileEnrollment resource.
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[str] unknown_user_action: Which action should be taken if this User is new. Valid values are: `"DENY"`, `"REGISTER"`.
        :param pulumi.Input[str] access: Allow or deny access based on the rule conditions. Valid values are: `"ALLOW"`, `"DENY"`. Default is `"ALLOW"`.
        :param pulumi.Input[bool] email_verification: Indicates whether email verification should occur before access is granted. Default is `true`.
        :param pulumi.Input[str] inline_hook_id: ID of a Registration Inline Hook.
        :param pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]] profile_attributes: A list of attributes to prompt the user during registration or progressive profiling. Where defined on the User schema, these attributes are persisted in the User profile. Non-schema attributes may also be added, which aren't persisted to the User's profile, but are included in requests to the registration inline hook. A maximum of 10 Profile properties is supported.
        :param pulumi.Input[str] target_group_id: The ID of a Group that this User should be added to.
        :param pulumi.Input[str] ui_schema_id: Value created by the backend. If present all policy updates must include this attribute/value.
        """
        pulumi.set(__self__, "policy_id", policy_id)
        pulumi.set(__self__, "unknown_user_action", unknown_user_action)
        if access is not None:
            pulumi.set(__self__, "access", access)
        if email_verification is not None:
            pulumi.set(__self__, "email_verification", email_verification)
        if inline_hook_id is not None:
            pulumi.set(__self__, "inline_hook_id", inline_hook_id)
        if profile_attributes is not None:
            pulumi.set(__self__, "profile_attributes", profile_attributes)
        if target_group_id is not None:
            pulumi.set(__self__, "target_group_id", target_group_id)
        if ui_schema_id is not None:
            pulumi.set(__self__, "ui_schema_id", ui_schema_id)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Input[str]:
        """
        Policy ID.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter(name="unknownUserAction")
    def unknown_user_action(self) -> pulumi.Input[str]:
        """
        Which action should be taken if this User is new. Valid values are: `"DENY"`, `"REGISTER"`.
        """
        return pulumi.get(self, "unknown_user_action")

    @unknown_user_action.setter
    def unknown_user_action(self, value: pulumi.Input[str]):
        pulumi.set(self, "unknown_user_action", value)

    @property
    @pulumi.getter
    def access(self) -> Optional[pulumi.Input[str]]:
        """
        Allow or deny access based on the rule conditions. Valid values are: `"ALLOW"`, `"DENY"`. Default is `"ALLOW"`.
        """
        return pulumi.get(self, "access")

    @access.setter
    def access(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access", value)

    @property
    @pulumi.getter(name="emailVerification")
    def email_verification(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether email verification should occur before access is granted. Default is `true`.
        """
        return pulumi.get(self, "email_verification")

    @email_verification.setter
    def email_verification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "email_verification", value)

    @property
    @pulumi.getter(name="inlineHookId")
    def inline_hook_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of a Registration Inline Hook.
        """
        return pulumi.get(self, "inline_hook_id")

    @inline_hook_id.setter
    def inline_hook_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "inline_hook_id", value)

    @property
    @pulumi.getter(name="profileAttributes")
    def profile_attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]]:
        """
        A list of attributes to prompt the user during registration or progressive profiling. Where defined on the User schema, these attributes are persisted in the User profile. Non-schema attributes may also be added, which aren't persisted to the User's profile, but are included in requests to the registration inline hook. A maximum of 10 Profile properties is supported.
        """
        return pulumi.get(self, "profile_attributes")

    @profile_attributes.setter
    def profile_attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]]):
        pulumi.set(self, "profile_attributes", value)

    @property
    @pulumi.getter(name="targetGroupId")
    def target_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a Group that this User should be added to.
        """
        return pulumi.get(self, "target_group_id")

    @target_group_id.setter
    def target_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_group_id", value)

    @property
    @pulumi.getter(name="uiSchemaId")
    def ui_schema_id(self) -> Optional[pulumi.Input[str]]:
        """
        Value created by the backend. If present all policy updates must include this attribute/value.
        """
        return pulumi.get(self, "ui_schema_id")

    @ui_schema_id.setter
    def ui_schema_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ui_schema_id", value)


@pulumi.input_type
class _PolicyRuleProfileEnrollmentState:
    def __init__(__self__, *,
                 access: Optional[pulumi.Input[str]] = None,
                 email_verification: Optional[pulumi.Input[bool]] = None,
                 inline_hook_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 profile_attributes: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 target_group_id: Optional[pulumi.Input[str]] = None,
                 ui_schema_id: Optional[pulumi.Input[str]] = None,
                 unknown_user_action: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PolicyRuleProfileEnrollment resources.
        :param pulumi.Input[str] access: Allow or deny access based on the rule conditions. Valid values are: `"ALLOW"`, `"DENY"`. Default is `"ALLOW"`.
        :param pulumi.Input[bool] email_verification: Indicates whether email verification should occur before access is granted. Default is `true`.
        :param pulumi.Input[str] inline_hook_id: ID of a Registration Inline Hook.
        :param pulumi.Input[str] name: The name of a User Profile property
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]] profile_attributes: A list of attributes to prompt the user during registration or progressive profiling. Where defined on the User schema, these attributes are persisted in the User profile. Non-schema attributes may also be added, which aren't persisted to the User's profile, but are included in requests to the registration inline hook. A maximum of 10 Profile properties is supported.
        :param pulumi.Input[str] status: Status of the Rule.
        :param pulumi.Input[str] target_group_id: The ID of a Group that this User should be added to.
        :param pulumi.Input[str] ui_schema_id: Value created by the backend. If present all policy updates must include this attribute/value.
        :param pulumi.Input[str] unknown_user_action: Which action should be taken if this User is new. Valid values are: `"DENY"`, `"REGISTER"`.
        """
        if access is not None:
            pulumi.set(__self__, "access", access)
        if email_verification is not None:
            pulumi.set(__self__, "email_verification", email_verification)
        if inline_hook_id is not None:
            pulumi.set(__self__, "inline_hook_id", inline_hook_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)
        if profile_attributes is not None:
            pulumi.set(__self__, "profile_attributes", profile_attributes)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if target_group_id is not None:
            pulumi.set(__self__, "target_group_id", target_group_id)
        if ui_schema_id is not None:
            pulumi.set(__self__, "ui_schema_id", ui_schema_id)
        if unknown_user_action is not None:
            pulumi.set(__self__, "unknown_user_action", unknown_user_action)

    @property
    @pulumi.getter
    def access(self) -> Optional[pulumi.Input[str]]:
        """
        Allow or deny access based on the rule conditions. Valid values are: `"ALLOW"`, `"DENY"`. Default is `"ALLOW"`.
        """
        return pulumi.get(self, "access")

    @access.setter
    def access(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access", value)

    @property
    @pulumi.getter(name="emailVerification")
    def email_verification(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether email verification should occur before access is granted. Default is `true`.
        """
        return pulumi.get(self, "email_verification")

    @email_verification.setter
    def email_verification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "email_verification", value)

    @property
    @pulumi.getter(name="inlineHookId")
    def inline_hook_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of a Registration Inline Hook.
        """
        return pulumi.get(self, "inline_hook_id")

    @inline_hook_id.setter
    def inline_hook_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "inline_hook_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of a User Profile property
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

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
    @pulumi.getter(name="profileAttributes")
    def profile_attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]]:
        """
        A list of attributes to prompt the user during registration or progressive profiling. Where defined on the User schema, these attributes are persisted in the User profile. Non-schema attributes may also be added, which aren't persisted to the User's profile, but are included in requests to the registration inline hook. A maximum of 10 Profile properties is supported.
        """
        return pulumi.get(self, "profile_attributes")

    @profile_attributes.setter
    def profile_attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]]):
        pulumi.set(self, "profile_attributes", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of the Rule.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="targetGroupId")
    def target_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a Group that this User should be added to.
        """
        return pulumi.get(self, "target_group_id")

    @target_group_id.setter
    def target_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_group_id", value)

    @property
    @pulumi.getter(name="uiSchemaId")
    def ui_schema_id(self) -> Optional[pulumi.Input[str]]:
        """
        Value created by the backend. If present all policy updates must include this attribute/value.
        """
        return pulumi.get(self, "ui_schema_id")

    @ui_schema_id.setter
    def ui_schema_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ui_schema_id", value)

    @property
    @pulumi.getter(name="unknownUserAction")
    def unknown_user_action(self) -> Optional[pulumi.Input[str]]:
        """
        Which action should be taken if this User is new. Valid values are: `"DENY"`, `"REGISTER"`.
        """
        return pulumi.get(self, "unknown_user_action")

    @unknown_user_action.setter
    def unknown_user_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unknown_user_action", value)


class PolicyRuleProfileEnrollment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access: Optional[pulumi.Input[str]] = None,
                 email_verification: Optional[pulumi.Input[bool]] = None,
                 inline_hook_id: Optional[pulumi.Input[str]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 profile_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]]] = None,
                 target_group_id: Optional[pulumi.Input[str]] = None,
                 ui_schema_id: Optional[pulumi.Input[str]] = None,
                 unknown_user_action: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        > **WARNING:** This feature is only available as a part of the Identity Engine. Contact support for further information.

        A [profile enrollment
        policy](https://developer.okta.com/docs/reference/api/policy/#profile-enrollment-policy)
        is limited to one default rule. This resource does not create a rule for an
        enrollment policy, it allows the default policy rule to be updated.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example_policy_profile_enrollment = okta.PolicyProfileEnrollment("examplePolicyProfileEnrollment")
        example_hook = okta.inline.Hook("exampleHook",
            status="ACTIVE",
            type="com.okta.user.pre-registration",
            version="1.0.3",
            channel={
                "type": "HTTP",
                "version": "1.0.0",
                "uri": "https://example.com/test2",
                "method": "POST",
            })
        example_group = okta.group.Group("exampleGroup", description="Group of some users")
        example_policy_rule_profile_enrollment = okta.PolicyRuleProfileEnrollment("examplePolicyRuleProfileEnrollment",
            policy_id=example_policy_profile_enrollment.id,
            inline_hook_id=example_hook.id,
            target_group_id=example_group.id,
            unknown_user_action="REGISTER",
            email_verification=True,
            access="ALLOW",
            profile_attributes=[
                okta.PolicyRuleProfileEnrollmentProfileAttributeArgs(
                    name="email",
                    label="Email",
                    required=True,
                ),
                okta.PolicyRuleProfileEnrollmentProfileAttributeArgs(
                    name="name",
                    label="Name",
                    required=True,
                ),
                okta.PolicyRuleProfileEnrollmentProfileAttributeArgs(
                    name="t-shirt",
                    label="T-Shirt Size",
                    required=False,
                ),
            ])
        ```

        ## Import

        A Policy Rule can be imported via the Policy and Rule ID.

        ```sh
         $ pulumi import okta:index/policyRuleProfileEnrollment:PolicyRuleProfileEnrollment example &#60;policy id&#62;/&#60;rule id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access: Allow or deny access based on the rule conditions. Valid values are: `"ALLOW"`, `"DENY"`. Default is `"ALLOW"`.
        :param pulumi.Input[bool] email_verification: Indicates whether email verification should occur before access is granted. Default is `true`.
        :param pulumi.Input[str] inline_hook_id: ID of a Registration Inline Hook.
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]] profile_attributes: A list of attributes to prompt the user during registration or progressive profiling. Where defined on the User schema, these attributes are persisted in the User profile. Non-schema attributes may also be added, which aren't persisted to the User's profile, but are included in requests to the registration inline hook. A maximum of 10 Profile properties is supported.
        :param pulumi.Input[str] target_group_id: The ID of a Group that this User should be added to.
        :param pulumi.Input[str] ui_schema_id: Value created by the backend. If present all policy updates must include this attribute/value.
        :param pulumi.Input[str] unknown_user_action: Which action should be taken if this User is new. Valid values are: `"DENY"`, `"REGISTER"`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PolicyRuleProfileEnrollmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > **WARNING:** This feature is only available as a part of the Identity Engine. Contact support for further information.

        A [profile enrollment
        policy](https://developer.okta.com/docs/reference/api/policy/#profile-enrollment-policy)
        is limited to one default rule. This resource does not create a rule for an
        enrollment policy, it allows the default policy rule to be updated.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example_policy_profile_enrollment = okta.PolicyProfileEnrollment("examplePolicyProfileEnrollment")
        example_hook = okta.inline.Hook("exampleHook",
            status="ACTIVE",
            type="com.okta.user.pre-registration",
            version="1.0.3",
            channel={
                "type": "HTTP",
                "version": "1.0.0",
                "uri": "https://example.com/test2",
                "method": "POST",
            })
        example_group = okta.group.Group("exampleGroup", description="Group of some users")
        example_policy_rule_profile_enrollment = okta.PolicyRuleProfileEnrollment("examplePolicyRuleProfileEnrollment",
            policy_id=example_policy_profile_enrollment.id,
            inline_hook_id=example_hook.id,
            target_group_id=example_group.id,
            unknown_user_action="REGISTER",
            email_verification=True,
            access="ALLOW",
            profile_attributes=[
                okta.PolicyRuleProfileEnrollmentProfileAttributeArgs(
                    name="email",
                    label="Email",
                    required=True,
                ),
                okta.PolicyRuleProfileEnrollmentProfileAttributeArgs(
                    name="name",
                    label="Name",
                    required=True,
                ),
                okta.PolicyRuleProfileEnrollmentProfileAttributeArgs(
                    name="t-shirt",
                    label="T-Shirt Size",
                    required=False,
                ),
            ])
        ```

        ## Import

        A Policy Rule can be imported via the Policy and Rule ID.

        ```sh
         $ pulumi import okta:index/policyRuleProfileEnrollment:PolicyRuleProfileEnrollment example &#60;policy id&#62;/&#60;rule id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param PolicyRuleProfileEnrollmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicyRuleProfileEnrollmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access: Optional[pulumi.Input[str]] = None,
                 email_verification: Optional[pulumi.Input[bool]] = None,
                 inline_hook_id: Optional[pulumi.Input[str]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 profile_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]]] = None,
                 target_group_id: Optional[pulumi.Input[str]] = None,
                 ui_schema_id: Optional[pulumi.Input[str]] = None,
                 unknown_user_action: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PolicyRuleProfileEnrollmentArgs.__new__(PolicyRuleProfileEnrollmentArgs)

            __props__.__dict__["access"] = access
            __props__.__dict__["email_verification"] = email_verification
            __props__.__dict__["inline_hook_id"] = inline_hook_id
            if policy_id is None and not opts.urn:
                raise TypeError("Missing required property 'policy_id'")
            __props__.__dict__["policy_id"] = policy_id
            __props__.__dict__["profile_attributes"] = profile_attributes
            __props__.__dict__["target_group_id"] = target_group_id
            __props__.__dict__["ui_schema_id"] = ui_schema_id
            if unknown_user_action is None and not opts.urn:
                raise TypeError("Missing required property 'unknown_user_action'")
            __props__.__dict__["unknown_user_action"] = unknown_user_action
            __props__.__dict__["name"] = None
            __props__.__dict__["status"] = None
        super(PolicyRuleProfileEnrollment, __self__).__init__(
            'okta:index/policyRuleProfileEnrollment:PolicyRuleProfileEnrollment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access: Optional[pulumi.Input[str]] = None,
            email_verification: Optional[pulumi.Input[bool]] = None,
            inline_hook_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            policy_id: Optional[pulumi.Input[str]] = None,
            profile_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]]] = None,
            status: Optional[pulumi.Input[str]] = None,
            target_group_id: Optional[pulumi.Input[str]] = None,
            ui_schema_id: Optional[pulumi.Input[str]] = None,
            unknown_user_action: Optional[pulumi.Input[str]] = None) -> 'PolicyRuleProfileEnrollment':
        """
        Get an existing PolicyRuleProfileEnrollment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access: Allow or deny access based on the rule conditions. Valid values are: `"ALLOW"`, `"DENY"`. Default is `"ALLOW"`.
        :param pulumi.Input[bool] email_verification: Indicates whether email verification should occur before access is granted. Default is `true`.
        :param pulumi.Input[str] inline_hook_id: ID of a Registration Inline Hook.
        :param pulumi.Input[str] name: The name of a User Profile property
        :param pulumi.Input[str] policy_id: Policy ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyRuleProfileEnrollmentProfileAttributeArgs']]]] profile_attributes: A list of attributes to prompt the user during registration or progressive profiling. Where defined on the User schema, these attributes are persisted in the User profile. Non-schema attributes may also be added, which aren't persisted to the User's profile, but are included in requests to the registration inline hook. A maximum of 10 Profile properties is supported.
        :param pulumi.Input[str] status: Status of the Rule.
        :param pulumi.Input[str] target_group_id: The ID of a Group that this User should be added to.
        :param pulumi.Input[str] ui_schema_id: Value created by the backend. If present all policy updates must include this attribute/value.
        :param pulumi.Input[str] unknown_user_action: Which action should be taken if this User is new. Valid values are: `"DENY"`, `"REGISTER"`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PolicyRuleProfileEnrollmentState.__new__(_PolicyRuleProfileEnrollmentState)

        __props__.__dict__["access"] = access
        __props__.__dict__["email_verification"] = email_verification
        __props__.__dict__["inline_hook_id"] = inline_hook_id
        __props__.__dict__["name"] = name
        __props__.__dict__["policy_id"] = policy_id
        __props__.__dict__["profile_attributes"] = profile_attributes
        __props__.__dict__["status"] = status
        __props__.__dict__["target_group_id"] = target_group_id
        __props__.__dict__["ui_schema_id"] = ui_schema_id
        __props__.__dict__["unknown_user_action"] = unknown_user_action
        return PolicyRuleProfileEnrollment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def access(self) -> pulumi.Output[Optional[str]]:
        """
        Allow or deny access based on the rule conditions. Valid values are: `"ALLOW"`, `"DENY"`. Default is `"ALLOW"`.
        """
        return pulumi.get(self, "access")

    @property
    @pulumi.getter(name="emailVerification")
    def email_verification(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether email verification should occur before access is granted. Default is `true`.
        """
        return pulumi.get(self, "email_verification")

    @property
    @pulumi.getter(name="inlineHookId")
    def inline_hook_id(self) -> pulumi.Output[Optional[str]]:
        """
        ID of a Registration Inline Hook.
        """
        return pulumi.get(self, "inline_hook_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of a User Profile property
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Output[str]:
        """
        Policy ID.
        """
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter(name="profileAttributes")
    def profile_attributes(self) -> pulumi.Output[Optional[Sequence['outputs.PolicyRuleProfileEnrollmentProfileAttribute']]]:
        """
        A list of attributes to prompt the user during registration or progressive profiling. Where defined on the User schema, these attributes are persisted in the User profile. Non-schema attributes may also be added, which aren't persisted to the User's profile, but are included in requests to the registration inline hook. A maximum of 10 Profile properties is supported.
        """
        return pulumi.get(self, "profile_attributes")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the Rule.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="targetGroupId")
    def target_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a Group that this User should be added to.
        """
        return pulumi.get(self, "target_group_id")

    @property
    @pulumi.getter(name="uiSchemaId")
    def ui_schema_id(self) -> pulumi.Output[Optional[str]]:
        """
        Value created by the backend. If present all policy updates must include this attribute/value.
        """
        return pulumi.get(self, "ui_schema_id")

    @property
    @pulumi.getter(name="unknownUserAction")
    def unknown_user_action(self) -> pulumi.Output[str]:
        """
        Which action should be taken if this User is new. Valid values are: `"DENY"`, `"REGISTER"`.
        """
        return pulumi.get(self, "unknown_user_action")

