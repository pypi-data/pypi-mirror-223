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
    'GetPackageHashResult',
    'AwaitableGetPackageHashResult',
    'get_package_hash',
    'get_package_hash_output',
]

@pulumi.output_type
class GetPackageHashResult:
    """
    A collection of values returned by getPackageHash.
    """
    def __init__(__self__, content=None, filename=None, hash=None, id=None):
        if content and not isinstance(content, str):
            raise TypeError("Expected argument 'content' to be a str")
        pulumi.set(__self__, "content", content)
        if filename and not isinstance(filename, str):
            raise TypeError("Expected argument 'filename' to be a str")
        pulumi.set(__self__, "filename", filename)
        if hash and not isinstance(hash, str):
            raise TypeError("Expected argument 'hash' to be a str")
        pulumi.set(__self__, "hash", hash)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def content(self) -> Optional[str]:
        """
        The contents of the Wasm deployment package as a base64 encoded string (e.g. could be provided using an input variable or via external data source output variable). Conflicts with `filename`. Exactly one of these two arguments must be specified
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def filename(self) -> Optional[str]:
        """
        The path to the Wasm deployment package within your local filesystem. Conflicts with `content`. Exactly one of these two arguments must be specified
        """
        return pulumi.get(self, "filename")

    @property
    @pulumi.getter
    def hash(self) -> str:
        """
        A SHA512 hash of all files (in sorted order) within the package.
        """
        return pulumi.get(self, "hash")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetPackageHashResult(GetPackageHashResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPackageHashResult(
            content=self.content,
            filename=self.filename,
            hash=self.hash,
            id=self.id)


def get_package_hash(content: Optional[str] = None,
                     filename: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPackageHashResult:
    """
    Use this data source to generate a SHA512 hash of all files (in sorted order) within the package.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    example_package_hash = fastly.get_package_hash(filename="./path/to/package.tar.gz")
    # ...
    example_service_compute = fastly.ServiceCompute("exampleServiceCompute", package=fastly.ServiceComputePackageArgs(
        filename="./path/to/package.tar.gz",
        source_code_hash=example_package_hash.hash,
    ))
    ```


    :param str content: The contents of the Wasm deployment package as a base64 encoded string (e.g. could be provided using an input variable or via external data source output variable). Conflicts with `filename`. Exactly one of these two arguments must be specified
    :param str filename: The path to the Wasm deployment package within your local filesystem. Conflicts with `content`. Exactly one of these two arguments must be specified
    """
    __args__ = dict()
    __args__['content'] = content
    __args__['filename'] = filename
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fastly:index/getPackageHash:getPackageHash', __args__, opts=opts, typ=GetPackageHashResult).value

    return AwaitableGetPackageHashResult(
        content=pulumi.get(__ret__, 'content'),
        filename=pulumi.get(__ret__, 'filename'),
        hash=pulumi.get(__ret__, 'hash'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_package_hash)
def get_package_hash_output(content: Optional[pulumi.Input[Optional[str]]] = None,
                            filename: Optional[pulumi.Input[Optional[str]]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPackageHashResult]:
    """
    Use this data source to generate a SHA512 hash of all files (in sorted order) within the package.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    example_package_hash = fastly.get_package_hash(filename="./path/to/package.tar.gz")
    # ...
    example_service_compute = fastly.ServiceCompute("exampleServiceCompute", package=fastly.ServiceComputePackageArgs(
        filename="./path/to/package.tar.gz",
        source_code_hash=example_package_hash.hash,
    ))
    ```


    :param str content: The contents of the Wasm deployment package as a base64 encoded string (e.g. could be provided using an input variable or via external data source output variable). Conflicts with `filename`. Exactly one of these two arguments must be specified
    :param str filename: The path to the Wasm deployment package within your local filesystem. Conflicts with `content`. Exactly one of these two arguments must be specified
    """
    ...
