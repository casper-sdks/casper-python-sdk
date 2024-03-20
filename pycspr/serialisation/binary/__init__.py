from pycspr.serialisation.binary import cl_type as serialiser_of_cl_types
from pycspr.serialisation.binary import cl_value as serialiser_of_cl_values
from pycspr.serialisation.binary import entity as serialiser_of_entites
from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLV_Value


def to_bytes(entity: object) -> bytes:
    if isinstance(entity, CLT_Type):
        return serialiser_of_cl_types.encode(entity)
    elif isinstance(entity, CLV_Value):
        return serialiser_of_cl_values.encode(entity)
    else:
        return serialiser_of_entites.encode(entity)


def from_bytes(bstream: bytes, typedef: object = None) -> object:
    if isinstance(typedef, type(None)):
        return serialiser_of_cl_types.decode(bstream)
    elif isinstance(typedef, CLT_Type):
        return serialiser_of_cl_values.decode(bstream, typedef)
    else:
        return serialiser_of_entites.decode(bstream, typedef)
