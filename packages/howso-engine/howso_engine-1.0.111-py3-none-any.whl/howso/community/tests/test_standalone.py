import warnings

from howso.utilities.installation_verification import InstallationCheckRegistry
from howso.utilities.installation_verification import configure


def test_installation():
    print("[bold]Validating Howso:registered: Installation")
    registry = InstallationCheckRegistry()
    configure(registry)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")