from typing import Callable
from marshmallow import validate
from beam.type import (
    PythonVersion,
    GpuType,
    TriggerType,
    VolumeType,
    AutoscalingType,
)
from beam.utils.parse import compose_cpu, compose_memory
from beam import validators
from marshmallow import Schema, fields, ValidationError
from marshmallow import EXCLUDE


class SerializerMethod(fields.Field):
    def __init__(self, method: Callable, **kwargs):
        self.method = method
        super().__init__(**kwargs)

    def serialize(self, value, attr, obj, **kwargs):
        try:
            return self.method(value)
        except Exception as e:
            raise ValidationError(str(e))

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.method(value)
        except Exception as e:
            raise ValidationError(str(e))


class ConfigurationBase(Schema):
    class Meta:
        ordered = True
        unknown = EXCLUDE


class AutoscalingConfiguration(ConfigurationBase):
    max_replicas = fields.Integer(required=True)
    desired_latency = fields.Float(required=True)
    autoscaling_type = fields.Enum(
        enum=AutoscalingType,
        by_value=True,
        validate=validate.OneOf(
            choices=[autoscaling.value for autoscaling in AutoscalingType]
        ),
        required=True,
    )


class VolumeConfiguration(ConfigurationBase):
    name = fields.String(required=True)
    app_path = fields.String(required=True)
    mount_type = fields.Enum(
        enum=VolumeType,
        by_value=True,
        validate=validate.OneOf(choices=[mount.value for mount in VolumeType]),
        required=True,
    )


class OutputConfiguration(ConfigurationBase):
    path = fields.String(required=True)


class ImageConfiguration(ConfigurationBase):
    python_version = fields.Enum(
        enum=PythonVersion,
        by_value=True,
        validate=validate.OneOf(choices=[version.value for version in PythonVersion]),
        dump_default=PythonVersion.Python38,
    )
    python_packages = fields.List(fields.String(), dump_default=[])
    commands = fields.List(fields.String(), dump_default=[])


class RuntimeConfiguration(ConfigurationBase):
    cpu = SerializerMethod(compose_cpu, required=True)
    memory = SerializerMethod(compose_memory, required=True)
    gpu = fields.Enum(
        enum=GpuType,
        by_value=True,
        validate=validate.OneOf(choices=[gpu.value for gpu in GpuType]),
    )
    image = fields.Nested(ImageConfiguration, required=True)


class RunConfiguration(ConfigurationBase):
    name = fields.String(allow_none=True)
    handler = fields.String(validate=validators.IsFileMethod(), required=True)
    callback_url = fields.Url(allow_none=True)
    outputs = fields.Nested(OutputConfiguration, dump_default=[], many=True)
    runtime = fields.Nested(RuntimeConfiguration, dump_default=None, allow_none=True)


class TriggerConfiguration(ConfigurationBase):
    handler = fields.String(validate=validators.IsFileMethod(), required=True)
    loader = fields.String(
        validate=validators.IsFileMethod(),
        allow_none=True,
    )
    callback_url = fields.Url(
        allow_none=True,
    )
    max_pending_tasks = fields.Integer()
    keep_warm_seconds = fields.Integer()
    trigger_type = fields.Enum(
        enum=TriggerType,
        by_value=True,
        validate=validate.OneOf(choices=[trigger.value for trigger in TriggerType]),
        required=True,
    )
    path = fields.String()
    method = fields.String(validate=validate.OneOf(choices=["GET", "POST"]))
    runtime = fields.Nested(RuntimeConfiguration, dump_default=None, allow_none=True)
    outputs = fields.Nested(OutputConfiguration, dump_default=[], many=True)
    autoscaling = fields.Nested(
        AutoscalingConfiguration, dump_default=None, allow_none=True
    )
    when = fields.String(
        validate=validators.IsValidCronOrEvery(), dump_default=None, allow_none=True
    )


class AppConfiguration(ConfigurationBase):
    app_spec_version = fields.String(required=True)
    sdk_version = fields.String(required=True)
    name = fields.String(required=True)
    runtime = fields.Nested(RuntimeConfiguration, dump_default=None, allow_none=True)
    mounts = fields.List(fields.Nested(VolumeConfiguration), dump_default=[])
    triggers = fields.Nested(TriggerConfiguration, dump_default=[], many=True)
    run = fields.Nested(RunConfiguration, dump_default=None, allow_none=True)
