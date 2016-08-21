from entity.sprites import GameSprite
import net.client
import net.host
import net.common as common

# map of entity ids to objects
#
net_entities = {}


def create_net_entity(entity):
    """Create a new net-synced entity.

    :param entity:
    :return:
    """
    if len(net_entities) == 0:
        return add_net_entity(0, entity)
    for i in range(len(net_entities)):
        if not net_entities.get(i):
            return add_net_entity(i, entity)
    return add_net_entity(len(net_entities), entity)


def add_net_entity(eid, entity):
    """Add a net-synced entity.

    :param eid:
    :param entity:
    :return:
    """
    net_entities[eid] = entity
    return eid


def set_player_to(eid):
    """Change the id of the player entity.

    i.e. if this client is PLAYER 2 in the co-op
    game, this should be set to 1 (not 0)

    :param eid:
    """
    if len(net_entities) > 0 and hasattr(net_entities[0], "add_item"):
        net_entities[0].id = eid
        net_entities[eid] = net_entities[0]
        net_entities[0] = None
    else:
        raise Exception("Tried to change a non-player entity's EID")


def entity_from_id(eid):
    return net_entities.get(eid, None)


def sync_positions():
    for entity in net_entities.values():
        entity.sync_position()


def sync_velocities():
    for entity in net_entities.values():
        entity.sync_velocity()


class NetEntity(GameSprite):
    def __init__(self, position):
        GameSprite.__init__(self, position)
        self.id = create_net_entity(self)
        self.last_pos = self.rect.topleft
        self.last_vel = self.velocity.tup

    def sync_position(self):
        if not self.rect.topleft == self.last_pos:
            net.host.broadcast(common.entity_move_packet(self.id, self.rect.topleft))
            self.last_pos = self.rect.topleft

    def sync_velocity(self):
        if not self.last_vel == self.velocity.tup:
            net.host.broadcast(common.entity_velocity_packet(self.id, self.velocity.tup))
            self.last_vel = self.velocity.tup
