# tidy-dir

tidy-dir is a simple tool designed to help you clean up your directories. It provides an easy and efficient way to manage and organize your files.

## Installation

You can install tidy-dir using pip. Run the following command in your terminal:

```bash
pip install tidy-dir
```

## Usage

Using tidy-dir is straightforward. After installation, you can run the command followed by the directory you want to tidy up:

```bash
tidy-dir /path/to/your/directory/
```

For example, if you want to tidy up a directory located at /mydirectory/smt/, you would use:

```bash
tidy-dir /mydirectory/smt/
```
or current directory:
```bash
tidy-dir .
```

## Configuration

tidy-dir requires a .tidy-dir-config.json file in the directory you want to tidy up. This configuration file should follow the schema:

```json
{
  "new_dir": [".fileextension"]
}
```
In this schema, replace ".fileextension" with the file extension of the files you want to move to the new directory.
For example:
```json
{
  "docs": [".txt", ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls"],
  "images": [".png", ".jpg", ".jpeg", ".gif", ".svg"],
  "videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
  "music": [".mp3", ".wav", ".ogg", ".flac", ".m4a"],
  "archives": [".zip", ".rar", ".tar", ".gz", ".7z", ".iso", ".xz", ".bz2"],
}
```



## Contributing

Contributions to tidy-dir are always welcome. If you have any ideas or suggestions, feel free to open an issue or submit a pull request.

## License

tidy-dir is licensed under the (MIT license)[./LICENSE]. For more information, see the LICENSE file in our repository.