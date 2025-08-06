#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poker Horse Racing Game Unit Tests
Complete test suite for English/Chinese bilingual version
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Import game modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from horse_racing_poker import (
    Suit, Rank, Card, Deck, Horse, Track, Player, 
    InputValidator, GameDisplay, HorseRacingGame, GameConfig,
    Language, lang
)

class TestLanguage(unittest.TestCase):
    """Test language system functionality"""
    
    def test_language_initialization(self):
        """Test language system initialization"""
        test_lang = Language('en')
        self.assertEqual(test_lang.current_language, 'en')
        
        test_lang_zh = Language('zh')
        self.assertEqual(test_lang_zh.current_language, 'zh')
    
    def test_language_get_text(self):
        """Test getting text in different languages"""
        test_lang = Language('en')
        self.assertEqual(test_lang.get('game_title'), 'Poker Horse Racing Game')
        
        test_lang.set_language('zh')
        self.assertEqual(test_lang.get('game_title'), '撲克牌賽馬遊戲')
    
    def test_language_set_language(self):
        """Test setting language"""
        test_lang = Language('en')
        test_lang.set_language('zh')
        self.assertEqual(test_lang.current_language, 'zh')
        
        # Test invalid language (should not change)
        test_lang.set_language('invalid')
        self.assertEqual(test_lang.current_language, 'zh')
    
    def test_horse_names_localization(self):
        """Test horse names in different languages"""
        # Test English
        lang.set_language('en')
        self.assertEqual(lang.get('spades_horse'), 'Spades Horse')
        self.assertEqual(lang.get('hearts_horse'), 'Hearts Horse')
        
        # Test Chinese
        lang.set_language('zh')
        self.assertEqual(lang.get('spades_horse'), '黑桃馬')
        self.assertEqual(lang.get('hearts_horse'), '紅心馬')

class TestCard(unittest.TestCase):
    """Test card-related functionality"""
    
    def test_card_creation(self):
        """Test card creation"""
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(str(card), "♥A")
        self.assertEqual(repr(card), "Card(HEARTS, ACE)")
    
    def test_all_suits_and_ranks(self):
        """Test all suit and rank combinations"""
        for suit in Suit:
            for rank in Rank:
                card = Card(suit, rank)
                self.assertIsInstance(card.suit, Suit)
                self.assertIsInstance(card.rank, Rank)
                # Ensure string representation is correct
                self.assertEqual(str(card), f"{suit.value}{rank.value}")

class TestDeck(unittest.TestCase):
    """Test deck functionality"""
    
    def test_deck_initialization(self):
        """Test deck initialization"""
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(deck.used_cards), 0)
        
        # Ensure all cards are present
        suits_count = {suit: 0 for suit in Suit}
        ranks_count = {rank: 0 for rank in Rank}
        
        for card in deck.cards:
            suits_count[card.suit] += 1
            ranks_count[card.rank] += 1
        
        # Each suit should have 13 cards
        for count in suits_count.values():
            self.assertEqual(count, 13)
        
        # Each rank should have 4 cards
        for count in ranks_count.values():
            self.assertEqual(count, 4)
    
    def test_deck_shuffle(self):
        """Test deck shuffling"""
        deck = Deck()
        original_order = [str(card) for card in deck.cards]
        deck.shuffle()
        shuffled_order = [str(card) for card in deck.cards]
        
        # After shuffling, order should be different (very high probability)
        # But card count remains the same
        self.assertEqual(len(deck.cards), 52)
        self.assertNotEqual(original_order, shuffled_order)
    
    def test_deck_draw_card(self):
        """Test drawing cards"""
        deck = Deck()
        initial_count = len(deck.cards)
        
        card = deck.draw_card()
        self.assertIsNotNone(card)
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), initial_count - 1)
        self.assertEqual(len(deck.used_cards), 1)
        self.assertIn(card, deck.used_cards)
    
    def test_deck_draw_all_cards(self):
        """Test drawing all cards"""
        deck = Deck()
        drawn_cards = []
        
        # Draw all 52 cards
        for _ in range(52):
            card = deck.draw_card()
            self.assertIsNotNone(card)
            drawn_cards.append(card)
        
        # Drawing another card should return None
        self.assertIsNone(deck.draw_card())
        self.assertEqual(len(deck.cards), 0)
        self.assertEqual(len(deck.used_cards), 52)
    
    def test_deck_reset(self):
        """Test deck reset"""
        deck = Deck()
        
        # Draw some cards
        for _ in range(10):
            deck.draw_card()
        
        self.assertEqual(len(deck.cards), 42)
        self.assertEqual(len(deck.used_cards), 10)
        
        # Reset
        deck.reset()
        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(deck.used_cards), 0)
    
    def test_remaining_count(self):
        """Test remaining card count"""
        deck = Deck()
        self.assertEqual(deck.remaining_count(), 52)
        
        deck.draw_card()
        self.assertEqual(deck.remaining_count(), 51)

