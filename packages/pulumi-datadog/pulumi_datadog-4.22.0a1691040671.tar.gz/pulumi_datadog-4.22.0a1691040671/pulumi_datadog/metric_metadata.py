# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['MetricMetadataArgs', 'MetricMetadata']

@pulumi.input_type
class MetricMetadataArgs:
    def __init__(__self__, *,
                 metric: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 per_unit: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 statsd_interval: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unit: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MetricMetadata resource.
        :param pulumi.Input[str] metric: The name of the metric.
        :param pulumi.Input[str] description: A description of the metric.
        :param pulumi.Input[str] per_unit: Per unit of the metric such as `second` in `bytes per second`.
        :param pulumi.Input[str] short_name: A short name of the metric.
        :param pulumi.Input[int] statsd_interval: If applicable, statsd flush interval in seconds for the metric.
        :param pulumi.Input[str] type: Metric type such as `gauge` or `rate`.
        :param pulumi.Input[str] unit: Primary unit of the metric such as `byte` or `operation`.
        """
        pulumi.set(__self__, "metric", metric)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if per_unit is not None:
            pulumi.set(__self__, "per_unit", per_unit)
        if short_name is not None:
            pulumi.set(__self__, "short_name", short_name)
        if statsd_interval is not None:
            pulumi.set(__self__, "statsd_interval", statsd_interval)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def metric(self) -> pulumi.Input[str]:
        """
        The name of the metric.
        """
        return pulumi.get(self, "metric")

    @metric.setter
    def metric(self, value: pulumi.Input[str]):
        pulumi.set(self, "metric", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the metric.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="perUnit")
    def per_unit(self) -> Optional[pulumi.Input[str]]:
        """
        Per unit of the metric such as `second` in `bytes per second`.
        """
        return pulumi.get(self, "per_unit")

    @per_unit.setter
    def per_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "per_unit", value)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> Optional[pulumi.Input[str]]:
        """
        A short name of the metric.
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "short_name", value)

    @property
    @pulumi.getter(name="statsdInterval")
    def statsd_interval(self) -> Optional[pulumi.Input[int]]:
        """
        If applicable, statsd flush interval in seconds for the metric.
        """
        return pulumi.get(self, "statsd_interval")

    @statsd_interval.setter
    def statsd_interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "statsd_interval", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Metric type such as `gauge` or `rate`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def unit(self) -> Optional[pulumi.Input[str]]:
        """
        Primary unit of the metric such as `byte` or `operation`.
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unit", value)


@pulumi.input_type
class _MetricMetadataState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 metric: Optional[pulumi.Input[str]] = None,
                 per_unit: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 statsd_interval: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unit: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MetricMetadata resources.
        :param pulumi.Input[str] description: A description of the metric.
        :param pulumi.Input[str] metric: The name of the metric.
        :param pulumi.Input[str] per_unit: Per unit of the metric such as `second` in `bytes per second`.
        :param pulumi.Input[str] short_name: A short name of the metric.
        :param pulumi.Input[int] statsd_interval: If applicable, statsd flush interval in seconds for the metric.
        :param pulumi.Input[str] type: Metric type such as `gauge` or `rate`.
        :param pulumi.Input[str] unit: Primary unit of the metric such as `byte` or `operation`.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if metric is not None:
            pulumi.set(__self__, "metric", metric)
        if per_unit is not None:
            pulumi.set(__self__, "per_unit", per_unit)
        if short_name is not None:
            pulumi.set(__self__, "short_name", short_name)
        if statsd_interval is not None:
            pulumi.set(__self__, "statsd_interval", statsd_interval)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the metric.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def metric(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the metric.
        """
        return pulumi.get(self, "metric")

    @metric.setter
    def metric(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric", value)

    @property
    @pulumi.getter(name="perUnit")
    def per_unit(self) -> Optional[pulumi.Input[str]]:
        """
        Per unit of the metric such as `second` in `bytes per second`.
        """
        return pulumi.get(self, "per_unit")

    @per_unit.setter
    def per_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "per_unit", value)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> Optional[pulumi.Input[str]]:
        """
        A short name of the metric.
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "short_name", value)

    @property
    @pulumi.getter(name="statsdInterval")
    def statsd_interval(self) -> Optional[pulumi.Input[int]]:
        """
        If applicable, statsd flush interval in seconds for the metric.
        """
        return pulumi.get(self, "statsd_interval")

    @statsd_interval.setter
    def statsd_interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "statsd_interval", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Metric type such as `gauge` or `rate`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def unit(self) -> Optional[pulumi.Input[str]]:
        """
        Primary unit of the metric such as `byte` or `operation`.
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unit", value)


