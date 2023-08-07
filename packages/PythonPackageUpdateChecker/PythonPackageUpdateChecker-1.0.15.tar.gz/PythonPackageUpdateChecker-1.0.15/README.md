# PythonPackageUpdateChecker

PythonPackageUpdateChecker is a utility that allows to automatically check for updates of installed Python packages and update them to the latest versions.

It uses asynchronous requests to PyPI to fetch information about newest versions of packages, compares them to locally installed ones and executes pip commands to update packages if needed.

Progress of update is displayed using tqdm library and overall execution time is measured.

## Usage

To use PythonPackageUpdateChecker, simply run the python script. It will:

- Get local Python packages and versions
- Fetch latest versions from PyPI asynchronously 
- Determine which packages need update
- Display list of outdated packages
- Update required packages with pip
- Show progress bars during update
- Play sound on finish
- Print total execution time

## Requirements

The following libraries are required:

- pkg_resources
- subprocess
- asyncio
- time
- aiohttp
- tqdm
- winsound

Python 3.6 or later is required.

## License

This project is licensed under the MIT license. See the LICENSE file for details.

## Author

Andrii Bohachev

Email: andriybogachev@gmail.com

Social profiles:
- https://www.facebook.com/andriybogachev
- https://github.com/andriybogachev/  
- https://t.me/starf1re
- https://www.linkedin.com/in/andriibohachev/