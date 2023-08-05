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

__all__ = ['SloArgs', 'Slo']

@pulumi.input_type
class SloArgs:
    def __init__(__self__, *,
                 compliances: pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]],
                 indicator: pulumi.Input['SloIndicatorArgs'],
                 signal_type: pulumi.Input[str],
                 application: Optional[pulumi.Input[str]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_locked: Optional[pulumi.Input[bool]] = None,
                 is_mutable: Optional[pulumi.Input[bool]] = None,
                 is_system: Optional[pulumi.Input[bool]] = None,
                 modified_at: Optional[pulumi.Input[str]] = None,
                 modified_by: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 post_request_map: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Slo resource.
        :param pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]] compliances: The compliance settings for the SLO.
        :param pulumi.Input['SloIndicatorArgs'] indicator: The service level indicator on which SLO is to be defined. more details on the difference
               b/w them can be found on
               the [slo help page](https://help.sumologic.com/Beta/SLO_Reliability_Management/Access_and_Create_SLOs)
               - window_based_evaluation - Evaluate SLI using successful/total windows.
               - request_based_evaluation - Evaluate SLI based on occurrence of successful
               events / total events over entire compliance period.
               - monitor_based_evaluation - SLIs for Monitor-based SLOs are calculated at a granularity of 1 minute. A minute is treated as unsuccessful if the Monitor threshold is violated at any point of time within that minute.
        :param pulumi.Input[str] signal_type: The type of SLO. Valid values are `Latency`, `Error`, `Throughput`, `Availability`
               , `Other`. Defaults to `Latency`.
        :param pulumi.Input[str] application: Name of the application.
        :param pulumi.Input[str] description: The description of the SLO.
        :param pulumi.Input[str] name: The name of the SLO. The name must be alphanumeric.
        :param pulumi.Input[str] parent_id: The ID of the SLO Folder that contains this SLO. Defaults to the root folder.
        :param pulumi.Input[str] service: Name of the service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map defining tag keys and tag values for the SLO.
        """
        pulumi.set(__self__, "compliances", compliances)
        pulumi.set(__self__, "indicator", indicator)
        pulumi.set(__self__, "signal_type", signal_type)
        if application is not None:
            pulumi.set(__self__, "application", application)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_locked is not None:
            pulumi.set(__self__, "is_locked", is_locked)
        if is_mutable is not None:
            pulumi.set(__self__, "is_mutable", is_mutable)
        if is_system is not None:
            pulumi.set(__self__, "is_system", is_system)
        if modified_at is not None:
            pulumi.set(__self__, "modified_at", modified_at)
        if modified_by is not None:
            pulumi.set(__self__, "modified_by", modified_by)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent_id is not None:
            pulumi.set(__self__, "parent_id", parent_id)
        if post_request_map is not None:
            pulumi.set(__self__, "post_request_map", post_request_map)
        if service is not None:
            pulumi.set(__self__, "service", service)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def compliances(self) -> pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]]:
        """
        The compliance settings for the SLO.
        """
        return pulumi.get(self, "compliances")

    @compliances.setter
    def compliances(self, value: pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]]):
        pulumi.set(self, "compliances", value)

    @property
    @pulumi.getter
    def indicator(self) -> pulumi.Input['SloIndicatorArgs']:
        """
        The service level indicator on which SLO is to be defined. more details on the difference
        b/w them can be found on
        the [slo help page](https://help.sumologic.com/Beta/SLO_Reliability_Management/Access_and_Create_SLOs)
        - window_based_evaluation - Evaluate SLI using successful/total windows.
        - request_based_evaluation - Evaluate SLI based on occurrence of successful
        events / total events over entire compliance period.
        - monitor_based_evaluation - SLIs for Monitor-based SLOs are calculated at a granularity of 1 minute. A minute is treated as unsuccessful if the Monitor threshold is violated at any point of time within that minute.
        """
        return pulumi.get(self, "indicator")

    @indicator.setter
    def indicator(self, value: pulumi.Input['SloIndicatorArgs']):
        pulumi.set(self, "indicator", value)

    @property
    @pulumi.getter(name="signalType")
    def signal_type(self) -> pulumi.Input[str]:
        """
        The type of SLO. Valid values are `Latency`, `Error`, `Throughput`, `Availability`
        , `Other`. Defaults to `Latency`.
        """
        return pulumi.get(self, "signal_type")

    @signal_type.setter
    def signal_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "signal_type", value)

    @property
    @pulumi.getter
    def application(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the application.
        """
        return pulumi.get(self, "application")

    @application.setter
    def application(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "created_by")

    @created_by.setter
    def created_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_by", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the SLO.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isLocked")
    def is_locked(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_locked")

    @is_locked.setter
    def is_locked(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_locked", value)

    @property
    @pulumi.getter(name="isMutable")
    def is_mutable(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_mutable")

    @is_mutable.setter
    def is_mutable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_mutable", value)

    @property
    @pulumi.getter(name="isSystem")
    def is_system(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_system")

    @is_system.setter
    def is_system(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_system", value)

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "modified_at")

    @modified_at.setter
    def modified_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "modified_at", value)

    @property
    @pulumi.getter(name="modifiedBy")
    def modified_by(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "modified_by")

    @modified_by.setter
    def modified_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "modified_by", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the SLO. The name must be alphanumeric.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the SLO Folder that contains this SLO. Defaults to the root folder.
        """
        return pulumi.get(self, "parent_id")

    @parent_id.setter
    def parent_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_id", value)

    @property
    @pulumi.getter(name="postRequestMap")
    def post_request_map(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "post_request_map")

    @post_request_map.setter
    def post_request_map(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "post_request_map", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the service.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map defining tag keys and tag values for the SLO.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class _SloState:
    def __init__(__self__, *,
                 application: Optional[pulumi.Input[str]] = None,
                 compliances: Optional[pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 indicator: Optional[pulumi.Input['SloIndicatorArgs']] = None,
                 is_locked: Optional[pulumi.Input[bool]] = None,
                 is_mutable: Optional[pulumi.Input[bool]] = None,
                 is_system: Optional[pulumi.Input[bool]] = None,
                 modified_at: Optional[pulumi.Input[str]] = None,
                 modified_by: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 post_request_map: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 signal_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Slo resources.
        :param pulumi.Input[str] application: Name of the application.
        :param pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]] compliances: The compliance settings for the SLO.
        :param pulumi.Input[str] description: The description of the SLO.
        :param pulumi.Input['SloIndicatorArgs'] indicator: The service level indicator on which SLO is to be defined. more details on the difference
               b/w them can be found on
               the [slo help page](https://help.sumologic.com/Beta/SLO_Reliability_Management/Access_and_Create_SLOs)
               - window_based_evaluation - Evaluate SLI using successful/total windows.
               - request_based_evaluation - Evaluate SLI based on occurrence of successful
               events / total events over entire compliance period.
               - monitor_based_evaluation - SLIs for Monitor-based SLOs are calculated at a granularity of 1 minute. A minute is treated as unsuccessful if the Monitor threshold is violated at any point of time within that minute.
        :param pulumi.Input[str] name: The name of the SLO. The name must be alphanumeric.
        :param pulumi.Input[str] parent_id: The ID of the SLO Folder that contains this SLO. Defaults to the root folder.
        :param pulumi.Input[str] service: Name of the service.
        :param pulumi.Input[str] signal_type: The type of SLO. Valid values are `Latency`, `Error`, `Throughput`, `Availability`
               , `Other`. Defaults to `Latency`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map defining tag keys and tag values for the SLO.
        """
        if application is not None:
            pulumi.set(__self__, "application", application)
        if compliances is not None:
            pulumi.set(__self__, "compliances", compliances)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if indicator is not None:
            pulumi.set(__self__, "indicator", indicator)
        if is_locked is not None:
            pulumi.set(__self__, "is_locked", is_locked)
        if is_mutable is not None:
            pulumi.set(__self__, "is_mutable", is_mutable)
        if is_system is not None:
            pulumi.set(__self__, "is_system", is_system)
        if modified_at is not None:
            pulumi.set(__self__, "modified_at", modified_at)
        if modified_by is not None:
            pulumi.set(__self__, "modified_by", modified_by)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent_id is not None:
            pulumi.set(__self__, "parent_id", parent_id)
        if post_request_map is not None:
            pulumi.set(__self__, "post_request_map", post_request_map)
        if service is not None:
            pulumi.set(__self__, "service", service)
        if signal_type is not None:
            pulumi.set(__self__, "signal_type", signal_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def application(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the application.
        """
        return pulumi.get(self, "application")

    @application.setter
    def application(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application", value)

    @property
    @pulumi.getter
    def compliances(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]]]:
        """
        The compliance settings for the SLO.
        """
        return pulumi.get(self, "compliances")

    @compliances.setter
    def compliances(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SloComplianceArgs']]]]):
        pulumi.set(self, "compliances", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "created_by")

    @created_by.setter
    def created_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_by", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the SLO.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def indicator(self) -> Optional[pulumi.Input['SloIndicatorArgs']]:
        """
        The service level indicator on which SLO is to be defined. more details on the difference
        b/w them can be found on
        the [slo help page](https://help.sumologic.com/Beta/SLO_Reliability_Management/Access_and_Create_SLOs)
        - window_based_evaluation - Evaluate SLI using successful/total windows.
        - request_based_evaluation - Evaluate SLI based on occurrence of successful
        events / total events over entire compliance period.
        - monitor_based_evaluation - SLIs for Monitor-based SLOs are calculated at a granularity of 1 minute. A minute is treated as unsuccessful if the Monitor threshold is violated at any point of time within that minute.
        """
        return pulumi.get(self, "indicator")

    @indicator.setter
    def indicator(self, value: Optional[pulumi.Input['SloIndicatorArgs']]):
        pulumi.set(self, "indicator", value)

    @property
    @pulumi.getter(name="isLocked")
    def is_locked(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_locked")

    @is_locked.setter
    def is_locked(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_locked", value)

    @property
    @pulumi.getter(name="isMutable")
    def is_mutable(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_mutable")

    @is_mutable.setter
    def is_mutable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_mutable", value)

    @property
    @pulumi.getter(name="isSystem")
    def is_system(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_system")

    @is_system.setter
    def is_system(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_system", value)

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "modified_at")

    @modified_at.setter
    def modified_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "modified_at", value)

    @property
    @pulumi.getter(name="modifiedBy")
    def modified_by(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "modified_by")

    @modified_by.setter
    def modified_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "modified_by", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the SLO. The name must be alphanumeric.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the SLO Folder that contains this SLO. Defaults to the root folder.
        """
        return pulumi.get(self, "parent_id")

    @parent_id.setter
    def parent_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_id", value)

    @property
    @pulumi.getter(name="postRequestMap")
    def post_request_map(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "post_request_map")

    @post_request_map.setter
    def post_request_map(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "post_request_map", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the service.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter(name="signalType")
    def signal_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of SLO. Valid values are `Latency`, `Error`, `Throughput`, `Availability`
        , `Other`. Defaults to `Latency`.
        """
        return pulumi.get(self, "signal_type")

    @signal_type.setter
    def signal_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signal_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map defining tag keys and tag values for the SLO.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


class Slo(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application: Optional[pulumi.Input[str]] = None,
                 compliances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SloComplianceArgs']]]]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 indicator: Optional[pulumi.Input[pulumi.InputType['SloIndicatorArgs']]] = None,
                 is_locked: Optional[pulumi.Input[bool]] = None,
                 is_mutable: Optional[pulumi.Input[bool]] = None,
                 is_system: Optional[pulumi.Input[bool]] = None,
                 modified_at: Optional[pulumi.Input[str]] = None,
                 modified_by: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 post_request_map: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 signal_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides the ability to create, read, delete, and update SLOs.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application: Name of the application.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SloComplianceArgs']]]] compliances: The compliance settings for the SLO.
        :param pulumi.Input[str] description: The description of the SLO.
        :param pulumi.Input[pulumi.InputType['SloIndicatorArgs']] indicator: The service level indicator on which SLO is to be defined. more details on the difference
               b/w them can be found on
               the [slo help page](https://help.sumologic.com/Beta/SLO_Reliability_Management/Access_and_Create_SLOs)
               - window_based_evaluation - Evaluate SLI using successful/total windows.
               - request_based_evaluation - Evaluate SLI based on occurrence of successful
               events / total events over entire compliance period.
               - monitor_based_evaluation - SLIs for Monitor-based SLOs are calculated at a granularity of 1 minute. A minute is treated as unsuccessful if the Monitor threshold is violated at any point of time within that minute.
        :param pulumi.Input[str] name: The name of the SLO. The name must be alphanumeric.
        :param pulumi.Input[str] parent_id: The ID of the SLO Folder that contains this SLO. Defaults to the root folder.
        :param pulumi.Input[str] service: Name of the service.
        :param pulumi.Input[str] signal_type: The type of SLO. Valid values are `Latency`, `Error`, `Throughput`, `Availability`
               , `Other`. Defaults to `Latency`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map defining tag keys and tag values for the SLO.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SloArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides the ability to create, read, delete, and update SLOs.

        :param str resource_name: The name of the resource.
        :param SloArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SloArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application: Optional[pulumi.Input[str]] = None,
                 compliances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SloComplianceArgs']]]]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 indicator: Optional[pulumi.Input[pulumi.InputType['SloIndicatorArgs']]] = None,
                 is_locked: Optional[pulumi.Input[bool]] = None,
                 is_mutable: Optional[pulumi.Input[bool]] = None,
                 is_system: Optional[pulumi.Input[bool]] = None,
                 modified_at: Optional[pulumi.Input[str]] = None,
                 modified_by: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 post_request_map: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 signal_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SloArgs.__new__(SloArgs)

            __props__.__dict__["application"] = application
            if compliances is None and not opts.urn:
                raise TypeError("Missing required property 'compliances'")
            __props__.__dict__["compliances"] = compliances
            __props__.__dict__["created_at"] = created_at
            __props__.__dict__["created_by"] = created_by
            __props__.__dict__["description"] = description
            if indicator is None and not opts.urn:
                raise TypeError("Missing required property 'indicator'")
            __props__.__dict__["indicator"] = indicator
            __props__.__dict__["is_locked"] = is_locked
            __props__.__dict__["is_mutable"] = is_mutable
            __props__.__dict__["is_system"] = is_system
            __props__.__dict__["modified_at"] = modified_at
            __props__.__dict__["modified_by"] = modified_by
            __props__.__dict__["name"] = name
            __props__.__dict__["parent_id"] = parent_id
            __props__.__dict__["post_request_map"] = post_request_map
            __props__.__dict__["service"] = service
            if signal_type is None and not opts.urn:
                raise TypeError("Missing required property 'signal_type'")
            __props__.__dict__["signal_type"] = signal_type
            __props__.__dict__["tags"] = tags
            __props__.__dict__["version"] = version
        super(Slo, __self__).__init__(
            'sumologic:index/slo:Slo',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            application: Optional[pulumi.Input[str]] = None,
            compliances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SloComplianceArgs']]]]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            created_by: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            indicator: Optional[pulumi.Input[pulumi.InputType['SloIndicatorArgs']]] = None,
            is_locked: Optional[pulumi.Input[bool]] = None,
            is_mutable: Optional[pulumi.Input[bool]] = None,
            is_system: Optional[pulumi.Input[bool]] = None,
            modified_at: Optional[pulumi.Input[str]] = None,
            modified_by: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parent_id: Optional[pulumi.Input[str]] = None,
            post_request_map: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            service: Optional[pulumi.Input[str]] = None,
            signal_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            version: Optional[pulumi.Input[int]] = None) -> 'Slo':
        """
        Get an existing Slo resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application: Name of the application.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SloComplianceArgs']]]] compliances: The compliance settings for the SLO.
        :param pulumi.Input[str] description: The description of the SLO.
        :param pulumi.Input[pulumi.InputType['SloIndicatorArgs']] indicator: The service level indicator on which SLO is to be defined. more details on the difference
               b/w them can be found on
               the [slo help page](https://help.sumologic.com/Beta/SLO_Reliability_Management/Access_and_Create_SLOs)
               - window_based_evaluation - Evaluate SLI using successful/total windows.
               - request_based_evaluation - Evaluate SLI based on occurrence of successful
               events / total events over entire compliance period.
               - monitor_based_evaluation - SLIs for Monitor-based SLOs are calculated at a granularity of 1 minute. A minute is treated as unsuccessful if the Monitor threshold is violated at any point of time within that minute.
        :param pulumi.Input[str] name: The name of the SLO. The name must be alphanumeric.
        :param pulumi.Input[str] parent_id: The ID of the SLO Folder that contains this SLO. Defaults to the root folder.
        :param pulumi.Input[str] service: Name of the service.
        :param pulumi.Input[str] signal_type: The type of SLO. Valid values are `Latency`, `Error`, `Throughput`, `Availability`
               , `Other`. Defaults to `Latency`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map defining tag keys and tag values for the SLO.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SloState.__new__(_SloState)

        __props__.__dict__["application"] = application
        __props__.__dict__["compliances"] = compliances
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["created_by"] = created_by
        __props__.__dict__["description"] = description
        __props__.__dict__["indicator"] = indicator
        __props__.__dict__["is_locked"] = is_locked
        __props__.__dict__["is_mutable"] = is_mutable
        __props__.__dict__["is_system"] = is_system
        __props__.__dict__["modified_at"] = modified_at
        __props__.__dict__["modified_by"] = modified_by
        __props__.__dict__["name"] = name
        __props__.__dict__["parent_id"] = parent_id
        __props__.__dict__["post_request_map"] = post_request_map
        __props__.__dict__["service"] = service
        __props__.__dict__["signal_type"] = signal_type
        __props__.__dict__["tags"] = tags
        __props__.__dict__["version"] = version
        return Slo(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def application(self) -> pulumi.Output[str]:
        """
        Name of the application.
        """
        return pulumi.get(self, "application")

    @property
    @pulumi.getter
    def compliances(self) -> pulumi.Output[Sequence['outputs.SloCompliance']]:
        """
        The compliance settings for the SLO.
        """
        return pulumi.get(self, "compliances")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> pulumi.Output[str]:
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the SLO.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def indicator(self) -> pulumi.Output['outputs.SloIndicator']:
        """
        The service level indicator on which SLO is to be defined. more details on the difference
        b/w them can be found on
        the [slo help page](https://help.sumologic.com/Beta/SLO_Reliability_Management/Access_and_Create_SLOs)
        - window_based_evaluation - Evaluate SLI using successful/total windows.
        - request_based_evaluation - Evaluate SLI based on occurrence of successful
        events / total events over entire compliance period.
        - monitor_based_evaluation - SLIs for Monitor-based SLOs are calculated at a granularity of 1 minute. A minute is treated as unsuccessful if the Monitor threshold is violated at any point of time within that minute.
        """
        return pulumi.get(self, "indicator")

    @property
    @pulumi.getter(name="isLocked")
    def is_locked(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "is_locked")

    @property
    @pulumi.getter(name="isMutable")
    def is_mutable(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "is_mutable")

    @property
    @pulumi.getter(name="isSystem")
    def is_system(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "is_system")

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> pulumi.Output[str]:
        return pulumi.get(self, "modified_at")

    @property
    @pulumi.getter(name="modifiedBy")
    def modified_by(self) -> pulumi.Output[str]:
        return pulumi.get(self, "modified_by")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the SLO. The name must be alphanumeric.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> pulumi.Output[str]:
        """
        The ID of the SLO Folder that contains this SLO. Defaults to the root folder.
        """
        return pulumi.get(self, "parent_id")

    @property
    @pulumi.getter(name="postRequestMap")
    def post_request_map(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "post_request_map")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[str]:
        """
        Name of the service.
        """
        return pulumi.get(self, "service")

    @property
    @pulumi.getter(name="signalType")
    def signal_type(self) -> pulumi.Output[str]:
        """
        The type of SLO. Valid values are `Latency`, `Error`, `Throughput`, `Availability`
        , `Other`. Defaults to `Latency`.
        """
        return pulumi.get(self, "signal_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map defining tag keys and tag values for the SLO.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        return pulumi.get(self, "version")

