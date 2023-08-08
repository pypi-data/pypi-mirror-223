# gitinspired-cli-june
# Subsys

Subsys is a Git-inspired assignment submission system that allows students to manage and submit their assignments easily.

## Features

- Initialize a new repository for assignment management.
- Create snapshots of assignment progress.
- Revert to previous snapshots.
- Submit snapshots to the central repository.
- Configure student details and assignment information.

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone or download this repository.
3. Navigate to the project directory.
4. Install the application using the following command:

Run: pip install .

NB: Permission will be required on some windows devices so it'll be best to start command prompt in administrator mode.

Alternatiely you can run:
pip install https://github.com/AmaliTech-Training-Academy/gitinspired-cli-june.git

## Usage

- To initialize a new repository, use the following command:

subsys init

- To configure student details and assignment information, use the following command:

subsys config

- To create a snapshot of assignment progress, use the following command:

subsys snap [SNAPSHOT_NAME]

- To submit a snapshot to the central repository, use the following command:

subsys submit [SNAPSHOT_ID]


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.