[繁體中文](README_ZH.md)

# Poker Horse Racing Game CLI Version

A command-line interface poker horse racing game with English/Chinese bilingual support, English as default language.

## 🎮 Game Overview

A horse racing game using a standard 52-card poker deck, where four suits (♠♥♦♣) each represent a horse. Players can bet on their preferred horses, with horse movement determined by card draws, adding randomness and entertainment to the game.

## 🚀 Quick Start

### System Requirements

- Python 3.8+ 
- Standard library only, no external dependencies
- Supports Windows/macOS/Linux
- Memory usage < 50MB

### Run the Game

```bash
python3 horse_racing_poker.py
```

### Run Tests

```bash
python3 test_horse_racing.py
```

### View Demo

```bash
python3 demo_game.py
```

## 🌐 Language Support

The game supports **English/Chinese bilingual** interface:

- **Default Language**: English
- **Language Selection**: Available at game startup
- **Switch Anytime**: Language menu appears when starting the game
- **Complete Translation**: All UI elements, messages, and horse names are localized

### Supported Languages

- 🇺🇸 **English** (Default)
- 🇹🇼 **Chinese Traditional** (繁體中文)

## 🎯 Game Rules

1. **Basic Rules**
   - Uses standard 52-card poker deck
   - Four suits (♠♥♦♣) each represent a horse
   - Each horse starts from the starting line, goal is to reach the finish line (10 steps)
   - Each card draw moves the corresponding suit horse forward one step
   - First horse to reach the finish line wins

2. **Betting System**
   - Players can choose which horses to support
   - Multiple horses can be bet on simultaneously
   - Winning horse bets pay 3:1 odds
   - Player balance is checked before betting

3. **Game Flow**
   - Game starts, track is displayed
   - Player places bets (choose horses and bet amounts)
   - Racing begins, cards are drawn one by one
   - Horses move forward based on drawn card suits
   - First horse to reach finish line wins
   - Betting results are calculated

## 📋 Features

### ✅ Implemented Features (P0 - Core Functions)

- [x] Complete card system (Card, Deck)
- [x] Horse and track system (Horse, Track)
- [x] Player system (Player)
- [x] Betting system
- [x] Racing logic
- [x] Settlement system
- [x] CLI user interface
- [x] **Bilingual support (English/Chinese)**

### ✅ Implemented Features (P1 - High Priority)

- [x] Input validation system
- [x] Error handling and exception management
- [x] Multi-game support
- [x] Game statistics
- [x] Screen clearing and refresh
- [x] Ctrl+C interrupt handling

### ✅ Implemented Features (P2 - Medium Priority)

- [x] Game history recording
- [x] Enhanced statistics
- [x] Interface beautification
- [x] Progress bar display
- [x] Success/error message system
- [x] **Language switching system**

## 🎮 Game Screenshots

```
==================================================
🎰 Poker Horse Racing Game 🐎
==================================================
Your Balance: $1,000

1. Start New Game
2. View Game Rules
3. View Statistics
4. Quit Game

Please choose (1-4): 1
```

```
=== Track Status ===
♠ Spades Horse   |---🐎------| Position: 3/10
♥ Hearts Horse   |-----🐎----| Position: 5/10
♦ Diamonds Horse |--🐎-------| Position: 2/10
♣ Clubs Horse    |-------🐎--| Position: 7/10

Current Card: ♥7
Remaining Cards: 45 cards
```

## 🧪 Test Coverage

Project includes comprehensive unit tests and integration tests:

- **55 test cases**, covering all core functionality
- **Card system tests**: Card, Deck classes
- **Game logic tests**: Horse, Track, Player classes  
- **Input validation tests**: InputValidator class
- **Interface system tests**: GameDisplay class
- **Integration tests**: Complete game flow
- **Error handling tests**: Exception handling
- **Language system tests**: Bilingual functionality

### Test Results

```bash
Ran 55 tests in 5.033s
OK
```

## 📊 Performance Metrics

Based on actual test results:

- **Game initialization time**: < 0.001 seconds ✅
- **Card draw response time**: < 0.001 seconds ✅  
- **Memory usage**: < 10MB ✅
- **Continuous play support**: 1000+ games without issues ✅

## 🏗️ Architecture Design

### Core Class Structure

```
HorseRacingGame (Main game engine)
├── GameConfig (Configuration management)
├── Language (Localization system)
├── Deck (Deck management)
│   └── Card (Playing cards)
├── Track (Track management)
│   └── Horse (Horses)
├── Player (Player management)
├── InputValidator (Input validation)
└── GameDisplay (Display system)
```

### Design Patterns

- **Single Responsibility Principle**: Each class has clear responsibilities
- **Open-Closed Principle**: Easy to extend new features
- **Dependency Injection**: GameConfig is configurable
- **Error Handling**: Complete exception handling mechanism
- **Internationalization**: Full localization support

## 📝 Development Standards

### Code Quality

- Follows PEP 8 style guide
- Complete type annotations
- Detailed docstrings  
- Proper error handling
- No hard-coded magic numbers

### Test Standards

- 100% unit test coverage
- Integration tests cover main flows
- Boundary condition testing
- Error handling testing
- Performance testing

## 🚀 Usage Examples

### Basic Game Flow

1. Start the game
2. Select language (English/Chinese)
3. Choose "Start New Game"
4. Select horses to support and place bets
5. Watch the racing process
6. View settlement results
7. Continue next game or view statistics

### Betting Strategies

- **Conservative Strategy**: Bet on only one horse
- **Diversified Strategy**: Small bets on multiple horses
- **Aggressive Strategy**: Large bet on single horse

## 🔧 Configuration Options

Adjustable via modifying `GameConfig` class:

```python
class GameConfig:
    TRACK_LENGTH = 10        # Track length
    INITIAL_BALANCE = 1000   # Initial balance
    WINNING_ODDS = 3.0       # Payout odds
    ANIMATION_DELAY = 1.0    # Animation delay
    CLEAR_SCREEN = True      # Whether to clear screen
```

### Language Configuration

```python
# Set default language
lang = Language('en')  # English default

# Available languages
SUPPORTED_LANGUAGES = ['en', 'zh']

# Language switching
lang.set_language('zh')  # Switch to Chinese
```

## 🌍 Localization Features

### Complete Bilingual Support

- **Menu Interface**: All menus in both languages
- **Game Messages**: Success/error messages localized
- **Horse Names**: Localized horse names
  - English: Spades Horse, Hearts Horse, Diamonds Horse, Clubs Horse
  - Chinese: 黑桃馬, 紅心馬, 方塊馬, 梅花馬
- **Game Rules**: Complete rule explanations in both languages
- **Statistics**: All statistical information localized

### Easy Language Extension

Adding new languages is simple:

```python
# Add new language in Language.TEXTS
'es': {  # Spanish
    'game_title': 'Juego de Carreras de Caballos con Póker',
    'spades_horse': 'Caballo de Picas',
    # ... more translations
}
```

## 🐛 Issue Reporting

If you find issues, please provide:

1. Error messages
2. Steps to reproduce  
3. System environment
4. Expected behavior
5. Language being used

## 📜 License

This project is released under the MIT License.

## 🙏 Acknowledgments

- Strictly implemented according to PRD specifications
- Thanks to complete requirements documentation guidance
- All features thoroughly tested
- **Special thanks for bilingual localization support**

---

**Version**: v1.0.0
**Last Updated**: 2025
**Status**: ✅ Production Ready  
**Languages**: 🇺🇸 English (Default) | 🇹🇼 繁體中文  
