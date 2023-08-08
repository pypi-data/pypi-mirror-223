"""
Main - Module responsible for the main program. Parses the arguments and calls the other modules.
"""
__version__ = "1.2.2"

import argparse
import os
import re

from src.ColoredLogger.ColoredLogger import ColoredLogger

from datetime import datetime

from src.ChangeMediaName import ChangeMediaName

logger = ColoredLogger()


def nameFormatter(nf: str, aux: str) -> bool:
    global logger
    logger.debug(f"Parsing {aux}name format")
    now = datetime.now().strftime(nf)
    nowdate = datetime.strptime(now, nf)

    if nowdate.year == 1900 and nowdate.month == 1 and nowdate.day == 1:
        logger.critical(f"The {aux}name format is not valid for a date.")
        return False

    if aux == "":
        invalid_characters = re.compile(r'[^\w\-.]')
        if invalid_characters.search(now):
            logger.critical(f"The {aux}name format is not valid for a file name.")
            return False
    else:
        invalid_characters = re.compile(r'[/<>:\"\\|?*]')
        if invalid_characters.search(now):
            logger.critical(f"The {aux}name format is not valid for a folder name.")
            return False

    logger.info(f"Example of {aux}name format: {now}")
    return True


def recursiveSearch(path: str) -> list[str]:
    files: list[str] = []
    for root, dirs, f in os.walk(path):
        for file in f:
            files.append(os.path.join(root, file))
    return [x.replace("\\", "/") for x in files]


def notRecursiveSearch(path: str) -> list[str]:
    return [os.path.join(path, x).replace("\\", "/") for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]


def getFiles(paths: list[str], recursive: bool) -> list[str]:
    global logger
    files: list[str] = []
    for path in paths:
        if not os.path.exists(path):
            raise BaseException(f"The path '{path}' does not exist.")
        elif os.path.isfile(path):
            files.append(path)
        else:
            if recursive:
                files += recursiveSearch(path)
            else:
                files += notRecursiveSearch(path)
    return files


def getScanFiles(input_files: list[str], recursive: bool, ignored_paths: list[str], not_ignore_subfolders: bool,
                 filetypes: list[str]) -> list[str]:
    global logger
    logger.debug("Getting files to scan")

    files = getFiles(input_files, recursive)
    ignored = getFiles(ignored_paths, not_ignore_subfolders)

    files = [x for x in files if x not in ignored and os.path.splitext(x)[1].lower() in filetypes]
    length = len(files)

    logger.info(f"{length} file{'s' if length != 1 else ''} to scan")

    return files


def main():
    global logger
    parser = argparse.ArgumentParser(
        description="Program to scan multimedia files and rename them to their creation date.")
    parser.add_argument("-i", "--input-files", nargs="+", required=True, help="File(s) or folder(s) to scan")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Verbose mode")
    parser.add_argument("-r", "--recursive", action="store_true", help="Scan folders recursively", default=False)
    parser.add_argument("-ni", "--ignored-paths", nargs="*", help="Files or folders to be ignored", default=[])
    parser.add_argument("-nr", "--not-ignore-subfolders", action="store_false", default=True,
                        help="Choose to not ignore subfolders of the ignored paths")
    parser.add_argument("-t", "--file-types", nargs="*", default=[], help="List of file types to consider")
    parser.add_argument("-nt", "--not-file-types", nargs="*", default=[], help="List of file types to ignore")
    parser.add_argument("-oi", "--only-images", action="store_true", help="Consider only images", default=False)
    parser.add_argument("-ov", "--only-videos", action="store_true", help="Consider only videos", default=False)
    parser.add_argument("-cf", "--create-new-folders", action="store_true", default=False,
                        help="Create new folders according to the new image names")
    parser.add_argument("-fn", "--name-format", default="%Y%m%d_%H%M%S", help="Format of the new names")
    parser.add_argument("-ff", "--name-folder-format", default="%Y - %m - %d", help="Format of the new folder names")

    args = parser.parse_args()

    logger = ColoredLogger(args.verbose)
    initialTimer = datetime.now()
    logger.debug("Program started.")

    if not nameFormatter(args.name_format, "") or not nameFormatter(args.name_folder_format, "folder "):
        return

    filetypes = getFiletypes(args.file_types, args.only_images, args.only_videos, args.not_file_types)
    files = getScanFiles(args.input_files, args.recursive, args.ignored_paths, args.not_ignore_subfolders, filetypes)

    nChanged, nErrors = ChangeMediaName.cmn(logger, files, args.create_new_folders, args.name_format, args.name_folder_format)
    nProcessed = len(files)
    endTimer = datetime.now()
    logger.info(f"Processed {nProcessed} file{'s' if nProcessed != 1 else ''} in {endTimer - initialTimer}.")
    logger.info(f"Changed {nChanged} file{'s' if nChanged != 1 else ''}.")
    logger.info(f"Errors: {nErrors}.")
    logger.info("Program finished.")


def getFiletypes(file_types: list[str], only_images: bool, only_videos: bool, not_file_types: list[str]) -> list[str]:
    global logger
    logger.debug("Getting file types to scan")
    supported = [".jpg", ".jpeg", ".png", ".heic", ".webp", '.mp4', '.avi', '.mov']
    filetypes = []
    if file_types:
        for file_type in file_types:
            if file_type not in supported:
                logger.warning(f"File type '{file_type}' is not supported.")
                continue
            filetypes.append(file_type)
    else:
        if only_images:
            filetypes = [".jpg", ".jpeg", ".png", ".heic", ".webp"]
        elif only_videos:
            filetypes = ['.mp4', '.avi', '.mov']

        if not_file_types:
            if filetypes:
                filetypes = [x for x in filetypes if x not in not_file_types]
            else:
                filetypes = [x for x in supported if x not in not_file_types]

        if not filetypes:
            filetypes = supported
    logger.info(f"{len(filetypes)} file types to scan: {filetypes}")
    return filetypes


if __name__ == "__main__":
    main()
