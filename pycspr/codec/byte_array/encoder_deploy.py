import typing

from pycspr.codec.byte_array.encoder_cl import encode_cl_value
from pycspr.codec.byte_array.encoder_cl import encode_string
from pycspr.codec.byte_array.encoder_cl import encode_byte_array
from pycspr.codec.byte_array.encoder_cl import encode_u8_array
from pycspr.codec.byte_array.encoder_cl import encode_vector_of_t
from pycspr.types import Deploy
from pycspr.types import DeployHeader
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutionInfo
from pycspr.types import ExecutionInfo_ModuleBytes
from pycspr.types import ExecutionInfo_StoredContract
from pycspr.types import ExecutionInfo_StoredContractByHash
from pycspr.types import ExecutionInfo_StoredContractByHashVersioned
from pycspr.types import ExecutionInfo_StoredContractByName
from pycspr.types import ExecutionInfo_StoredContractByNameVersioned
from pycspr.types import ExecutionInfo_Transfer



def encode_deploy(entity: Deploy) -> typing.List[int]:
    """Encodes a deploy.
    
    """
    raise NotImplementedError()


def encode_deploy_header(entity: DeployHeader) -> typing.List[int]:
    """Encodes a deploy header.
    
    """
    raise NotImplementedError()


def encode_execution_argument(entity: ExecutionArgument) -> typing.List[int]:
    """Encodes an execution argument.
    
    """
    return encode_string(entity.name) + encode_cl_value(entity.value)


def encode_execution_info(entity: ExecutionInfo) -> typing.List[int]:
    """Encodes execution information for subsequent interpretation by VM.
    
    """
    def _encode_args(args: typing.List[ExecutionArgument]):
        return encode_vector_of_t(list(map(encode_execution_argument, args)))

    def _encode_module_bytes():
        return encode_u8_array(list(entity.module_bytes)) + _encode_args(entity.args)

    def _encode_stored_contract_by_hash():
        return encode_byte_array(entity.hash) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_stored_contract_by_hash_versioned():
        # TODO: encode optional U32 :: contract version
        return encode_byte_array(entity.hash) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_stored_contract_by_name():
        return encode_string(entity.name) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_stored_contract_by_name_versioned():
        # TODO: encode optional U32 :: contract version
        return encode_string(entity.name) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_transfer():
        return _encode_args(entity.args)

    _ENCODERS = {
        ExecutionInfo_ModuleBytes: (0, _encode_module_bytes),
        ExecutionInfo_StoredContractByHash: (1, _encode_stored_contract_by_hash),
        ExecutionInfo_StoredContractByHashVersioned: (3, _encode_stored_contract_by_hash_versioned),
        ExecutionInfo_StoredContractByName: (2, _encode_stored_contract_by_name),
        ExecutionInfo_StoredContractByNameVersioned: (4, _encode_stored_contract_by_name_versioned),
        ExecutionInfo_Transfer: (5, _encode_transfer),
    }

    try:
        type_tag, encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("Unencodeable domain type.")
    else:
        return [type_tag] + encoder()


# Map: Deploy type <-> encoder.
ENCODERS = {
    Deploy: encode_deploy,
    DeployHeader: encode_deploy_header,
    ExecutionArgument: encode_execution_argument,
    ExecutionInfo_ModuleBytes: encode_execution_info,
    ExecutionInfo_StoredContractByHash: encode_execution_info,
    ExecutionInfo_StoredContractByHashVersioned: encode_execution_info,
    ExecutionInfo_StoredContractByName: encode_execution_info,
    ExecutionInfo_StoredContractByNameVersioned: encode_execution_info,
    ExecutionInfo_Transfer: encode_execution_info,
}


def encode(entity) -> typing.List[int]:
    """Encodes a higher order domain entity as an array of bytes.
    
    """
    try:
        encoder = ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unencodeable type: {type(entity)}")
    else:
        return encoder(entity)
