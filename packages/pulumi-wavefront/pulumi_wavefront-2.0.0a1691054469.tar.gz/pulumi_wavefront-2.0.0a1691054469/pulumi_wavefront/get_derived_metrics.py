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

__all__ = [
    'GetDerivedMetricsResult',
    'AwaitableGetDerivedMetricsResult',
    'get_derived_metrics',
    'get_derived_metrics_output',
]

@pulumi.output_type
class GetDerivedMetricsResult:
    """
    A collection of values returned by getDerivedMetrics.
    """
    def __init__(__self__, derived_metrics=None, id=None, limit=None, offset=None):
        if derived_metrics and not isinstance(derived_metrics, list):
            raise TypeError("Expected argument 'derived_metrics' to be a list")
        pulumi.set(__self__, "derived_metrics", derived_metrics)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if limit and not isinstance(limit, int):
            raise TypeError("Expected argument 'limit' to be a int")
        pulumi.set(__self__, "limit", limit)
        if offset and not isinstance(offset, int):
            raise TypeError("Expected argument 'offset' to be a int")
        pulumi.set(__self__, "offset", offset)

    @property
    @pulumi.getter(name="derivedMetrics")
    def derived_metrics(self) -> Sequence['outputs.GetDerivedMetricsDerivedMetricResult']:
        """
        List of all derived metrics in Wavefront. For each derived metric you will see a list of attributes.
        """
        return pulumi.get(self, "derived_metrics")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def limit(self) -> Optional[int]:
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def offset(self) -> Optional[int]:
        return pulumi.get(self, "offset")


class AwaitableGetDerivedMetricsResult(GetDerivedMetricsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDerivedMetricsResult(
            derived_metrics=self.derived_metrics,
            id=self.id,
            limit=self.limit,
            offset=self.offset)


def get_derived_metrics(limit: Optional[int] = None,
                        offset: Optional[int] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDerivedMetricsResult:
    """
    Use this data source to get information about all Wavefront derived metrics.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    example = wavefront.get_derived_metrics(limit=10,
        offset=0)
    ```


    :param int limit: Limit is the maximum number of results to be returned. Defaults to 100.
    :param int offset: Offset is the offset from the first result to be returned. Defaults to 0.
    """
    __args__ = dict()
    __args__['limit'] = limit
    __args__['offset'] = offset
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('wavefront:index/getDerivedMetrics:getDerivedMetrics', __args__, opts=opts, typ=GetDerivedMetricsResult).value

    return AwaitableGetDerivedMetricsResult(
        derived_metrics=pulumi.get(__ret__, 'derived_metrics'),
        id=pulumi.get(__ret__, 'id'),
        limit=pulumi.get(__ret__, 'limit'),
        offset=pulumi.get(__ret__, 'offset'))


@_utilities.lift_output_func(get_derived_metrics)
def get_derived_metrics_output(limit: Optional[pulumi.Input[Optional[int]]] = None,
                               offset: Optional[pulumi.Input[Optional[int]]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDerivedMetricsResult]:
    """
    Use this data source to get information about all Wavefront derived metrics.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    example = wavefront.get_derived_metrics(limit=10,
        offset=0)
    ```


    :param int limit: Limit is the maximum number of results to be returned. Defaults to 100.
    :param int offset: Offset is the offset from the first result to be returned. Defaults to 0.
    """
    ...
