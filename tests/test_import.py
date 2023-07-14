"""Test world-parser."""

import world_parser


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(world_parser.__name__, str)
