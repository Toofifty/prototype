"""
Shared network functions and values

Packet structure:

A packet begins with the OP code,
using one from the list below.

Follows should be a period . and
the net entity ID.

Values are then separated by a colon :
and are in name=value pairs for each piece
of data.

For example, creating an "arnold" player at 500, 200
will look like:

0.24:name=arnold:x=500:y=200

All values that can be transformed to ints will be,
to avoid, end an integer number with S.
Use a period to denote a decimal number.

(loose example)
16.24:msg=400S:time=20.3

After parsing, all information is placed into a dict
with default keys of "op" and "eid".

eg1: { "op": 0, "eid": 24, "name": "arnold", "x": 500, "y": 200 }
eg2: { "op": 16, "eid": 24, "msg": "400", "time": 20.3 }

An eid can be set to -1 if not applicable. However, it may be useful
to send the enacting player's eid instead.

"""

# op codes
OP_PLAYER_CREATE = 0
OP_ENTITY_CREATE = 1
OP_ENTITY_DESTROY = 2
OP_ENTITY_VEL = 3
OP_ENTITY_MOVE = 4

OP_ENTITY_MESSAGE = 16

# entity types
ENT_PLAYER = 0


def parse_packet_string(packet_str):
    """Fill a dict with data from a string packet.

    :param packet_str:
    :return: dict
    """
    pieces = packet_str.split(":")
    data = {}

    for piece in pieces[1:]:
        key, value = piece.split("=")
        try:
            # try to turn the value into a float or int
            value = float(value) if "." in value else int(value)
        except ValueError:
            # check if the number COULD be a num without S
            # if it COULD, remove the S and keep the string
            # (placing the number into a string by itself)
            if value[-1] is "S":
                try:
                    float(value[:-1])
                    value = value[:-1]
                except ValueError:
                    pass
        # add to dict
        data[key] = value

    data["op"], data["eid"] = (int(i) for i in pieces[0].split("."))
    return data


# functions to create packets for certain situations

def player_create_packet(eid, player_name, position):
    x, y = position
    return "{}.{}:name={}:x={}:y={}".format(OP_PLAYER_CREATE, eid, player_name, x, y)


def entity_create_packet(eid, entity_type, position):
    x, y = position
    return "{}.{}:type={}:x={}:y={}".format(OP_PLAYER_CREATE, eid, entity_type, x, y)


def entity_destroy_packet(eid):
    return "{}.{}".format(OP_ENTITY_DESTROY, eid)


def entity_velocity_packet(eid, velocity):
    vx, vy = velocity
    return "{}.{}:vx={}:vy={}".format(OP_ENTITY_VEL, eid, vx, vy)


def entity_move_packet(eid, position):
    x, y = position
    return "{}.{}:x={}:y={}".format(OP_ENTITY_MOVE, eid, x, y)
