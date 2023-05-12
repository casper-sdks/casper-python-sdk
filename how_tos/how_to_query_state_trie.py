import argparse

from pycspr import NodeClient
from pycspr import NodeConnection


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to qeury global state trie store.")

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

# CLI argument: path to trie store key.
_ARGS.add_argument(
    "--trie-key",
    dest="trie_key",
    help="Hex encoded key of a leaf within global state trie store.",
    type=str,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client: NodeClient = _get_client(args)

    # Set node JSON-RPC query response.
    response = client.get_state_trie(args.trie_key)

    print("-" * 72)
    print(response.hex() if response else response)
    print("-" * 72)


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
