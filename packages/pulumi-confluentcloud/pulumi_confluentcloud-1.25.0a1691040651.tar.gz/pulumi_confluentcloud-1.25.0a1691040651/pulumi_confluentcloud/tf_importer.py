# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['TfImporterArgs', 'TfImporter']

@pulumi.input_type
class TfImporterArgs:
    def __init__(__self__, *,
                 output_path: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a TfImporter resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: A list of resources names to export. Defaults to all exportable resources.
        """
        if output_path is not None:
            pulumi.set(__self__, "output_path", output_path)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter(name="outputPath")
    def output_path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "output_path")

    @output_path.setter
    def output_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output_path", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of resources names to export. Defaults to all exportable resources.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources", value)


@pulumi.input_type
class _TfImporterState:
    def __init__(__self__, *,
                 output_path: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering TfImporter resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: A list of resources names to export. Defaults to all exportable resources.
        """
        if output_path is not None:
            pulumi.set(__self__, "output_path", output_path)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter(name="outputPath")
    def output_path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "output_path")

    @output_path.setter
    def output_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output_path", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of resources names to export. Defaults to all exportable resources.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources", value)


class TfImporter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 output_path: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Create a TfImporter resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: A list of resources names to export. Defaults to all exportable resources.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[TfImporterArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a TfImporter resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param TfImporterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TfImporterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 output_path: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TfImporterArgs.__new__(TfImporterArgs)

            __props__.__dict__["output_path"] = output_path
            __props__.__dict__["resources"] = resources
        super(TfImporter, __self__).__init__(
            'confluentcloud:index/tfImporter:TfImporter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            output_path: Optional[pulumi.Input[str]] = None,
            resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'TfImporter':
        """
        Get an existing TfImporter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: A list of resources names to export. Defaults to all exportable resources.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TfImporterState.__new__(_TfImporterState)

        __props__.__dict__["output_path"] = output_path
        __props__.__dict__["resources"] = resources
        return TfImporter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="outputPath")
    def output_path(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "output_path")

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of resources names to export. Defaults to all exportable resources.
        """
        return pulumi.get(self, "resources")

