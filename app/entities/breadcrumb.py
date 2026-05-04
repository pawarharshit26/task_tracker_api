from app.entities.base import BaseEntity


class BreadcrumbEntity(BaseEntity):
    theme_preset_key: str
    theme_name: str
    track_name: str
    goal_title: str | None = None
