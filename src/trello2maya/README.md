# trello2maya
Manage your [Trello](https://trello.com/) boards inside Maya

To install:
1. Copy files to Maya scripts folder
2. Execute trello2maya.util.setup_shelf() in script editor to install shelf
3. Open T2M Config and click Authorize button to generate user token
4. Copy token to T2M Config field and click Save

### Modules
#### [trelloapi](trelloapi)
Provides communication methods with Trello REST API

#### [config](config.py)
Provides logic and user interface for managing Trello2Maya configuration and authorization

#### [main](main.py)
Main application logic and user interface

#### [util](util.py)
Provides shared utility functions