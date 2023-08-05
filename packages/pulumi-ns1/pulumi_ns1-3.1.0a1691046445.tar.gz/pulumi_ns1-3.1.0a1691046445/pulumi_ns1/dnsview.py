# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['DnsviewArgs', 'Dnsview']

@pulumi.input_type
class DnsviewArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 networks: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 preference: Optional[pulumi.Input[int]] = None,
                 read_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 update_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Dnsview resource.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if networks is not None:
            pulumi.set(__self__, "networks", networks)
        if preference is not None:
            pulumi.set(__self__, "preference", preference)
        if read_acls is not None:
            pulumi.set(__self__, "read_acls", read_acls)
        if update_acls is not None:
            pulumi.set(__self__, "update_acls", update_acls)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def networks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        return pulumi.get(self, "networks")

    @networks.setter
    def networks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "networks", value)

    @property
    @pulumi.getter
    def preference(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "preference")

    @preference.setter
    def preference(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "preference", value)

    @property
    @pulumi.getter(name="readAcls")
    def read_acls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "read_acls")

    @read_acls.setter
    def read_acls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "read_acls", value)

    @property
    @pulumi.getter(name="updateAcls")
    def update_acls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "update_acls")

    @update_acls.setter
    def update_acls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "update_acls", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "zones", value)


@pulumi.input_type
class _DnsviewState:
    def __init__(__self__, *,
                 created_at: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 networks: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 preference: Optional[pulumi.Input[int]] = None,
                 read_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 update_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 updated_at: Optional[pulumi.Input[int]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Dnsview resources.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if networks is not None:
            pulumi.set(__self__, "networks", networks)
        if preference is not None:
            pulumi.set(__self__, "preference", preference)
        if read_acls is not None:
            pulumi.set(__self__, "read_acls", read_acls)
        if update_acls is not None:
            pulumi.set(__self__, "update_acls", update_acls)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def networks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        return pulumi.get(self, "networks")

    @networks.setter
    def networks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "networks", value)

    @property
    @pulumi.getter
    def preference(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "preference")

    @preference.setter
    def preference(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "preference", value)

    @property
    @pulumi.getter(name="readAcls")
    def read_acls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "read_acls")

    @read_acls.setter
    def read_acls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "read_acls", value)

    @property
    @pulumi.getter(name="updateAcls")
    def update_acls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "update_acls")

    @update_acls.setter
    def update_acls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "update_acls", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "updated_at", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "zones", value)


class Dnsview(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 networks: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 preference: Optional[pulumi.Input[int]] = None,
                 read_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 update_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Create a Dnsview resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[DnsviewArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Dnsview resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param DnsviewArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DnsviewArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 networks: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 preference: Optional[pulumi.Input[int]] = None,
                 read_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 update_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DnsviewArgs.__new__(DnsviewArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["networks"] = networks
            __props__.__dict__["preference"] = preference
            __props__.__dict__["read_acls"] = read_acls
            __props__.__dict__["update_acls"] = update_acls
            __props__.__dict__["zones"] = zones
            __props__.__dict__["created_at"] = None
            __props__.__dict__["updated_at"] = None
        super(Dnsview, __self__).__init__(
            'ns1:index/dnsview:Dnsview',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_at: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            networks: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
            preference: Optional[pulumi.Input[int]] = None,
            read_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            update_acls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            updated_at: Optional[pulumi.Input[int]] = None,
            zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Dnsview':
        """
        Get an existing Dnsview resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DnsviewState.__new__(_DnsviewState)

        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["name"] = name
        __props__.__dict__["networks"] = networks
        __props__.__dict__["preference"] = preference
        __props__.__dict__["read_acls"] = read_acls
        __props__.__dict__["update_acls"] = update_acls
        __props__.__dict__["updated_at"] = updated_at
        __props__.__dict__["zones"] = zones
        return Dnsview(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[int]:
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def networks(self) -> pulumi.Output[Optional[Sequence[int]]]:
        return pulumi.get(self, "networks")

    @property
    @pulumi.getter
    def preference(self) -> pulumi.Output[int]:
        return pulumi.get(self, "preference")

    @property
    @pulumi.getter(name="readAcls")
    def read_acls(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "read_acls")

    @property
    @pulumi.getter(name="updateAcls")
    def update_acls(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "update_acls")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[int]:
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "zones")