class MetricMetadata(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 metric: Optional[pulumi.Input[str]] = None,
                 per_unit: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 statsd_interval: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unit: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Datadog metric_metadata resource. This can be used to manage a metric's metadata.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Manage a Datadog metric's metadata
        request_time = datadog.MetricMetadata("requestTime",
            description="99th percentile request time in millseconds",
            metric="request.time",
            short_name="Request time",
            type="gauge",
            unit="millisecond")
        ```

        ## Import

        ```sh
         $ pulumi import datadog:index/metricMetadata:MetricMetadata request_time request.time
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of the metric.
        :param pulumi.Input[str] metric: The name of the metric.
        :param pulumi.Input[str] per_unit: Per unit of the metric such as `second` in `bytes per second`.
        :param pulumi.Input[str] short_name: A short name of the metric.
        :param pulumi.Input[int] statsd_interval: If applicable, statsd flush interval in seconds for the metric.
        :param pulumi.Input[str] type: Metric type such as `gauge` or `rate`.
        :param pulumi.Input[str] unit: Primary unit of the metric such as `byte` or `operation`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MetricMetadataArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog metric_metadata resource. This can be used to manage a metric's metadata.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Manage a Datadog metric's metadata
        request_time = datadog.MetricMetadata("requestTime",
            description="99th percentile request time in millseconds",
            metric="request.time",
            short_name="Request time",
            type="gauge",
            unit="millisecond")
        ```

        ## Import

        ```sh
         $ pulumi import datadog:index/metricMetadata:MetricMetadata request_time request.time
        ```

        :param str resource_name: The name of the resource.
        :param MetricMetadataArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MetricMetadataArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 metric: Optional[pulumi.Input[str]] = None,
                 per_unit: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 statsd_interval: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unit: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MetricMetadataArgs.__new__(MetricMetadataArgs)

            __props__.__dict__["description"] = description
            if metric is None and not opts.urn:
                raise TypeError("Missing required property 'metric'")
            __props__.__dict__["metric"] = metric
            __props__.__dict__["per_unit"] = per_unit
            __props__.__dict__["short_name"] = short_name
            __props__.__dict__["statsd_interval"] = statsd_interval
            __props__.__dict__["type"] = type
            __props__.__dict__["unit"] = unit
        super(MetricMetadata, __self__).__init__(
            'datadog:index/metricMetadata:MetricMetadata',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            metric: Optional[pulumi.Input[str]] = None,
            per_unit: Optional[pulumi.Input[str]] = None,
            short_name: Optional[pulumi.Input[str]] = None,
            statsd_interval: Optional[pulumi.Input[int]] = None,
            type: Optional[pulumi.Input[str]] = None,
            unit: Optional[pulumi.Input[str]] = None) -> 'MetricMetadata':
        """
        Get an existing MetricMetadata resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of the metric.
        :param pulumi.Input[str] metric: The name of the metric.
        :param pulumi.Input[str] per_unit: Per unit of the metric such as `second` in `bytes per second`.
        :param pulumi.Input[str] short_name: A short name of the metric.
        :param pulumi.Input[int] statsd_interval: If applicable, statsd flush interval in seconds for the metric.
        :param pulumi.Input[str] type: Metric type such as `gauge` or `rate`.
        :param pulumi.Input[str] unit: Primary unit of the metric such as `byte` or `operation`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MetricMetadataState.__new__(_MetricMetadataState)

        __props__.__dict__["description"] = description
        __props__.__dict__["metric"] = metric
        __props__.__dict__["per_unit"] = per_unit
        __props__.__dict__["short_name"] = short_name
        __props__.__dict__["statsd_interval"] = statsd_interval
        __props__.__dict__["type"] = type
        __props__.__dict__["unit"] = unit
        return MetricMetadata(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the metric.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def metric(self) -> pulumi.Output[str]:
        """
        The name of the metric.
        """
        return pulumi.get(self, "metric")

    @property
    @pulumi.getter(name="perUnit")
    def per_unit(self) -> pulumi.Output[Optional[str]]:
        """
        Per unit of the metric such as `second` in `bytes per second`.
        """
        return pulumi.get(self, "per_unit")

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Output[Optional[str]]:
        """
        A short name of the metric.
        """
        return pulumi.get(self, "short_name")

    @property
    @pulumi.getter(name="statsdInterval")
    def statsd_interval(self) -> pulumi.Output[Optional[int]]:
        """
        If applicable, statsd flush interval in seconds for the metric.
        """
        return pulumi.get(self, "statsd_interval")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Metric type such as `gauge` or `rate`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def unit(self) -> pulumi.Output[Optional[str]]:
        """
        Primary unit of the metric such as `byte` or `operation`.
        """
        return pulumi.get(self, "unit")

