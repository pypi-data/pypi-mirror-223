from pathlib import Path
from typing import Optional

from atoti_core import Plugin


class DatabricksPlugin(Plugin):
    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-directquery-databricks.jar"

    @property
    def java_package_name(self) -> Optional[str]:
        return "io.atoti.directquery.databricks"