class TestHorse(unittest.TestCase):
    """Test horse functionality"""
    
    def setUp(self):
        """Set up test environment"""
        lang.set_language('en')  # Use English for testing
    
    def test_horse_creation(self):
        """Test horse creation"""
        horse = Horse(Suit.SPADES, track_length=10)
        self.assertEqual(horse.suit, Suit.SPADES)
        self.assertEqual(horse.position, 0)
        self.assertEqual(horse.track_length, 10)
        self.assertEqual(horse.name, "Spades Horse")
        self.assertFalse(horse.is_winner())
    
    def test_horse_names_english(self):
        """Test all horse names in English"""
        lang.set_language('en')
        expected_names = {
            Suit.SPADES: "Spades Horse",
            Suit.HEARTS: "Hearts Horse",
            Suit.DIAMONDS: "Diamonds Horse",
            Suit.CLUBS: "Clubs Horse"
        }
        
        for suit, expected_name in expected_names.items():
            horse = Horse(suit)
            self.assertEqual(horse._get_localized_horse_name(), expected_name)
    
    def test_horse_names_chinese(self):
        """Test all horse names in Chinese"""
        lang.set_language('zh')
        expected_names = {
            Suit.SPADES: "黑桃馬",
            Suit.HEARTS: "紅心馬",
            Suit.DIAMONDS: "方塊馬",
            Suit.CLUBS: "梅花馬"
        }
        
        for suit, expected_name in expected_names.items():
            horse = Horse(suit)
            self.assertEqual(horse._get_localized_horse_name(), expected_name)
    
    def test_horse_movement(self):
        """Test horse movement"""
        horse = Horse(Suit.HEARTS, track_length=10)
        
        # Move forward 3 steps
        horse.move_forward(3)
        self.assertEqual(horse.position, 3)
        self.assertFalse(horse.is_winner())
        
        # Move forward 5 more steps
        horse.move_forward(5)
        self.assertEqual(horse.position, 8)
        self.assertFalse(horse.is_winner())
        
        # Move to finish line
        horse.move_forward(2)
        self.assertEqual(horse.position, 10)
        self.assertTrue(horse.is_winner())
        
        # Moving beyond finish line shouldn't continue
        horse.move_forward(5)
        self.assertEqual(horse.position, 10)
    
    def test_progress_bar_generation(self):
        """Test progress bar generation"""
        horse = Horse(Suit.CLUBS, track_length=5)
        
        # Starting position
        horse.position = 0
        bar = horse.get_progress_bar()
        self.assertEqual(bar, "|🐎----|")
        
        # Middle position
        horse.position = 2
        bar = horse.get_progress_bar()
        self.assertEqual(bar, "|--🐎--|")
        
        # At finish line
        horse.position = 5
        bar = horse.get_progress_bar()
        self.assertEqual(bar, "|----🏆|")
    
    def test_horse_string_representation(self):
        """Test horse string representation"""
        lang.set_language('en')
        horse = Horse(Suit.DIAMONDS)
        expected = "♦ Diamonds Horse"
        self.assertEqual(str(horse), expected)

