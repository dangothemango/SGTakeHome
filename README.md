# SGTakeHome-Dan Gorman
## Usage Instructions
### Helper Scripts
Two helper scripts are provided for convinence
* `runLocally.bat` - This script will run the tests and start the server if successful or exit if not
* `buildAndRunInDocker.bat` - This script runs the test suite, docker build, and docker run. It exits if any of these steps fail
### Manual Commands
It is expected that these commands be run from the top level directory of the project
* To run the test suite use `python3 -m unittest discover -s src`
* To run the server use `python3 src/run.py`
