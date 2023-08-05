# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['CseNetworkBlockArgs', 'CseNetworkBlock']

@pulumi.input_type
class CseNetworkBlockArgs:
    def __init__(__self__, *,
                 address_block: pulumi.Input[str],
                 internal: Optional[pulumi.Input[bool]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 suppresses_signals: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a CseNetworkBlock resource.
        :param pulumi.Input[str] address_block: The address block.
        :param pulumi.Input[bool] internal: Internal flag.
        :param pulumi.Input[str] label: The displayable label of the address block.
        :param pulumi.Input[bool] suppresses_signals: Suppresses signal flag.
               
               The following attributes are exported:
        """
        pulumi.set(__self__, "address_block", address_block)
        if internal is not None:
            pulumi.set(__self__, "internal", internal)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if suppresses_signals is not None:
            pulumi.set(__self__, "suppresses_signals", suppresses_signals)

    @property
    @pulumi.getter(name="addressBlock")
    def address_block(self) -> pulumi.Input[str]:
        """
        The address block.
        """
        return pulumi.get(self, "address_block")

    @address_block.setter
    def address_block(self, value: pulumi.Input[str]):
        pulumi.set(self, "address_block", value)

    @property
    @pulumi.getter
    def internal(self) -> Optional[pulumi.Input[bool]]:
        """
        Internal flag.
        """
        return pulumi.get(self, "internal")

    @internal.setter
    def internal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "internal", value)

    @property
    @pulumi.getter
    def label(self) -> Optional[pulumi.Input[str]]:
        """
        The displayable label of the address block.
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter(name="suppressesSignals")
    def suppresses_signals(self) -> Optional[pulumi.Input[bool]]:
        """
        Suppresses signal flag.

        The following attributes are exported:
        """
        return pulumi.get(self, "suppresses_signals")

    @suppresses_signals.setter
    def suppresses_signals(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suppresses_signals", value)


@pulumi.input_type
class _CseNetworkBlockState:
    def __init__(__self__, *,
                 address_block: Optional[pulumi.Input[str]] = None,
                 internal: Optional[pulumi.Input[bool]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 suppresses_signals: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering CseNetworkBlock resources.
        :param pulumi.Input[str] address_block: The address block.
        :param pulumi.Input[bool] internal: Internal flag.
        :param pulumi.Input[str] label: The displayable label of the address block.
        :param pulumi.Input[bool] suppresses_signals: Suppresses signal flag.
               
               The following attributes are exported:
        """
        if address_block is not None:
            pulumi.set(__self__, "address_block", address_block)
        if internal is not None:
            pulumi.set(__self__, "internal", internal)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if suppresses_signals is not None:
            pulumi.set(__self__, "suppresses_signals", suppresses_signals)

    @property
    @pulumi.getter(name="addressBlock")
    def address_block(self) -> Optional[pulumi.Input[str]]:
        """
        The address block.
        """
        return pulumi.get(self, "address_block")

    @address_block.setter
    def address_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_block", value)

    @property
    @pulumi.getter
    def internal(self) -> Optional[pulumi.Input[bool]]:
        """
        Internal flag.
        """
        return pulumi.get(self, "internal")

    @internal.setter
    def internal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "internal", value)

    @property
    @pulumi.getter
    def label(self) -> Optional[pulumi.Input[str]]:
        """
        The displayable label of the address block.
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter(name="suppressesSignals")
    def suppresses_signals(self) -> Optional[pulumi.Input[bool]]:
        """
        Suppresses signal flag.

        The following attributes are exported:
        """
        return pulumi.get(self, "suppresses_signals")

    @suppresses_signals.setter
    def suppresses_signals(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suppresses_signals", value)


class CseNetworkBlock(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_block: Optional[pulumi.Input[str]] = None,
                 internal: Optional[pulumi.Input[bool]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 suppresses_signals: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Provides a Sumo Logic CSE Network Block.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        network_block = sumologic.CseNetworkBlock("networkBlock",
            address_block="10.0.1.0/26",
            internal=True,
            label="network block from terraform",
            suppresses_signals=False)
        ```

        ## Import

        Network Block can be imported using the field id, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/cseNetworkBlock:CseNetworkBlock network_block id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_block: The address block.
        :param pulumi.Input[bool] internal: Internal flag.
        :param pulumi.Input[str] label: The displayable label of the address block.
        :param pulumi.Input[bool] suppresses_signals: Suppresses signal flag.
               
               The following attributes are exported:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CseNetworkBlockArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Sumo Logic CSE Network Block.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        network_block = sumologic.CseNetworkBlock("networkBlock",
            address_block="10.0.1.0/26",
            internal=True,
            label="network block from terraform",
            suppresses_signals=False)
        ```

        ## Import

        Network Block can be imported using the field id, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/cseNetworkBlock:CseNetworkBlock network_block id
        ```

        :param str resource_name: The name of the resource.
        :param CseNetworkBlockArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CseNetworkBlockArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_block: Optional[pulumi.Input[str]] = None,
                 internal: Optional[pulumi.Input[bool]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 suppresses_signals: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CseNetworkBlockArgs.__new__(CseNetworkBlockArgs)

            if address_block is None and not opts.urn:
                raise TypeError("Missing required property 'address_block'")
            __props__.__dict__["address_block"] = address_block
            __props__.__dict__["internal"] = internal
            __props__.__dict__["label"] = label
            __props__.__dict__["suppresses_signals"] = suppresses_signals
        super(CseNetworkBlock, __self__).__init__(
            'sumologic:index/cseNetworkBlock:CseNetworkBlock',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            address_block: Optional[pulumi.Input[str]] = None,
            internal: Optional[pulumi.Input[bool]] = None,
            label: Optional[pulumi.Input[str]] = None,
            suppresses_signals: Optional[pulumi.Input[bool]] = None) -> 'CseNetworkBlock':
        """
        Get an existing CseNetworkBlock resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_block: The address block.
        :param pulumi.Input[bool] internal: Internal flag.
        :param pulumi.Input[str] label: The displayable label of the address block.
        :param pulumi.Input[bool] suppresses_signals: Suppresses signal flag.
               
               The following attributes are exported:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CseNetworkBlockState.__new__(_CseNetworkBlockState)

        __props__.__dict__["address_block"] = address_block
        __props__.__dict__["internal"] = internal
        __props__.__dict__["label"] = label
        __props__.__dict__["suppresses_signals"] = suppresses_signals
        return CseNetworkBlock(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addressBlock")
    def address_block(self) -> pulumi.Output[str]:
        """
        The address block.
        """
        return pulumi.get(self, "address_block")

    @property
    @pulumi.getter
    def internal(self) -> pulumi.Output[Optional[bool]]:
        """
        Internal flag.
        """
        return pulumi.get(self, "internal")

    @property
    @pulumi.getter
    def label(self) -> pulumi.Output[Optional[str]]:
        """
        The displayable label of the address block.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="suppressesSignals")
    def suppresses_signals(self) -> pulumi.Output[Optional[bool]]:
        """
        Suppresses signal flag.

        The following attributes are exported:
        """
        return pulumi.get(self, "suppresses_signals")

