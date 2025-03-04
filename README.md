# EPSIRoguelike (EPSImester)

## Table of Contents
- [Project Overview](#project-overview)
- [Game Mechanics](#game-mechanics)
- [Game Controls](#game-controls)
- [Code Structure](#code-structure)
- [Class Documentation](#class-documentation)
- [Installation](#installation)
- [Dependencies](#dependencies)

## Project Overview
EPSIRoguelike (EPSImester) is a roguelike game developed with Pygame where players navigate through a semester of events while managing various resources. The game features:

- Resource management (energy, morale, money, project progress)
- Time-based progression system (hours, days, weeks, months)
- Event system with choices and consequences
- Inventory and item management
- Shop system for purchasing items
- Random event generation

## Game Mechanics

### Core Game Loop
1. Players start at the main menu and can begin a new game
2. The player goes through a tutorial explaining the game
3. The game progresses through time periods (Early-Morning, Morning, Lunch, Afternoon, Evening)
4. Each time period may trigger events that require player choices
5. Players manage resources (energy, morale, money) while trying to complete their project
6. The game ends when the player completes their project or fails to do so within the time limit

### Resource Management
- **Energy**: Required for activities, depletes with certain actions
- **Morale**: Represents player's mental state, affects gameplay
- **Money**: Currency for purchasing items in the shop
- **Project Progress**: Main objective to complete

### Time System
- 5 time periods per day (Early-Morning, Morning, Lunch, Afternoon, Evening)
- 7 days per week (Monday to Sunday)
- 4 weeks per month
- Special events occur on specific days (e.g., shop opens on Wednesday at lunch)

### Event System
Events trigger during gameplay with multiple phases:
1. Event description is presented
2. Player makes choices that affect resources
3. Effects are applied to the player's stats

### Inventory System
- 4 equipment slots for non-consumable items
- Bag can hold up to 32 consumable items
- Items can be dragged and dropped between the bag and equipment slots
- Consumable items can be right-clicked to use them

### Shop System
- Opens on Wednesday at lunchtime
- Allows players to purchase items that help manage resources
- New items are available each week

## Game Controls
- **Mouse**: Click to make choices, interact with UI elements
- **I key**: Open inventory
- **ESC key**: Open pause menu

## Code Structure

### Main Components
- **Game (main.py)**: Main game loop and state management
- **Menu (menu.py)**: Main menu interface
- **InGame (ingame.py)**: Core gameplay logic
- **PauseMenu (PauseMenu.py)**: Pause screen
- **Inventory (Inventory.py)**: Inventory management
- **Event (event_gestion.py)**: Event handling system
- **Item (item_gestion.py)**: Item management
- **Shop (shop.py)**: Shop interface
- **Generator (generator.py)**: Random content generation

### File organisation
  ```
  /EPSIRoguelike
  │
  ├── main.py              # Entry point and game loop
  ├── player.py            # Player class and stats
  ├── menu.py              # Main menu interface
  ├── ingame.py            # Core gameplay and event handling
  ├── PauseMenu.py         # Pause menu functionality
  ├── Inventory.py         # Inventory management system
  ├── event_gestion.py     # Event system implementation
  ├── item_gestion.py      # Item system implementation
  ├── jsonLoader.py        # JSON data loading utilities
  ├── generator.py         # Random content generation
  ├── shop.py              # Shop system
  ├── tuto.py              # Tutorial system
  │
  └── Data/                # Game assets and data
      ├── Events/          # Event definitions
      ├── Items/           # Item definitions
      ├── Sounds/          # Sound effects and music
      └── Sprites/         # Game graphics
  ```
## Class Documentation

### Player
Manages character stats and inventory.

**Attributes:**
- `energy`: Current energy points (max 10)
- `moral`: Current morale points (max 10)
- `money`: Currency for purchases
- `project`: Project completion progress (max 10)
- `inventory_slot_1-4`: Equipment slots
- `bag`: List of items in player's bag (max 32)
- `effects`: not yet implemented

**Methods:**
- `update_player(event)`: Updates player stats based on event effects
- `statChange(money, moral, energy, project)`: Changes player stats
- `negative_stats`: vérifies if a stat is negative and returns it to 0 also prints the said value.

### Game
The main game controller that manages game states and components.

**States:**
- `menu`: Main menu screen
- `tutorial`: Tutorial screen
- `in_game`: Main gameplay
- `pause_menu`: Pause screen
- `inventory`: Inventory screen
- `shop`: Shop screen

**Methods:**
- `handle_events()`: Processes user input
- `draw()`: Renders the current game state
- `run()`: Main game loop

### InGame
Handles the main gameplay, events, and time progression.

**States:**
- `EVENT_PROGRESS`: Triggering and processing events
- `PHASE_PROGRESS`: Moving through event phases
- `CHOICE_MAKING`: Player making choices

**Methods:**
- `handle_time()`: Manages game time progression
- `advance_event()`: Moves to next event
- `draw_current_phase()`: Renders event phases and choices
- `select_choice(choice_number)`: Processes player choices

### Event
Represents game events with multiple phases and choices.

**Methods:**
- `load_events(file_path)`: Loads events from JSON file
- `phases_data()`: Returns event phase information
- `phases_choices_data(phase_number)`: Returns choices for a specific phase

### Item
Represents game items with effects and properties.

**Methods:**
- `load_items(file_path)`: Loads items from JSON file
- `get_shop_items()`: returns the list of shop items

### Month/Week/Day
Generate random game content for each time period.

**Methods:**
- `generate_month()`: Creates a month's worth of events
- `generate_week()`: Generates weekly events
- `generate_day()`: Creates daily event schedule
- `return_month()`: returns the month in a list of values that is of a variable size (e.g : ['4D', 'B2', 'A6', ...])

### Shop
Manages the shop interface where players can purchase items.

**Attributes:**
- `screen`: Pygame surface for rendering
- `player`: Reference to the player object
- `ingame`: Reference to the InGame object for shop items
- `sound_played`: Track if the shop sound has been played

**Methods:**
- `load_assets()`: Loads the shop graphics
- `handle_events(event)`: Processes user input in the shop
- `draw()`: Renders the shop interface
- `draw_items()`: Renders the items available for sale
- `add_item_to_bag(item)`: Purchases an item and adds it to player's inventory
- `play_shop_sound()`: Plays the shop entrance sound

### Tutorial
Manages the tutorial screens that guide new players through the game mechanics.

**Attributes:**
- `screen`: Pygame surface for rendering
- `pages`: List of tutorial text pages to display
- `images`: Optional images to show with tutorial pages
- `current_page`: Tracks the current tutorial page
- `running`: Whether the tutorial is still active

**Methods:**
- `draw()`: Renders the current tutorial page
- `handle_events(event)`: Processes user input during the tutorial
- `draw_button()`: Renders the navigation button

## Installation
1. Ensure Python and Pygame are installed
2. Clone the repository
3. Navigate to the game directory
4. install dependencies from `requirements.txt`
5. Run `python main.py`

Or

```shell
git clone https://github.com/blndl/EPSIRoguelike
cd EPSIRoguelike
pip install -r requirements.txt
python main.py
```

## Dependencies
- Python 3.x
- Pygame

The game expects a Data directory with:
- Events/events.json: Event definitions
- Items/items.json: Item definitions
- Sprites/: Game graphics
- Sounds/: Game audio
- pixeboy.ttf: Game font