class TestTrack(unittest.TestCase):
    """Test track functionality"""
    
    def setUp(self):
        """Set up test environment"""
        lang.set_language('en')
    
    def test_track_initialization(self):
        """Test track initialization"""
        track = Track(length=10)
        self.assertEqual(track.length, 10)
        self.assertEqual(len(track.horses), 4)
        
        # Ensure all suit horses exist
        for suit in Suit:
            self.assertIn(suit, track.horses)
            self.assertEqual(track.horses[suit].position, 0)
    
    def test_move_horse(self):
        """Test moving horses"""
        track = Track(length=10)
        
        # Move hearts horse
        track.move_horse(Suit.HEARTS, 3)
        self.assertEqual(track.horses[Suit.HEARTS].position, 3)
        
        # Other horses should not have moved
        for suit in [Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS]:
            self.assertEqual(track.horses[suit].position, 0)
    
    def test_get_winner(self):
        """Test winner detection"""
        track = Track(length=5)
        
        # Initially no winner
        self.assertIsNone(track.get_winner())
        
        # Move spades horse to finish line
        track.move_horse(Suit.SPADES, 5)
        winner = track.get_winner()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.suit, Suit.SPADES)
    
    def test_get_positions(self):
        """Test getting positions"""
        track = Track(length=10)
        
        # Move some horses
        track.move_horse(Suit.HEARTS, 3)
        track.move_horse(Suit.SPADES, 1)
        
        positions = track.get_positions()
        expected = {
            Suit.SPADES: 1,
            Suit.HEARTS: 3,
            Suit.DIAMONDS: 0,
            Suit.CLUBS: 0
        }
        self.assertEqual(positions, expected)
    
    def test_track_reset(self):
        """Test track reset"""
        track = Track(length=10)
        
        # Move all horses
        for suit in Suit:
            track.move_horse(suit, 5)
        
        # Reset
        track.reset()
        
        # All horses should be back at starting position
        for suit in Suit:
            self.assertEqual(track.horses[suit].position, 0)
    
    def test_display_track(self):
        """Test track display"""
        lang.set_language('en')
        track = Track(length=5)
        display = track.display_track()
        
        self.assertIn("Track Status", display)
        self.assertIn("Spades Horse", display)
        self.assertIn("Hearts Horse", display)
        self.assertIn("Diamonds Horse", display)
        self.assertIn("Clubs Horse", display)

