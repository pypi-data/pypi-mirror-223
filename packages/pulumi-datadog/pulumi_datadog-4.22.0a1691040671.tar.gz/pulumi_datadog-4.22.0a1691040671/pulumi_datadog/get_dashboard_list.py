# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetDashboardListResult',
    'AwaitableGetDashboardListResult',
    'get_dashboard_list',
    'get_dashboard_list_output',
]

@pulumi.output_type
class GetDashboardListResult:
    """
    A collection of values returned by getDashboardList.
    """
    def __init__(__self__, id=None, name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A dashboard list name to limit the search.
        """
        return pulumi.get(self, "name")


class AwaitableGetDashboardListResult(GetDashboardListResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDashboardListResult(
            id=self.id,
            name=self.name)


def get_dashboard_list(name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDashboardListResult:
    """
    Use this data source to retrieve information about an existing dashboard list, for use in other resources. In particular, it can be used in a dashboard to register it in the list.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_datadog as datadog

    test = datadog.get_dashboard_list(name="My super list")
    # Create a dashboard and register it in the list above.
    time = datadog.Dashboard("time",
        dashboard_lists=[test.id],
        description="Created using the Datadog provider in Terraform",
        is_read_only=True,
        layout_type="ordered",
        title="TF Test Layout Dashboard",
        widgets=[datadog.DashboardWidgetArgs(
            alert_graph_definition=datadog.DashboardWidgetAlertGraphDefinitionArgs(
                alert_id="1234",
                live_span="1h",
                title="Widget Title",
                viz_type="timeseries",
            ),
        )])
    ```


    :param str name: A dashboard list name to limit the search.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('datadog:index/getDashboardList:getDashboardList', __args__, opts=opts, typ=GetDashboardListResult).value

    return AwaitableGetDashboardListResult(
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'))


@_utilities.lift_output_func(get_dashboard_list)
def get_dashboard_list_output(name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDashboardListResult]:
    """
    Use this data source to retrieve information about an existing dashboard list, for use in other resources. In particular, it can be used in a dashboard to register it in the list.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_datadog as datadog

    test = datadog.get_dashboard_list(name="My super list")
    # Create a dashboard and register it in the list above.
    time = datadog.Dashboard("time",
        dashboard_lists=[test.id],
        description="Created using the Datadog provider in Terraform",
        is_read_only=True,
        layout_type="ordered",
        title="TF Test Layout Dashboard",
        widgets=[datadog.DashboardWidgetArgs(
            alert_graph_definition=datadog.DashboardWidgetAlertGraphDefinitionArgs(
                alert_id="1234",
                live_span="1h",
                title="Widget Title",
                viz_type="timeseries",
            ),
        )])
    ```


    :param str name: A dashboard list name to limit the search.
    """
    ...
