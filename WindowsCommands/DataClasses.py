from OperaPowerRelay import opr
import subprocess
from PluginTemplate import PluginTemplate, DSL

class WindowsCommandsClass:

    
    def __init__(self, type_of_input: str = "console"):
        self._commands = {
            "shutdown": self.shutdown,
            "restart": self.restart,
            "logoff": self.logoff,
            "cancel shutdown": self.cancel_shutdown,
        }
        self.type_of_input = type_of_input
        self.DEFAULT_PAGE = DSL.JS_Div(
                                id="windows-command-input-div",
                                children=[
                                    DSL.JS_Label(
                                        id="windows-command-input-textbox",
                                        text="Windows Command Input"
                                    ),
                                    DSL.JS_Select(
                                        id="windows-command-input-select",
                                        label="Select Command",
                                        options=list(self._commands.keys()),
                                    ),
                                    DSL.JS_Div(
                                        id="windows-command-input-delay-div",
                                        children=[
                                            DSL.JS_Label(
                                                id="windows-command-input-label",
                                                text="Enter Delay (where applicable)"
                                            ),
                                            DSL.JS_Div(
                                                id="windows-command-input-div",
                                                classes="horizontal-div",
                                                children=[
                                                    DSL.JS_TextBox(
                                                        id="windows-command-input-textbox-hours",
                                                        label="H",
                                                        placeholder="0",
                                                    ),
                                                    DSL.JS_TextBox(
                                                        id="windows-command-input-textbox-minutes",
                                                        label="M",
                                                        placeholder="0",
                                                    ),
                                                    DSL.JS_TextBox(
                                                        id="windows-command-input-textbox-seconds",
                                                        label="S",
                                                        placeholder="0",   
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                ] # type: ignore
                            )

    def shutdown(self, **kwargs):
        """
        
        NOTE: Kwargs includes delay in seconds before shutdown. 

        """

        command = f"shutdown /s /t {kwargs.get('delay', 0)}"

        try:
            subprocess.run(command, shell=True, check=True)
            opr.print_from(name="WindowsCommands", message="Shutdown command executed successfully.")
            return True
        except subprocess.CalledProcessError:
            return False

    def restart(self, **kwargs):
        """
        
        NOTE: Kwargs includes delay in seconds before shutdown. 

        """

        command = f"shutdown /r /t {kwargs.get('delay', 0)}"

        try:
            subprocess.run(command, shell=True, check=True)
            opr.print_from(name="WindowsCommands", message="Restart command executed successfully.")
            return True
        except subprocess.CalledProcessError:
            return False

    def logoff(self, **kwargs):
        """
        
        NOTE: Kwargs includes delay in seconds before shutdown. 

        """


        command = f"shutdown /l /t {kwargs.get('delay', 0)}"

        try:
            subprocess.run(command, shell=True, check=True)
            opr.print_from(name="WindowsCommands", message="Logoff command executed successfully.")
            return True
        except subprocess.CalledProcessError:
            return False

    def cancel_shutdown(self, **kwargs):
        command = "shutdown /a"

        try:
            subprocess.run(command, shell=True, check=True)
            opr.print_from(name="WindowsCommands", message="Shutdown cancelled successfully.")
            return True
        except subprocess.CalledProcessError:
            return False

    def execute_command(self, command: str = "", type_of_input: str = None, **kwargs):

        delay = kwargs.get("delay", 0)

        if not type_of_input: 
            type_of_input = self.type_of_input

        if not command:
            match type_of_input:
                case "console":
                    while True:
                        try:
                            opr.list_choices(choices=list(self._commands.keys()), title="Available Windows Commands")
                            command = list(self._commands.keys())[int(PluginTemplate.ophelia_input.console_input(prompt=f"Input [1 - {len(self._commands)}]", opr= False)) - 1]
                            delay = int(opr.input_from(name="WindowsCommands", message="Enter delay in minutes if applicable (0 for no delay)",)) * 60
                            break
                        except (ValueError, IndexError):
                            opr.print_from(name="WindowsCommands", message="\nInvalid selection. Please try again.")
                        except KeyboardInterrupt:
                            opr.print_from(name="WindowsCommands", message="\nOperation cancelled by user.")
                            return None
                case "browser":
                    answer = PluginTemplate.ophelia_input.browser_input(
                        prompt=DSL.JS_Page(
                            title="Windows Command Input",
                            root=self.DEFAULT_PAGE,
                        ))  
                    command = answer.get("windows-command-input-select", "")
                    delay = (
                        int(answer.get("windows-command-input-textbox-hours", 0)) * 3600 +
                        int(answer.get("windows-command-input-textbox-minutes", 0)) * 60 +
                        int(answer.get("windows-command-input-textbox-seconds", 0))
                    )
                case _:
                    raise ValueError("Invalid type_of_input. Must be 'console' or 'browser'.")
                


        if command not in self._commands:
            raise ValueError(f"Command '{command}' is not recognized.")
        
        return self._commands[command](delay=delay)

