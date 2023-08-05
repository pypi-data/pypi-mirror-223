# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['IngestBudgetV2Args', 'IngestBudgetV2']

@pulumi.input_type
class IngestBudgetV2Args:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 capacity_bytes: pulumi.Input[int],
                 reset_time: pulumi.Input[str],
                 scope: pulumi.Input[str],
                 timezone: pulumi.Input[str],
                 audit_threshold: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a IngestBudgetV2 resource.
        :param pulumi.Input[str] action: Action to take when ingest budget's capacity is reached. All actions are audited. Supported values are `stopCollecting` and `keepCollecting`.
        :param pulumi.Input[int] capacity_bytes: Capacity of the ingest budget, in bytes.
        :param pulumi.Input[str] reset_time: Reset time of the ingest budget in HH:MM format. Defaults to `00:00`
        :param pulumi.Input[str] scope: A scope is a constraint that will be used to identify the messages on which budget needs to be applied. A scope is consists of key and value separated by =. The field must be enabled in the fields table.
        :param pulumi.Input[str] timezone: The time zone to use for this collector. The value follows the [tzdata](https://en.wikipedia.org/wiki/Tz_database) naming convention. Defaults to `Etc/UTC`
        :param pulumi.Input[int] audit_threshold: The threshold as a percentage of when an ingest budget's capacity usage is logged in the Audit Index.
               
               The following attributes are exported:
        :param pulumi.Input[str] description: The description of the collector.
        :param pulumi.Input[str] name: Display name of the ingest budget. This must be unique across all of the ingest budgets
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "capacity_bytes", capacity_bytes)
        pulumi.set(__self__, "reset_time", reset_time)
        pulumi.set(__self__, "scope", scope)
        pulumi.set(__self__, "timezone", timezone)
        if audit_threshold is not None:
            pulumi.set(__self__, "audit_threshold", audit_threshold)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        Action to take when ingest budget's capacity is reached. All actions are audited. Supported values are `stopCollecting` and `keepCollecting`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="capacityBytes")
    def capacity_bytes(self) -> pulumi.Input[int]:
        """
        Capacity of the ingest budget, in bytes.
        """
        return pulumi.get(self, "capacity_bytes")

    @capacity_bytes.setter
    def capacity_bytes(self, value: pulumi.Input[int]):
        pulumi.set(self, "capacity_bytes", value)

    @property
    @pulumi.getter(name="resetTime")
    def reset_time(self) -> pulumi.Input[str]:
        """
        Reset time of the ingest budget in HH:MM format. Defaults to `00:00`
        """
        return pulumi.get(self, "reset_time")

    @reset_time.setter
    def reset_time(self, value: pulumi.Input[str]):
        pulumi.set(self, "reset_time", value)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        A scope is a constraint that will be used to identify the messages on which budget needs to be applied. A scope is consists of key and value separated by =. The field must be enabled in the fields table.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def timezone(self) -> pulumi.Input[str]:
        """
        The time zone to use for this collector. The value follows the [tzdata](https://en.wikipedia.org/wiki/Tz_database) naming convention. Defaults to `Etc/UTC`
        """
        return pulumi.get(self, "timezone")

    @timezone.setter
    def timezone(self, value: pulumi.Input[str]):
        pulumi.set(self, "timezone", value)

    @property
    @pulumi.getter(name="auditThreshold")
    def audit_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The threshold as a percentage of when an ingest budget's capacity usage is logged in the Audit Index.

        The following attributes are exported:
        """
        return pulumi.get(self, "audit_threshold")

    @audit_threshold.setter
    def audit_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "audit_threshold", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the collector.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Display name of the ingest budget. This must be unique across all of the ingest budgets
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _IngestBudgetV2State:
    def __init__(__self__, *,
                 action: Optional[pulumi.Input[str]] = None,
                 audit_threshold: Optional[pulumi.Input[int]] = None,
                 capacity_bytes: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reset_time: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 timezone: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IngestBudgetV2 resources.
        :param pulumi.Input[str] action: Action to take when ingest budget's capacity is reached. All actions are audited. Supported values are `stopCollecting` and `keepCollecting`.
        :param pulumi.Input[int] audit_threshold: The threshold as a percentage of when an ingest budget's capacity usage is logged in the Audit Index.
               
               The following attributes are exported:
        :param pulumi.Input[int] capacity_bytes: Capacity of the ingest budget, in bytes.
        :param pulumi.Input[str] description: The description of the collector.
        :param pulumi.Input[str] name: Display name of the ingest budget. This must be unique across all of the ingest budgets
        :param pulumi.Input[str] reset_time: Reset time of the ingest budget in HH:MM format. Defaults to `00:00`
        :param pulumi.Input[str] scope: A scope is a constraint that will be used to identify the messages on which budget needs to be applied. A scope is consists of key and value separated by =. The field must be enabled in the fields table.
        :param pulumi.Input[str] timezone: The time zone to use for this collector. The value follows the [tzdata](https://en.wikipedia.org/wiki/Tz_database) naming convention. Defaults to `Etc/UTC`
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if audit_threshold is not None:
            pulumi.set(__self__, "audit_threshold", audit_threshold)
        if capacity_bytes is not None:
            pulumi.set(__self__, "capacity_bytes", capacity_bytes)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if reset_time is not None:
            pulumi.set(__self__, "reset_time", reset_time)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if timezone is not None:
            pulumi.set(__self__, "timezone", timezone)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[str]]:
        """
        Action to take when ingest budget's capacity is reached. All actions are audited. Supported values are `stopCollecting` and `keepCollecting`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="auditThreshold")
    def audit_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The threshold as a percentage of when an ingest budget's capacity usage is logged in the Audit Index.

        The following attributes are exported:
        """
        return pulumi.get(self, "audit_threshold")

    @audit_threshold.setter
    def audit_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "audit_threshold", value)

    @property
    @pulumi.getter(name="capacityBytes")
    def capacity_bytes(self) -> Optional[pulumi.Input[int]]:
        """
        Capacity of the ingest budget, in bytes.
        """
        return pulumi.get(self, "capacity_bytes")

    @capacity_bytes.setter
    def capacity_bytes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity_bytes", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the collector.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Display name of the ingest budget. This must be unique across all of the ingest budgets
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resetTime")
    def reset_time(self) -> Optional[pulumi.Input[str]]:
        """
        Reset time of the ingest budget in HH:MM format. Defaults to `00:00`
        """
        return pulumi.get(self, "reset_time")

    @reset_time.setter
    def reset_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reset_time", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input[str]]:
        """
        A scope is a constraint that will be used to identify the messages on which budget needs to be applied. A scope is consists of key and value separated by =. The field must be enabled in the fields table.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def timezone(self) -> Optional[pulumi.Input[str]]:
        """
        The time zone to use for this collector. The value follows the [tzdata](https://en.wikipedia.org/wiki/Tz_database) naming convention. Defaults to `Etc/UTC`
        """
        return pulumi.get(self, "timezone")

    @timezone.setter
    def timezone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "timezone", value)


