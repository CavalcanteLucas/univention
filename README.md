### Task

**Implementation of a Python script for archieving files on a Linux system**

A Python script should be implemented which moves all files from all members of a group to an archive folder.
The name of the group should be a parameter of the program.

The program should be robust, e.g. with respect to multiple invocations in short time.
The events and results should be available in a log file.

The program should be installable as a Debian package and should be made available for download.
The Debian package does not have to be built, the sources are sufficient.

##

### Instructions of use:

Run:

```
>>> python /task-0.1/usr/bin/main.py --groupname {GROUP_NAME}
```

Optionally, change the targe directory setting the `TARGETDIR` environment variable.
You can use the file `.envrc`, with the command `direnv allow`.

Output log will be reported on file `out.log`.


**Test**:

In order to run the test suite, make sure to have all required dependencies installed.
For that, it is mostly recommended to create a virtual environment.
If you have pyenv installed, run:
```
pyenv virtualenv 3.8.10 univention
pyenv activate univention
pip install -r requirements.txt
```

Then run:
```
>>> python /task-0.1/usr/bin/test.py
```

##

<sup>**Author: Lucas Cavalcante\<lucascpcavalcante@gmail.com\>, 2021**</sup>

