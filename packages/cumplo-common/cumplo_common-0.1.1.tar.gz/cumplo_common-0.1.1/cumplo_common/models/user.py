# pylint: disable=no-member

from pydantic import BaseModel, Field

from cumplo_common.models.configuration import Configuration
from cumplo_common.models.notification import Notification


class User(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    is_admin: bool = Field(False)
    webhook_url: str | None = Field(None)
    notifications: dict[int, Notification] = Field(default_factory=dict, exclude=True)
    configurations: dict[int, Configuration] = Field(default_factory=dict, exclude=True)
