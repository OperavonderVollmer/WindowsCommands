import os, sys
root = os.path.dirname(os.path.abspath(__file__))
if root not in sys.path:
    sys.path.insert(0, root)
import DataClasses
from OperaPowerRelay import opr




def main():
    wc = DataClasses.WindowsCommandsClass(type_of_input="console")

    try:
        wc.execute_command()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        opr.error_pretty(
            exc=e,
            name="Windows Commands",
            message=f"An error occurred while executing Windows Commands: {str(e)}",
        )


    sys.exit(0)
    pass