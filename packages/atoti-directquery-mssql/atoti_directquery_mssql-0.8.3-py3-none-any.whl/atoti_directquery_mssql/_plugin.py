from pathlib import Path
from typing import Optional

from atoti_core import Plugin


class MsSqlPlugin(Plugin):
    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-directquery-mssql.jar"

    @property
    def java_package_name(self) -> Optional[str]:
        return "io.atoti.directquery.mssql"
