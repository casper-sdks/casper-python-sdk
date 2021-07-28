import pytest



@pytest.fixture(scope="function")
def account_main_purse_uref(CLIENT, account_key: bytes, state_root_hash) -> str:
    """Returns an on-chain account's main purse unforgeable reference. 
    
    """
    return CLIENT.queries.get_account_main_purse_uref(account_key, state_root_hash)


@pytest.fixture(scope="function")
def block(CLIENT) -> str:
    """Returns most recent block. 
    
    """
    return CLIENT.queries.get_block()["hash"]


@pytest.fixture(scope="function")
def block_hash(block) -> str:
    """Returns hash of most recent block. 
    
    """
    return block["hash"]


@pytest.fixture(scope="function")
def state_root_hash(CLIENT) -> bytes:
    """Returns current state root hash. 
    
    """
    return CLIENT.queries.get_state_root_hash()


@pytest.fixture(scope="session")
def switch_block(CLIENT) -> str:
    """Returns hash of most recent switch block. 
    
    """
    return CLIENT.queries.get_block_at_era_switch()


@pytest.fixture(scope="session")
def switch_block_hash(switch_block) -> str:
    """Returns hash of most recent switch block. 
    
    """
    return switch_block["hash"]