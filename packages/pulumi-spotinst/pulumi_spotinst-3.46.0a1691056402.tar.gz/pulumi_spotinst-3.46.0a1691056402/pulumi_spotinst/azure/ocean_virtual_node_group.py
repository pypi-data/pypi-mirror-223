# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['OceanVirtualNodeGroupArgs', 'OceanVirtualNodeGroup']

@pulumi.input_type
class OceanVirtualNodeGroupArgs:
    def __init__(__self__, *,
                 ocean_id: pulumi.Input[str],
                 autoscales: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]]] = None,
                 launch_specifications: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_limits: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]]] = None,
                 taints: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a OceanVirtualNodeGroup resource.
        :param pulumi.Input[str] ocean_id: The Ocean cluster ID.
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]] autoscales: .
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]] labels: Additional labels for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]] launch_specifications: .
        :param pulumi.Input[str] name: Set name for the virtual node group.
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]] resource_limits: .
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]] taints: Additional taints for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: An Array holding Availability Zones, this configures the availability zones the Ocean may launch instances in per VNG.
        """
        pulumi.set(__self__, "ocean_id", ocean_id)
        if autoscales is not None:
            pulumi.set(__self__, "autoscales", autoscales)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if launch_specifications is not None:
            pulumi.set(__self__, "launch_specifications", launch_specifications)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_limits is not None:
            pulumi.set(__self__, "resource_limits", resource_limits)
        if taints is not None:
            pulumi.set(__self__, "taints", taints)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="oceanId")
    def ocean_id(self) -> pulumi.Input[str]:
        """
        The Ocean cluster ID.
        """
        return pulumi.get(self, "ocean_id")

    @ocean_id.setter
    def ocean_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "ocean_id", value)

    @property
    @pulumi.getter
    def autoscales(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]]]:
        """
        .
        """
        return pulumi.get(self, "autoscales")

    @autoscales.setter
    def autoscales(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]]]):
        pulumi.set(self, "autoscales", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]]]:
        """
        Additional labels for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter(name="launchSpecifications")
    def launch_specifications(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]]]:
        """
        .
        """
        return pulumi.get(self, "launch_specifications")

    @launch_specifications.setter
    def launch_specifications(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]]]):
        pulumi.set(self, "launch_specifications", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Set name for the virtual node group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceLimits")
    def resource_limits(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]]]:
        """
        .
        """
        return pulumi.get(self, "resource_limits")

    @resource_limits.setter
    def resource_limits(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]]]):
        pulumi.set(self, "resource_limits", value)

    @property
    @pulumi.getter
    def taints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]]]:
        """
        Additional taints for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        """
        return pulumi.get(self, "taints")

    @taints.setter
    def taints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]]]):
        pulumi.set(self, "taints", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An Array holding Availability Zones, this configures the availability zones the Ocean may launch instances in per VNG.
        """
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "zones", value)


@pulumi.input_type
class _OceanVirtualNodeGroupState:
    def __init__(__self__, *,
                 autoscales: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]]] = None,
                 launch_specifications: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 ocean_id: Optional[pulumi.Input[str]] = None,
                 resource_limits: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]]] = None,
                 taints: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering OceanVirtualNodeGroup resources.
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]] autoscales: .
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]] labels: Additional labels for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]] launch_specifications: .
        :param pulumi.Input[str] name: Set name for the virtual node group.
        :param pulumi.Input[str] ocean_id: The Ocean cluster ID.
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]] resource_limits: .
        :param pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]] taints: Additional taints for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: An Array holding Availability Zones, this configures the availability zones the Ocean may launch instances in per VNG.
        """
        if autoscales is not None:
            pulumi.set(__self__, "autoscales", autoscales)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if launch_specifications is not None:
            pulumi.set(__self__, "launch_specifications", launch_specifications)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if ocean_id is not None:
            pulumi.set(__self__, "ocean_id", ocean_id)
        if resource_limits is not None:
            pulumi.set(__self__, "resource_limits", resource_limits)
        if taints is not None:
            pulumi.set(__self__, "taints", taints)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def autoscales(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]]]:
        """
        .
        """
        return pulumi.get(self, "autoscales")

    @autoscales.setter
    def autoscales(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupAutoscaleArgs']]]]):
        pulumi.set(self, "autoscales", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]]]:
        """
        Additional labels for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLabelArgs']]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter(name="launchSpecifications")
    def launch_specifications(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]]]:
        """
        .
        """
        return pulumi.get(self, "launch_specifications")

    @launch_specifications.setter
    def launch_specifications(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupLaunchSpecificationArgs']]]]):
        pulumi.set(self, "launch_specifications", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Set name for the virtual node group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="oceanId")
    def ocean_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Ocean cluster ID.
        """
        return pulumi.get(self, "ocean_id")

    @ocean_id.setter
    def ocean_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ocean_id", value)

    @property
    @pulumi.getter(name="resourceLimits")
    def resource_limits(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]]]:
        """
        .
        """
        return pulumi.get(self, "resource_limits")

    @resource_limits.setter
    def resource_limits(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupResourceLimitArgs']]]]):
        pulumi.set(self, "resource_limits", value)

    @property
    @pulumi.getter
    def taints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]]]:
        """
        Additional taints for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        """
        return pulumi.get(self, "taints")

    @taints.setter
    def taints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OceanVirtualNodeGroupTaintArgs']]]]):
        pulumi.set(self, "taints", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An Array holding Availability Zones, this configures the availability zones the Ocean may launch instances in per VNG.
        """
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "zones", value)


class OceanVirtualNodeGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscales: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupAutoscaleArgs']]]]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLabelArgs']]]]] = None,
                 launch_specifications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLaunchSpecificationArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 ocean_id: Optional[pulumi.Input[str]] = None,
                 resource_limits: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupResourceLimitArgs']]]]] = None,
                 taints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupTaintArgs']]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a Spotinst Ocean AKS Virtual Node Group resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_spotinst as spotinst

        example = spotinst.azure.OceanVirtualNodeGroup("example",
            autoscales=[spotinst.azure.OceanVirtualNodeGroupAutoscaleArgs(
                auto_headroom_percentage=5,
                autoscale_headrooms=[spotinst.azure.OceanVirtualNodeGroupAutoscaleAutoscaleHeadroomArgs(
                    cpu_per_unit=4,
                    gpu_per_unit=8,
                    memory_per_unit=100,
                    num_of_units=16,
                )],
            )],
            labels=[spotinst.azure.OceanVirtualNodeGroupLabelArgs(
                key="label_key",
                value="label_value",
            )],
            launch_specifications=[spotinst.azure.OceanVirtualNodeGroupLaunchSpecificationArgs(
                max_pods=30,
                os_disk=spotinst.azure.OceanVirtualNodeGroupLaunchSpecificationOsDiskArgs(
                    size_gb=100,
                    type="Standard_LRS",
                    utilize_ephemeral_storage=False,
                ),
                tags=[spotinst.azure.OceanVirtualNodeGroupLaunchSpecificationTagArgs(
                    key="label_key",
                    value="label_value",
                )],
            )],
            ocean_id="o-12345",
            resource_limits=[spotinst.azure.OceanVirtualNodeGroupResourceLimitArgs(
                max_instance_count=4,
            )],
            taints=[spotinst.azure.OceanVirtualNodeGroupTaintArgs(
                effect="NoSchedule",
                key="taint_key",
                value="taint_value",
            )],
            zones=[
                "1",
                "2",
                "3",
            ])
        ```

        ```python
        import pulumi

        pulumi.export("oceanId", spotinst_ocean_aks_["example"]["id"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupAutoscaleArgs']]]] autoscales: .
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLabelArgs']]]] labels: Additional labels for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLaunchSpecificationArgs']]]] launch_specifications: .
        :param pulumi.Input[str] name: Set name for the virtual node group.
        :param pulumi.Input[str] ocean_id: The Ocean cluster ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupResourceLimitArgs']]]] resource_limits: .
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupTaintArgs']]]] taints: Additional taints for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: An Array holding Availability Zones, this configures the availability zones the Ocean may launch instances in per VNG.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OceanVirtualNodeGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Spotinst Ocean AKS Virtual Node Group resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_spotinst as spotinst

        example = spotinst.azure.OceanVirtualNodeGroup("example",
            autoscales=[spotinst.azure.OceanVirtualNodeGroupAutoscaleArgs(
                auto_headroom_percentage=5,
                autoscale_headrooms=[spotinst.azure.OceanVirtualNodeGroupAutoscaleAutoscaleHeadroomArgs(
                    cpu_per_unit=4,
                    gpu_per_unit=8,
                    memory_per_unit=100,
                    num_of_units=16,
                )],
            )],
            labels=[spotinst.azure.OceanVirtualNodeGroupLabelArgs(
                key="label_key",
                value="label_value",
            )],
            launch_specifications=[spotinst.azure.OceanVirtualNodeGroupLaunchSpecificationArgs(
                max_pods=30,
                os_disk=spotinst.azure.OceanVirtualNodeGroupLaunchSpecificationOsDiskArgs(
                    size_gb=100,
                    type="Standard_LRS",
                    utilize_ephemeral_storage=False,
                ),
                tags=[spotinst.azure.OceanVirtualNodeGroupLaunchSpecificationTagArgs(
                    key="label_key",
                    value="label_value",
                )],
            )],
            ocean_id="o-12345",
            resource_limits=[spotinst.azure.OceanVirtualNodeGroupResourceLimitArgs(
                max_instance_count=4,
            )],
            taints=[spotinst.azure.OceanVirtualNodeGroupTaintArgs(
                effect="NoSchedule",
                key="taint_key",
                value="taint_value",
            )],
            zones=[
                "1",
                "2",
                "3",
            ])
        ```

        ```python
        import pulumi

        pulumi.export("oceanId", spotinst_ocean_aks_["example"]["id"])
        ```

        :param str resource_name: The name of the resource.
        :param OceanVirtualNodeGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OceanVirtualNodeGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscales: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupAutoscaleArgs']]]]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLabelArgs']]]]] = None,
                 launch_specifications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLaunchSpecificationArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 ocean_id: Optional[pulumi.Input[str]] = None,
                 resource_limits: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupResourceLimitArgs']]]]] = None,
                 taints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupTaintArgs']]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OceanVirtualNodeGroupArgs.__new__(OceanVirtualNodeGroupArgs)

            __props__.__dict__["autoscales"] = autoscales
            __props__.__dict__["labels"] = labels
            __props__.__dict__["launch_specifications"] = launch_specifications
            __props__.__dict__["name"] = name
            if ocean_id is None and not opts.urn:
                raise TypeError("Missing required property 'ocean_id'")
            __props__.__dict__["ocean_id"] = ocean_id
            __props__.__dict__["resource_limits"] = resource_limits
            __props__.__dict__["taints"] = taints
            __props__.__dict__["zones"] = zones
        super(OceanVirtualNodeGroup, __self__).__init__(
            'spotinst:azure/oceanVirtualNodeGroup:OceanVirtualNodeGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            autoscales: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupAutoscaleArgs']]]]] = None,
            labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLabelArgs']]]]] = None,
            launch_specifications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLaunchSpecificationArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            ocean_id: Optional[pulumi.Input[str]] = None,
            resource_limits: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupResourceLimitArgs']]]]] = None,
            taints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupTaintArgs']]]]] = None,
            zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'OceanVirtualNodeGroup':
        """
        Get an existing OceanVirtualNodeGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupAutoscaleArgs']]]] autoscales: .
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLabelArgs']]]] labels: Additional labels for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupLaunchSpecificationArgs']]]] launch_specifications: .
        :param pulumi.Input[str] name: Set name for the virtual node group.
        :param pulumi.Input[str] ocean_id: The Ocean cluster ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupResourceLimitArgs']]]] resource_limits: .
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OceanVirtualNodeGroupTaintArgs']]]] taints: Additional taints for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: An Array holding Availability Zones, this configures the availability zones the Ocean may launch instances in per VNG.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OceanVirtualNodeGroupState.__new__(_OceanVirtualNodeGroupState)

        __props__.__dict__["autoscales"] = autoscales
        __props__.__dict__["labels"] = labels
        __props__.__dict__["launch_specifications"] = launch_specifications
        __props__.__dict__["name"] = name
        __props__.__dict__["ocean_id"] = ocean_id
        __props__.__dict__["resource_limits"] = resource_limits
        __props__.__dict__["taints"] = taints
        __props__.__dict__["zones"] = zones
        return OceanVirtualNodeGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def autoscales(self) -> pulumi.Output[Optional[Sequence['outputs.OceanVirtualNodeGroupAutoscale']]]:
        """
        .
        """
        return pulumi.get(self, "autoscales")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Sequence['outputs.OceanVirtualNodeGroupLabel']]]:
        """
        Additional labels for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="launchSpecifications")
    def launch_specifications(self) -> pulumi.Output[Optional[Sequence['outputs.OceanVirtualNodeGroupLaunchSpecification']]]:
        """
        .
        """
        return pulumi.get(self, "launch_specifications")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Set name for the virtual node group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="oceanId")
    def ocean_id(self) -> pulumi.Output[str]:
        """
        The Ocean cluster ID.
        """
        return pulumi.get(self, "ocean_id")

    @property
    @pulumi.getter(name="resourceLimits")
    def resource_limits(self) -> pulumi.Output[Optional[Sequence['outputs.OceanVirtualNodeGroupResourceLimit']]]:
        """
        .
        """
        return pulumi.get(self, "resource_limits")

    @property
    @pulumi.getter
    def taints(self) -> pulumi.Output[Optional[Sequence['outputs.OceanVirtualNodeGroupTaint']]]:
        """
        Additional taints for the virtual node group. Only custom user labels are allowed. Kubernetes built-in labels and Spot internal labels are not allowed.
        """
        return pulumi.get(self, "taints")

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        An Array holding Availability Zones, this configures the availability zones the Ocean may launch instances in per VNG.
        """
        return pulumi.get(self, "zones")

