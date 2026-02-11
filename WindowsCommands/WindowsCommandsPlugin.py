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
                "shutdown": self.windows_commands.shutdown,
                "restart": self.windows_commands.restart,
                "logoff": self.windows_commands.logoff,
                "cancel": self.windows_commands.cancel_shutdown
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

    def input_scheme(self, root: JS_Container = None, form: bool = None, serialize: bool = False):
        presets = {
            "Shutdown now":{
                "windows-commands-select-command": "shutdown",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Shutdown in 30 minutes":{
                "windows-commands-select-command": "shutdown",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "30",
                "windows-commands-delay-input-seconds": "0",
            },
            "Shutdown in 1 hour":{
                "windows-commands-select-command": "shutdown",
                "windows-commands-delay-input-hours": "1",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Restart now":{
                "windows-commands-select-command": "restart",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Restart in 30 minutes":{
                "windows-commands-select-command": "restart",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "30",
                "windows-commands-delay-input-seconds": "0",
            },
            "Restart in 1 hour":{
                "windows-commands-select-command": "restart",
                "windows-commands-delay-input-hours": "1",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Logoff now":{
                "windows-commands-select-command": "logoff",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            },
            "Cancel Previous Command":{
                "windows-commands-select-command": "cancel",
                "windows-commands-delay-input-hours": "0",
                "windows-commands-delay-input-minutes": "0",
                "windows-commands-delay-input-seconds": "0",
            }
        }
        return super().input_scheme(root = DSL.JS_Div(
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
                                label="HH",
                                type="number",
                                hint="Hours",
                            ),
                            DSL.JS_TextBox(
                                id="windows-commands-delay-input-minutes",
                                label="MM",
                                type="number",
                                hint="Minutes",
                            ),
                            DSL.JS_TextBox(
                                id="windows-commands-delay-input-seconds",
                                label="SS",
                                type="number",
                                hint="Seconds",
                            ),
                        ]
                    )
                )
            ]
        ), 
        form=form, serialize=serialize, 
        effects = { "windows-commands-select-quick-command": "applyPreset" },
        presets=presets
        )

    
    def execute(self, *args, **kwargs):
        return self.windows_commands.execute_command(type_of_input=self._meta["type_of_input"], **kwargs)

    def direct_execute(self, *args, **kwargs):
        command = kwargs.get("command", "")
        delay = kwargs.get("delay", 0)

        return super().run_command(command=command,delay=delay,)

    def clean_up(self, *args, **kwargs):
        pass


def get_plugin(): return plugin()



