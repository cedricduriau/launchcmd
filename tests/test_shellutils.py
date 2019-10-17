# tool modules
from launchcmd import shellutils


def test_run_check_output():
    """Test running a valid command and checking its output type/format."""
    assert shellutils.run_check_output("exit 0") == []
