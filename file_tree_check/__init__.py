"""Structure of the script.

- main.py is where the sequential series of processing takes places.
- statBuilder.py handles the creation of the output files.
- identifierEngine.py contains the IdentifierEngine class.
    This class is used to extract the identifier string
    from files and directories based on the regular expression
    given to it (from the config file).
- smartPath.py contains the SmartPath abstract class.
    The SmartFilePath and SmartDirectoryPath both inherit from it.
- smartFilePath.py contains the SmartDirectoryPath class,
    the implementation of SmartPath for files.
- smartDirectoryPath.py contains the SmartFilePath class,
    the implementation of SmartPath for directories.

"""

from __future__ import annotations
