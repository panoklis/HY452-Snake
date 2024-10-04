# HY452-Snake


## Overview

**HY452-Snake** is a proof-of-concept snake game featuring a cloud-based scoring system. Players can register and log in to track their high scores, change backgrounds, and customize music settings. The game allows users to control the snake with keyboard commands while their scores are managed in a DynamoDB Table. This project demonstrates the use of cloud services, such as AWS, to create a simple game with a cloud-based scoring system.

## Dependencies

To run this application, you will need the following Python packages:

- `pygame`
- `requests`
- `pillow`
- `pyyaml`

You can install these dependencies using pip:

```bash
pip install pygame requests pillow pyyaml  
```

## Controls

- **Arrow keys**: Move the snake (Up, Down, Left, Right)
- **AWSD**: Move the snake (Up, Down, Left, Right)
- **Space**: Speed up the Snake
- **UP/DOWN**: Move up/down in the menu
- **Enter**: Select an option
- **BACKSPACE**: Go back to the main menu
- **M**: Mute/Unmute the music

## How to run

To run the application, simply execute the following command:

```bash
cd src
python main.py
```

## Credits

Developed by Panos Alexiou and Efthymios Papageorgiou for the HY452 course.