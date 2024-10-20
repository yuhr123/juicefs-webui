# JuiceFS WebUI

[简体中文](README_ZH.md)

This project is developed based on Flask + YAML, allowing users to manage the JuiceFS file system in a local browser and perform formatting operations in the browser.

For an already formatted JuiceFS file system, the metadata engine remains unchanged, the access address of the object storage remains unchanged, and the AK and SK remain unchanged. Therefore, we can save this information in a local YAML configuration file, add file system records in the web interface, and manage them uniformly.

⚠️ Note that this is a hobbyist project and does not guarantee stability and security. Please assess the potential risks yourself.

## Usage

```sh
# Clone the project
git clone https://github.com/yuhr123/juicefs-webui.git

# Install dependencies
cd juicefs-webui
pipenv --python 3
pipenv install

# Download JuiceFS Client
curl -sSL https://d.juicefs.com/install | sh -s .

# Start WebUI
pipenv shell
python app.py
```

## Roadmaps

- [x] Check if the configuration file exists and create it automatically
- [x] Read and display the configuration
- [x] Add, delete, and modify the configuration file
- [x] Hide SK by default, click to display
- [x] Identify and display the current operating system
- [x] Call the juicefs client in the current directory and display the version number
- [x] Display the status information of the file system
- [x] Format the file system (currently only supports s3)
- [ ] Validate the file system
- [ ] Automatically download the client suitable for the current system
- [ ] One-click copy mount command
- [ ] Form validation
- [ ] Logic for interacting with the client when editing the configuration
- [ ] Optimize UI

