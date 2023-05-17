# Glossary

Short explanation of some terms used in the documentation and the code.

## Identifier

In a repeating file structure, we need to aggregate files and directories that
are equivalent to each other under a common name. This name is the identifier
and can be simply the name of the file or directory or is extracted from its
name with a regular expression to only keep the par of the name that is coming
to every equivalent file.

Example: the directories "sub-15056", "sub-15888", "sub-24530", etc. would be
aggregated under the identifier "sub-" for the regular expression "^.\*-". This
identifier will then be used to compare them between each other.

Files their parent folder as a prefix in their identifier to allow a distinction
between files of the same name but in different locations under the same
"subject" folder.

## Configuration

A unique layout of files and sub-directories. In this script, two directories
are said to share the same configuration if they have sub-directories and files
in the same arrangement with the same identifiers.

In this example, none of the folders share the same configuration :

```
folder
├── text.txt
└── image.png
folder
├── text.txt
└── imagege.png
folder
├── text.docx
└── image.png
folder
├── sub
│   └── text.txt
└── image.png
folder
└── image.png
```

\*Assuming the identifiers used are the file/directory name as per default.

## Path

A reference to a location in a directory system. All paths in this script are
assumed to be absolute paths (starting from the root of the directory system)
but since the paths are handled by pathlib.Path objects, relative paths should
work as well.

## SmartPath

The custom class used by this script to represent each path (file or directory).
This custom class contains some methods that facilitate the computing of metrics
and comparison.

## Parent

The logical parent of the path, meaning the directory containing the path.

## Children

The files and sub-directories contained in the directory.

## File Structure / file hierarchy

The logical organization of the files and sub-directories under the given
directory.

## File/directory Name

From the patlib library : "A string representing the final path component,
excluding the drive and root, if any: "

```
PurePosixPath('my/library/setup.py').name
---> 'setup.py'
```
