# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ExternalLinkArgs', 'ExternalLink']

@pulumi.input_type
class ExternalLinkArgs:
    def __init__(__self__, *,
                 description: pulumi.Input[str],
                 template: pulumi.Input[str],
                 is_log_integration: Optional[pulumi.Input[bool]] = None,
                 metric_filter_regex: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 point_tag_filter_regexes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 source_filter_regex: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ExternalLink resource.
        :param pulumi.Input[str] description: Human-readable description for this link.
        :param pulumi.Input[str] template: The mustache template for this link. The template must expand to a full URL, including scheme, origin, etc.
        :param pulumi.Input[bool] is_log_integration: Whether this is a "Log Integration" subType of external link.
        :param pulumi.Input[str] metric_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        :param pulumi.Input[str] name: The name of the external link.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] point_tag_filter_regexes: Controls whether a link is displayed in the context menu of a highlighted
               series. This is a map from string to regular expression. The highlighted series must contain point tags whose
               keys are present in the keys of this map and whose values match the regular expressions associated with those
               keys in order for the link to be displayed.
        :param pulumi.Input[str] source_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "template", template)
        if is_log_integration is not None:
            pulumi.set(__self__, "is_log_integration", is_log_integration)
        if metric_filter_regex is not None:
            pulumi.set(__self__, "metric_filter_regex", metric_filter_regex)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if point_tag_filter_regexes is not None:
            pulumi.set(__self__, "point_tag_filter_regexes", point_tag_filter_regexes)
        if source_filter_regex is not None:
            pulumi.set(__self__, "source_filter_regex", source_filter_regex)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        Human-readable description for this link.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def template(self) -> pulumi.Input[str]:
        """
        The mustache template for this link. The template must expand to a full URL, including scheme, origin, etc.
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: pulumi.Input[str]):
        pulumi.set(self, "template", value)

    @property
    @pulumi.getter(name="isLogIntegration")
    def is_log_integration(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this is a "Log Integration" subType of external link.
        """
        return pulumi.get(self, "is_log_integration")

    @is_log_integration.setter
    def is_log_integration(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_log_integration", value)

    @property
    @pulumi.getter(name="metricFilterRegex")
    def metric_filter_regex(self) -> Optional[pulumi.Input[str]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "metric_filter_regex")

    @metric_filter_regex.setter
    def metric_filter_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_filter_regex", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the external link.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="pointTagFilterRegexes")
    def point_tag_filter_regexes(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted
        series. This is a map from string to regular expression. The highlighted series must contain point tags whose
        keys are present in the keys of this map and whose values match the regular expressions associated with those
        keys in order for the link to be displayed.
        """
        return pulumi.get(self, "point_tag_filter_regexes")

    @point_tag_filter_regexes.setter
    def point_tag_filter_regexes(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "point_tag_filter_regexes", value)

    @property
    @pulumi.getter(name="sourceFilterRegex")
    def source_filter_regex(self) -> Optional[pulumi.Input[str]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "source_filter_regex")

    @source_filter_regex.setter
    def source_filter_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_filter_regex", value)


@pulumi.input_type
class _ExternalLinkState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 is_log_integration: Optional[pulumi.Input[bool]] = None,
                 metric_filter_regex: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 point_tag_filter_regexes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 source_filter_regex: Optional[pulumi.Input[str]] = None,
                 template: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ExternalLink resources.
        :param pulumi.Input[str] description: Human-readable description for this link.
        :param pulumi.Input[bool] is_log_integration: Whether this is a "Log Integration" subType of external link.
        :param pulumi.Input[str] metric_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        :param pulumi.Input[str] name: The name of the external link.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] point_tag_filter_regexes: Controls whether a link is displayed in the context menu of a highlighted
               series. This is a map from string to regular expression. The highlighted series must contain point tags whose
               keys are present in the keys of this map and whose values match the regular expressions associated with those
               keys in order for the link to be displayed.
        :param pulumi.Input[str] source_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        :param pulumi.Input[str] template: The mustache template for this link. The template must expand to a full URL, including scheme, origin, etc.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_log_integration is not None:
            pulumi.set(__self__, "is_log_integration", is_log_integration)
        if metric_filter_regex is not None:
            pulumi.set(__self__, "metric_filter_regex", metric_filter_regex)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if point_tag_filter_regexes is not None:
            pulumi.set(__self__, "point_tag_filter_regexes", point_tag_filter_regexes)
        if source_filter_regex is not None:
            pulumi.set(__self__, "source_filter_regex", source_filter_regex)
        if template is not None:
            pulumi.set(__self__, "template", template)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Human-readable description for this link.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isLogIntegration")
    def is_log_integration(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this is a "Log Integration" subType of external link.
        """
        return pulumi.get(self, "is_log_integration")

    @is_log_integration.setter
    def is_log_integration(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_log_integration", value)

    @property
    @pulumi.getter(name="metricFilterRegex")
    def metric_filter_regex(self) -> Optional[pulumi.Input[str]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "metric_filter_regex")

    @metric_filter_regex.setter
    def metric_filter_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_filter_regex", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the external link.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="pointTagFilterRegexes")
    def point_tag_filter_regexes(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted
        series. This is a map from string to regular expression. The highlighted series must contain point tags whose
        keys are present in the keys of this map and whose values match the regular expressions associated with those
        keys in order for the link to be displayed.
        """
        return pulumi.get(self, "point_tag_filter_regexes")

    @point_tag_filter_regexes.setter
    def point_tag_filter_regexes(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "point_tag_filter_regexes", value)

    @property
    @pulumi.getter(name="sourceFilterRegex")
    def source_filter_regex(self) -> Optional[pulumi.Input[str]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "source_filter_regex")

    @source_filter_regex.setter
    def source_filter_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_filter_regex", value)

    @property
    @pulumi.getter
    def template(self) -> Optional[pulumi.Input[str]]:
        """
        The mustache template for this link. The template must expand to a full URL, including scheme, origin, etc.
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template", value)


class ExternalLink(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_log_integration: Optional[pulumi.Input[bool]] = None,
                 metric_filter_regex: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 point_tag_filter_regexes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 source_filter_regex: Optional[pulumi.Input[str]] = None,
                 template: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Wavefront External Link Resource. This allows external links to be created, updated, and deleted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_wavefront as wavefront

        basic = wavefront.ExternalLink("basic",
            description="An external link description",
            template="https://example.com/source={{{source}}}&startTime={{startEpochMillis}}")
        ```

        ## Import

        Maintenance windows can be imported by using the `id`, e.g.

        ```sh
         $ pulumi import wavefront:index/externalLink:ExternalLink basic fVj6fz6zYC4aBkID
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Human-readable description for this link.
        :param pulumi.Input[bool] is_log_integration: Whether this is a "Log Integration" subType of external link.
        :param pulumi.Input[str] metric_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        :param pulumi.Input[str] name: The name of the external link.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] point_tag_filter_regexes: Controls whether a link is displayed in the context menu of a highlighted
               series. This is a map from string to regular expression. The highlighted series must contain point tags whose
               keys are present in the keys of this map and whose values match the regular expressions associated with those
               keys in order for the link to be displayed.
        :param pulumi.Input[str] source_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        :param pulumi.Input[str] template: The mustache template for this link. The template must expand to a full URL, including scheme, origin, etc.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ExternalLinkArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Wavefront External Link Resource. This allows external links to be created, updated, and deleted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_wavefront as wavefront

        basic = wavefront.ExternalLink("basic",
            description="An external link description",
            template="https://example.com/source={{{source}}}&startTime={{startEpochMillis}}")
        ```

        ## Import

        Maintenance windows can be imported by using the `id`, e.g.

        ```sh
         $ pulumi import wavefront:index/externalLink:ExternalLink basic fVj6fz6zYC4aBkID
        ```

        :param str resource_name: The name of the resource.
        :param ExternalLinkArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ExternalLinkArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_log_integration: Optional[pulumi.Input[bool]] = None,
                 metric_filter_regex: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 point_tag_filter_regexes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 source_filter_regex: Optional[pulumi.Input[str]] = None,
                 template: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ExternalLinkArgs.__new__(ExternalLinkArgs)

            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            __props__.__dict__["is_log_integration"] = is_log_integration
            __props__.__dict__["metric_filter_regex"] = metric_filter_regex
            __props__.__dict__["name"] = name
            __props__.__dict__["point_tag_filter_regexes"] = point_tag_filter_regexes
            __props__.__dict__["source_filter_regex"] = source_filter_regex
            if template is None and not opts.urn:
                raise TypeError("Missing required property 'template'")
            __props__.__dict__["template"] = template
        super(ExternalLink, __self__).__init__(
            'wavefront:index/externalLink:ExternalLink',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            is_log_integration: Optional[pulumi.Input[bool]] = None,
            metric_filter_regex: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            point_tag_filter_regexes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            source_filter_regex: Optional[pulumi.Input[str]] = None,
            template: Optional[pulumi.Input[str]] = None) -> 'ExternalLink':
        """
        Get an existing ExternalLink resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Human-readable description for this link.
        :param pulumi.Input[bool] is_log_integration: Whether this is a "Log Integration" subType of external link.
        :param pulumi.Input[str] metric_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        :param pulumi.Input[str] name: The name of the external link.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] point_tag_filter_regexes: Controls whether a link is displayed in the context menu of a highlighted
               series. This is a map from string to regular expression. The highlighted series must contain point tags whose
               keys are present in the keys of this map and whose values match the regular expressions associated with those
               keys in order for the link to be displayed.
        :param pulumi.Input[str] source_filter_regex: Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        :param pulumi.Input[str] template: The mustache template for this link. The template must expand to a full URL, including scheme, origin, etc.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ExternalLinkState.__new__(_ExternalLinkState)

        __props__.__dict__["description"] = description
        __props__.__dict__["is_log_integration"] = is_log_integration
        __props__.__dict__["metric_filter_regex"] = metric_filter_regex
        __props__.__dict__["name"] = name
        __props__.__dict__["point_tag_filter_regexes"] = point_tag_filter_regexes
        __props__.__dict__["source_filter_regex"] = source_filter_regex
        __props__.__dict__["template"] = template
        return ExternalLink(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Human-readable description for this link.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="isLogIntegration")
    def is_log_integration(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether this is a "Log Integration" subType of external link.
        """
        return pulumi.get(self, "is_log_integration")

    @property
    @pulumi.getter(name="metricFilterRegex")
    def metric_filter_regex(self) -> pulumi.Output[Optional[str]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "metric_filter_regex")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the external link.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pointTagFilterRegexes")
    def point_tag_filter_regexes(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted
        series. This is a map from string to regular expression. The highlighted series must contain point tags whose
        keys are present in the keys of this map and whose values match the regular expressions associated with those
        keys in order for the link to be displayed.
        """
        return pulumi.get(self, "point_tag_filter_regexes")

    @property
    @pulumi.getter(name="sourceFilterRegex")
    def source_filter_regex(self) -> pulumi.Output[Optional[str]]:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "source_filter_regex")

    @property
    @pulumi.getter
    def template(self) -> pulumi.Output[str]:
        """
        The mustache template for this link. The template must expand to a full URL, including scheme, origin, etc.
        """
        return pulumi.get(self, "template")

