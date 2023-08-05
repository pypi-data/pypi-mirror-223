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
    'GetTlsConfigurationResult',
    'AwaitableGetTlsConfigurationResult',
    'get_tls_configuration',
    'get_tls_configuration_output',
]

@pulumi.output_type
class GetTlsConfigurationResult:
    """
    A collection of values returned by getTlsConfiguration.
    """
    def __init__(__self__, created_at=None, default=None, dns_records=None, http_protocols=None, id=None, name=None, tls_protocols=None, tls_service=None, updated_at=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if default and not isinstance(default, bool):
            raise TypeError("Expected argument 'default' to be a bool")
        pulumi.set(__self__, "default", default)
        if dns_records and not isinstance(dns_records, list):
            raise TypeError("Expected argument 'dns_records' to be a list")
        pulumi.set(__self__, "dns_records", dns_records)
        if http_protocols and not isinstance(http_protocols, list):
            raise TypeError("Expected argument 'http_protocols' to be a list")
        pulumi.set(__self__, "http_protocols", http_protocols)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tls_protocols and not isinstance(tls_protocols, list):
            raise TypeError("Expected argument 'tls_protocols' to be a list")
        pulumi.set(__self__, "tls_protocols", tls_protocols)
        if tls_service and not isinstance(tls_service, str):
            raise TypeError("Expected argument 'tls_service' to be a str")
        pulumi.set(__self__, "tls_service", tls_service)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Timestamp (GMT) when the configuration was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def default(self) -> bool:
        """
        Signifies whether Fastly will use this configuration as a default when creating a new TLS activation.
        """
        return pulumi.get(self, "default")

    @property
    @pulumi.getter(name="dnsRecords")
    def dns_records(self) -> Sequence['outputs.GetTlsConfigurationDnsRecordResult']:
        """
        The available DNS addresses that can be used to enable TLS for a domain. DNS must be configured for a domain for TLS handshakes to succeed. If enabling TLS on an apex domain (e.g. `example.com`) you must create four A records (or four AAAA records for IPv6 support) using the displayed global A record's IP addresses with your DNS provider. For subdomains and wildcard domains (e.g. `www.example.com` or `*.example.com`) you will need to create a relevant CNAME record.
        """
        return pulumi.get(self, "dns_records")

    @property
    @pulumi.getter(name="httpProtocols")
    def http_protocols(self) -> Sequence[str]:
        """
        HTTP protocols available on the TLS configuration.
        """
        return pulumi.get(self, "http_protocols")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the TLS configuration obtained from the Fastly API or another data source. Conflicts with all the other filters.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Custom name of the TLS configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="tlsProtocols")
    def tls_protocols(self) -> Sequence[str]:
        """
        TLS protocols available on the TLS configuration.
        """
        return pulumi.get(self, "tls_protocols")

    @property
    @pulumi.getter(name="tlsService")
    def tls_service(self) -> str:
        """
        Whether the configuration should support the `PLATFORM` or `CUSTOM` TLS service.
        """
        return pulumi.get(self, "tls_service")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        Timestamp (GMT) when the configuration was last updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetTlsConfigurationResult(GetTlsConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTlsConfigurationResult(
            created_at=self.created_at,
            default=self.default,
            dns_records=self.dns_records,
            http_protocols=self.http_protocols,
            id=self.id,
            name=self.name,
            tls_protocols=self.tls_protocols,
            tls_service=self.tls_service,
            updated_at=self.updated_at)


def get_tls_configuration(default: Optional[bool] = None,
                          http_protocols: Optional[Sequence[str]] = None,
                          id: Optional[str] = None,
                          name: Optional[str] = None,
                          tls_protocols: Optional[Sequence[str]] = None,
                          tls_service: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTlsConfigurationResult:
    """
    Use this data source to get the ID of a TLS configuration for use with other resources.

    > **Warning:** The data source's filters are applied using an **AND** boolean operator, so depending on the combination
    of filters, they may become mutually exclusive. The exception to this is `id` which must not be specified in combination
    with any of the others.

    > **Note:** If more or less than a single match is returned by the search, this provider will fail. Ensure that your search is specific enough to return a single key.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    example_tls_configuration = fastly.get_tls_configuration(default=True)
    example_tls_activation = fastly.TlsActivation("exampleTlsActivation", configuration_id=example_tls_configuration.id)
    # ...
    ```


    :param bool default: Signifies whether Fastly will use this configuration as a default when creating a new TLS activation.
    :param Sequence[str] http_protocols: HTTP protocols available on the TLS configuration.
    :param str id: ID of the TLS configuration obtained from the Fastly API or another data source. Conflicts with all the other filters.
    :param str name: Custom name of the TLS configuration.
    :param Sequence[str] tls_protocols: TLS protocols available on the TLS configuration.
    :param str tls_service: Whether the configuration should support the `PLATFORM` or `CUSTOM` TLS service.
    """
    __args__ = dict()
    __args__['default'] = default
    __args__['httpProtocols'] = http_protocols
    __args__['id'] = id
    __args__['name'] = name
    __args__['tlsProtocols'] = tls_protocols
    __args__['tlsService'] = tls_service
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fastly:index/getTlsConfiguration:getTlsConfiguration', __args__, opts=opts, typ=GetTlsConfigurationResult).value

    return AwaitableGetTlsConfigurationResult(
        created_at=pulumi.get(__ret__, 'created_at'),
        default=pulumi.get(__ret__, 'default'),
        dns_records=pulumi.get(__ret__, 'dns_records'),
        http_protocols=pulumi.get(__ret__, 'http_protocols'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tls_protocols=pulumi.get(__ret__, 'tls_protocols'),
        tls_service=pulumi.get(__ret__, 'tls_service'),
        updated_at=pulumi.get(__ret__, 'updated_at'))


@_utilities.lift_output_func(get_tls_configuration)
def get_tls_configuration_output(default: Optional[pulumi.Input[Optional[bool]]] = None,
                                 http_protocols: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                 id: Optional[pulumi.Input[Optional[str]]] = None,
                                 name: Optional[pulumi.Input[Optional[str]]] = None,
                                 tls_protocols: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                 tls_service: Optional[pulumi.Input[Optional[str]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTlsConfigurationResult]:
    """
    Use this data source to get the ID of a TLS configuration for use with other resources.

    > **Warning:** The data source's filters are applied using an **AND** boolean operator, so depending on the combination
    of filters, they may become mutually exclusive. The exception to this is `id` which must not be specified in combination
    with any of the others.

    > **Note:** If more or less than a single match is returned by the search, this provider will fail. Ensure that your search is specific enough to return a single key.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    example_tls_configuration = fastly.get_tls_configuration(default=True)
    example_tls_activation = fastly.TlsActivation("exampleTlsActivation", configuration_id=example_tls_configuration.id)
    # ...
    ```


    :param bool default: Signifies whether Fastly will use this configuration as a default when creating a new TLS activation.
    :param Sequence[str] http_protocols: HTTP protocols available on the TLS configuration.
    :param str id: ID of the TLS configuration obtained from the Fastly API or another data source. Conflicts with all the other filters.
    :param str name: Custom name of the TLS configuration.
    :param Sequence[str] tls_protocols: TLS protocols available on the TLS configuration.
    :param str tls_service: Whether the configuration should support the `PLATFORM` or `CUSTOM` TLS service.
    """
    ...