class IngestBudgetV2(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 audit_threshold: Optional[pulumi.Input[int]] = None,
                 capacity_bytes: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reset_time: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 timezone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a [Sumologic Ingest Budget v2][1].

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        budget = sumologic.IngestBudgetV2("budget",
            action="keepCollecting",
            audit_threshold=85,
            capacity_bytes=30000000000,
            description="For testing purposes",
            reset_time="00:00",
            scope="_sourceCategory=*prod*nginx*",
            timezone="Etc/UTC")
        ```

        ## Import

        Ingest budgets can be imported using the name, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/ingestBudgetV2:IngestBudgetV2 budget budgetName
        ```

         [1]https://help.sumologic.com/Beta/Metadata_Ingest_Budgets [2]https://en.wikipedia.org/wiki/Tz_database

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: Action to take when ingest budget's capacity is reached. All actions are audited. Supported values are `stopCollecting` and `keepCollecting`.
        :param pulumi.Input[int] audit_threshold: The threshold as a percentage of when an ingest budget's capacity usage is logged in the Audit Index.
               
               The following attributes are exported:
        :param pulumi.Input[int] capacity_bytes: Capacity of the ingest budget, in bytes.
        :param pulumi.Input[str] description: The description of the collector.
        :param pulumi.Input[str] name: Display name of the ingest budget. This must be unique across all of the ingest budgets
        :param pulumi.Input[str] reset_time: Reset time of the ingest budget in HH:MM format. Defaults to `00:00`
        :param pulumi.Input[str] scope: A scope is a constraint that will be used to identify the messages on which budget needs to be applied. A scope is consists of key and value separated by =. The field must be enabled in the fields table.
        :param pulumi.Input[str] timezone: The time zone to use for this collector. The value follows the [tzdata](https://en.wikipedia.org/wiki/Tz_database) naming convention. Defaults to `Etc/UTC`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IngestBudgetV2Args,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a [Sumologic Ingest Budget v2][1].

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        budget = sumologic.IngestBudgetV2("budget",
            action="keepCollecting",
            audit_threshold=85,
            capacity_bytes=30000000000,
            description="For testing purposes",
            reset_time="00:00",
            scope="_sourceCategory=*prod*nginx*",
            timezone="Etc/UTC")
        ```

        ## Import

        Ingest budgets can be imported using the name, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/ingestBudgetV2:IngestBudgetV2 budget budgetName
        ```

         [1]https://help.sumologic.com/Beta/Metadata_Ingest_Budgets [2]https://en.wikipedia.org/wiki/Tz_database

        :param str resource_name: The name of the resource.
        :param IngestBudgetV2Args args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IngestBudgetV2Args, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 audit_threshold: Optional[pulumi.Input[int]] = None,
                 capacity_bytes: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reset_time: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 timezone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IngestBudgetV2Args.__new__(IngestBudgetV2Args)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["audit_threshold"] = audit_threshold
            if capacity_bytes is None and not opts.urn:
                raise TypeError("Missing required property 'capacity_bytes'")
            __props__.__dict__["capacity_bytes"] = capacity_bytes
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if reset_time is None and not opts.urn:
                raise TypeError("Missing required property 'reset_time'")
            __props__.__dict__["reset_time"] = reset_time
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            if timezone is None and not opts.urn:
                raise TypeError("Missing required property 'timezone'")
            __props__.__dict__["timezone"] = timezone
        super(IngestBudgetV2, __self__).__init__(
            'sumologic:index/ingestBudgetV2:IngestBudgetV2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[str]] = None,
            audit_threshold: Optional[pulumi.Input[int]] = None,
            capacity_bytes: Optional[pulumi.Input[int]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            reset_time: Optional[pulumi.Input[str]] = None,
            scope: Optional[pulumi.Input[str]] = None,
            timezone: Optional[pulumi.Input[str]] = None) -> 'IngestBudgetV2':
        """
        Get an existing IngestBudgetV2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: Action to take when ingest budget's capacity is reached. All actions are audited. Supported values are `stopCollecting` and `keepCollecting`.
        :param pulumi.Input[int] audit_threshold: The threshold as a percentage of when an ingest budget's capacity usage is logged in the Audit Index.
               
               The following attributes are exported:
        :param pulumi.Input[int] capacity_bytes: Capacity of the ingest budget, in bytes.
        :param pulumi.Input[str] description: The description of the collector.
        :param pulumi.Input[str] name: Display name of the ingest budget. This must be unique across all of the ingest budgets
        :param pulumi.Input[str] reset_time: Reset time of the ingest budget in HH:MM format. Defaults to `00:00`
        :param pulumi.Input[str] scope: A scope is a constraint that will be used to identify the messages on which budget needs to be applied. A scope is consists of key and value separated by =. The field must be enabled in the fields table.
        :param pulumi.Input[str] timezone: The time zone to use for this collector. The value follows the [tzdata](https://en.wikipedia.org/wiki/Tz_database) naming convention. Defaults to `Etc/UTC`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IngestBudgetV2State.__new__(_IngestBudgetV2State)

        __props__.__dict__["action"] = action
        __props__.__dict__["audit_threshold"] = audit_threshold
        __props__.__dict__["capacity_bytes"] = capacity_bytes
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["reset_time"] = reset_time
        __props__.__dict__["scope"] = scope
        __props__.__dict__["timezone"] = timezone
        return IngestBudgetV2(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        Action to take when ingest budget's capacity is reached. All actions are audited. Supported values are `stopCollecting` and `keepCollecting`.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="auditThreshold")
    def audit_threshold(self) -> pulumi.Output[Optional[int]]:
        """
        The threshold as a percentage of when an ingest budget's capacity usage is logged in the Audit Index.

        The following attributes are exported:
        """
        return pulumi.get(self, "audit_threshold")

    @property
    @pulumi.getter(name="capacityBytes")
    def capacity_bytes(self) -> pulumi.Output[int]:
        """
        Capacity of the ingest budget, in bytes.
        """
        return pulumi.get(self, "capacity_bytes")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the collector.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Display name of the ingest budget. This must be unique across all of the ingest budgets
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resetTime")
    def reset_time(self) -> pulumi.Output[str]:
        """
        Reset time of the ingest budget in HH:MM format. Defaults to `00:00`
        """
        return pulumi.get(self, "reset_time")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[str]:
        """
        A scope is a constraint that will be used to identify the messages on which budget needs to be applied. A scope is consists of key and value separated by =. The field must be enabled in the fields table.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def timezone(self) -> pulumi.Output[str]:
        """
        The time zone to use for this collector. The value follows the [tzdata](https://en.wikipedia.org/wiki/Tz_database) naming convention. Defaults to `Etc/UTC`
        """
        return pulumi.get(self, "timezone")