class TestPlayer(unittest.TestCase):
    """Test player functionality"""
    
    def setUp(self):
        """Set up test environment"""
        lang.set_language('en')
    
    def test_player_initialization(self):
        """Test player initialization"""
        player = Player(initial_balance=1000)
        self.assertEqual(player.balance, 1000)
        self.assertEqual(player.bets, {})
        self.assertEqual(player.total_bet, 0)
        self.assertEqual(len(player.game_history), 0)
    
    def test_place_bet_success(self):
        """Test successful betting"""
        player = Player(1000)
        success, message = player.place_bet(Suit.HEARTS, 100)
        
        self.assertTrue(success)
        self.assertIn("Bet successful", message)
        self.assertEqual(player.balance, 900)
        self.assertEqual(player.bets[Suit.HEARTS], 100)
        self.assertEqual(player.total_bet, 100)
    
    def test_place_bet_multiple_same_horse(self):
        """Test multiple bets on same horse"""
        player = Player(1000)
        
        # First bet
        player.place_bet(Suit.HEARTS, 100)
        # Second bet
        player.place_bet(Suit.HEARTS, 50)
        
        self.assertEqual(player.bets[Suit.HEARTS], 150)
        self.assertEqual(player.total_bet, 150)
        self.assertEqual(player.balance, 850)
    
    def test_place_bet_insufficient_balance(self):
        """Test insufficient balance"""
        player = Player(50)
        success, message = player.place_bet(Suit.HEARTS, 100)
        
        self.assertFalse(success)
        self.assertIn("Insufficient balance", message)
        self.assertEqual(player.balance, 50)  # Balance unchanged
        self.assertEqual(player.bets, {})
    
    def test_place_bet_invalid_amount(self):
        """Test invalid amount"""
        player = Player(1000)
        success, message = player.place_bet(Suit.HEARTS, 0)
        
        self.assertFalse(success)
        self.assertIn("must be greater than 0", message)
        
        success, message = player.place_bet(Suit.HEARTS, -50)
        self.assertFalse(success)
        self.assertIn("must be greater than 0", message)
    
    def test_calculate_winnings_win(self):
        """Test calculating winnings for win"""
        player = Player(1000)
        player.place_bet(Suit.HEARTS, 100)
        player.place_bet(Suit.SPADES, 50)
        
        # Hearts horse wins, odds 3.0
        net_profit = player.calculate_winnings(Suit.HEARTS, 3.0)
        
        # Win 300, total bet 150, net profit 150
        self.assertEqual(net_profit, 150)
        # 1000-150+300 = 1150
        self.assertEqual(player.balance, 1150)
        self.assertEqual(len(player.game_history), 1)
    
    def test_calculate_winnings_lose(self):
        """Test calculating winnings for loss"""
        player = Player(1000)
        player.place_bet(Suit.HEARTS, 100)
        player.place_bet(Suit.SPADES, 50)
        
        # Diamonds horse wins (no bet placed)
        net_profit = player.calculate_winnings(Suit.DIAMONDS, 3.0)
        
        # No winnings, net loss 150
        self.assertEqual(net_profit, -150)
        # Balance remains 850 (already deducted bet amount)
        self.assertEqual(player.balance, 850)
    
    def test_clear_bets(self):
        """Test clearing bets"""
        player = Player(1000)
        player.place_bet(Suit.HEARTS, 100)
        
        player.clear_bets()
        self.assertEqual(player.bets, {})
        self.assertEqual(player.total_bet, 0)
    
    def test_cancel_bets(self):
        """Test canceling bets and refunding amount"""
        player = Player(1000)
        player.place_bet(Suit.HEARTS, 100)
        player.place_bet(Suit.SPADES, 50)
        
        # Balance should be 850, total bet 150
        self.assertEqual(player.balance, 850)
        self.assertEqual(player.total_bet, 150)
        
        # Cancel bets
        player.cancel_bets()
        
        # Balance should return to 1000, bets cleared
        self.assertEqual(player.balance, 1000)
        self.assertEqual(player.bets, {})
        self.assertEqual(player.total_bet, 0)
    
    def test_get_bet_summary(self):
        """Test getting bet summary"""
        player = Player(1000)
        
        # No bets
        summary = player.get_bet_summary()
        self.assertEqual(summary, "No bets placed yet")
        
        # With bets
        player.place_bet(Suit.HEARTS, 100)
        player.place_bet(Suit.SPADES, 50)
        summary = player.get_bet_summary()
        
        self.assertIn("Current Bets", summary)
        self.assertIn("Hearts Horse", summary)
        self.assertIn("Spades Horse", summary)
        self.assertIn("Total Bet: $150", summary)
    
    def test_get_statistics_no_games(self):
        """Test statistics with no game history"""
        player = Player(1000)
        stats = player.get_statistics()
        
        expected = {"games_played": 0, "total_profit": 0, "win_rate": 0, "current_balance": 1000}
        self.assertEqual(stats, expected)
    
    def test_get_statistics_with_games(self):
        """Test statistics with game history"""
        player = Player(1000)
        
        # Simulate a few games
        player.place_bet(Suit.HEARTS, 100)
        player.calculate_winnings(Suit.HEARTS, 3.0)  # Win 200
        player.clear_bets()
        
        player.place_bet(Suit.SPADES, 50)
        player.calculate_winnings(Suit.CLUBS, 3.0)  # Lose 50
        player.clear_bets()
        
        stats = player.get_statistics()
        self.assertEqual(stats["games_played"], 2)
        self.assertEqual(stats["total_profit"], 150)  # 200-50
        self.assertEqual(stats["win_rate"], 50.0)  # 1 win, 1 loss

