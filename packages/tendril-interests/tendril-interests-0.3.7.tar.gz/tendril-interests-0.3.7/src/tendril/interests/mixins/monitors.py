

from pprint import pprint
import time
import re
import json
from decimal import Decimal
from fnmatch import fnmatch
from typing import List
from typing import Any
from typing import Optional

from tendril.caching import transit
from tendril.utils.pydantic import TendrilTBaseModel
from tendril.utils.types.unitbase import NumericalUnitBase
from tendril.core.mq.aio import with_mq_client

from tendril.monitors.spec import MonitorSpec
from tendril.monitors.spec import MonitorExportLevel
from tendril.monitors.spec import MonitorPublishFrequency
from tendril.monitors.spec import bool_parser
from tendril.monitors.spec import DecimalEncoder

from .base import InterestMixinBase


idx_rex = re.compile(r"^(?P<key>\S+)\[(?P<idx>\d+)\]")


class InterestBaseMonitorsTMixin(TendrilTBaseModel):
    monitors: Optional[Any]


class InterestMonitorsMixin(InterestMixinBase):
    monitors_spec : List[MonitorSpec] = []

    @property
    def monitors(self):
        if not hasattr(self, '_monitors'):
            self._monitors = {}
        return self._monitors

    def monitor_get_spec(self, monitor):
        for spec in self.monitors_spec:
            if fnmatch(monitor, spec.publish_name()):
                return spec

    # def monitors_print(self):
    #     pprint(self.monitors)
    #     for spec in self.monitors_spec:
    #         try:
    #             print(spec.publish_name(), spec.hot_cache_key(self.id), self.monitors[spec.publish_name()])
    #         except KeyError:
    #             # print(f"err {spec.publish_name()}")
    #             pass

    def _monitor_get_cache_loc(self, spec):
        return {
            'namespace': f'im:{self.id}',
            'key': spec.publish_name()
        }

    @with_mq_client
    async def monitor_publish(self, spec: MonitorSpec, value,
                              name=None, timestamp=None, mq=None):
        # TODO
        #  - This is all very fragile.
        #  - Move big chucks of this into some influxdb connector.
        if not timestamp:
            timestamp = time.clock_gettime_ns(time.CLOCK_REALTIME)
        if not name:
            name = spec.publish_name()
        bucket = 'im'
        tags = {'device_id': str(self.id),
                'device': str(self.name)}
        if isinstance(spec.publish_measurement, str):
            measurement = spec.publish_measurement
        else:
            measurement = spec.publish_measurement(name)
        if measurement != name:
            parts = name.split('.')
            if measurement in parts:
                parts.remove(measurement)
            if len(parts) == 1:
                tags['identifier'] = parts[0]
            if len(parts) > 1:
                raise ValueError("Don't know how to construct an influxdb string")

        # We don't use the usual serializers here. Instead, we rely on the DecimalEncoder
        # This is another significant source of fragility and may need to be improved.
        # value = spec.get_serializer()(value)
        fields = {'value': value}

        msg = json.dumps({'measurement': measurement,
                       'tags': tags,
                     'fields': fields,
                  'timestamp': timestamp}, cls=DecimalEncoder)

        key = f'{bucket}.{self.type_name}.{measurement}'
        await mq.publish(key, msg)
        print('SENT', key, msg)
        # line_protocol_tags = ','.join(f'{x}={y}' for x, y in tags.items())
        # line_protocol_b1_parts = [measurement, line_protocol_tags]
        # line_protocol_b1 = ','.join(line_protocol_b1_parts)
        #
        # line_protocol_values = ','.join(f'{x}={y}' for x, y in fields.items())
        #
        # line_protocol_b2 = line_protocol_values
        # line_protocol_b3 = str(timestamp)
        #
        # line_protocol_parts = [line_protocol_b1, line_protocol_b2, line_protocol_b3]
        # line_protocol = ' '.join(line_protocol_parts)
        # print(name, 'LP', line_protocol)
        # mq.publish(key, value)

    async def monitor_write(self, spec: MonitorSpec, value,
                            name=None, timestamp=None):
        if spec.keep_hot:
            # Publish to cache
            kwargs = self._monitor_get_cache_loc(spec)
            kwargs.update({'ttl': spec.expire, 'ser': spec.get_serializer(), 'get': True})

            # TODO Replace with async when tendril-caching allows it
            old_value = transit.write(value, **kwargs)
            if old_value:
                deser = spec.get_deserializer()
                if isinstance(old_value, bytes):
                    old_value = old_value.decode()
                if deser:
                    old_value = deser(old_value)
        publish = False
        match spec.publish_frequency:
            case MonitorPublishFrequency.ALWAYS:
                publish = True
            case MonitorPublishFrequency.ONCHANGE:
                if old_value != value:
                    publish = True
        if publish:
            await self.monitor_publish(spec, value,
                                       name=name, timestamp=timestamp)


    def monitor_report(self, monitor, value, timestamp=None,
                       background_tasks=None):
        spec = self.monitor_get_spec(monitor)
        if not spec:
            return
        if not background_tasks:
            raise NotImplementedError("Monitors currently need to be updated through "
                                      "apiserver endpoints with background_tasks.")
        if not timestamp:
            timestamp = time.clock_gettime_ns(time.CLOCK_REALTIME)
        background_tasks.add_task(self.monitor_write, spec, value,
                                  name=monitor, timestamp=timestamp)

    def _monitor_extract(self, parts, walker):
        for part in parts:
            match = idx_rex.match(part)
            try:
                if match:
                    walker = walker[match.group('key')]
                    walker = walker[int(match.group('idx'))]
                else:
                    walker = walker[part]
            except KeyError:
                return None
        return walker

    def _monitor_extract_discriminated(self, parts, walker, discriminators):
        rv = {}
        for discriminator in discriminators:
            rv[discriminator] = self._monitor_extract(parts, walker[discriminator])
        return rv

    def _monitor_extract_from_report(self, path, report):
        parts = path.split('.')
        walker = report
        discriminators = None
        for part in parts:
            if discriminators:
                subparts.append(parts)
                continue
            elif part == '*':
                subparts = []
                discriminators = walker.keys()
                continue
            else:
                match = idx_rex.match(part)
                try:
                    if match:
                        walker = walker[match.group('key')]
                        walker = walker[int(match.group('idx'))]
                    else:
                        walker = walker[part]
                except KeyError:
                    return None
        if not discriminators:
            return walker
        else:
            return self._monitor_extract_discriminated(subparts, walker, discriminators)

    def _monitor_process_value(self, monitor_spec, value):
        if value is not None:
            if monitor_spec.preprocessor:
                if isinstance(monitor_spec.preprocessor, list):
                    for preprocessor in monitor_spec.preprocessor:
                        value = preprocessor(value)
                else:
                    value = monitor_spec.preprocessor(value)
            if monitor_spec.deserializer:
                value = monitor_spec.deserializer(value)
        return value

    def _monitor_process_discriminated_value(self, monitor_spec, values,
                                             timestamp=None, background_tasks=None):
        if isinstance(values, dict):
            for discriminator, discriminated_value in values.items():
                value = self._monitor_process_value(monitor_spec, discriminated_value)
                name = monitor_spec.publish_name().replace('*', discriminator)
                self.monitor_report(name, value, timestamp=timestamp,
                                    background_tasks=background_tasks)

    def monitors_report(self, report, timestamp=None, background_tasks=None):
        # pprint(report)
        if not timestamp:
            timestamp = time.clock_gettime_ns(time.CLOCK_REALTIME)
        for monitor_spec in self.monitors_spec:
            value = self._monitor_extract_from_report(monitor_spec.path, report)
            if value is None:
                continue
            if monitor_spec.multiple_container and isinstance(value, monitor_spec.multiple_container):
                self._monitor_process_discriminated_value(monitor_spec, value, timestamp=timestamp,
                                                          background_tasks=background_tasks)
            else:
                value = self._monitor_process_value(monitor_spec, value)
                self.monitor_report(monitor_spec.publish_name(), value,
                                    timestamp=timestamp,
                                    background_tasks=background_tasks)

    def _monitor_get_value(self, spec):
        kwargs = self._monitor_get_cache_loc(spec)
        kwargs.update({
            'deser': spec.get_deserializer()
        })
        value = transit.read(**kwargs)
        if spec.default is not None and not value:
            value = spec.default
        return value

    def _monitors_at_export_level(self, export_level):
        return [x for x in self.monitors_spec if x.export_level <= export_level]

    def export(self, session=None, auth_user=None, **kwargs):
        rv = {}
        if hasattr(super(), 'export'):
            rv.update(super().export(session=session, auth_user=auth_user, **kwargs))
        export_level = MonitorExportLevel.NORMAL
        monitors = self._monitors_at_export_level(export_level)
        if not monitors:
            return rv
        monitor_values = {}
        for monitor_spec in self._monitors_at_export_level(export_level):
            value = self._monitor_get_value(monitor_spec)
            if value is None:
                continue
            if monitor_spec.export_processor:
                value = monitor_spec.export_processor(value)
            monitor_values[monitor_spec.publish_name()] = value
        rv['monitors'] = monitor_values
        return rv
