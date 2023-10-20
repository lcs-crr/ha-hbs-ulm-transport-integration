from dataclasses import dataclass
from datetime import datetime
from .const import TRANSPORT_TYPE_VISUALS, DEFAULT_ICON


@dataclass
class Departure:
    route_number: int
    time: datetime
    countdown: int
    route_type: str | None = None
    time_str: str | None = None
    direction: str | None = None
    platform: str | None = None
    icon: str | None = None
    bg_color: str | None = None
    fallback_color: str | None = None

    @classmethod
    def from_dict(cls, source):

        # As the API fails to realiably provide a route type, we need to do it ourselfs
        route_number = source.get("RouteNumber")
        if route_number == 1 or route_number == 2:
            route_type = "tram"
        else:
            route_type = "bus"

        line_visuals = TRANSPORT_TYPE_VISUALS.get(route_type) or {}

        # get departure time, convert from iso to datetime
        time = datetime.fromisoformat(source.get("DepartureTimeActual"))
        # drop tz info and format "H:M"
        time_str = time.replace(tzinfo=None).strftime("%H:%M")

        return cls(
            route_number=route_number,
            time = time,
            countdown = int(source.get("DepartureCountdown") / 60),
            route_type=route_type,
            time_str = time_str,
            direction=source.get("DepartureDirectionText"),
            platform=source.get("PlatformName"),
            icon=line_visuals.get("icon") or DEFAULT_ICON,
            bg_color=source.get("line", {}).get("color", {}).get("bg"),
            fallback_color=line_visuals.get("color"),
        )

    def to_dict(self):
        return {
            "route_number": self.route_number,
            "platform": self.platform,
            "direction": self.direction,
            "countdown": self.countdown,
            "time_str": self.time_str,
            "color": self.fallback_color or self.bg_color,
        }
