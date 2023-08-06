from pathlib import Path
from typing import Optional

from atoti_core import Plugin


class AwsPlugin(Plugin):
    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-aws.jar"

    @property
    def java_package_name(self) -> Optional[str]:
        return "io.atoti.loading.s3"
