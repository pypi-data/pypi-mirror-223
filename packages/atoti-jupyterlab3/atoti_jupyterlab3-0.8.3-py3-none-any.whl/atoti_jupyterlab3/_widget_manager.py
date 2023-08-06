from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional
from uuid import uuid4

from atoti_core import (
    TEXT_MIME_TYPE,
    BaseSessionBound,
    get_ipython,
    keyword_only_dataclass,
)

from ._comm_targets import WIDGET_COMM_TARGET_NAME
from ._mime_types import WIDGET_MIME_TYPE

if TYPE_CHECKING:
    from ipykernel.ipkernel import (  # pylint: disable=undeclared-dependency, nested-import
        IPythonKernel,
    )

WIDGET_MANAGER_ATTRIBUTE_NAME = "_widget_manager"


@keyword_only_dataclass
@dataclass(frozen=True)
class Cell:
    """Hold some details about the notebook cell currently being executed."""

    has_built_widget: bool
    id: str  # noqa: A003


class WidgetManager:
    """Manage Jupyter comms and keep track of the widget state coming from kernel requests."""

    _cell: Optional[Cell] = None
    _running_in_supported_kernel: bool = False

    def __init__(self) -> None:
        """Create the manager."""
        ipython = get_ipython()

        if ipython is None:
            return

        kernel = getattr(ipython, "kernel", None)

        if kernel is None or not hasattr(kernel, "comm_manager"):
            # When run from IPython or another less elaborated environment
            # than JupyterLab, these attributes might be missing.
            # In that case, there is no need to register anything.
            return

        self._running_in_supported_kernel = True

        self._wrap_execute_request_handler_to_extract_widget_details(kernel)

    def display_widget(
        self, session: BaseSessionBound, /, *, name: Optional[str]
    ) -> None:
        """Display the output that will lead the Atoti JupyterLab extension to show a widget."""
        if not self._running_in_supported_kernel:
            print(  # noqa: T201
                "Atoti widgets can only be shown in JupyterLab with the Atoti JupyterLab extension enabled."
            )
            return

        from ipykernel.comm import (  # pylint: disable=undeclared-dependency, nested-import
            Comm,
        )
        from IPython.display import (  # pylint: disable=undeclared-dependency, nested-import
            publish_display_data,
        )

        data: dict[str, Any] = {
            TEXT_MIME_TYPE: f"""Open the notebook in JupyterLab with the Atoti extension enabled to {"see" if self._cell and self._cell.has_built_widget else "build"} this widget."""
        }

        widget_creation_code = session._get_widget_creation_code()

        if widget_creation_code:
            data[WIDGET_MIME_TYPE] = {
                "name": name,
                "sessionId": session._id,
                "sessionLocation": session._location,
                "widgetCreationCode": session._get_widget_creation_code(),
            }

        # Mypy cannot find the type of this function.
        publish_display_data(data)  # type: ignore[no-untyped-call]

        if self._cell is None:
            return

        widget_id = str(uuid4())

        # Mypy cannot find the type of this class.
        Comm(  # type: ignore[no-untyped-call]
            WIDGET_COMM_TARGET_NAME,
            # The data below is either sensitive (e.g. auth headers) or change from one cell run to the other.
            # It is better to not send it through publish_display_data so that it does not end up in the .ipynb file.
            data={
                "cellId": self._cell.id,
                "sessionHeaders": session._generate_auth_headers(),
                "widgetId": widget_id,
            },
        ).close()

        session._block_until_widget_loaded(widget_id)

    def _wrap_execute_request_handler_to_extract_widget_details(
        self,
        kernel: IPythonKernel,
    ) -> None:
        original_handler = kernel.shell_handlers["execute_request"]

        def execute_request(  # pylint: disable=too-many-positional-parameters
            stream: Any, ident: Any, parent: Any
        ) -> Any:
            metadata = parent["metadata"]
            cell_id = metadata.get("cellId")
            self._cell = (
                Cell(
                    has_built_widget=bool(metadata.get("atoti", {}).get("state")),
                    id=cell_id,
                )
                if cell_id is not None
                else None
            )

            return original_handler(stream, ident, parent)

        kernel.shell_handlers["execute_request"] = execute_request
