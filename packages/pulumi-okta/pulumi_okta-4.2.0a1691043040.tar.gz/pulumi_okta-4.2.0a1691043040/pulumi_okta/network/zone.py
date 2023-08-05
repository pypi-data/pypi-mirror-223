# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ZoneArgs', 'Zone']

@pulumi.input_type
class ZoneArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 asns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_proxy_type: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 proxies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Zone resource.
        :param pulumi.Input[str] type: Type of the Network Zone - can either be `"IP"` or `"DYNAMIC"` only.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asns: Array of Autonomous System Numbers (each element is a string representation of an ASN numeric value).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dynamic_locations: Array of locations [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
               and [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2). Format code: countryCode OR countryCode-regionCode.
        :param pulumi.Input[str] dynamic_proxy_type: Type of proxy being controlled by this dynamic network zone - can be one of `Any`, `TorAnonymizer` or `NotTorAnonymizer`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Array of values in CIDR/range form.
        :param pulumi.Input[str] name: Name of the Network Zone Resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] proxies: Array of values in CIDR/range form. Can not be set if `usage` is set to `"BLOCKLIST"`.
        :param pulumi.Input[str] status: Network Status - can either be ACTIVE or INACTIVE only.
        :param pulumi.Input[str] usage: Usage of the Network Zone - can be either `"POLICY"` or `"BLOCKLIST"`. By default, it is `"POLICY"`.
        """
        pulumi.set(__self__, "type", type)
        if asns is not None:
            pulumi.set(__self__, "asns", asns)
        if dynamic_locations is not None:
            pulumi.set(__self__, "dynamic_locations", dynamic_locations)
        if dynamic_proxy_type is not None:
            pulumi.set(__self__, "dynamic_proxy_type", dynamic_proxy_type)
        if gateways is not None:
            pulumi.set(__self__, "gateways", gateways)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if proxies is not None:
            pulumi.set(__self__, "proxies", proxies)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if usage is not None:
            pulumi.set(__self__, "usage", usage)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of the Network Zone - can either be `"IP"` or `"DYNAMIC"` only.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def asns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of Autonomous System Numbers (each element is a string representation of an ASN numeric value).
        """
        return pulumi.get(self, "asns")

    @asns.setter
    def asns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "asns", value)

    @property
    @pulumi.getter(name="dynamicLocations")
    def dynamic_locations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of locations [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
        and [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2). Format code: countryCode OR countryCode-regionCode.
        """
        return pulumi.get(self, "dynamic_locations")

    @dynamic_locations.setter
    def dynamic_locations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dynamic_locations", value)

    @property
    @pulumi.getter(name="dynamicProxyType")
    def dynamic_proxy_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of proxy being controlled by this dynamic network zone - can be one of `Any`, `TorAnonymizer` or `NotTorAnonymizer`.
        """
        return pulumi.get(self, "dynamic_proxy_type")

    @dynamic_proxy_type.setter
    def dynamic_proxy_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dynamic_proxy_type", value)

    @property
    @pulumi.getter
    def gateways(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of values in CIDR/range form.
        """
        return pulumi.get(self, "gateways")

    @gateways.setter
    def gateways(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "gateways", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Network Zone Resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def proxies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of values in CIDR/range form. Can not be set if `usage` is set to `"BLOCKLIST"`.
        """
        return pulumi.get(self, "proxies")

    @proxies.setter
    def proxies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "proxies", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Network Status - can either be ACTIVE or INACTIVE only.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def usage(self) -> Optional[pulumi.Input[str]]:
        """
        Usage of the Network Zone - can be either `"POLICY"` or `"BLOCKLIST"`. By default, it is `"POLICY"`.
        """
        return pulumi.get(self, "usage")

    @usage.setter
    def usage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage", value)


@pulumi.input_type
class _ZoneState:
    def __init__(__self__, *,
                 asns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_proxy_type: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 proxies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Zone resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asns: Array of Autonomous System Numbers (each element is a string representation of an ASN numeric value).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dynamic_locations: Array of locations [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
               and [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2). Format code: countryCode OR countryCode-regionCode.
        :param pulumi.Input[str] dynamic_proxy_type: Type of proxy being controlled by this dynamic network zone - can be one of `Any`, `TorAnonymizer` or `NotTorAnonymizer`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Array of values in CIDR/range form.
        :param pulumi.Input[str] name: Name of the Network Zone Resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] proxies: Array of values in CIDR/range form. Can not be set if `usage` is set to `"BLOCKLIST"`.
        :param pulumi.Input[str] status: Network Status - can either be ACTIVE or INACTIVE only.
        :param pulumi.Input[str] type: Type of the Network Zone - can either be `"IP"` or `"DYNAMIC"` only.
        :param pulumi.Input[str] usage: Usage of the Network Zone - can be either `"POLICY"` or `"BLOCKLIST"`. By default, it is `"POLICY"`.
        """
        if asns is not None:
            pulumi.set(__self__, "asns", asns)
        if dynamic_locations is not None:
            pulumi.set(__self__, "dynamic_locations", dynamic_locations)
        if dynamic_proxy_type is not None:
            pulumi.set(__self__, "dynamic_proxy_type", dynamic_proxy_type)
        if gateways is not None:
            pulumi.set(__self__, "gateways", gateways)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if proxies is not None:
            pulumi.set(__self__, "proxies", proxies)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if usage is not None:
            pulumi.set(__self__, "usage", usage)

    @property
    @pulumi.getter
    def asns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of Autonomous System Numbers (each element is a string representation of an ASN numeric value).
        """
        return pulumi.get(self, "asns")

    @asns.setter
    def asns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "asns", value)

    @property
    @pulumi.getter(name="dynamicLocations")
    def dynamic_locations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of locations [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
        and [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2). Format code: countryCode OR countryCode-regionCode.
        """
        return pulumi.get(self, "dynamic_locations")

    @dynamic_locations.setter
    def dynamic_locations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dynamic_locations", value)

    @property
    @pulumi.getter(name="dynamicProxyType")
    def dynamic_proxy_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of proxy being controlled by this dynamic network zone - can be one of `Any`, `TorAnonymizer` or `NotTorAnonymizer`.
        """
        return pulumi.get(self, "dynamic_proxy_type")

    @dynamic_proxy_type.setter
    def dynamic_proxy_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dynamic_proxy_type", value)

    @property
    @pulumi.getter
    def gateways(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of values in CIDR/range form.
        """
        return pulumi.get(self, "gateways")

    @gateways.setter
    def gateways(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "gateways", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Network Zone Resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def proxies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of values in CIDR/range form. Can not be set if `usage` is set to `"BLOCKLIST"`.
        """
        return pulumi.get(self, "proxies")

    @proxies.setter
    def proxies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "proxies", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Network Status - can either be ACTIVE or INACTIVE only.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the Network Zone - can either be `"IP"` or `"DYNAMIC"` only.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def usage(self) -> Optional[pulumi.Input[str]]:
        """
        Usage of the Network Zone - can be either `"POLICY"` or `"BLOCKLIST"`. By default, it is `"POLICY"`.
        """
        return pulumi.get(self, "usage")

    @usage.setter
    def usage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage", value)


class Zone(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_proxy_type: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 proxies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates an Okta Network Zone.

        This resource allows you to create and configure an Okta Network Zone.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.network.Zone("example",
            gateways=[
                "1.2.3.4/24",
                "2.3.4.5-2.3.4.15",
            ],
            proxies=[
                "2.2.3.4/24",
                "3.3.4.5-3.3.4.15",
            ],
            type="IP")
        ```
        ### Dynamic Tor Blocker

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.network.Zone("example",
            dynamic_proxy_type="TorAnonymizer",
            type="DYNAMIC",
            usage="BLOCKLIST")
        ```

        ## Import

        Okta Network Zone can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:network/zone:Zone example &#60;zone id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asns: Array of Autonomous System Numbers (each element is a string representation of an ASN numeric value).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dynamic_locations: Array of locations [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
               and [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2). Format code: countryCode OR countryCode-regionCode.
        :param pulumi.Input[str] dynamic_proxy_type: Type of proxy being controlled by this dynamic network zone - can be one of `Any`, `TorAnonymizer` or `NotTorAnonymizer`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Array of values in CIDR/range form.
        :param pulumi.Input[str] name: Name of the Network Zone Resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] proxies: Array of values in CIDR/range form. Can not be set if `usage` is set to `"BLOCKLIST"`.
        :param pulumi.Input[str] status: Network Status - can either be ACTIVE or INACTIVE only.
        :param pulumi.Input[str] type: Type of the Network Zone - can either be `"IP"` or `"DYNAMIC"` only.
        :param pulumi.Input[str] usage: Usage of the Network Zone - can be either `"POLICY"` or `"BLOCKLIST"`. By default, it is `"POLICY"`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ZoneArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates an Okta Network Zone.

        This resource allows you to create and configure an Okta Network Zone.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.network.Zone("example",
            gateways=[
                "1.2.3.4/24",
                "2.3.4.5-2.3.4.15",
            ],
            proxies=[
                "2.2.3.4/24",
                "3.3.4.5-3.3.4.15",
            ],
            type="IP")
        ```
        ### Dynamic Tor Blocker

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.network.Zone("example",
            dynamic_proxy_type="TorAnonymizer",
            type="DYNAMIC",
            usage="BLOCKLIST")
        ```

        ## Import

        Okta Network Zone can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:network/zone:Zone example &#60;zone id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param ZoneArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ZoneArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dynamic_proxy_type: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 proxies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 usage: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ZoneArgs.__new__(ZoneArgs)

            __props__.__dict__["asns"] = asns
            __props__.__dict__["dynamic_locations"] = dynamic_locations
            __props__.__dict__["dynamic_proxy_type"] = dynamic_proxy_type
            __props__.__dict__["gateways"] = gateways
            __props__.__dict__["name"] = name
            __props__.__dict__["proxies"] = proxies
            __props__.__dict__["status"] = status
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["usage"] = usage
        super(Zone, __self__).__init__(
            'okta:network/zone:Zone',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            asns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            dynamic_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            dynamic_proxy_type: Optional[pulumi.Input[str]] = None,
            gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            proxies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            status: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            usage: Optional[pulumi.Input[str]] = None) -> 'Zone':
        """
        Get an existing Zone resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asns: Array of Autonomous System Numbers (each element is a string representation of an ASN numeric value).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dynamic_locations: Array of locations [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
               and [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2). Format code: countryCode OR countryCode-regionCode.
        :param pulumi.Input[str] dynamic_proxy_type: Type of proxy being controlled by this dynamic network zone - can be one of `Any`, `TorAnonymizer` or `NotTorAnonymizer`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Array of values in CIDR/range form.
        :param pulumi.Input[str] name: Name of the Network Zone Resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] proxies: Array of values in CIDR/range form. Can not be set if `usage` is set to `"BLOCKLIST"`.
        :param pulumi.Input[str] status: Network Status - can either be ACTIVE or INACTIVE only.
        :param pulumi.Input[str] type: Type of the Network Zone - can either be `"IP"` or `"DYNAMIC"` only.
        :param pulumi.Input[str] usage: Usage of the Network Zone - can be either `"POLICY"` or `"BLOCKLIST"`. By default, it is `"POLICY"`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ZoneState.__new__(_ZoneState)

        __props__.__dict__["asns"] = asns
        __props__.__dict__["dynamic_locations"] = dynamic_locations
        __props__.__dict__["dynamic_proxy_type"] = dynamic_proxy_type
        __props__.__dict__["gateways"] = gateways
        __props__.__dict__["name"] = name
        __props__.__dict__["proxies"] = proxies
        __props__.__dict__["status"] = status
        __props__.__dict__["type"] = type
        __props__.__dict__["usage"] = usage
        return Zone(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def asns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Array of Autonomous System Numbers (each element is a string representation of an ASN numeric value).
        """
        return pulumi.get(self, "asns")

    @property
    @pulumi.getter(name="dynamicLocations")
    def dynamic_locations(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Array of locations [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
        and [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2). Format code: countryCode OR countryCode-regionCode.
        """
        return pulumi.get(self, "dynamic_locations")

    @property
    @pulumi.getter(name="dynamicProxyType")
    def dynamic_proxy_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of proxy being controlled by this dynamic network zone - can be one of `Any`, `TorAnonymizer` or `NotTorAnonymizer`.
        """
        return pulumi.get(self, "dynamic_proxy_type")

    @property
    @pulumi.getter
    def gateways(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Array of values in CIDR/range form.
        """
        return pulumi.get(self, "gateways")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Network Zone Resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def proxies(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Array of values in CIDR/range form. Can not be set if `usage` is set to `"BLOCKLIST"`.
        """
        return pulumi.get(self, "proxies")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Network Status - can either be ACTIVE or INACTIVE only.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the Network Zone - can either be `"IP"` or `"DYNAMIC"` only.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def usage(self) -> pulumi.Output[Optional[str]]:
        """
        Usage of the Network Zone - can be either `"POLICY"` or `"BLOCKLIST"`. By default, it is `"POLICY"`.
        """
        return pulumi.get(self, "usage")

