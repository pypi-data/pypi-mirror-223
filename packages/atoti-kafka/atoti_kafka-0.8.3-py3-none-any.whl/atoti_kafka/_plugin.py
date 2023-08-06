from pathlib import Path
from typing import Optional

import atoti as tt
from atoti_core import BaseSessionBound, Plugin

from ._source import load_kafka


class KafkaPlugin(Plugin):
    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-kafka.jar"

    @property
    def java_package_name(self) -> Optional[str]:
        return "io.atoti.loading.kafka"

    def post_init_session(self, session: BaseSessionBound, /) -> None:
        if not isinstance(session, tt.Session):
            return

        session._load_kafka = load_kafka
