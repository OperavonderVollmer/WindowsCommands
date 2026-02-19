import os, sys

from PluginTemplate.DSL import JS_Container
root = os.path.dirname(os.path.abspath(__file__))
if root not in sys.path:
    sys.path.insert(0, root)
from WindowsCommandsDataClasses import WindowsCommandsClass
from PluginTemplate import PluginTemplate, DSL

class plugin(PluginTemplate.ophelia_plugin):
    def __init__(self):
        
        # TODO: Change to browser once HUD side is implemented
        self.windows_commands = WindowsCommandsClass(type_of_input="console") 
        super().__init__(
            name="WindowsCommands",
            description="A plugin to execute Windows system commands like shutdown, restart, and logoff.",
            needs_args=True,
            type_of_input="console",
            command_map={
                "shutdown": self.handle_shutdown,
                "restart": self.handle_restart,
                "logoff": self.handle_logoff,
                "cancel": self.handle_cancel_shutdown
            },
            quick_commands={
                "Shutdown now": self.windows_commands.shutdown,
                "Shutdown in 30 minutes": lambda **kwargs: self.windows_commands.shutdown(delay=1800),
                "Shutdown in 1 hour": lambda **kwargs: self.windows_commands.shutdown(delay=3600),
                "Restart now": self.windows_commands.restart,
                "Restart in 30 minutes": lambda **kwargs: self.windows_commands.restart(delay=1800),
                "Restart in 1 hour": lambda **kwargs: self.windows_commands.restart(delay=3600),
                "Logoff now": self.windows_commands.logoff,
                "Cancel Previous Command": self.windows_commands.cancel_shutdown
            },
        )

    def handle_shutdown(self, delay=0, **kwargs):
        if self.windows_commands.shutdown(delay=delay or kwargs.get("delay", 0)):
            text = f"Shutdown command executed with delay of {delay} seconds."
        else:
            text = "Failed to execute shutdown command."
        return super().input_scheme(
            root=DSL.JS_Div(
                id="windows-commands-shutdown-div",
                children=[
                    DSL.JS_Label(
                        id="windows-commands-shutdown-label",
                        text=text
                    ),
                ]
            ),
            form=True, serialize=True)

    def handle_restart(self, delay=0, **kwargs):
        if self.windows_commands.restart(delay=delay or kwargs.get("delay", 0)):
            text = f"Restart command executed with delay of {delay} seconds."
        else:
            text = "Failed to execute restart command."
        return super().input_scheme(
            root=DSL.JS_Div(
                id="windows-commands-restart-div",
                children=[
                    DSL.JS_Label(
                        id="windows-commands-restart-label",
                        text=text
                    ),
                ]
            ),
            form=True, serialize=True)

    def handle_logoff(self, delay=0, **kwargs):
        if self.windows_commands.logoff(delay=delay or kwargs.get("delay", 0)):
            text = f"Logoff command executed with delay of {delay} seconds."
        else:
            text = "Failed to execute logoff command."
        return super().input_scheme(
            root=DSL.JS_Div(
                id="windows-commands-logoff-div",
                children=[
                    DSL.JS_Label(
                        id="windows-commands-logoff-label",
                        text=text
                    ),
                ]
            ),
            form=True, serialize=True)

    def handle_cancel_shutdown(self, **kwargs):
        if self.windows_commands.cancel_shutdown():
            text = "Cancel shutdown command executed."
        else:
            text = "Failed to execute cancel previous command."
        return super().input_scheme(
            root=DSL.JS_Div(
                id="windows-commands-cancel-div",
                children=[
                    DSL.JS_Label(
                        id="windows-commands-cancel-label",
                        text=text
                    ),
                ]
            ),
            form=True, serialize=True)

    def input_scheme(self, root: JS_Container = None, form: bool = None, serialize: bool = True):
        presets = {
            "Shutdown now":{
                "windows-commands-select-command": "SHUTDOWN",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Shutdown in 30 minutes":{
                "windows-commands-select-command": "SHUTDOWN",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "30",
                "windows-commands-delay-input-seconds": "0",
            },
            "Shutdown in 1 hour":{
                "windows-commands-select-command": "SHUTDOWN",
                "windows-commands-delay-input-hours": "1",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Restart now":{
                "windows-commands-select-command": "RESTART",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Restart in 30 minutes":{
                "windows-commands-select-command": "RESTART",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "30",
                "windows-commands-delay-input-seconds": "0",
            },
            "Restart in 1 hour":{
                "windows-commands-select-command": "RESTART",
                "windows-commands-delay-input-hours": "1",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Logoff now":{
                "windows-commands-select-command": "LOGOFF",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Cancel Previous Command":{
                "windows-commands-select-command": "CANCEL",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            }
        }
        scheme = super().input_scheme(root = DSL.JS_Div(
            id="windows-commands-div",
            children=[
                DSL.JS_Select(
                    id="windows-commands-select-quick-command",
                    label="Preset Commands",
                    options=list(key for key in presets.keys())
                ),
                DSL.JS_Select(
                    id="windows-commands-select-command",
                    label="Select Command",
                    options=list(key.upper() for key in self._meta["command_map"].keys())
                ),
                DSL.JS_Header_Div(
                    id="windows-commands-delay-div",
                    header="Delay - 0 for no delay",
                    header_level=3,
                    child=DSL.JS_Div(
                        id="windows-commands-delay-input-div",
                        classes="horizontal-div",
                        children=[
                            DSL.JS_TextBox(
                                id="windows-commands-delay-input-hours",
                                label="Hours",
                                input_type="number-pad",
                                hint="HH",
                            ),
                            DSL.JS_TextBox(
                                id="windows-commands-delay-input-minutes",
                                label="Minutes",
                                input_type="number-pad",
                                hint="MM",
                            ),
                            DSL.JS_TextBox(
                                id="windows-commands-delay-input-seconds",
                                label="Seconds",
                                input_type="number-pad",
                                hint="SS",
                            ),
                        ]
                    )
                )
            
            ]
        ), form=form, serialize=serialize, 
        effects = { "windows-commands-select-quick-command": "applyPreset" },
        presets=presets)

        return scheme

    
    def execute(self, *args, **kwargs):
        if "windows-commands-select-command" in kwargs:
            return self.direct_execute(*args, **kwargs)
        return self.windows_commands.execute_command(type_of_input=self._meta["type_of_input"], **kwargs)

    def direct_execute(self, *args, **kwargs):
        command = str(kwargs.get("windows-commands-select-command", "")).lower()
        delay = int(kwargs.get("windows-commands-delay-input-hours", 0))*3600 + int(kwargs.get("windows-commands-delay-input-minutes", 0))*60 + int(kwargs.get("windows-commands-delay-input-seconds", 0))


        return super().run_command(command=command,delay=delay,)

    def clean_up(self, *args, **kwargs):
        pass


def get_plugin(): return plugin()



