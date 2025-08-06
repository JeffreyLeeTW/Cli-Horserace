#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poker Horse Racing Game CLI Version
Single file implementation with multi-language support
English/Chinese bilingual version with English as default
"""

import os
import sys
import time
import random
from enum import Enum
from typing import List, Dict, Optional, Tuple

# =============================================================================
# Constants
# =============================================================================

VERSION = "1.0.1"
AUTHOR = "AI Assistant"

# =============================================================================
# Language System
# =============================================================================

class Language:
    """Language configuration and text management"""
    
    TEXTS = {
        'en': {
            # Game title and basic
            'game_title': 'Poker Horse Racing Game',
            'welcome': 'Welcome to Poker Horse Racing Game!',
            'initializing': 'Initializing...',
            'goodbye': 'Thanks for playing! Goodbye!',
            
            # Horse names
            'spades_horse': 'Spades Horse',
            'hearts_horse': 'Hearts Horse',
            'diamonds_horse': 'Diamonds Horse',
            'clubs_horse': 'Clubs Horse',
            
            # Menu options
            'main_menu_title': 'Main Menu',
            'start_new_game': '1. Start New Game',
            'view_rules': '2. View Game Rules',
            'view_stats': '3. View Statistics',
            'quit_game': '4. Quit Game',
            'choose_option': 'Please choose (1-4): ',
            
            # Betting phase
            'betting_phase': 'Betting Phase',
            'your_balance': 'Your Balance: ',
            'current_bets': 'Current Bets:',
            'choose_horse': 'Choose a horse to support:',
            'spades_option': '1. ♠ Spades Horse',
            'hearts_option': '2. ♥ Hearts Horse',
            'diamonds_option': '3. ♦ Diamonds Horse',
            'clubs_option': '4. ♣ Clubs Horse',
            'finish_betting': '5. Finish Betting',
            'return_menu': '0. Return to Main Menu',
            'choose_bet_option': 'Please choose (0-5): ',
            'enter_bet_amount': 'Enter bet amount: $',
            'total_bet': 'Total Bet: ',
            'remaining_balance': 'Remaining Balance: ',
            
            # Racing phase
            'race_start': 'Race Start',
            'press_enter_start': 'Press Enter to start drawing cards...',
            'track_status': 'Track Status',
            'position': 'Position: ',
            'current_card': 'Current Card: ',
            'remaining_cards': 'Remaining Cards: ',
            'cards_suffix': ' cards',
            'winner_announcement': 'Winner: ',
            'press_enter_results': 'Press Enter to view results...',
            
            # Settlement phase
            'race_results': 'Race Results',
            'winner': 'Winner: ',
            'your_bet_results': 'Your Betting Results:',
            'win_result': ' → 🎉 Win! Earned $',
            'lose_result': ' → ❌ Lost',
            'total_profit_loss': 'Total Profit/Loss: ',
            'current_balance': 'Current Balance: ',
            'press_enter_continue': 'Press Enter to continue...',
            
            # Game rules
            'game_rules_title': 'Game Rules',
            'rule_1': '1. Four suits (♠♥♦♣) each represent a horse',
            'rule_2': '2. Each horse starts from the starting point, goal is to reach the finish line (10 steps)',
            'rule_3': '3. Each time a card is drawn, the corresponding suit horse moves forward one step',
            'rule_4': '4. The first horse to reach the finish line wins',
            'rule_5': '5. Betting on the winning horse gets 3x payout',
            'rule_6': '6. You can bet on multiple horses simultaneously',
            'press_enter_return': 'Press Enter to return...',
            
            # Statistics
            'game_stats_title': 'Game Statistics',
            'games_played': 'Games Played: ',
            'total_profit': 'Total Profit: ',
            'win_rate': 'Win Rate: ',
            'games_suffix': ' games',
            
            # Messages
            'bet_success': 'Bet successful! ',
            'bet_cancelled': 'Betting cancelled and amount refunded',
            'insufficient_balance': 'Insufficient balance, current balance: $',
            'invalid_bet_amount': 'Bet amount must be greater than 0',
            'bet_at_least_one': 'Please bet on at least one horse!',
            'insufficient_balance_game': 'Insufficient balance, cannot start game!',
            'invalid_choice': 'Invalid choice, please try again',
            'invalid_number': 'Please enter a valid number',
            'invalid_amount': 'Please enter a valid amount',
            'game_interrupted': 'Game interrupted',
            'error_occurred': 'Error occurred: ',
            'no_bets_placed': 'No bets placed yet',
            
            # Language selection
            'language_menu': 'Language Selection',
            'english_option': '1. English',
            'chinese_option': '2. 中文',
            'choose_language': 'Choose language (1-2): ',
            
            # Others
            'and': ' and ',
            'dollars': '$',
            'percent': '%'
        },
        'zh': {
            # Game title and basic
            'game_title': '撲克牌賽馬遊戲',
            'welcome': '歡迎來到撲克牌賽馬遊戲！',
            'initializing': '正在初始化...',
            'goodbye': '感謝遊玩！再見！',
            
            # Horse names
            'spades_horse': '黑桃馬',
            'hearts_horse': '紅心馬',
            'diamonds_horse': '方塊馬',
            'clubs_horse': '梅花馬',
            
            # Menu options
            'main_menu_title': '主選單',
            'start_new_game': '1. 開始新遊戲',
            'view_rules': '2. 查看遊戲說明',
            'view_stats': '3. 查看統計',
            'quit_game': '4. 退出遊戲',
            'choose_option': '請選擇 (1-4): ',
            
            # Betting phase
            'betting_phase': '下注階段',
            'your_balance': '您的餘額: ',
            'current_bets': '目前下注狀況:',
            'choose_horse': '選擇支持的馬匹:',
            'spades_option': '1. ♠ 黑桃馬',
            'hearts_option': '2. ♥ 紅心馬',
            'diamonds_option': '3. ♦ 方塊馬',
            'clubs_option': '4. ♣ 梅花馬',
            'finish_betting': '5. 完成下注',
            'return_menu': '0. 返回主菜單',
            'choose_bet_option': '請選擇 (0-5): ',
            'enter_bet_amount': '請輸入下注金額: $',
            'total_bet': '總下注: ',
            'remaining_balance': '餘額: ',
            
            # Racing phase
            'race_start': '比賽開始',
            'press_enter_start': '按 Enter 開始翻牌...',
            'track_status': '賽道狀況',
            'position': '位置: ',
            'current_card': '當前翻出: ',
            'remaining_cards': '剩餘卡牌: ',
            'cards_suffix': '張',
            'winner_announcement': '獲勝者: ',
            'press_enter_results': '按 Enter 查看結果...',
            
            # Settlement phase
            'race_results': '比賽結果',
            'winner': '獲勝者: ',
            'your_bet_results': '您的下注結果:',
            'win_result': ' → 🎉 獲勝！贏得 $',
            'lose_result': ' → ❌ 失敗',
            'total_profit_loss': '總盈虧: ',
            'current_balance': '目前餘額: ',
            'press_enter_continue': '按 Enter 繼續...',
            
            # Game rules
            'game_rules_title': '遊戲說明',
            'rule_1': '1. 四種花色(♠♥♦♣)各代表一匹馬',
            'rule_2': '2. 每匹馬從起點開始，目標是到達終點(10步)',
            'rule_3': '3. 每次翻開一張牌，對應花色的馬前進一步',
            'rule_4': '4. 最先到達終點的馬獲勝',
            'rule_5': '5. 下注獲勝的馬可獲得3倍賠率',
            'rule_6': '6. 可以對多匹馬同時下注',
            'press_enter_return': '按 Enter 返回...',
            
            # Statistics
            'game_stats_title': '遊戲統計',
            'games_played': '已進行遊戲: ',
            'total_profit': '總盈虧: ',
            'win_rate': '勝率: ',
            'games_suffix': ' 局',
            
            # Messages
            'bet_success': '下注成功！',
            'bet_cancelled': '已取消下注並退還金額',
            'insufficient_balance': '餘額不足，當前餘額: $',
            'invalid_bet_amount': '下注金額必須大於0',
            'bet_at_least_one': '請至少下注一匹馬！',
            'insufficient_balance_game': '餘額不足，無法進行遊戲！',
            'invalid_choice': '無效選擇，請重新輸入',
            'invalid_number': '請輸入有效的數字',
            'invalid_amount': '請輸入有效的金額數字',
            'game_interrupted': '遊戲被中斷',
            'error_occurred': '發生錯誤: ',
            'no_bets_placed': '尚未下注',
            
            # Language selection
            'language_menu': '語言選擇',
            'english_option': '1. English',
            'chinese_option': '2. 中文',
            'choose_language': '選擇語言 (1-2): ',
            
            # Others
            'and': '和',
            'dollars': '$',
            'percent': '%'
        }
    }
    
    def __init__(self, language: str = 'en'):
        self.current_language = language
    
    def get(self, key: str) -> str:
        """Get text in current language"""
        return self.TEXTS.get(self.current_language, {}).get(key, key)
    
    def set_language(self, language: str) -> None:
        """Set current language"""
        if language in self.TEXTS:
            self.current_language = language

# Global language instance
lang = Language('en')  # Default to English

# =============================================================================
# Enumerations
# =============================================================================

class Suit(Enum):
    """Card suit enumeration"""
    SPADES = "♠"    # Spades
    HEARTS = "♥"    # Hearts  
    DIAMONDS = "♦"  # Diamonds
    CLUBS = "♣"     # Clubs

class Rank(Enum):
    """Card rank enumeration"""
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

# =============================================================================
# Configuration Class
# =============================================================================

class GameConfig:
    """Game configuration class"""
    TRACK_LENGTH = 10
    INITIAL_BALANCE = 1000
    WINNING_ODDS = 3.0
    ANIMATION_DELAY = 1.0  # seconds
    CLEAR_SCREEN = True

# =============================================================================
# Basic Classes - Card System
# =============================================================================

class Card:
    """Playing card class"""
    __slots__ = ['suit', 'rank']
    
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        return f"{self.suit.value}{self.rank.value}"
    
    def __repr__(self) -> str:
        return f"Card({self.suit.name}, {self.rank.name})"

class Deck:
    """Deck class"""
    
    def __init__(self):
        self.cards: List[Card] = []
        self.used_cards: List[Card] = []
        self._initialize_deck()
    
    def _initialize_deck(self) -> None:
        """Create standard 52-card deck"""
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self) -> None:
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def draw_card(self) -> Optional[Card]:
        """Draw a card, return None if deck is empty"""
        if not self.cards:
            return None
        card = self.cards.pop()
        self.used_cards.append(card)
        return card
    
    def remaining_count(self) -> int:
        """Number of remaining cards"""
        return len(self.cards)
    
    def reset(self) -> None:
        """Reset the deck"""
        self.cards.extend(self.used_cards)
        self.used_cards.clear()
        self.shuffle()

# =============================================================================
# Game Logic Classes - Horses and Track
# =============================================================================

class Horse:
    """Horse class"""
    __slots__ = ['suit', 'position', 'track_length', 'name']
    
    def __init__(self, suit: Suit, track_length: int = 10):
        self.suit = suit
        self.position = 0  # Starting position
        self.track_length = track_length
        self.name = self._get_horse_name()
    
    def _get_horse_name(self) -> str:
        """Get horse name based on suit"""
        return self._get_localized_horse_name()
    
    def _get_localized_horse_name(self) -> str:
        """Get localized horse name"""
        names = {
            Suit.SPADES: lang.get('spades_horse'),
            Suit.HEARTS: lang.get('hearts_horse'), 
            Suit.DIAMONDS: lang.get('diamonds_horse'),
            Suit.CLUBS: lang.get('clubs_horse')
        }
        return names[self.suit]
    
    def move_forward(self, steps: int = 1) -> None:
        """Move forward by specified steps"""
        self.position = min(self.position + steps, self.track_length)
    
    def is_winner(self) -> bool:
        """Check if reached finish line"""
        return self.position >= self.track_length
    
    def get_progress_bar(self) -> str:
        """Return progress bar string"""
        bar = ['-'] * self.track_length
        if self.position < self.track_length:
            bar[self.position] = '🐎'
        else:
            bar[-1] = '🏆'
        return '|' + ''.join(bar) + '|'
    
    def __str__(self) -> str:
        return f"{self.suit.value} {self.name}"

class Track:
    """Track class"""
    
    def __init__(self, length: int = 10):
        self.length = length
        self.horses: Dict[Suit, Horse] = {}
        self._initialize_horses()
    
    def _initialize_horses(self) -> None:
        """Initialize four horses"""
        for suit in Suit:
            self.horses[suit] = Horse(suit, self.length)
    
    def move_horse(self, suit: Suit, steps: int = 1) -> None:
        """Move specified suit horse"""
        if suit in self.horses:
            self.horses[suit].move_forward(steps)
    
    def get_winner(self) -> Optional[Horse]:
        """Get winning horse, return None if no winner"""
        for horse in self.horses.values():
            if horse.is_winner():
                return horse
        return None
    
    def get_positions(self) -> Dict[Suit, int]:
        """Get all horse positions"""
        return {suit: horse.position for suit, horse in self.horses.items()}
    
    def display_track(self) -> str:
        """Return track display string"""
        lines = [f"=== {lang.get('track_status')} ==="]
        for suit in Suit:
            horse = self.horses[suit]
            progress_bar = horse.get_progress_bar()
            position_info = f"{lang.get('position')}{horse.position}/{self.length}"
            lines.append(f"{horse} {progress_bar} {position_info}")
        return "\n".join(lines)
    
    def reset(self) -> None:
        """Reset track"""
        for horse in self.horses.values():
            horse.position = 0

# =============================================================================
# Player System
# =============================================================================

class Player:
    """Player class"""
    
    def __init__(self, initial_balance: int = 1000):
        self.balance = initial_balance
        self.bets: Dict[Suit, int] = {}  # {suit: bet_amount}
        self.total_bet = 0
        self.game_history: List[Dict] = []  # Game history
    
    def place_bet(self, suit: Suit, amount: int) -> Tuple[bool, str]:
        """Place bet, return (success, message)"""
        if amount <= 0:
            return False, lang.get('invalid_bet_amount')
        
        if amount > self.balance:
            return False, f"{lang.get('insufficient_balance')}{self.balance}"
        
        # Accumulate bets (allow multiple bets on same horse)
        if suit in self.bets:
            self.bets[suit] += amount
        else:
            self.bets[suit] = amount
        
        self.balance -= amount
        self.total_bet += amount
        return True, f"{lang.get('bet_success')}{suit.value} ${amount}"
    
    def calculate_winnings(self, winning_suit: Suit, odds: float = 3.0) -> int:
        """Calculate winnings, return net profit/loss"""
        winnings = 0
        if winning_suit in self.bets:
            bet_amount = self.bets[winning_suit]
            winnings = int(bet_amount * odds)  # Odds multiplier
            self.balance += winnings
        
        net_profit = winnings - self.total_bet
        
        # Record game history
        self.game_history.append({
            'bets': self.bets.copy(),
            'winner': winning_suit,
            'winnings': winnings,
            'net_profit': net_profit,
            'balance_after': self.balance
        })
        
        return net_profit
    
    def clear_bets(self) -> None:
        """Clear current bets"""
        self.bets.clear()
        self.total_bet = 0
    
    def cancel_bets(self) -> None:
        """Cancel bets and refund amount"""
        self.balance += self.total_bet
        self.bets.clear()
        self.total_bet = 0
    
    def get_bet_summary(self) -> str:
        """Get betting summary"""
        if not self.bets:
            return lang.get('no_bets_placed')
        
        lines = [f"{lang.get('current_bets')}"]
        for suit, amount in self.bets.items():
            horse_name = self._get_horse_name_for_suit(suit)
            lines.append(f"{suit.value} {horse_name}: ${amount}")
        lines.append(f"{lang.get('total_bet')}${self.total_bet}")
        lines.append(f"{lang.get('remaining_balance')}${self.balance}")
        return "\n".join(lines)
    
    def _get_horse_name_for_suit(self, suit: Suit) -> str:
        """Get horse name for specific suit"""
        names = {
            Suit.SPADES: lang.get('spades_horse'),
            Suit.HEARTS: lang.get('hearts_horse'), 
            Suit.DIAMONDS: lang.get('diamonds_horse'),
            Suit.CLUBS: lang.get('clubs_horse')
        }
        return names[suit]
    
    def get_statistics(self) -> Dict:
        """Get game statistics"""
        if not self.game_history:
            return {"games_played": 0, "total_profit": 0, "win_rate": 0, "current_balance": self.balance}
        
        games_played = len(self.game_history)
        total_profit = sum(game['net_profit'] for game in self.game_history)
        wins = sum(1 for game in self.game_history if game['net_profit'] > 0)
        win_rate = wins / games_played * 100
        
        return {
            "games_played": games_played,
            "total_profit": total_profit,
            "win_rate": win_rate,
            "current_balance": self.balance
        }

# =============================================================================
# Input Validation System
# =============================================================================

class InputValidator:
    """Input validation class"""
    
    @staticmethod
    def validate_menu_choice(input_str: str, valid_range: range) -> Tuple[bool, int, str]:
        """
        Validate menu choice
        Return: (is_valid, value, error_message)
        """
        try:
            choice = int(input_str.strip())
            if choice in valid_range:
                return True, choice, ""
            else:
                return False, 0, f"Please choose {valid_range.start}-{valid_range.stop-1}"
        except ValueError:
            return False, 0, lang.get('invalid_number')
    
    @staticmethod
    def validate_bet_amount(input_str: str, max_amount: int) -> Tuple[bool, int, str]:
        """
        Validate bet amount
        Return: (is_valid, amount, error_message)
        """
        try:
            # Remove possible $ symbol
            amount_str = input_str.strip().replace('$', '')
            amount = int(amount_str)
            
            if amount <= 0:
                return False, 0, lang.get('invalid_bet_amount')
            elif amount > max_amount:
                return False, 0, f"Bet amount cannot exceed balance ${max_amount}"
            else:
                return True, amount, ""
        except ValueError:
            return False, 0, lang.get('invalid_amount')

# =============================================================================
# Display System
# =============================================================================

class GameDisplay:
    """Game display class"""
    
    @staticmethod
    def print_error(message: str) -> None:
        print(f"❌ Error: {message}")
    
    @staticmethod
    def print_success(message: str) -> None:
        print(f"✅ {message}")
    
    @staticmethod
    def print_info(message: str) -> None:
        print(f"ℹ️ {message}")
    
    @staticmethod
    def print_warning(message: str) -> None:
        print(f"⚠️ Warning: {message}")
    
    @staticmethod
    def format_currency(amount: int) -> str:
        return f"${amount:,}"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        return f"{value:.1f}%"

# =============================================================================
# Main Game Engine
# =============================================================================

class HorseRacingGame:
    """Horse racing game main class"""
    
    def __init__(self, config: GameConfig = None):
        self.config = config or GameConfig()
        self.deck = Deck()
        self.track = Track(self.config.TRACK_LENGTH)
        self.player = Player(self.config.INITIAL_BALANCE)
        self.current_card: Optional[Card] = None
        self.game_running = False
        self.display = GameDisplay()
    
    def clear_screen(self) -> None:
        """Clear screen"""
        if self.config.CLEAR_SCREEN:
            os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self) -> None:
        """Display game title"""
        print("="*50)
        print(f"🎰 {lang.get('game_title')} 🐎")
        print("="*50)
    
    def show_language_menu(self) -> None:
        """Show language selection menu"""
        self.clear_screen()
        print("="*50)
        print(f"🌐 {lang.get('language_menu')}")
        print("="*50)
        print(lang.get('english_option'))
        print(lang.get('chinese_option'))
        print()
        
        while True:
            choice = input(lang.get('choose_language')).strip()
            valid, choice_num, error_msg = InputValidator.validate_menu_choice(choice, range(1, 3))
            
            if valid:
                if choice_num == 1:
                    lang.set_language('en')
                elif choice_num == 2:
                    lang.set_language('zh')
                break
            else:
                print(f"❌ {error_msg}")
    
    def start_game(self) -> None:
        """Start game main loop"""
        # Show language selection first
        self.show_language_menu()
        
        self.game_running = True
        
        print(lang.get('welcome'))
        print(lang.get('initializing'))
        time.sleep(1)
        
        while self.game_running:
            try:
                self.show_main_menu()
                choice = input(lang.get('choose_option')).strip()
                
                valid, choice_num, error_msg = InputValidator.validate_menu_choice(choice, range(1, 5))
                if not valid:
                    self.display.print_error(error_msg)
                    time.sleep(1)
                    continue
                
                if choice_num == 1:
                    self.play_single_game()
                elif choice_num == 2:
                    self.show_rules()
                elif choice_num == 3:
                    self.show_statistics()
                elif choice_num == 4:
                    self.quit_game()
            
            except KeyboardInterrupt:
                print(f"\n{lang.get('game_interrupted')}")
                self.quit_game()
            except Exception as e:
                self.display.print_error(f"{lang.get('error_occurred')}{e}")
                input(lang.get('press_enter_continue'))
    
    def show_main_menu(self) -> None:
        """Display main menu"""
        self.clear_screen()
        self.display_header()
        print(f"{lang.get('your_balance')}{self.display.format_currency(self.player.balance)}")
        print()
        print(lang.get('start_new_game'))
        print(lang.get('view_rules'))
        print(lang.get('view_stats'))
        print(lang.get('quit_game'))
        print()
    
    def play_single_game(self) -> None:
        """Play single game"""
        # Check balance
        if self.player.balance <= 0:
            self.display.print_error(lang.get('insufficient_balance_game'))
            input(lang.get('press_enter_continue'))
            return
        
        # Initialize game
        self.deck.reset()
        self.track.reset()
        self.player.clear_bets()
        
        # Game phases
        if self.betting_phase():
            self.racing_phase()
            self.settlement_phase()
    
    def betting_phase(self) -> bool:
        """Betting phase, return whether betting was successful"""
        while True:
            self.clear_screen()
            self.display_header()
            print(f"=== {lang.get('betting_phase')} ===")
            print(f"{lang.get('your_balance')}{self.display.format_currency(self.player.balance)}")
            print()
            
            # Display current betting status
            if self.player.bets:
                print(self.player.get_bet_summary())
                print()
            
            print(f"{lang.get('choose_horse')}")
            print(lang.get('spades_option'))
            print(lang.get('hearts_option'))
            print(lang.get('diamonds_option'))
            print(lang.get('clubs_option'))
            print(lang.get('finish_betting'))
            print(lang.get('return_menu'))
            print()
            
            choice = input(lang.get('choose_bet_option')).strip()
            
            valid, choice_num, error_msg = InputValidator.validate_menu_choice(choice, range(0, 6))
            if not valid:
                self.display.print_error(error_msg)
                time.sleep(1)
                continue
            
            if choice_num == 0:
                # Refund bet amount
                if self.player.bets:
                    self.player.cancel_bets()
                    self.display.print_info(lang.get('bet_cancelled'))
                    time.sleep(1)
                return False
            elif choice_num == 5:
                if self.player.bets:
                    return True
                else:
                    self.display.print_error(lang.get('bet_at_least_one'))
                    time.sleep(1)
            elif choice_num in [1, 2, 3, 4]:
                suit_map = {
                    1: Suit.SPADES,
                    2: Suit.HEARTS,
                    3: Suit.DIAMONDS,
                    4: Suit.CLUBS
                }
                selected_suit = suit_map[choice_num]
                
                amount_str = input(lang.get('enter_bet_amount')).strip()
                valid, amount, error_msg = InputValidator.validate_bet_amount(amount_str, self.player.balance)
                
                if valid:
                    success, message = self.player.place_bet(selected_suit, amount)
                    if success:
                        self.display.print_success(message)
                    else:
                        self.display.print_error(message)
                else:
                    self.display.print_error(error_msg)
                
                time.sleep(1)
    
    def racing_phase(self) -> None:
        """Racing phase"""
        self.clear_screen()
        print(f"=== {lang.get('race_start')} ===")
        print(lang.get('press_enter_start'))
        input()
        
        while True:
            # Draw card
            self.current_card = self.deck.draw_card()
            if not self.current_card:
                print("Deck is empty, game ended")
                break
            
            # Move corresponding horse
            self.track.move_horse(self.current_card.suit)
            
            # Display current status
            self.clear_screen()
            print(self.track.display_track())
            print()
            print(f"{lang.get('current_card')}{self.current_card}")
            print(f"{lang.get('remaining_cards')}{self.deck.remaining_count()}{lang.get('cards_suffix')}")
            
            # Check winning condition
            winner = self.track.get_winner()
            if winner:
                print(f"\n🏆 {lang.get('winner_announcement')}{winner.name}!")
                break
            
            # Animation delay
            time.sleep(self.config.ANIMATION_DELAY)
        
        input(f"\n{lang.get('press_enter_results')}")
    
    def settlement_phase(self) -> None:
        """Settlement phase"""
        winner = self.track.get_winner()
        if not winner:
            print("Game ended abnormally")
            return
        
        self.clear_screen()
        print(f"=== {lang.get('race_results')} ===")
        print(f"🏆 {lang.get('winner')}{winner}")
        print()
        
        # Calculate profit/loss
        net_profit = self.player.calculate_winnings(winner.suit, self.config.WINNING_ODDS)
        
        print(f"{lang.get('your_bet_results')}")
        for suit, amount in self.player.bets.items():
            horse_name = self.player._get_horse_name_for_suit(suit)
            if suit == winner.suit:
                winnings = int(amount * self.config.WINNING_ODDS)
                print(f"{suit.value} {horse_name}: ${amount}{lang.get('win_result')}{winnings}")
            else:
                print(f"{suit.value} {horse_name}: ${amount}{lang.get('lose_result')}")
        
        print(f"\n{lang.get('total_profit_loss')}{'+' if net_profit >= 0 else ''}${net_profit}")
        print(f"{lang.get('current_balance')}{self.display.format_currency(self.player.balance)}")
        
        input(f"\n{lang.get('press_enter_continue')}")
    
    def show_rules(self) -> None:
        """Display game rules"""
        self.clear_screen()
        print(f"=== {lang.get('game_rules_title')} ===")
        print(lang.get('rule_1'))
        print(lang.get('rule_2'))
        print(lang.get('rule_3'))
        print(lang.get('rule_4'))
        print(lang.get('rule_5'))
        print(lang.get('rule_6'))
        print()
        input(lang.get('press_enter_return'))
    
    def show_statistics(self) -> None:
        """Display statistics"""
        self.clear_screen()
        stats = self.player.get_statistics()
        print(f"=== {lang.get('game_stats_title')} ===")
        print(f"{lang.get('games_played')}{stats['games_played']}{lang.get('games_suffix')}")
        print(f"{lang.get('total_profit')}${stats['total_profit']}")
        print(f"{lang.get('win_rate')}{self.display.format_percentage(stats['win_rate'])}")
        print(f"{lang.get('current_balance')}{self.display.format_currency(stats['current_balance'])}")
        print()
        input(lang.get('press_enter_return'))
    
    def quit_game(self) -> None:
        """Quit game"""
        print(lang.get('goodbye'))
        self.game_running = False

# =============================================================================
# Main Program Entry Point
# =============================================================================

def main():
    """Main program entry point"""
    try:
        # Set encoding
        if sys.platform.startswith('win'):
            os.system('chcp 65001')
        
        config = GameConfig()
        game = HorseRacingGame(config)
        game.start_game()
        
    except Exception as e:
        print(f"Program startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()