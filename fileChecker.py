from pathlib import Path


def check_size(path, min_size=50):
    return path.stat().st_size > min_size


def check_permissions(path, min_permissions=(4, 4, 0)):
    path = Path(path)
    perm = list(oct(path.stat().st_mode))

    return perm[-3] >= min_permissions[-3] & perm[-2] >= min_permissions[-2] & perm[-1] >= min_permissions[-1]


def get_total_file_count(path, print_items=False):
    # Count and optionally list all files in directory using pathlib
    base_path = Path(path)
    # Get the files in the given path
    files_in_base_path = (entry for entry in base_path.iterdir() if entry.is_file())
    # Show their name in the std_output
    if print_items:
        for item in files_in_base_path:  # update to count items in subdirectory too?
            print(item.name)
    # Iterate through the directory and count all the files
    return sum(len(files) for _, _, files in os.walk(base_path))