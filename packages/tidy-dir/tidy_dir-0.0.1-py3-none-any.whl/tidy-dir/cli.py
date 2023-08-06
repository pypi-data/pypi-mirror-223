import argparse
from tidy_dir.clean import clean_directory


def main():
    parser = argparse.ArgumentParser(
        prog="tidy-dir",
        description="Tidy up a directory using a configuration file",
    )
    parser.add_argument("directory", help="The directory to tidy up")
    args = parser.parse_args()

    clean_directory(args.directory)


if __name__ == "__main__":
    main()
