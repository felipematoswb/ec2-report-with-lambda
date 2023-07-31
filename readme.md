## Checking if `Python` and `pip` are installed

To get started, open a terminal or command prompt and type the following commands:

```bash
python --version
pip --version
```

This will display the versions of `Python` and `pip`, verifying if they are correctly installed on your system.

## Installing packages

If the Python file requires external packages, you will need to install them before running the file. You can do this using the `pip install -r` command followed by the name of the requirements.txt file:

```bash
pip install -r requirements.txt
```

This will install the necessary packages to run the script.

## Running the Python file using `pip`

Now that you have the required packages installed, you can run the Python file directly using the `python` command followed by the file name. For example:

```bash
python app.py
```

The script will prompt for the instance ID. If you don't provide an ID, it will fetch all instances. You can search for an instance using any part of its name.

Make sure you are in the correct directory containing the Python file you want to execute, or provide the full path to the file.