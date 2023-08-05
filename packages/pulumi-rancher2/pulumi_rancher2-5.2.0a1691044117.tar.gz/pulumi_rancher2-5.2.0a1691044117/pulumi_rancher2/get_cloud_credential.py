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
    'GetCloudCredentialResult',
    'AwaitableGetCloudCredentialResult',
    'get_cloud_credential',
    'get_cloud_credential_output',
]

@pulumi.output_type
class GetCloudCredentialResult:
    """
    A collection of values returned by getCloudCredential.
    """
    def __init__(__self__, annotations=None, id=None, labels=None, name=None):
        if annotations and not isinstance(annotations, dict):
            raise TypeError("Expected argument 'annotations' to be a dict")
        pulumi.set(__self__, "annotations", annotations)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def annotations(self) -> Mapping[str, Any]:
        """
        (Computed) Annotations for the Cloud Credential (map)
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, Any]:
        """
        (Computed) Labels for the Cloud Credential (map)
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


class AwaitableGetCloudCredentialResult(GetCloudCredentialResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudCredentialResult(
            annotations=self.annotations,
            id=self.id,
            labels=self.labels,
            name=self.name)


def get_cloud_credential(name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudCredentialResult:
    """
    Use this data source to retrieve information about a Rancher v2 Cloud Credential.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_rancher2 as rancher2

    test = rancher2.get_cloud_credential(name="test")
    ```


    :param str name: The Cloud Credential name.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('rancher2:index/getCloudCredential:getCloudCredential', __args__, opts=opts, typ=GetCloudCredentialResult).value

    return AwaitableGetCloudCredentialResult(
        annotations=__ret__.annotations,
        id=__ret__.id,
        labels=__ret__.labels,
        name=__ret__.name)


@_utilities.lift_output_func(get_cloud_credential)
def get_cloud_credential_output(name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCloudCredentialResult]:
    """
    Use this data source to retrieve information about a Rancher v2 Cloud Credential.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_rancher2 as rancher2

    test = rancher2.get_cloud_credential(name="test")
    ```


    :param str name: The Cloud Credential name.
    """
    ...
