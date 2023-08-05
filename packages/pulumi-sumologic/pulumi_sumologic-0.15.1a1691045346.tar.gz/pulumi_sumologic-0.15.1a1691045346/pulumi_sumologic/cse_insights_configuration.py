# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['CseInsightsConfigurationArgs', 'CseInsightsConfiguration']

@pulumi.input_type
class CseInsightsConfigurationArgs:
    def __init__(__self__, *,
                 global_signal_suppression_window: Optional[pulumi.Input[float]] = None,
                 lookback_days: Optional[pulumi.Input[float]] = None,
                 threshold: Optional[pulumi.Input[float]] = None):
        """
        The set of arguments for constructing a CseInsightsConfiguration resource.
        :param pulumi.Input[float] global_signal_suppression_window: Detection global signal suppression window expressed in hours.
               
               The following attributes are exported:
        :param pulumi.Input[float] lookback_days: Detection window expressed in days.
        :param pulumi.Input[float] threshold: Detection threshold activity score.
        """
        if global_signal_suppression_window is not None:
            pulumi.set(__self__, "global_signal_suppression_window", global_signal_suppression_window)
        if lookback_days is not None:
            pulumi.set(__self__, "lookback_days", lookback_days)
        if threshold is not None:
            pulumi.set(__self__, "threshold", threshold)

    @property
    @pulumi.getter(name="globalSignalSuppressionWindow")
    def global_signal_suppression_window(self) -> Optional[pulumi.Input[float]]:
        """
        Detection global signal suppression window expressed in hours.

        The following attributes are exported:
        """
        return pulumi.get(self, "global_signal_suppression_window")

    @global_signal_suppression_window.setter
    def global_signal_suppression_window(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "global_signal_suppression_window", value)

    @property
    @pulumi.getter(name="lookbackDays")
    def lookback_days(self) -> Optional[pulumi.Input[float]]:
        """
        Detection window expressed in days.
        """
        return pulumi.get(self, "lookback_days")

    @lookback_days.setter
    def lookback_days(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "lookback_days", value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[float]]:
        """
        Detection threshold activity score.
        """
        return pulumi.get(self, "threshold")

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "threshold", value)


@pulumi.input_type
class _CseInsightsConfigurationState:
    def __init__(__self__, *,
                 global_signal_suppression_window: Optional[pulumi.Input[float]] = None,
                 lookback_days: Optional[pulumi.Input[float]] = None,
                 threshold: Optional[pulumi.Input[float]] = None):
        """
        Input properties used for looking up and filtering CseInsightsConfiguration resources.
        :param pulumi.Input[float] global_signal_suppression_window: Detection global signal suppression window expressed in hours.
               
               The following attributes are exported:
        :param pulumi.Input[float] lookback_days: Detection window expressed in days.
        :param pulumi.Input[float] threshold: Detection threshold activity score.
        """
        if global_signal_suppression_window is not None:
            pulumi.set(__self__, "global_signal_suppression_window", global_signal_suppression_window)
        if lookback_days is not None:
            pulumi.set(__self__, "lookback_days", lookback_days)
        if threshold is not None:
            pulumi.set(__self__, "threshold", threshold)

    @property
    @pulumi.getter(name="globalSignalSuppressionWindow")
    def global_signal_suppression_window(self) -> Optional[pulumi.Input[float]]:
        """
        Detection global signal suppression window expressed in hours.

        The following attributes are exported:
        """
        return pulumi.get(self, "global_signal_suppression_window")

    @global_signal_suppression_window.setter
    def global_signal_suppression_window(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "global_signal_suppression_window", value)

    @property
    @pulumi.getter(name="lookbackDays")
    def lookback_days(self) -> Optional[pulumi.Input[float]]:
        """
        Detection window expressed in days.
        """
        return pulumi.get(self, "lookback_days")

    @lookback_days.setter
    def lookback_days(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "lookback_days", value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[float]]:
        """
        Detection threshold activity score.
        """
        return pulumi.get(self, "threshold")

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "threshold", value)


class CseInsightsConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_signal_suppression_window: Optional[pulumi.Input[float]] = None,
                 lookback_days: Optional[pulumi.Input[float]] = None,
                 threshold: Optional[pulumi.Input[float]] = None,
                 __props__=None):
        """
        Provides the Sumologic CSE Insights Configuration for the whole organization. There can be only one configuration per organization.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        insights_configuration = sumologic.CseInsightsConfiguration("insightsConfiguration",
            global_signal_suppression_window=48,
            lookback_days=13,
            threshold=12)
        ```

        ## Import

        Insights Configuration can be imported using the id `cse-insights-configuration`hcl

        ```sh
         $ pulumi import sumologic:index/cseInsightsConfiguration:CseInsightsConfiguration insights_configuration cse-insights-configuration
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] global_signal_suppression_window: Detection global signal suppression window expressed in hours.
               
               The following attributes are exported:
        :param pulumi.Input[float] lookback_days: Detection window expressed in days.
        :param pulumi.Input[float] threshold: Detection threshold activity score.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[CseInsightsConfigurationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides the Sumologic CSE Insights Configuration for the whole organization. There can be only one configuration per organization.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        insights_configuration = sumologic.CseInsightsConfiguration("insightsConfiguration",
            global_signal_suppression_window=48,
            lookback_days=13,
            threshold=12)
        ```

        ## Import

        Insights Configuration can be imported using the id `cse-insights-configuration`hcl

        ```sh
         $ pulumi import sumologic:index/cseInsightsConfiguration:CseInsightsConfiguration insights_configuration cse-insights-configuration
        ```

        :param str resource_name: The name of the resource.
        :param CseInsightsConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CseInsightsConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_signal_suppression_window: Optional[pulumi.Input[float]] = None,
                 lookback_days: Optional[pulumi.Input[float]] = None,
                 threshold: Optional[pulumi.Input[float]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CseInsightsConfigurationArgs.__new__(CseInsightsConfigurationArgs)

            __props__.__dict__["global_signal_suppression_window"] = global_signal_suppression_window
            __props__.__dict__["lookback_days"] = lookback_days
            __props__.__dict__["threshold"] = threshold
        super(CseInsightsConfiguration, __self__).__init__(
            'sumologic:index/cseInsightsConfiguration:CseInsightsConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            global_signal_suppression_window: Optional[pulumi.Input[float]] = None,
            lookback_days: Optional[pulumi.Input[float]] = None,
            threshold: Optional[pulumi.Input[float]] = None) -> 'CseInsightsConfiguration':
        """
        Get an existing CseInsightsConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] global_signal_suppression_window: Detection global signal suppression window expressed in hours.
               
               The following attributes are exported:
        :param pulumi.Input[float] lookback_days: Detection window expressed in days.
        :param pulumi.Input[float] threshold: Detection threshold activity score.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CseInsightsConfigurationState.__new__(_CseInsightsConfigurationState)

        __props__.__dict__["global_signal_suppression_window"] = global_signal_suppression_window
        __props__.__dict__["lookback_days"] = lookback_days
        __props__.__dict__["threshold"] = threshold
        return CseInsightsConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="globalSignalSuppressionWindow")
    def global_signal_suppression_window(self) -> pulumi.Output[Optional[float]]:
        """
        Detection global signal suppression window expressed in hours.

        The following attributes are exported:
        """
        return pulumi.get(self, "global_signal_suppression_window")

    @property
    @pulumi.getter(name="lookbackDays")
    def lookback_days(self) -> pulumi.Output[Optional[float]]:
        """
        Detection window expressed in days.
        """
        return pulumi.get(self, "lookback_days")

    @property
    @pulumi.getter
    def threshold(self) -> pulumi.Output[Optional[float]]:
        """
        Detection threshold activity score.
        """
        return pulumi.get(self, "threshold")

