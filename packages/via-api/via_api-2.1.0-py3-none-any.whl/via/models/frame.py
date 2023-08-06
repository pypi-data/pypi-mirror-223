from via.models.generic import GenericObject, GenericObjects
from via.models.gps import GPSPoint


class Frame(GenericObject):
    """
    A single snapshot of data on a journey containing gps, acceleration
    and time info
    """

    def __init__(self, time: float, gps: GPSPoint, acceleration: list):
        """

        :param time:
        :param gps: GPSPoint or dict serialization of GPSPoint
        :param acceleration:
        """
        super().__init__()
        self.time = time
        self.gps = GPSPoint.parse(gps)
        self.acceleration = acceleration

    @staticmethod
    def parse(obj):
        if isinstance(obj, dict):
            return Frame(obj.get("time", None), obj["gps"], obj["acc"])
        if isinstance(obj, Frame):
            return obj
        raise NotImplementedError("Can't parse Frame from type %s" % (type(obj)))

    def distance_from(self, point: GPSPoint) -> float:
        """

        :param point: GPSPoint or tuple of (lat, lng) or Frame object
        :rtype: float
        :return: Distance between points in metres
        """
        if isinstance(point, Frame):
            point = point.gps
        return self.gps.distance_from(point)

    @property
    def is_complete(self) -> bool:
        """
        Does the frame contain all expected data
        """
        return (
            isinstance(self.time, float)
            and self.gps.is_populated
            and self.acceleration != []
        )

    def serialize(self, **kwargs) -> dict:
        data = {"gps": self.gps.serialize(), "acc": self.acceleration}
        if kwargs.get("include_time", True):
            data["time"] = round(self.time, 2)
        return data


class Frames(GenericObjects):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("child_class", Frame)
        super().__init__(*args, **kwargs)

    @property
    def most_northern(self) -> float:
        return max([frame.gps.lat for frame in self])

    @property
    def most_southern(self) -> float:
        return min([frame.gps.lat for frame in self])

    @property
    def most_eastern(self) -> float:
        return max([frame.gps.lng for frame in self])

    @property
    def most_western(self) -> float:
        return min([frame.gps.lng for frame in self])

    @property
    def data_quality(self) -> float:
        """
        Get the percentage of frames that are good. Should
        automatically disregard journeys with low data quality

        :rtype: float
        :return: The percent between 0 and 1
        """
        # Mixed with the deviation between times?
        return len([f for f in self if f.is_complete]) / float(len(self))

    @property
    def origin(self) -> Frame:
        """
        The first frame of the journey

        :rtype: via.models.Frame
        :return: The first frame of the journey
        """
        return self[0]

    @property
    def destination(self) -> Frame:
        """
        The last frame of the journey

        :rtype: via.models.Frame
        :return: The last frame of the journey
        """
        return self[-1]

    @property
    def duration(self) -> float:
        """
        Get the time in seconds

        Note that much of the start and end may have been removed.

        :rtype: float
        :return: The number of seconds the journey took
        """
        if self.destination.time is None or self.origin.time is None:
            return None
        return self.destination.time - self.origin.time

    @property
    def direct_distance(self) -> float:
        """
        Get the distance in metres as the crow flies

        Note that much of the start and end may have been removed.

        :rtype: float
        :return: distance from origin to destination in metres
        """
        return self[0].distance_from(self[-1])

    def serialize(self, include_time: bool = True) -> list:
        return [frame.serialize(include_time=include_time) for frame in self]
