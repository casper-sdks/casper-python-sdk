from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.types.cl.values import CLV_Value
from pycspr.types.rpc.identifiers import AccountID
from pycspr.types.rpc.identifiers import BlockHash
from pycspr.types.rpc.identifiers import BlockHeight
from pycspr.types.rpc.identifiers import DeployHash
from pycspr.types.rpc.identifiers import MerkleProofBytes
from pycspr.types.rpc.identifiers import Motes
from pycspr.types.rpc.identifiers import StateRootHash
from pycspr.types.rpc.identifiers import WasmModule
from pycspr.types.rpc.identifiers import Weight


@dataclasses.dataclass
class AccountInfo():
    account_hash: AccountID
    action_thresholds: ActionThresholds
    associated_keys: typing.List[AssociatedKey]
    main_purse: URef
    named_keys: typing.List[NamedKey]


@dataclasses.dataclass
class ActionThresholds():
    deployment: Weight
    key_management: Weight


@dataclasses.dataclass
class AssociatedKey():
    account_hash: AccountID
    weight: Weight


@dataclasses.dataclass
class AuctionBidByDelegator():
    bonding_purse: URef
    public_key: PublicKeyBytes
    delegatee: AccountID
    staked_amount: Motes


@dataclasses.dataclass
class AuctionBidByValidator():
    public_key: PublicKeyBytes
    bid: AuctionBidByValidatorInfo


@dataclasses.dataclass
class AuctionBidByValidatorInfo():
    bonding_purse: URef
    delegation_rate: int
    delegators: typing.List[AuctionBidByDelegator]
    inactive: bool
    staked_amount: Motes


@dataclasses.dataclass
class AuctionState():
    bids: typing.List[AuctionBidByValidator]
    block_height: BlockHeight
    era_validators: EraValidators
    state_root: StateRootHash


@dataclasses.dataclass
class Block():
    body: BlockBody
    hash: BlockHash
    header: BlockHeader
    proofs: typing.List[BlockSignature]


@dataclasses.dataclass
class BlockBody():
    proposer: AccountID
    deploy_hashes: typing.List[DeployHash]
    transfer_hashes: typing.List[DeployHash]


@dataclasses.dataclass
class BlockHeader():
    accumulated_seed: bytes
    body_hash: Digest
    era_id: EraID
    height: BlockHeight
    parent_hash: BlockHash
    protocol_version: ProtocolVersion
    random_bit: bool
    state_root: StateRootHash


@dataclasses.dataclass
class BlockSignature():
    public_key: PublicKeyBytes
    signature: SignatureBytes


@dataclasses.dataclass
class BlockTransfers():
    block_hash: BlockHash
    transfers: typing.List[Transfer]


@dataclasses.dataclass
class Deploy():
    approvals: typing.List[DeployApproval]
    hash: DeployHash
    header: DeployHeader
    payment: dict
    session: dict
    execution_info: DeployExecutionInfo = None


@dataclasses.dataclass
class DeployApproval():
    signer: PublicKeyBytes
    signature: SignatureBytes


@dataclasses.dataclass
class DeployArgument():
    name: str
    value: CLV_Value

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.value == other.value


@dataclasses.dataclass
class DeployExecutionInfo():
    block_hash: BlockHash
    results: dict


@dataclasses.dataclass
class DeployExecutableItem():
    args: typing.Union[typing.List[DeployArgument], typing.Dict[str, CLV_Value]]

    def __eq__(self, other) -> bool:
        return self.arguments == other.arguments

    @property
    def arguments(self) -> typing.List[DeployArgument]:
        if isinstance(self.args, list):
            return self.args
        elif isinstance(self.args, dict):
            return [DeployArgument(k, v) for (k, v) in self.args.items()]
        else:
            raise ValueError("Deploy arguments can be passed as either a list or dictionary")


@dataclasses.dataclass
class DeployHeader():
    account: bytes
    body_hash: Digest
    chain_name: str
    dependencies: typing.List[DeployHash]
    gas_price: GasPrice
    timestamp: Timestamp
    ttl: DeployTimeToLive


@dataclasses.dataclass
class DeployOfModuleBytes(DeployExecutableItem):
    module_bytes: WasmModule

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.module_bytes == other.module_bytes


@dataclasses.dataclass
class DeployOfStoredContract(DeployExecutableItem):
    pass


@dataclasses.dataclass
class DeployOfStoredContractByHash(DeployOfStoredContract):
    hash: ContractID


@dataclasses.dataclass
class DeployOfStoredContractByHashVersioned(DeployOfStoredContractByHash):
    version: ContractVersion


@dataclasses.dataclass
class DeployOfStoredContractByName(DeployOfStoredContract):
    name: str


@dataclasses.dataclass
class DeployOfStoredContractByNameVersioned(DeployOfStoredContractByName):
    version: ContractVersion


@dataclasses.dataclass
class DeployOfTransfer(DeployExecutableItem):
    pass


@dataclasses.dataclass
class DeployTimeToLive():
    as_milliseconds: int
    humanized: str


@dataclasses.dataclass
class EraInfo():
    seigniorage_allocations: typing.List[SeigniorageAllocation]


@dataclasses.dataclass
class EraSummary():
    block_hash: BlockHash
    era_id: EraID
    era_info: EraInfo
    merkle_proof: MerkleProofBytes
    state_root: Digest


@dataclasses.dataclass
class EraValidators():
    era_id: EraID
    validator_weights: typing.List[EraValidatorWeight]


@dataclasses.dataclass
class EraValidatorWeight():
    public_key: PublicKeyBytes
    weight: Weight


@dataclasses.dataclass
class NamedKey():
    key: str
    name: str


@dataclasses.dataclass
class ProtocolVersion():
    major: int
    minor: int
    revision: int


@dataclasses.dataclass
class SeigniorageAllocation():
    amount: Motes


@dataclasses.dataclass
class SeigniorageAllocationForDelegator(SeigniorageAllocation):
    delegator_public_key: PublicKeyBytes
    validator_public_key: PublicKeyBytes


@dataclasses.dataclass
class SeigniorageAllocationForValidator(SeigniorageAllocation):
    validator_public_key: PublicKeyBytes


@dataclasses.dataclass
class Timestamp():
    value: float


@dataclasses.dataclass
class Transfer():
    amount: Motes
    deploy_hash: DeployHash
    from_: PublicKeyBytes
    gas: Gas
    source: URef
    target: URef
    correlation_id: int = None
    to_: PublicKeyBytes = None


@dataclasses.dataclass
class URef():
    access_rights: URefAccessRights
    address: Address


class URefAccessRights(enum.Enum):
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7


@dataclasses.dataclass
class ValidatorChanges():
    public_key: PublicKeyBytes
    status_changes: typing.List[ValidatorStatusChange]


@dataclasses.dataclass
class ValidatorStatusChange():
    era_id: EraID
    status_change: ValidatorStatusChangeType


class ValidatorStatusChangeType(enum.Enum):
    Added = 0
    Removed = 1
    Banned = 2
    CannotPropose = 4
    SeenAsFaulty = 3