from pyunitsystem.energysystem import (
    EnergySI,
)  # noqa F401  kept for bacward compatibility
from pyunitsystem.unit import Unit

# Default units:
#  - lenght: meter (m)
#  - energy: kilo Electronvolt (keV)
_meter = 1.0
_kev = 1.0


class MetricSystem(Unit):
    """Util enum to retrieve metric"""

    METER = _meter
    m = _meter
    CENTIMETER = _meter / 100.0
    MILLIMETER = _meter / 1000.0
    MICROMETER = _meter * 1e-6
    NANOMETER = _meter * 1e-9

    KILOELECTRONVOLT = _kev
    ELECTRONVOLT = _kev * 1e-3
    JOULE = _kev / EnergySI.KILOELECTRONVOLT.value
    KILOJOULE = _kev / EnergySI.KILOELECTRONVOLT.value * 1e3

    @classmethod
    def from_str(cls, value: str):
        assert isinstance(value, str)
        if value.lower() in ("m", "meter"):
            return MetricSystem.METER
        elif value.lower() in ("cm", "centimeter"):
            return MetricSystem.CENTIMETER
        elif value.lower() in ("mm", "millimeter"):
            return MetricSystem.MILLIMETER
        elif value.lower() in ("um", "micrometer", "microns"):
            return MetricSystem.MICROMETER
        elif value.lower() in ("nm", "nanometer"):
            return MetricSystem.NANOMETER
        else:
            raise ValueError(f"Cannot convert: {value}")

    def __str__(self):
        if self == MetricSystem.METER:
            return "m"
        elif self == MetricSystem.CENTIMETER:
            return "cm"
        elif self == MetricSystem.MILLIMETER:
            return "mm"
        elif self == MetricSystem.MICROMETER:
            return "um"
        elif self == MetricSystem.NANOMETER:
            return "nm"
        else:
            raise ValueError(f"Cannot convert: {self}")


m = MetricSystem.METER
meter = MetricSystem.METER

centimeter = MetricSystem.CENTIMETER
cm = centimeter

millimeter = MetricSystem.MILLIMETER
mm = MetricSystem.MILLIMETER

micrometer = MetricSystem.MICROMETER

nanometer = MetricSystem.NANOMETER
