# Torrent Vault

Torrent Vault is a script to help you keep your uploads safe, and well organized.

## Features

- Gets uploads from an API
- Checks if upload has been archived, and uploads if not
- Makes sure the torrent has a label in your client

### Currently Supported

- Torrent clients: rtorrent
- Backup methods: rclone
- Tracker software: UNIT3D

### Planned Support

- Torrent clients: qBittorrent
- Backup methods: Nothing planned
- Tracker software: Gazelle

## Requirements

- Python 3.12.0+
- Required Python packages (listed in `requirements.txt`)
- rclone

## Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:lewler/torrent-vault.git
    cd torrent-vault
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create your own config file, and update it as needed:
    ```sh
    cp config.example.yaml config.yaml
    nano config.yaml
    ```

## Configuration

Edit the `config.yaml` file to set up your preferences and API keys. The file has comments, and it's hopefully easy enough to understand what everything does.

## Upgrading

Upgrading should be fairly simple, but if you're jumping versions it might get messy. In that case, do a fresh install and copy your settings over. To upgrade do the following:

1. Update the codebase
    ```sh
    git pull
    ````

2. Make sure requirements are up-to-date
    ```sh
     pip install -r requirements.txt --upgrade
    ```

## Usage

### Command Line Interface

Run the script using the command line interface:

```sh
python torrent-vault
```

Note that if your on Linux, you should be able to run the script in this way:
```sh
chmod +x torrent-vault
./torrent-vault
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
