import tkinter as tk
from typing import Callable

import customtkinter as ctk

import flowmatic
from flowmatic import gui
from flowmatic.flows.flow import Flow
from flowmatic.gui.screens.screen import FlowScreen, Screen
from ...forms import FormValidation
from ...forms.fields.field import Field


class FormScreen(Screen):
    field_list: list[Field] | None
    fields: dict[str, Field]
    validations: list[FormValidation] | None = None
    __message: tk.StringVar

    @property
    def message(self) -> str:
        return self.__message.get()

    @message.setter
    def message(self, value: str) -> None:
        """Set message.

        Args:
            value (str): Message."""
        self.__message.set(value)

    def __init__(
        self,
    ) -> None:
        self.fields = {}
        self.__message = tk.StringVar(value="")

    @property
    def values(self) -> dict[str, str | int | list[str]]:
        """Get values from fields.

        Returns:
            dict[str, str]: Values from fields."""
        return {
            label: field.value for label, field in self.fields.items() if field.value
        }

    def validate(self) -> None:
        if not self.validations:
            return

        for validation in self.validations:
            validation.validate(self.values)

    def build(  # pylint: disable=arguments-differ
        self,
        *,
        title: str,
        validations: list[FormValidation] | None = None,
        on_submit: Callable[[], None],
        submit_text: str = "Submit",
        back_command: Callable[[], None] | None = None,
        fields: list[Field] | None = None,
        field_factory: Callable[..., list[Field]] | None = None,
    ) -> None:
        """Build screen.

        Args:

            title (str): Title of screen.
            validate_command (Callable[[], None]): Command to run when validate button is pressed.
            validate_text (str, optional): Text of validate button. Defaults to "Submit".
            back_command (Callable[[], None], optional): Command to run when back button is pressed.
                 Defaults to None.
        """
        # Variables
        self.field_list = (fields or []) + (field_factory() if field_factory else [])
        self.validations = validations

        def validate_command() -> None:
            try:
                self.validate()
            except AssertionError as error:
                self.message = str(error)
                flowmatic.update_gui()
            else:
                on_submit()

        # Title
        ctk.CTkLabel(self.master, text=title).pack(**gui.pack_defaults)

        # Fields
        if self.field_list:
            fields_frame = (
                ctk.CTkScrollableFrame(
                    self.master, height=gui.HEIGHT - 150, width=gui.WIDTH
                )
                if not isinstance(self.master, ctk.CTkScrollableFrame)
                else ctk.CTkFrame(self.master)
            )
            fields_frame.pack(**gui.pack_defaults)
            for field in self.field_list:
                self.fields[field.label] = field(fields_frame).build(
                    **gui.pack_defaults
                )

        # Message
        ctk.CTkLabel(self.master, textvariable=self.__message).pack(**gui.pack_defaults)

        # Buttons
        pack_args = gui.pack_defaults  # | {"pady": (10, 20)}
        button_frame = ctk.CTkFrame(self.master)
        button_frame.pack(**pack_args)
        ctk.CTkButton(button_frame, text=submit_text, command=validate_command).pack(
            **gui.pack_defaults, side=tk.RIGHT
        )
        if back_command:
            ctk.CTkButton(button_frame, text="Back", command=back_command).pack(
                **gui.pack_defaults, side=tk.LEFT
            )


class FlowFormScreen(FormScreen, FlowScreen):
    def __init__(self, flow: Flow) -> None:
        self.flow = flow
        super().__init__()
