# Korbit

Korbit mentor CLI will allow you to analyze any local files.

## Development

### Create env

```
conda env update -f environment.yml -n korbit-cli
```

### Run

```
python korbit.py example/subfolder
```

### Troubleshooting

We are using Python=3.11.3 because 3.11.4 and pyinstaller are causing a crash on execution of the script.

https://stackoverflow.com/a/76731974

<details>
<summary>Exception on python==3.11.4</summary>

```
❯ dist/korbit example/subfolder
[8650] Module object for pyimod02_importers is NULL!
Traceback (most recent call last):
  File "PyInstaller/loader/pyimod02_importers.py", line 22, in <module>
  File "pathlib.py", line 14, in <module>
  File "urllib/parse.py", line 40, in <module>
ModuleNotFoundError: No module named 'ipaddress'
Traceback (most recent call last):
  File "PyInstaller/loader/pyiboot01_bootstrap.py", line 17, in <module>
ModuleNotFoundError: No module named 'pyimod02_importers'
[8650] Failed to execute script 'pyiboot01_bootstrap' due to unhandled exception!
```

</details>

## Installation

To install Korbit, you can use pip:

```
pip install korbit-mentor
```

## Usage

To use Korbit, simply run the `korbit` command followed by the path of the file or folder you want to zip. For example, to zip the current folder, you can run:

```
python -m korbit example/subfolder
```

This will create a zip file containing all the files and folders in the current directory.

## Contributing

Contributions are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue or submit a pull request.

## Contact

If you have any questions or need further assistance, feel free to reach out to us at [support@korbit.ai](mailto:support@korbit.ai).
