from functools import lru_cache

from atoti_core import BaseSessionBound, Plugin

from ._visualize import visualize
from ._widget_manager import WIDGET_MANAGER_ATTRIBUTE_NAME, WidgetManager


@lru_cache
def _get_widget_manager() -> WidgetManager:
    return WidgetManager()


class JupyterLab3Plugin(Plugin):
    def post_init_session(self, session: BaseSessionBound, /) -> None:
        session._visualize = visualize

        setattr(session, WIDGET_MANAGER_ATTRIBUTE_NAME, _get_widget_manager())
