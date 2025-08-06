#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
撲克牌賽馬遊戲演示腳本
自動演示完整遊戲流程
"""

import sys
import os
from unittest.mock import patch
from io import StringIO

# 導入遊戲模組
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from horse_racing_poker import HorseRacingGame, GameConfig, Suit, Rank, Card

def demo_complete_game():
    """演示完整遊戲流程"""
    print("=== 撲克牌賽馬遊戲演示 ===\n")
    
    # 創建遊戲配置
    config = GameConfig()
    config.ANIMATION_DELAY = 0.5  # 加快演示速度
    config.CLEAR_SCREEN = False   # 演示時不清屏
    
    # 創建遊戲實例
    game = HorseRacingGame(config)
    
    print("1. 遊戲初始化完成")
    print(f"   - 初始餘額: ${game.player.balance}")
    print(f"   - 賽道長度: {game.track.length}")
    print(f"   - 牌組數量: {game.deck.remaining_count()}")
    print()
    
    print("2. 模擬下注階段")
    # 模擬玩家下注
    game.player.place_bet(Suit.HEARTS, 100)
    game.player.place_bet(Suit.SPADES, 50)
    
    print(game.player.get_bet_summary())
    print()
    
    print("3. 開始賽馬階段")
    print("   初始賽道狀況:")
    print(game.track.display_track())
    print()
    
    # 模擬賽馬過程
    card_count = 0
    while not game.track.get_winner() and card_count < 50:  # 防止無限循環
        card = game.deck.draw_card()
        if not card:
            break
            
        game.track.move_horse(card.suit)
        card_count += 1
        
        print(f"   翻出卡牌: {card}")
        print(f"   {card.suit.value} 馬前進一步")
        
        # 每5張牌顯示一次賽道狀況
        if card_count % 5 == 0:
            print("   當前賽道狀況:")
            print(game.track.display_track())
            print()
    
    print("4. 比賽結果")
    winner = game.track.get_winner()
    if winner:
        print(f"   🏆 獲勝者: {winner}")
        print("   最終賽道狀況:")
        print(game.track.display_track())
        print()
        
        print("5. 結算階段")
        initial_balance = game.player.balance
        net_profit = game.player.calculate_winnings(winner.suit, config.WINNING_ODDS)
        
        print("   下注結果:")
        for suit, amount in game.player.bets.items():
            horse_name = game.track.horses[suit].name
            if suit == winner.suit:
                winnings = int(amount * config.WINNING_ODDS)
                print(f"   {suit.value} {horse_name}: ${amount} → 🎉 獲勝！贏得 ${winnings}")
            else:
                print(f"   {suit.value} {horse_name}: ${amount} → ❌ 失敗")
        
        print(f"\n   總盈虧: {'+' if net_profit >= 0 else ''}${net_profit}")
        print(f"   餘額變化: ${initial_balance} → ${game.player.balance}")
        
        print("\n6. 遊戲統計")
        stats = game.player.get_statistics()
        print(f"   已進行遊戲: {stats['games_played']} 局")
        print(f"   總盈虧: ${stats['total_profit']}")
        print(f"   勝率: {stats['win_rate']:.1f}%")
        print(f"   當前餘額: ${stats['current_balance']}")
    else:
        print("   比賽異常結束（可能是牌用完了）")
    
    print("\n=== 演示完成 ===")

def test_error_handling():
    """測試錯誤處理機制"""
    print("\n=== 錯誤處理測試 ===\n")
    
    config = GameConfig()
    config.CLEAR_SCREEN = False
    game = HorseRacingGame(config)
    
    print("1. 測試餘額不足下注")
    game.player.balance = 50
    success, message = game.player.place_bet(Suit.HEARTS, 100)
    print(f"   結果: {message}")
    
    print("\n2. 測試無效下注金額")
    success, message = game.player.place_bet(Suit.HEARTS, -10)
    print(f"   結果: {message}")
    
    print("\n3. 測試空牌組")
    # 清空牌組
    game.deck.cards.clear()
    card = game.deck.draw_card()
    print(f"   從空牌組抽牌結果: {card}")
    
    print("\n=== 錯誤處理測試完成 ===")

def performance_test():
    """性能測試"""
    print("\n=== 性能測試 ===\n")
    
    import time
    
    # 測試遊戲初始化時間
    start_time = time.time()
    config = GameConfig()
    config.CLEAR_SCREEN = False
    game = HorseRacingGame(config)
    init_time = time.time() - start_time
    print(f"1. 遊戲初始化時間: {init_time:.4f}秒")
    
    # 測試大量下注操作
    start_time = time.time()
    for i in range(1000):
        if game.player.balance > 10:
            game.player.place_bet(Suit.HEARTS, 10)
            game.player.clear_bets()
    bet_time = time.time() - start_time
    print(f"2. 1000次下注操作時間: {bet_time:.4f}秒")
    
    # 測試大量卡牌操作
    start_time = time.time()
    for i in range(100):
        game.deck.reset()
        for j in range(52):
            game.deck.draw_card()
    card_time = time.time() - start_time
    print(f"3. 100次完整抽牌時間: {card_time:.4f}秒")
    
    print("\n=== 性能測試完成 ===")

def main():
    """主函數"""
    print("撲克牌賽馬遊戲 - 完整演示與測試")
    print("="*50)
    
    # 演示完整遊戲
    demo_complete_game()
    
    # 測試錯誤處理
    test_error_handling()
    
    # 性能測試
    performance_test()
    
    print("\n所有測試完成！遊戲已準備好供用戶使用。")

if __name__ == "__main__":
    main()