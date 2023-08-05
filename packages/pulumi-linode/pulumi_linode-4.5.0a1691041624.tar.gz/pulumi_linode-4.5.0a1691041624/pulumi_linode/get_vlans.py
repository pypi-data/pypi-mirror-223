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

__all__ = [
    'GetVlansResult',
    'AwaitableGetVlansResult',
    'get_vlans',
    'get_vlans_output',
]

@pulumi.output_type
class GetVlansResult:
    """
    A collection of values returned by getVlans.
    """
    def __init__(__self__, filters=None, id=None, order=None, order_by=None, vlans=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if order and not isinstance(order, str):
            raise TypeError("Expected argument 'order' to be a str")
        pulumi.set(__self__, "order", order)
        if order_by and not isinstance(order_by, str):
            raise TypeError("Expected argument 'order_by' to be a str")
        pulumi.set(__self__, "order_by", order_by)
        if vlans and not isinstance(vlans, list):
            raise TypeError("Expected argument 'vlans' to be a list")
        pulumi.set(__self__, "vlans", vlans)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetVlansFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def order(self) -> Optional[str]:
        return pulumi.get(self, "order")

    @property
    @pulumi.getter(name="orderBy")
    def order_by(self) -> Optional[str]:
        return pulumi.get(self, "order_by")

    @property
    @pulumi.getter
    def vlans(self) -> Optional[Sequence['outputs.GetVlansVlanResult']]:
        return pulumi.get(self, "vlans")


class AwaitableGetVlansResult(GetVlansResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVlansResult(
            filters=self.filters,
            id=self.id,
            order=self.order,
            order_by=self.order_by,
            vlans=self.vlans)


def get_vlans(filters: Optional[Sequence[pulumi.InputType['GetVlansFilterArgs']]] = None,
              order: Optional[str] = None,
              order_by: Optional[str] = None,
              vlans: Optional[Sequence[pulumi.InputType['GetVlansVlanArgs']]] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVlansResult:
    """
    Provides details about Linode VLANs.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_linode as linode

    my_instance = linode.Instance("myInstance",
        label="my_instance",
        image="linode/ubuntu18.04",
        region="us-southeast",
        type="g6-standard-1",
        root_pass="bogusPassword$",
        interfaces=[linode.InstanceInterfaceArgs(
            purpose="vlan",
            label="my-vlan",
        )])
    my_vlans = linode.get_vlans(filters=[linode.GetVlansFilterArgs(
        name="label",
        values=["my-vlan"],
    )])
    pulumi.export("vlanLinodes", my_vlans.vlans[0].linodes)
    ```
    ## Filterable Fields

    * `label`

    * `region`


    :param str order: The order in which results should be returned. (`asc`, `desc`; default `asc`)
    :param str order_by: The attribute to order the results by. See the Filterable Fields section for a list of valid fields.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['order'] = order
    __args__['orderBy'] = order_by
    __args__['vlans'] = vlans
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('linode:index/getVlans:getVlans', __args__, opts=opts, typ=GetVlansResult).value

    return AwaitableGetVlansResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        order=pulumi.get(__ret__, 'order'),
        order_by=pulumi.get(__ret__, 'order_by'),
        vlans=pulumi.get(__ret__, 'vlans'))


@_utilities.lift_output_func(get_vlans)
def get_vlans_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetVlansFilterArgs']]]]] = None,
                     order: Optional[pulumi.Input[Optional[str]]] = None,
                     order_by: Optional[pulumi.Input[Optional[str]]] = None,
                     vlans: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetVlansVlanArgs']]]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVlansResult]:
    """
    Provides details about Linode VLANs.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_linode as linode

    my_instance = linode.Instance("myInstance",
        label="my_instance",
        image="linode/ubuntu18.04",
        region="us-southeast",
        type="g6-standard-1",
        root_pass="bogusPassword$",
        interfaces=[linode.InstanceInterfaceArgs(
            purpose="vlan",
            label="my-vlan",
        )])
    my_vlans = linode.get_vlans(filters=[linode.GetVlansFilterArgs(
        name="label",
        values=["my-vlan"],
    )])
    pulumi.export("vlanLinodes", my_vlans.vlans[0].linodes)
    ```
    ## Filterable Fields

    * `label`

    * `region`


    :param str order: The order in which results should be returned. (`asc`, `desc`; default `asc`)
    :param str order_by: The attribute to order the results by. See the Filterable Fields section for a list of valid fields.
    """
    ...
