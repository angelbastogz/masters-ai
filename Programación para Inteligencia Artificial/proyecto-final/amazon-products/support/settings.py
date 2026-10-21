from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    model_name: str = Field(..., description="Nombre del modelo", min_length=1)
    batch_size: int = Field(..., description="Batch size", gt=0)
    device: str = Field(..., description="Device")


def load_config(path: Path) -> Settings:
    return Settings.model_validate_json(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    config = load_config(CONFIG_PATH)
    print(config)
