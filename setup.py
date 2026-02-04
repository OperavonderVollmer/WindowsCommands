from setuptools import setup, find_packages

setup(
    name="WindowsCommands",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "OperaPowerRelay @ git+https://github.com/OperavonderVollmer/OperaPowerRelay.git",
        "PluginTemplate @ git+https://github.com/OperavonderVollmer/PluginTemplate.git",
        "TrayIcon @ git+https://github.com/OperavonderVollmer/TrayIcon.git",
    ],
    python_requires=">=3.7",
    author="Opera von der Vollmer",
    description="A plugin to execute Windows system commands like shutdown, restart, and logoff.",
    url="https://github.com/OperavonderVollmer/WindowsCommands", 
    license="MIT",
)
