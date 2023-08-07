"""
Utilities to easily read PlaygroundClient arguments from the command line 
"""

import argparse
from typing import Tuple, Dict, Any
from .client import *
import random

SLEEP_TIME = 1


def get_arguments(pettingzoo=False) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    A utility function to read arguments to initialize and run a
    playground client from the command line.

    Returns (init_arguments, run_arguments)
    """
    args = _parse_arguments()

    init_args = {
        "auth_file": args.authfile,
        "render_gameplay": args.render,
    }

    run_args = {
        "pool": Pool(args.pool),
        "num_games": args.num_games,
        "maximum_messages": args.max_messages,
        "self_training": args.self_training,
        "create_lobby": args.create_lobby,
        "lobby_id": args.lobby_id,
    }
    if not pettingzoo:
        run_args["game_parameters"] = json.loads(args.params)

    return init_args, run_args


def _parse_arguments() -> argparse.Namespace:
    random_model_name = f"model-{random.randrange(1e4, 1e5)}"
    description = f"Runs an instance of a playgroundrl client. "
    parser = argparse.ArgumentParser(prog="your_client.py", description=description)
    parser.add_argument(
        "authfile", help="Path to your authfile. Can be generated on your profile page."
    )
    parser.add_argument(
        "-p",
        "--pool",
        dest="pool",
        help="Which pool to join. (1 is model-only, 2 is open)",
        choices=[1, 2],
        type=int,
        default=2,
    )
    parser.add_argument(
        "-s",
        "--self-training",
        dest="self_training",
        help="When set, model plays itself instead of entering game matching",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--render",
        dest="render",
        help="Create link to view game in browser",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--num_games",
        dest="num_games",
        type=int,
        help="Number of games to play before exiting",
        default=1,
    )
    parser.add_argument(
        "--params",
        dest="params",
        help="JSON Dict of optional game parameters.",
        type=str,
        default="{}",
    )
    parser.add_argument(
        "-c",
        "--create_lobby",
        dest="create_lobby",
        help="When set, we create a new lobby and display the code.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--lobby_id",
        dest="lobby_id",
        help="Optional parameter specifying the six-digit code of the lobby to join.",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--max-messages",
        dest="max_messages",
        help="Timeout after X messages exchanged",
        type=int,
        default=500000,
    )
    return parser.parse_args()
