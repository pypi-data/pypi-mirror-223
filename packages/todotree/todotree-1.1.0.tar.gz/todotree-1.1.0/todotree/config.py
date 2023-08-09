from pathlib import Path

import xdg_base_dirs as xdg
import yaml

from todotree.Errors import ConfigFileNotFound


class Config:
    """
    The configuration of todotree.
    """
    def __init__(self):
        #  Main variables.
        self.todo_folder: Path = xdg.xdg_data_home() / "todotree"
        """
        Path to the folder containing the data files.
        
        Relative paths are calculated from the HOME folder. 
        """

        self.project_tree_folder: Path = xdg.xdg_data_home() / "todotree" / "projects"
        """
        Path to the folder containing the projects.
        Defaults to the XDG_DATA_DIR/todotree/projects if not set.
        """

        self.wishlist_folder: Path = xdg.xdg_data_home() / "todotree" / "wishlists"
        """
        Path to the folder containing the wishlist items.
        Defaults to XDG_DATA_DIR/todotree/wishlist if not set.
        """

        self.todofile = Path(self.todo_folder) / "todo.txt"
        """
        Path to the todo.txt file.
        """

        self.donefile = Path(self.todo_folder) / "done.txt"
        """
        Path to the done.txt file.
        """

        self.git_mode = "None"
        """The mode that git runs in. 
        - None disables it,
        - Local add and commits, 
        - Full also pushes it to a remote repo.
        """

        # Features - Enables or disables certain features.
        self.quiet = False
        """A value indicating whether to print anything except the output. Useful in scripts."""

        self.verbose = False
        """A value indicating whether to print more detailed messages."""

        self.enable_wishlist_folder = True
        """A value indicating whether to enable the wishlist folder functionality."""

        self.enable_project_folder = True
        """A value indicating whether to enable the project folder functionality."""

        #  Localization. #
        self.wishlistName = "wenslijst"
        self.noProjectString = "Geen Project"
        self.noContextString = "Geen Context"
        self.emptyProjectString = "> (A) Todo: add next todo for this."
        self.consoleUsage: str = "Usage: "
        self.extendedGood = ' Notice:'
        self.extendedWarn = ' Warning:'
        self.extendedError = ' Error:'

        #  Status Decorators.

        self.consoleGood: str = ' * '
        self.consoleWarn: str = ' ! '
        self.consoleError: str = '!!!'

        # Tree prints.
        self.t_print: str = " ├──"
        self.l_print: str = " │  "
        self.s_print: str = " └──"
        self.e_print: str = "    "

    def read_from_file(self, file: Path):
        """Reads and parses yaml content from `file`."""
        try:
            with open(file, 'r') as f:
                self.read_from_yaml(f.read())
        except FileNotFoundError as e:
            raise ConfigFileNotFound from e

    def read_from_yaml(self, yaml_content: str):
        """Reads and overrides config settings defined in `yaml_content`."""
        # Convert yaml to python object.
        yaml_object = yaml.safe_load(yaml_content)
        if yaml_object is None:
            return
        # Map each item to the self config. TODO: ALL options.
        if yaml_object['main'] is not None:
            main = yaml_object['main']  # Readability.
            self.todo_folder = main['todoFolder']
            # Note: Below may be overridden by command line options.
            self.todofile = main.get('todoFile', Path(self.todo_folder) / "todo.txt")
            self.donefile = main.get('doneFile', Path(self.todo_folder) / "done.txt")
            self.enable_wishlist_folder = main.get('enable_wishlist_folder', self.enable_wishlist_folder)
            self.enable_project_folder = main.get('enable_project_folder', self.enable_project_folder)
            self.project_tree_folder = main.get('projecttree_folder', self.project_tree_folder)
            self.wishlist_folder = main.get('wishlist_folder', self.wishlist_folder)
            self.git_mode = main.get("git_mode", self.git_mode)
            self.quiet = main.get("quiet", self.quiet)
            self.verbose = main.get("verbose", self.verbose)

        # Task manager options.
        try:
            if yaml_object['taskmanager'] is not None:
                self.emptyProjectString = yaml_object['taskmanager'].get('noProjectString', self.emptyProjectString)
                self.wishlistName = yaml_object['taskmanager'].get('wishlistName', self.wishlistName)
                self.noProjectString = yaml_object['taskmanager'].get('noProjectString', self.noProjectString)
                self.noContextString = yaml_object['taskmanager'].get('noContextString', self.noContextString)
        except KeyError:
            # Then the task manager key did not exist.
            pass

        # Status decorator options.
        try:
            if yaml_object['messages'] is not None:
                self.consoleGood = yaml_object['messages'].get('consoleGood', self.consoleGood)
                self.consoleWarn = yaml_object['messages'].get('consoleWarn', self.consoleWarn)
                self.consoleError = yaml_object['messages'].get('consoleError', self.consoleError)
                self.extendedGood = yaml_object['messages'].get('extendedGood', self.extendedGood)
                self.extendedWarn = yaml_object['messages'].get('extendedWarn', self.extendedWarn)
                self.extendedError = yaml_object['messages'].get('extendedError', self.extendedError)
                self.consoleUsage = yaml_object['messages'].get('consoleUsage', self.consoleUsage)
        except KeyError:
            # Then the messages key did not exist.
            pass

        # Tree options.
        if yaml_object['tree'] is not None:
            self.t_print = yaml_object['tree'].get('tprint', self.t_print)
            self.l_print = yaml_object['tree'].get('lprint', self.l_print)
            self.s_print = yaml_object['tree'].get('sprint', self.s_print)
            self.e_print = yaml_object['tree'].get('eprint', self.e_print)
