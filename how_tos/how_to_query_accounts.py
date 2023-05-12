import argparse
import os
import pathlib

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr.types import CL_Key
from pycspr.types import PrivateKey
from pycspr.types import PublicKey


def _get_default_account_id():
    return "ed1fa62fe1913ab0aa6b8eea70b89967a9b5f0b21f51678134a95dc82421ce9d"
	pycspr.create_deploy_approval
	# pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "users" / "user-1"


# Path to NCTL assets.
_PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to qeury on-chain account information.")

# CLI argument: hex encoded key of an on-chain account identifier - defaults to NCTL user 1.
_ARGS.add_argument(
    "--account-id",
    default=_get_default_account_id(),
    dest="account_id",
    help="Hex encoded key of an on-chain account identifier.",
    type=str,
    )

# CLI argument: name of target chain - defaults to NCTL chain.
_ARGS.add_argument(
    "--chain",
    default="casper-net-1",
    dest="chain_name",
    help="Name of target chain.",
    type=str,
    )

# CLI argument: host address of target node - defaults to NCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client: NodeClient = _get_client(args)

    print(str(args.account_id))

    response = client.get_account_info(args.account_id)

    # print(response)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
