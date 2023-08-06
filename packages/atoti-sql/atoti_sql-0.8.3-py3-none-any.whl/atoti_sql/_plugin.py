from pathlib import Path
from typing import Optional

import atoti as tt
from atoti_core import BaseSessionBound, Plugin

from ._source import infer_sql_types, load_sql


class SqlPlugin(Plugin):
    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-sql.jar"

    @property
    def java_package_name(self) -> Optional[str]:
        return "io.atoti.loading.sql"

    def post_init_session(self, session: BaseSessionBound, /) -> None:
        if not isinstance(session, tt.Session):
            return

        session._infer_sql_types = infer_sql_types
        session._load_sql = load_sql
