# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['FieldArgs', 'Field']

@pulumi.input_type
class FieldArgs:
    def __init__(__self__, *,
                 field_name: pulumi.Input[str],
                 data_type: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Field resource.
        :param pulumi.Input[str] field_name: Name of the field.
        :param pulumi.Input[str] data_type: Field type. Possible values are `String`, `Long`, `Int`, `Double`, and `Boolean`.
        :param pulumi.Input[str] state: State of the field (either `Enabled` or `Disabled`).
        """
        pulumi.set(__self__, "field_name", field_name)
        if data_type is not None:
            pulumi.set(__self__, "data_type", data_type)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="fieldName")
    def field_name(self) -> pulumi.Input[str]:
        """
        Name of the field.
        """
        return pulumi.get(self, "field_name")

    @field_name.setter
    def field_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "field_name", value)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> Optional[pulumi.Input[str]]:
        """
        Field type. Possible values are `String`, `Long`, `Int`, `Double`, and `Boolean`.
        """
        return pulumi.get(self, "data_type")

    @data_type.setter
    def data_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_type", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the field (either `Enabled` or `Disabled`).
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


@pulumi.input_type
class _FieldState:
    def __init__(__self__, *,
                 data_type: Optional[pulumi.Input[str]] = None,
                 field_id: Optional[pulumi.Input[str]] = None,
                 field_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Field resources.
        :param pulumi.Input[str] data_type: Field type. Possible values are `String`, `Long`, `Int`, `Double`, and `Boolean`.
        :param pulumi.Input[str] field_id: Field identifier.
        :param pulumi.Input[str] field_name: Name of the field.
        :param pulumi.Input[str] state: State of the field (either `Enabled` or `Disabled`).
        """
        if data_type is not None:
            pulumi.set(__self__, "data_type", data_type)
        if field_id is not None:
            pulumi.set(__self__, "field_id", field_id)
        if field_name is not None:
            pulumi.set(__self__, "field_name", field_name)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> Optional[pulumi.Input[str]]:
        """
        Field type. Possible values are `String`, `Long`, `Int`, `Double`, and `Boolean`.
        """
        return pulumi.get(self, "data_type")

    @data_type.setter
    def data_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_type", value)

    @property
    @pulumi.getter(name="fieldId")
    def field_id(self) -> Optional[pulumi.Input[str]]:
        """
        Field identifier.
        """
        return pulumi.get(self, "field_id")

    @field_id.setter
    def field_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "field_id", value)

    @property
    @pulumi.getter(name="fieldName")
    def field_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the field.
        """
        return pulumi.get(self, "field_name")

    @field_name.setter
    def field_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "field_name", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the field (either `Enabled` or `Disabled`).
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


class Field(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_type: Optional[pulumi.Input[str]] = None,
                 field_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a [Sumologic Field](https://help.sumologic.com/Manage/Fields).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        field = sumologic.Field("field",
            data_type="Int",
            field_name="int_field_1")
        ```

        ## Import

        Fields can be imported using the field id, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/field:Field field 000000000ABC1234
        ```

         [1]https://help.sumologic.com/Manage/Fields

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_type: Field type. Possible values are `String`, `Long`, `Int`, `Double`, and `Boolean`.
        :param pulumi.Input[str] field_name: Name of the field.
        :param pulumi.Input[str] state: State of the field (either `Enabled` or `Disabled`).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FieldArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a [Sumologic Field](https://help.sumologic.com/Manage/Fields).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        field = sumologic.Field("field",
            data_type="Int",
            field_name="int_field_1")
        ```

        ## Import

        Fields can be imported using the field id, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/field:Field field 000000000ABC1234
        ```

         [1]https://help.sumologic.com/Manage/Fields

        :param str resource_name: The name of the resource.
        :param FieldArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FieldArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_type: Optional[pulumi.Input[str]] = None,
                 field_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FieldArgs.__new__(FieldArgs)

            __props__.__dict__["data_type"] = data_type
            if field_name is None and not opts.urn:
                raise TypeError("Missing required property 'field_name'")
            __props__.__dict__["field_name"] = field_name
            __props__.__dict__["state"] = state
            __props__.__dict__["field_id"] = None
        super(Field, __self__).__init__(
            'sumologic:index/field:Field',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            data_type: Optional[pulumi.Input[str]] = None,
            field_id: Optional[pulumi.Input[str]] = None,
            field_name: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None) -> 'Field':
        """
        Get an existing Field resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_type: Field type. Possible values are `String`, `Long`, `Int`, `Double`, and `Boolean`.
        :param pulumi.Input[str] field_id: Field identifier.
        :param pulumi.Input[str] field_name: Name of the field.
        :param pulumi.Input[str] state: State of the field (either `Enabled` or `Disabled`).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FieldState.__new__(_FieldState)

        __props__.__dict__["data_type"] = data_type
        __props__.__dict__["field_id"] = field_id
        __props__.__dict__["field_name"] = field_name
        __props__.__dict__["state"] = state
        return Field(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> pulumi.Output[Optional[str]]:
        """
        Field type. Possible values are `String`, `Long`, `Int`, `Double`, and `Boolean`.
        """
        return pulumi.get(self, "data_type")

    @property
    @pulumi.getter(name="fieldId")
    def field_id(self) -> pulumi.Output[str]:
        """
        Field identifier.
        """
        return pulumi.get(self, "field_id")

    @property
    @pulumi.getter(name="fieldName")
    def field_name(self) -> pulumi.Output[str]:
        """
        Name of the field.
        """
        return pulumi.get(self, "field_name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[Optional[str]]:
        """
        State of the field (either `Enabled` or `Disabled`).
        """
        return pulumi.get(self, "state")