class TestInputValidator(unittest.TestCase):
    """Test input validation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        lang.set_language('en')
    
    def test_validate_menu_choice_valid(self):
        """Test valid menu choice"""
        valid, choice, msg = InputValidator.validate_menu_choice("2", range(1, 5))
        self.assertTrue(valid)
        self.assertEqual(choice, 2)
        self.assertEqual(msg, "")
    
    def test_validate_menu_choice_invalid_range(self):
        """Test invalid range"""
        valid, choice, msg = InputValidator.validate_menu_choice("5", range(1, 5))
        self.assertFalse(valid)
        self.assertEqual(choice, 0)
        self.assertIn("Please choose", msg)
    
    def test_validate_menu_choice_invalid_format(self):
        """Test invalid format"""
        valid, choice, msg = InputValidator.validate_menu_choice("abc", range(1, 5))
        self.assertFalse(valid)
        self.assertEqual(choice, 0)
        self.assertIn("valid number", msg)
    
    def test_validate_bet_amount_valid(self):
        """Test valid bet amount"""
        valid, amount, msg = InputValidator.validate_bet_amount("100", 1000)
        self.assertTrue(valid)
        self.assertEqual(amount, 100)
        self.assertEqual(msg, "")
    
    def test_validate_bet_amount_with_dollar_sign(self):
        """Test amount with $ symbol"""
        valid, amount, msg = InputValidator.validate_bet_amount("$250", 1000)
        self.assertTrue(valid)
        self.assertEqual(amount, 250)
        self.assertEqual(msg, "")
    
    def test_validate_bet_amount_zero_or_negative(self):
        """Test zero or negative amount"""
        valid, amount, msg = InputValidator.validate_bet_amount("0", 1000)
        self.assertFalse(valid)
        self.assertIn("must be greater than 0", msg)
        
        valid, amount, msg = InputValidator.validate_bet_amount("-50", 1000)
        self.assertFalse(valid)
        self.assertIn("must be greater than 0", msg)
    
    def test_validate_bet_amount_exceeds_balance(self):
        """Test amount exceeding balance"""
        valid, amount, msg = InputValidator.validate_bet_amount("1500", 1000)
        self.assertFalse(valid)
        self.assertIn("cannot exceed balance", msg)
    
    def test_validate_bet_amount_invalid_format(self):
        """Test invalid format"""
        valid, amount, msg = InputValidator.validate_bet_amount("abc", 1000)
        self.assertFalse(valid)
        self.assertIn("valid amount", msg)

class TestGameDisplay(unittest.TestCase):
    """Test display system functionality"""
    
    def test_format_currency(self):
        """Test currency formatting"""
        self.assertEqual(GameDisplay.format_currency(1000), "$1,000")
        self.assertEqual(GameDisplay.format_currency(123456), "$123,456")
        self.assertEqual(GameDisplay.format_currency(0), "$0")
    
    def test_format_percentage(self):
        """Test percentage formatting"""
        self.assertEqual(GameDisplay.format_percentage(66.666), "66.7%")
        self.assertEqual(GameDisplay.format_percentage(0), "0.0%")
        self.assertEqual(GameDisplay.format_percentage(100), "100.0%")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_methods(self, mock_stdout):
        """Test various print methods"""
        GameDisplay.print_error("Error message")
        GameDisplay.print_success("Success message")
        GameDisplay.print_info("Info message")
        GameDisplay.print_warning("Warning message")
        
        output = mock_stdout.getvalue()
        self.assertIn("❌ Error: Error message", output)
        self.assertIn("✅ Success message", output)
        self.assertIn("ℹ️ Info message", output)
        self.assertIn("⚠️ Warning: Warning message", output)

class TestGameConfig(unittest.TestCase):
    """Test game configuration"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = GameConfig()
        self.assertEqual(config.TRACK_LENGTH, 10)
        self.assertEqual(config.INITIAL_BALANCE, 1000)
        self.assertEqual(config.WINNING_ODDS, 3.0)
        self.assertEqual(config.ANIMATION_DELAY, 1.0)
        self.assertTrue(config.CLEAR_SCREEN)

