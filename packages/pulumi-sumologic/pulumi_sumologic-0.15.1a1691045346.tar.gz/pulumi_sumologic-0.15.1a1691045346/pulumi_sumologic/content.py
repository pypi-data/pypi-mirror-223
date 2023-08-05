# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ContentArgs', 'Content']

@pulumi.input_type
class ContentArgs:
    def __init__(__self__, *,
                 config: pulumi.Input[str],
                 parent_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a Content resource.
        :param pulumi.Input[str] config: JSON block for the content to import. NOTE: Updating the name will create a new object and leave a untracked content item (delete the existing content item and create a new content item if you want to update the name).
        :param pulumi.Input[str] parent_id: The identifier of the folder to import into. Identifiers from the Library in the Sumo user interface are provided in decimal format which is incompatible with this provider. The identifier needs to be in hexadecimal format.
        """
        pulumi.set(__self__, "config", config)
        pulumi.set(__self__, "parent_id", parent_id)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Input[str]:
        """
        JSON block for the content to import. NOTE: Updating the name will create a new object and leave a untracked content item (delete the existing content item and create a new content item if you want to update the name).
        """
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: pulumi.Input[str]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> pulumi.Input[str]:
        """
        The identifier of the folder to import into. Identifiers from the Library in the Sumo user interface are provided in decimal format which is incompatible with this provider. The identifier needs to be in hexadecimal format.
        """
        return pulumi.get(self, "parent_id")

    @parent_id.setter
    def parent_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent_id", value)


@pulumi.input_type
class _ContentState:
    def __init__(__self__, *,
                 config: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Content resources.
        :param pulumi.Input[str] config: JSON block for the content to import. NOTE: Updating the name will create a new object and leave a untracked content item (delete the existing content item and create a new content item if you want to update the name).
        :param pulumi.Input[str] parent_id: The identifier of the folder to import into. Identifiers from the Library in the Sumo user interface are provided in decimal format which is incompatible with this provider. The identifier needs to be in hexadecimal format.
        """
        if config is not None:
            pulumi.set(__self__, "config", config)
        if parent_id is not None:
            pulumi.set(__self__, "parent_id", parent_id)

    @property
    @pulumi.getter
    def config(self) -> Optional[pulumi.Input[str]]:
        """
        JSON block for the content to import. NOTE: Updating the name will create a new object and leave a untracked content item (delete the existing content item and create a new content item if you want to update the name).
        """
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the folder to import into. Identifiers from the Library in the Sumo user interface are provided in decimal format which is incompatible with this provider. The identifier needs to be in hexadecimal format.
        """
        return pulumi.get(self, "parent_id")

    @parent_id.setter
    def parent_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_id", value)


class Content(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_sumologic as sumologic

        personal_folder = sumologic.get_personal_folder()
        test = sumologic.Content("test",
            parent_id=personal_folder.id,
            config=json.dumps({
                "type": "SavedSearchWithScheduleSyncDefinition",
                "name": "test-333",
                "search": {
                    "queryText": "\\"warn\\"",
                    "defaultTimeRange": "-15m",
                    "byReceiptTime": False,
                    "viewName": "",
                    "viewStartTime": "1970-01-01T00:00:00Z",
                    "queryParameters": [],
                    "parsingMode": "Manual",
                },
                "searchSchedule": {
                    "cronExpression": "0 0 * * * ? *",
                    "displayableTimeRange": "-10m",
                    "parseableTimeRange": {
                        "type": "BeginBoundedTimeRange",
                        "from": {
                            "type": "RelativeTimeRangeBoundary",
                            "relativeTime": "-50m",
                        },
                        "to": None,
                    },
                    "timeZone": "America/Los_Angeles",
                    "threshold": {
                        "operator": "gt",
                        "count": 0,
                    },
                    "notification": {
                        "taskType": "EmailSearchNotificationSyncDefinition",
                        "toList": ["ops@acme.org"],
                        "subjectTemplate": "Search Results: {{Name}}",
                        "includeQuery": True,
                        "includeResultSet": True,
                        "includeHistogram": False,
                        "includeCsvAttachment": False,
                    },
                    "scheduleType": "1Hour",
                    "muteErrorEmails": False,
                    "parameters": [],
                },
                "description": "Runs every hour with timerange of 15m and sends email notifications",
            }))
        ```
        ## Attributes reference

        The following attributes are exported:

        - `id` - Unique identifier for the content item.

        [1]: https://help.sumologic.com/APIs/Content-Management-API

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] config: JSON block for the content to import. NOTE: Updating the name will create a new object and leave a untracked content item (delete the existing content item and create a new content item if you want to update the name).
        :param pulumi.Input[str] parent_id: The identifier of the folder to import into. Identifiers from the Library in the Sumo user interface are provided in decimal format which is incompatible with this provider. The identifier needs to be in hexadecimal format.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_sumologic as sumologic

        personal_folder = sumologic.get_personal_folder()
        test = sumologic.Content("test",
            parent_id=personal_folder.id,
            config=json.dumps({
                "type": "SavedSearchWithScheduleSyncDefinition",
                "name": "test-333",
                "search": {
                    "queryText": "\\"warn\\"",
                    "defaultTimeRange": "-15m",
                    "byReceiptTime": False,
                    "viewName": "",
                    "viewStartTime": "1970-01-01T00:00:00Z",
                    "queryParameters": [],
                    "parsingMode": "Manual",
                },
                "searchSchedule": {
                    "cronExpression": "0 0 * * * ? *",
                    "displayableTimeRange": "-10m",
                    "parseableTimeRange": {
                        "type": "BeginBoundedTimeRange",
                        "from": {
                            "type": "RelativeTimeRangeBoundary",
                            "relativeTime": "-50m",
                        },
                        "to": None,
                    },
                    "timeZone": "America/Los_Angeles",
                    "threshold": {
                        "operator": "gt",
                        "count": 0,
                    },
                    "notification": {
                        "taskType": "EmailSearchNotificationSyncDefinition",
                        "toList": ["ops@acme.org"],
                        "subjectTemplate": "Search Results: {{Name}}",
                        "includeQuery": True,
                        "includeResultSet": True,
                        "includeHistogram": False,
                        "includeCsvAttachment": False,
                    },
                    "scheduleType": "1Hour",
                    "muteErrorEmails": False,
                    "parameters": [],
                },
                "description": "Runs every hour with timerange of 15m and sends email notifications",
            }))
        ```
        ## Attributes reference

        The following attributes are exported:

        - `id` - Unique identifier for the content item.

        [1]: https://help.sumologic.com/APIs/Content-Management-API

        :param str resource_name: The name of the resource.
        :param ContentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContentArgs.__new__(ContentArgs)

            if config is None and not opts.urn:
                raise TypeError("Missing required property 'config'")
            __props__.__dict__["config"] = config
            if parent_id is None and not opts.urn:
                raise TypeError("Missing required property 'parent_id'")
            __props__.__dict__["parent_id"] = parent_id
        super(Content, __self__).__init__(
            'sumologic:index/content:Content',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            config: Optional[pulumi.Input[str]] = None,
            parent_id: Optional[pulumi.Input[str]] = None) -> 'Content':
        """
        Get an existing Content resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] config: JSON block for the content to import. NOTE: Updating the name will create a new object and leave a untracked content item (delete the existing content item and create a new content item if you want to update the name).
        :param pulumi.Input[str] parent_id: The identifier of the folder to import into. Identifiers from the Library in the Sumo user interface are provided in decimal format which is incompatible with this provider. The identifier needs to be in hexadecimal format.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ContentState.__new__(_ContentState)

        __props__.__dict__["config"] = config
        __props__.__dict__["parent_id"] = parent_id
        return Content(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output[str]:
        """
        JSON block for the content to import. NOTE: Updating the name will create a new object and leave a untracked content item (delete the existing content item and create a new content item if you want to update the name).
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> pulumi.Output[str]:
        """
        The identifier of the folder to import into. Identifiers from the Library in the Sumo user interface are provided in decimal format which is incompatible with this provider. The identifier needs to be in hexadecimal format.
        """
        return pulumi.get(self, "parent_id")

