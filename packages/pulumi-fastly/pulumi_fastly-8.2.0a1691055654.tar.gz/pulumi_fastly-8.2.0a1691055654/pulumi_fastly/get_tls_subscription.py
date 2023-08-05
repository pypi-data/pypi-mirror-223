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
    'GetTlsSubscriptionResult',
    'AwaitableGetTlsSubscriptionResult',
    'get_tls_subscription',
    'get_tls_subscription_output',
]

@pulumi.output_type
class GetTlsSubscriptionResult:
    """
    A collection of values returned by getTlsSubscription.
    """
    def __init__(__self__, certificate_authority=None, common_name=None, configuration_id=None, created_at=None, domains=None, id=None, state=None, updated_at=None):
        if certificate_authority and not isinstance(certificate_authority, str):
            raise TypeError("Expected argument 'certificate_authority' to be a str")
        pulumi.set(__self__, "certificate_authority", certificate_authority)
        if common_name and not isinstance(common_name, str):
            raise TypeError("Expected argument 'common_name' to be a str")
        pulumi.set(__self__, "common_name", common_name)
        if configuration_id and not isinstance(configuration_id, str):
            raise TypeError("Expected argument 'configuration_id' to be a str")
        pulumi.set(__self__, "configuration_id", configuration_id)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if domains and not isinstance(domains, list):
            raise TypeError("Expected argument 'domains' to be a list")
        pulumi.set(__self__, "domains", domains)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="certificateAuthority")
    def certificate_authority(self) -> str:
        """
        The entity that issues and certifies the TLS certificates for the subscription.
        """
        return pulumi.get(self, "certificate_authority")

    @property
    @pulumi.getter(name="commonName")
    def common_name(self) -> str:
        """
        The common name associated with the subscription generated by Fastly TLS.
        """
        return pulumi.get(self, "common_name")

    @property
    @pulumi.getter(name="configurationId")
    def configuration_id(self) -> str:
        """
        ID of TLS configuration used to terminate TLS traffic.
        """
        return pulumi.get(self, "configuration_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Timestamp (GMT) when subscription was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def domains(self) -> Sequence[str]:
        """
        List of domains on which to enable TLS.
        """
        return pulumi.get(self, "domains")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of TLS subscription. Conflicts with all the other filters.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current state of the subscription. The list of possible states are: `pending`, `processing`, `issued`, and `renewing`.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        Timestamp (GMT) when subscription was last updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetTlsSubscriptionResult(GetTlsSubscriptionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTlsSubscriptionResult(
            certificate_authority=self.certificate_authority,
            common_name=self.common_name,
            configuration_id=self.configuration_id,
            created_at=self.created_at,
            domains=self.domains,
            id=self.id,
            state=self.state,
            updated_at=self.updated_at)


def get_tls_subscription(certificate_authority: Optional[str] = None,
                         configuration_id: Optional[str] = None,
                         domains: Optional[Sequence[str]] = None,
                         id: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTlsSubscriptionResult:
    """
    Use this data source to get information about a TLS subscription.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    example = fastly.get_tls_subscription(domains=["example.com"])
    ```


    :param str certificate_authority: The entity that issues and certifies the TLS certificates for the subscription.
    :param str configuration_id: ID of TLS configuration used to terminate TLS traffic.
    :param Sequence[str] domains: List of domains on which to enable TLS.
    :param str id: ID of TLS subscription. Conflicts with all the other filters.
    """
    __args__ = dict()
    __args__['certificateAuthority'] = certificate_authority
    __args__['configurationId'] = configuration_id
    __args__['domains'] = domains
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fastly:index/getTlsSubscription:getTlsSubscription', __args__, opts=opts, typ=GetTlsSubscriptionResult).value

    return AwaitableGetTlsSubscriptionResult(
        certificate_authority=pulumi.get(__ret__, 'certificate_authority'),
        common_name=pulumi.get(__ret__, 'common_name'),
        configuration_id=pulumi.get(__ret__, 'configuration_id'),
        created_at=pulumi.get(__ret__, 'created_at'),
        domains=pulumi.get(__ret__, 'domains'),
        id=pulumi.get(__ret__, 'id'),
        state=pulumi.get(__ret__, 'state'),
        updated_at=pulumi.get(__ret__, 'updated_at'))


@_utilities.lift_output_func(get_tls_subscription)
def get_tls_subscription_output(certificate_authority: Optional[pulumi.Input[Optional[str]]] = None,
                                configuration_id: Optional[pulumi.Input[Optional[str]]] = None,
                                domains: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                id: Optional[pulumi.Input[Optional[str]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTlsSubscriptionResult]:
    """
    Use this data source to get information about a TLS subscription.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    example = fastly.get_tls_subscription(domains=["example.com"])
    ```


    :param str certificate_authority: The entity that issues and certifies the TLS certificates for the subscription.
    :param str configuration_id: ID of TLS configuration used to terminate TLS traffic.
    :param Sequence[str] domains: List of domains on which to enable TLS.
    :param str id: ID of TLS subscription. Conflicts with all the other filters.
    """
    ...