class TestHorseRacingGameIntegration(unittest.TestCase):
    """Test game integration functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = GameConfig()
        self.config.ANIMATION_DELAY = 0  # Disable animation delay for testing
        self.config.CLEAR_SCREEN = False  # Don't clear screen during testing
        self.game = HorseRacingGame(self.config)
        lang.set_language('en')  # Use English for testing
    
    def test_game_initialization(self):
        """Test game initialization"""
        self.assertIsInstance(self.game.deck, Deck)
        self.assertIsInstance(self.game.track, Track)
        self.assertIsInstance(self.game.player, Player)
        self.assertEqual(self.game.player.balance, 1000)
        self.assertFalse(self.game.game_running)
    
    @patch('builtins.input', side_effect=['1', '4'])  # Choose English, then quit
    def test_start_game_quit_immediately(self, mock_input):
        """Test quitting game immediately"""
        with patch('sys.stdout', new_callable=StringIO):
            self.game.start_game()
        self.assertFalse(self.game.game_running)
    
    def test_play_single_game_insufficient_balance(self):
        """Test game behavior with insufficient balance"""
        self.game.player.balance = 0
        
        with patch('builtins.input', return_value=''):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.game.play_single_game()
            
            output = mock_stdout.getvalue()
            self.assertIn("Insufficient balance", output)
    
    @patch('builtins.input', side_effect=['2', '100', '5'])  # Choose hearts horse, bet 100, finish betting
    def test_betting_phase_success(self, mock_input):
        """Test successful betting phase"""
        with patch('sys.stdout', new_callable=StringIO):
            result = self.game.betting_phase()
        
        self.assertTrue(result)
        self.assertEqual(self.game.player.bets[Suit.HEARTS], 100)
        self.assertEqual(self.game.player.balance, 900)
    
    @patch('builtins.input', side_effect=['0'])  # Return to main menu
    def test_betting_phase_cancel(self, mock_input):
        """Test canceling betting"""
        with patch('sys.stdout', new_callable=StringIO):
            result = self.game.betting_phase()
        
        self.assertFalse(result)
        self.assertEqual(self.game.player.bets, {})
    
    @patch('builtins.input', side_effect=['2', '150', '0'])  # Bet hearts horse 150, then return to main menu
    def test_betting_phase_cancel_with_bets(self, mock_input):
        """Test canceling with bets and refunding amount"""
        initial_balance = self.game.player.balance
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.game.betting_phase()
        
        # Should return False (cancelled)
        self.assertFalse(result)
        # Bets should be cleared
        self.assertEqual(self.game.player.bets, {})
        # Balance should return to initial value
        self.assertEqual(self.game.player.balance, initial_balance)
        # Output should contain cancellation message
        output = mock_stdout.getvalue()
        self.assertIn("cancelled and amount refunded", output)

class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def setUp(self):
        """Set up test environment"""
        lang.set_language('en')
    
    def test_keyboard_interrupt_handling(self):
        """Test Ctrl+C interrupt handling"""
        config = GameConfig()
        config.CLEAR_SCREEN = False
        game = HorseRacingGame(config)
        
        with patch('builtins.input', side_effect=['1', KeyboardInterrupt]):  # Choose English, then interrupt
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                game.start_game()
            
            output = mock_stdout.getvalue()
            self.assertIn("Game interrupted", output)
            self.assertFalse(game.game_running)

def run_tests():
    """Run all tests"""
    # Create test suite
    test_classes = [
        TestLanguage, TestCard, TestDeck, TestHorse, TestTrack, TestPlayer,
        TestInputValidator, TestGameDisplay, TestGameConfig,
        TestHorseRacingGameIntegration, TestErrorHandling
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return test results
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)