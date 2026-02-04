import os, sys
root = os.path.dirname(os.path.abspath(__file__))
if root not in sys.path:
    sys.path.insert(0, root)
import DataClasses
from PluginTemplate import PluginTemplate

class plugin(PluginTemplate.ophelia_plugin):
    def __init__(self):
        
        # TODO: Change to browser once HUD side is implemented
        self.windows_commands = DataClasses.WindowsCommandsClass(type_of_input="console") 
        super().__init__(
            name="WindowsCommands",
            description="A plugin to execute Windows system commands like shutdown, restart, and logoff.",
            needs_args=True,
            type_of_input="console",
            command_map={
                "shutdown": self.windows_commands.shutdown,
                "restart": self.windows_commands.restart,
                "logoff": self.windows_commands.logoff
            },
            quick_commands={
                "Shutdown now": self.windows_commands.shutdown,
                "Shutdown in 30 minutes": lambda **kwargs: self.windows_commands.shutdown(delay=1800),
                "Shutdown in 1 hour": lambda **kwargs: self.windows_commands.shutdown(delay=3600),
                "Restart now": self.windows_commands.restart,
                "Restart in 30 minutes": lambda **kwargs: self.windows_commands.restart(delay=1800),
                "Restart in 1 hour": lambda **kwargs: self.windows_commands.restart(delay=3600),
                "Logoff now": self.windows_commands.logoff,
                "Cancel Command": self.windows_commands.cancel_shutdown
            },
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



