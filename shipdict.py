"""
Module managing informations about ships
Contains 3 classes:
- Position
- Ship
- ShipDict
"""

ID = 0
LATITUDE = 1
LONGITUDE = 2
NAME = 6
COUNTRY = 10


class Position:
    """
    Contains latitude, longitude and timestamp
    """

    def __init__(self, latitude, longitude, timestamp):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

    def __repr__(self):
        lat = d_m_s(self.latitude)
        lat_s = 'N' if self.latitude >= 0 else 'S'
        lon = d_m_s(self.longitude)
        lon_s = 'E' if self.longitude >= 0 else 'W'
        fstring = f"<{lat} {lat_s} {lon} {lon_s} @ {self.timestamp}>"
        print(fstring)
        return fstring


class Ship:
    """
    Contains ship's ID, and optionaly name and country
    """

    def __init__(self, ship_id, name=None, country=None):

        self.ship_id = ship_id
        self.name = name
        self.country = country
        self.positions = []

    def add_position(self, latitude, longitude, timestamp):
        """Add a position"""
        self.positions.append(Position(latitude, longitude, timestamp))

    def sort_positions(self):
        """Sort the positions based on timestamp"""
        self.positions.sort(key=lambda pos: pos.timestamp)


class ShipDict:
    """
    Contains ships, essentialy a dictionary
    """

    def __init__(self):
        self.ships = dict()

    def add_chunk(self, ship):
        ship_id = ship[ID]

        if ship_id not in self.ships:
            self.ships[ship_id] = Ship(ship[ID])
            # , ship[NAME], ship[COUNTRY])

        wship = self.ships[ship_id]

        if len(ship) > 7:
            timestamp = ship[5]
            if not wship.name:
                wship.name = ship[NAME]
                wship.country = ship[COUNTRY]
        else:
            timestamp = ship[6]

        wship.add_position(ship[LATITUDE],
                           ship[LONGITUDE],
                           timestamp)
        self.ships[ship_id] = wship

    def clean_unnamed(self):
        self.ships = {key: value for key, value
                      in self.ships.items() if value.name}

    def sort(self):
        for _, ship in self.ships.items():
            ship.sort_positions()

    def all_ships(self):
        return self.ships.values()

    def ships_by_name(self, name):
        return [ship for k, ship in self.ships if self.ships[k].name == name]


def d_m_s(f):
    """Convert a coordonate in float to formated degree.minute'.sec''"""
    # valabs = value if value > 0 else -value
    # degrees = int(valabs)
    # minutes = valabs % 1 * 60
    # secondes = minutes % 1 * 60
    # return f"{degrees:02d}.{int(minutes):02d}'{int(secondes):02d}''"
    f = f if f > 0 else -f
    d = int(f)
    m = int((f-d)*60)
    s = int((f-d)*3600 - 60*m)
    return f"{d:02d}.{m:02d}'{s:02d}''"
