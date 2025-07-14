# HassBeam Connect Backend

A Home Assistant integration for managing and sending IR codes with [HassBeam](https://github.com/BasilBerg/hassbeam) devices.

This integration is designed to work with the [HassBeam Connect Cards](https://github.com/BasilBerg/hassbeam_connect_cards) frontend components for a complete IR remote control solution.

## Features

- **Save IR codes** - Store captured IR codes with device and action names
- **Retrieve codes** - Get recently saved IR codes from database
- **Send IR codes** - Transmit stored IR codes via HassBeam devices
- **Delete codes** - Remove unwanted IR codes from database
- **Multiple protocols** - Supports NEC, Samsung, Sony, RC5, Pronto, and more

## Services

- `get_recent_codes` - Retrieve IR codes from database
- `save_ir_code` - Save new IR codes
- `send_ir_code` - Send stored IR codes to devices
- `delete_ir_code` - Remove IR codes by ID

## Installation

### HACS Installation (recommended)

It is recommended to install this integration with [HACS](https://www.hacs.xyz/docs/use/):

#### Add this repository to HACS

- Open HACS in Home Assistant
- Open the menu in the top-right corner
- Click 'Custom Repositories'
- Enter the URL of this repository `https://github.com/BasilBerg/hassbeam_connect_backend`
- Select type: `Integration` and add the repository

#### Install the Integration

- Open HACS in Home Assistant
- Search for HassBeam
- Click on `HassBeam Connect Backend` and install the integration
- Go to Devices and Services and add the `HassBEam Connect Backend` Integration


### Manual Installation

- Copy the `hassbeam_connect_backend` folder to your `custom_components` directory
- Restart Home Assistant
- Add the integration via Settings → Integrations
- Go to Devices and Services and add the `HassBEam Connect Backend` Integration

## Install Lovelace Frontend

For the complete setup, also install the [HassBeam Connect Cards](https://github.com/BasilBerg/hassbeam_connect_cards) for the frontend UI.


## Links

- [HassBeam](https://github.com/BasilBerg/hassbeam)
- [HassBeam Connect Cards](https://github.com/BasilBerg/hassbeam_connect_cards)
- [Issues](https://github.com/BasilBerg/hassbeam_connect_backend/issues)