from pathlib import Path
from typing import Optional

from atoti_core import Plugin


class SynapsePlugin(Plugin):
    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-directquery-synapse.jar"

    @property
    def java_package_name(self) -> Optional[str]:
        return "io.atoti.directquery.synapse"
