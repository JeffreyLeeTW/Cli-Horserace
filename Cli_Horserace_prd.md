# 撲克牌賽馬遊戲 CLI 版本 - 產品需求文檔 (PRD)

## 0. 文檔目的與AI實現指南

### 0.1 文檔目的
本PRD專為AI代碼生成優化，提供明確的技術規格、接口定義和實現細節，確保AI能夠準確理解需求並生成高質量代碼。

### 0.2 實現優先級
- **P0 (必須實現)**: 核心遊戲邏輯、基本CLI界面
- **P1 (高優先級)**: 下注系統、資金管理、錯誤處理
- **P2 (中優先級)**: 界面美化、統計功能
- **P3 (低優先級)**: 動畫效果、擴展功能

### 0.3 技術約束
- 使用Python 3.8+
- 僅使用標準庫（無外部依賴）
- 支持Windows/macOS/Linux
- 內存使用 < 50MB
- 單文件實現（可選模塊化）

## 1. 產品概述

### 1.1 產品名稱
撲克牌賽馬遊戲 (Poker Horse Racing CLI)

### 1.2 產品描述
一個基於命令行界面的撲克牌賽馬遊戲，玩家可以觀看四匹馬(四種花色)進行比賽，並進行下注。遊戲使用標準52張撲克牌，通過翻牌決定馬匹前進，增加遊戲的隨機性和娛樂性。

### 1.3 目標用戶
- 撲克愛好者
- 命令行遊戲愛好者
- 想要體驗簡單博弈遊戲的用戶

### 1.4 核心價值
- 簡單易懂的遊戲規則
- 快節奏的遊戲體驗
- 命令行環境下的娛樂選擇

## 2. 遊戲規則

### 2.1 基本規則
1. 使用標準52張撲克牌
2. 四種花色(♠♥♦♣)各代表一匹馬
3. 每匹馬從起點開始，目標是到達終點(通常10步)
4. 每次翻開一張牌，對應花色的馬前進一步
5. 最先到達終點的馬獲勝

### 2.2 遊戲流程
1. 遊戲開始，展示賽道
2. 玩家下注(選擇支持的馬匹和賭注金額)
3. 開始賽馬，逐張翻牌
4. 馬匹根據翻出的牌的花色前進
5. 第一匹到達終點的馬獲勝
6. 結算賭注

## 3. 功能需求

### 3.1 核心功能

#### 3.1.1 遊戲初始化
- 洗牌功能
- 賽道初始化(10格長度)
- 四匹馬初始位置設定
- 玩家資金初始化

#### 3.1.2 下注系統
- 玩家可選擇支持的馬匹(♠♥♦♣)
- 設定下注金額(需檢查玩家餘額)
- 顯示當前下注狀況
- 支援多匹馬下注

#### 3.1.3 賽馬系統
- 逐張翻牌機制
- 根據花色移動對應馬匹
- 實時更新賽道顯示
- 檢測獲勝條件

#### 3.1.4 結算系統
- 計算獲勝結果
- 賭注結算(賠率 1:3，即下注100贏300)
- 更新玩家資金
- 顯示遊戲結果

### 3.2 輔助功能

#### 3.2.1 顯示系統
- 賽道視覺化顯示
- 馬匹位置實時更新
- 當前翻出的牌顯示
- 玩家資金和下注狀況

#### 3.2.2 用戶交互
- 命令行選單系統
- 輸入驗證
- 錯誤處理和提示
- 遊戲說明功能

#### 3.2.3 遊戲管理
- 多局遊戲支持
- 遊戲統計(勝率、總盈虧等)
- 存檔/讀檔功能(可選)
- 退出遊戲確認

## 4. 技術需求

### 4.1 開發語言
推薦使用 Python 開發，原因：
- 豐富的內建數據結構
- 良好的字符串處理能力
- 簡潔的語法適合快速開發
- 跨平台支持

### 4.2 詳細類別設計與接口規範

#### 4.2.1 卡牌模組 (Card Module)
```python
from enum import Enum
from typing import List, Optional
import random

class Suit(Enum):
    SPADES = "♠"    # 黑桃
    HEARTS = "♥"    # 紅心  
    DIAMONDS = "♦"  # 方塊
    CLUBS = "♣"     # 梅花

class Rank(Enum):
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

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        return f"{self.suit.value}{self.rank.value}"
    
    def __repr__(self) -> str:
        return f"Card({self.suit.name}, {self.rank.name})"

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.used_cards: List[Card] = []
        self._initialize_deck()
    
    def _initialize_deck(self) -> None:
        """創建標準52張撲克牌"""
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self) -> None:
        """洗牌"""
        random.shuffle(self.cards)
    
    def draw_card(self) -> Optional[Card]:
        """抽一張牌，返回None如果牌組為空"""
        if not self.cards:
            return None
        card = self.cards.pop()
        self.used_cards.append(card)
        return card
    
    def remaining_count(self) -> int:
        """剩餘卡牌數量"""
        return len(self.cards)
    
    def reset(self) -> None:
        """重置牌組"""
        self.cards.extend(self.used_cards)
        self.used_cards.clear()
        self.shuffle()
```

#### 4.2.2 馬匹模組 (Horse Module)
```python
class Horse:
    def __init__(self, suit: Suit, track_length: int = 10):
        self.suit = suit
        self.position = 0  # 起始位置
        self.track_length = track_length
        self.name = self._get_horse_name()
    
    def _get_horse_name(self) -> str:
        """根據花色返回馬名"""
        names = {
            Suit.SPADES: "黑桃馬",
            Suit.HEARTS: "紅心馬", 
            Suit.DIAMONDS: "方塊馬",
            Suit.CLUBS: "梅花馬"
        }
        return names[self.suit]
    
    def move_forward(self, steps: int = 1) -> None:
        """前進指定步數"""
        self.position = min(self.position + steps, self.track_length)
    
    def is_winner(self) -> bool:
        """檢查是否到達終點"""
        return self.position >= self.track_length
    
    def get_progress_bar(self) -> str:
        """返回進度條字符串"""
        bar = ['-'] * self.track_length
        if self.position < self.track_length:
            bar[self.position] = '🐎'
        else:
            bar[-1] = '🏆'
        return '|' + ''.join(bar) + '|'
    
    def __str__(self) -> str:
        return f"{self.suit.value} {self.name}"
```

#### 4.2.3 賽道模組 (Track Module)
```python
from typing import Dict, List, Optional

class Track:
    def __init__(self, length: int = 10):
        self.length = length
        self.horses: Dict[Suit, Horse] = {}
        self._initialize_horses()
    
    def _initialize_horses(self) -> None:
        """初始化四匹馬"""
        for suit in Suit:
            self.horses[suit] = Horse(suit, self.length)
    
    def move_horse(self, suit: Suit, steps: int = 1) -> None:
        """移動指定花色的馬"""
        if suit in self.horses:
            self.horses[suit].move_forward(steps)
    
    def get_winner(self) -> Optional[Horse]:
        """獲取獲勝的馬，如果沒有則返回None"""
        for horse in self.horses.values():
            if horse.is_winner():
                return horse
        return None
    
    def get_positions(self) -> Dict[Suit, int]:
        """獲取所有馬的位置"""
        return {suit: horse.position for suit, horse in self.horses.items()}
    
    def display_track(self) -> str:
        """返回賽道顯示字符串"""
        lines = ["=== 賽道狀況 ==="]
        for suit in Suit:
            horse = self.horses[suit]
            progress_bar = horse.get_progress_bar()
            position_info = f"位置: {horse.position}/{self.length}"
            lines.append(f"{horse} {progress_bar} {position_info}")
        return "\n".join(lines)
    
    def reset(self) -> None:
        """重置賽道"""
        for horse in self.horses.values():
            horse.position = 0
```

#### 4.2.4 玩家模組 (Player Module)
```python
from typing import Dict, Tuple

class Player:
    def __init__(self, initial_balance: int = 1000):
        self.balance = initial_balance
        self.bets: Dict[Suit, int] = {}  # {花色: 下注金額}
        self.total_bet = 0
        self.game_history: List[Dict] = []  # 遊戲歷史記錄
    
    def place_bet(self, suit: Suit, amount: int) -> Tuple[bool, str]:
        """下注，返回(是否成功, 消息)"""
        if amount <= 0:
            return False, "下注金額必須大於0"
        
        if amount > self.balance:
            return False, f"餘額不足，當前餘額: ${self.balance}"
        
        # 累加下注（允許對同一匹馬多次下注）
        if suit in self.bets:
            self.bets[suit] += amount
        else:
            self.bets[suit] = amount
        
        self.balance -= amount
        self.total_bet += amount
        return True, f"下注成功！{suit.value} {amount}元"
    
    def calculate_winnings(self, winning_suit: Suit, odds: float = 3.0) -> int:
        """計算獲勝金額，返回淨盈虧"""
        winnings = 0
        if winning_suit in self.bets:
            bet_amount = self.bets[winning_suit]
            winnings = int(bet_amount * odds)  # 賠率倍數
            self.balance += winnings
        
        net_profit = winnings - self.total_bet
        
        # 記錄遊戲歷史
        self.game_history.append({
            'bets': self.bets.copy(),
            'winner': winning_suit,
            'winnings': winnings,
            'net_profit': net_profit,
            'balance_after': self.balance
        })
        
        return net_profit
    
    def clear_bets(self) -> None:
        """清空當前下注"""
        self.bets.clear()
        self.total_bet = 0
    
    def get_bet_summary(self) -> str:
        """獲取下注摘要"""
        if not self.bets:
            return "尚未下注"
        
        lines = ["目前下注狀況:"]
        for suit, amount in self.bets.items():
            horse_name = Horse(suit).name
            lines.append(f"{suit.value} {horse_name}: ${amount}")
        lines.append(f"總下注: ${self.total_bet}")
        lines.append(f"餘額: ${self.balance}")
        return "\n".join(lines)
    
    def get_statistics(self) -> Dict:
        """獲取遊戲統計"""
        if not self.game_history:
            return {"games_played": 0, "total_profit": 0, "win_rate": 0}
        
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
```

#### 4.2.5 遊戲引擎 (Game Engine)
```python
import time
import os
from typing import Optional

class GameConfig:
    """遊戲配置類"""
    TRACK_LENGTH = 10
    INITIAL_BALANCE = 1000
    WINNING_ODDS = 3.0
    ANIMATION_DELAY = 1.0  # 秒
    CLEAR_SCREEN = True

class HorseRacingGame:
    def __init__(self, config: GameConfig = None):
        self.config = config or GameConfig()
        self.deck = Deck()
        self.track = Track(self.config.TRACK_LENGTH)
        self.player = Player(self.config.INITIAL_BALANCE)
        self.current_card: Optional[Card] = None
        self.game_running = False
    
    def clear_screen(self) -> None:
        """清屏"""
        if self.config.CLEAR_SCREEN:
            os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self) -> None:
        """顯示遊戲標題"""
        print("="*50)
        print("🎰 撲克牌賽馬遊戲 🐎")
        print("="*50)
    
    def start_game(self) -> None:
        """開始遊戲主循環"""
        self.game_running = True
        
        while self.game_running:
            try:
                self.show_main_menu()
                choice = input("請選擇 (1-4): ").strip()
                
                if choice == '1':
                    self.play_single_game()
                elif choice == '2':
                    self.show_rules()
                elif choice == '3':
                    self.show_statistics()
                elif choice == '4':
                    self.quit_game()
                else:
                    print("無效選擇，請重新輸入")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print("\n遊戲被中斷")
                self.quit_game()
            except Exception as e:
                print(f"發生錯誤: {e}")
                input("按 Enter 繼續...")
    
    def show_main_menu(self) -> None:
        """顯示主菜單"""
        self.clear_screen()
        self.display_header()
        print(f"玩家餘額: ${self.player.balance}")
        print()
        print("1. 開始新遊戲")
        print("2. 查看遊戲說明")
        print("3. 查看統計")
        print("4. 退出遊戲")
        print()
    
    def play_single_game(self) -> None:
        """進行單局遊戲"""
        # 檢查餘額
        if self.player.balance <= 0:
            print("餘額不足，無法進行遊戲！")
            input("按 Enter 繼續...")
            return
        
        # 初始化遊戲
        self.deck.reset()
        self.track.reset()
        self.player.clear_bets()
        
        # 遊戲階段
        if self.betting_phase():
            self.racing_phase()
            self.settlement_phase()
    
    def betting_phase(self) -> bool:
        """下注階段，返回是否成功下注"""
        while True:
            self.clear_screen()
            self.display_header()
            print("=== 下注階段 ===")
            print(f"您的餘額: ${self.player.balance}")
            print()
            
            # 顯示當前下注狀況
            if self.player.bets:
                print(self.player.get_bet_summary())
                print()
            
            print("選擇支持的馬匹:")
            print("1. ♠ 黑桃馬")
            print("2. ♥ 紅心馬")
            print("3. ♦ 方塊馬")
            print("4. ♣ 梅花馬")
            print("5. 完成下注")
            print("0. 返回主菜單")
            print()
            
            choice = input("請選擇 (0-5): ").strip()
            
            if choice == '0':
                return False
            elif choice == '5':
                if self.player.bets:
                    return True
                else:
                    print("請至少下注一匹馬！")
                    time.sleep(1)
            elif choice in ['1', '2', '3', '4']:
                suit_map = {
                    '1': Suit.SPADES,
                    '2': Suit.HEARTS,
                    '3': Suit.DIAMONDS,
                    '4': Suit.CLUBS
                }
                selected_suit = suit_map[choice]
                
                try:
                    amount_str = input("請輸入下注金額: $").strip()
                    amount = int(amount_str)
                    success, message = self.player.place_bet(selected_suit, amount)
                    print(message)
                    if not success:
                        time.sleep(2)
                except ValueError:
                    print("請輸入有效的數字")
                    time.sleep(1)
            else:
                print("無效選擇")
                time.sleep(1)
    
    def racing_phase(self) -> None:
        """賽馬階段"""
        self.clear_screen()
        print("=== 比賽開始 ===")
        print("按 Enter 開始翻牌...")
        input()
        
        while True:
            # 翻牌
            self.current_card = self.deck.draw_card()
            if not self.current_card:
                print("牌組已空，遊戲結束")
                break
            
            # 移動對應馬匹
            self.track.move_horse(self.current_card.suit)
            
            # 顯示當前狀態
            self.clear_screen()
            print(self.track.display_track())
            print()
            print(f"當前翻出: {self.current_card}")
            print(f"剩餘卡牌: {self.deck.remaining_count()}張")
            
            # 檢查獲勝條件
            winner = self.track.get_winner()
            if winner:
                print(f"\n🏆 {winner.name} 獲勝！")
                break
            
            # 延遲動畫效果
            time.sleep(self.config.ANIMATION_DELAY)
        
        input("\n按 Enter 查看結果...")
    
    def settlement_phase(self) -> None:
        """結算階段"""
        winner = self.track.get_winner()
        if not winner:
            print("遊戲異常結束")
            return
        
        self.clear_screen()
        print("=== 比賽結果 ===")
        print(f"🏆 獲勝者: {winner}")
        print()
        
        # 計算盈虧
        net_profit = self.player.calculate_winnings(winner.suit, self.config.WINNING_ODDS)
        
        print("您的下注結果:")
        for suit, amount in self.player.bets.items():
            horse_name = Horse(suit).name
            if suit == winner.suit:
                winnings = int(amount * self.config.WINNING_ODDS)
                print(f"{suit.value} {horse_name}: ${amount} → 🎉 獲勝！贏得 ${winnings}")
            else:
                print(f"{suit.value} {horse_name}: ${amount} → ❌ 失敗")
        
        print(f"\n總盈虧: {'+' if net_profit >= 0 else ''}${net_profit}")
        print(f"目前餘額: ${self.player.balance}")
        
        input("\n按 Enter 繼續...")
    
    def show_rules(self) -> None:
        """顯示遊戲規則"""
        self.clear_screen()
        print("=== 遊戲說明 ===")
        print("1. 四種花色(♠♥♦♣)各代表一匹馬")
        print("2. 每匹馬從起點開始，目標是到達終點(10步)")
        print("3. 每次翻開一張牌，對應花色的馬前進一步")
        print("4. 最先到達終點的馬獲勝")
        print("5. 下注獲勝的馬可獲得3倍賠率")
        print("6. 可以對多匹馬同時下注")
        print()
        input("按 Enter 返回...")
    
    def show_statistics(self) -> None:
        """顯示統計信息"""
        self.clear_screen()
        stats = self.player.get_statistics()
        print("=== 遊戲統計 ===")
        print(f"已進行遊戲: {stats['games_played']} 局")
        print(f"總盈虧: ${stats['total_profit']}")
        print(f"勝率: {stats['win_rate']:.1f}%")
        print(f"當前餘額: ${stats['current_balance']}")
        print()
        input("按 Enter 返回...")
    
    def quit_game(self) -> None:
        """退出遊戲"""
        print("感謝遊玩！再見！")
        self.game_running = False

# 主程序入口
def main():
    """主程序入口點"""
    config = GameConfig()
    game = HorseRacingGame(config)
    game.start_game()

if __name__ == "__main__":
    main()
```

### 4.3 數據結構與存儲格式

#### 4.3.1 遊戲狀態數據結構
```python
# 遊戲狀態數據結構
GameState = {
    "deck": {
        "remaining_cards": int,
        "used_cards": List[str],  # ["♠A", "♥7", ...]
    },
    "track": {
        "length": int,
        "positions": {  # 馬匹位置
            "♠": int,
            "♥": int, 
            "♦": int,
            "♣": int
        }
    },
    "player": {
        "balance": int,
        "bets": {"♠": int, "♥": int, "♦": int, "♣": int},
        "total_bet": int
    },
    "current_card": Optional[str],  # "♠A"
    "winner": Optional[str],  # "♠"
    "game_phase": str  # "betting", "racing", "settlement", "finished"
}
```

#### 4.3.2 配置文件格式 (config.json)
```json
{
    "game_settings": {
        "track_length": 10,
        "initial_balance": 1000,
        "winning_odds": 3.0,
        "animation_delay": 1.0,
        "clear_screen": true
    },
    "display_settings": {
        "horse_emoji": "🐎",
        "winner_emoji": "🏆",
        "track_char": "-",
        "border_char": "|",
        "languages": {
            "zh_TW": {
                "spades_name": "黑桃馬",
                "hearts_name": "紅心馬",
                "diamonds_name": "方塊馬",
                "clubs_name": "梅花馬"
            }
        }
    }
}
```

#### 4.3.3 遊戲歷史記錄格式
```python
GameHistory = {
    "timestamp": str,  # ISO format
    "game_id": str,
    "initial_balance": int,
    "bets_placed": Dict[str, int],
    "cards_drawn": List[str],
    "winner": str,
    "winnings": int,
    "net_profit": int,
    "final_balance": int,
    "game_duration": float  # seconds
}
```

## 5. 用戶界面設計與輸入輸出規範

### 5.1 輸入驗證規範

#### 5.1.1 用戶輸入驗證
```python
class InputValidator:
    @staticmethod
    def validate_menu_choice(input_str: str, valid_range: range) -> Tuple[bool, int, str]:
        """
        驗證菜單選擇
        返回: (是否有效, 數值, 錯誤消息)
        """
        try:
            choice = int(input_str.strip())
            if choice in valid_range:
                return True, choice, ""
            else:
                return False, 0, f"請選擇 {valid_range.start}-{valid_range.stop-1} 之間的數字"
        except ValueError:
            return False, 0, "請輸入有效的數字"
    
    @staticmethod
    def validate_bet_amount(input_str: str, max_amount: int) -> Tuple[bool, int, str]:
        """
        驗證下注金額
        返回: (是否有效, 金額, 錯誤消息)
        """
        try:
            # 移除可能的 $ 符號
            amount_str = input_str.strip().replace('$', '')
            amount = int(amount_str)
            
            if amount <= 0:
                return False, 0, "下注金額必須大於 0"
            elif amount > max_amount:
                return False, 0, f"下注金額不能超過餘額 ${max_amount}"
            else:
                return True, amount, ""
        except ValueError:
            return False, 0, "請輸入有效的金額數字"
```

### 5.2 界面模板與輸出格式

#### 5.2.1 主選單界面模板
```python
MAIN_MENU_TEMPLATE = '''
{'='*50}
🎰 撲克牌賽馬遊戲 🐎
{'='*50}
玩家餘額: ${balance}

1. 開始新遊戲
2. 查看遊戲說明
3. 查看統計
4. 退出遊戲

請選擇 (1-4): '''
```

#### 5.2.2 賽道顯示模板
```python
TRACK_DISPLAY_TEMPLATE = '''
=== 賽道狀況 ===
{track_lines}

當前翻出: {current_card}
剩餘卡牌: {remaining_cards}張

{additional_info}
'''

# 單匹馬的顯示格式
HORSE_LINE_TEMPLATE = "{suit} {name}: {progress_bar} 位置: {position}/{total}"

# 進度條生成函數
def generate_progress_bar(position: int, total_length: int, 
                         horse_char: str = "🐎", 
                         track_char: str = "-",
                         border_char: str = "|") -> str:
    bar = [track_char] * total_length
    if position < total_length:
        bar[position] = horse_char
    else:
        bar[-1] = "🏆"
    return f"{border_char}{''.join(bar)}{border_char}"
```

#### 5.2.3 下注界面模板
```python
BETTING_MENU_TEMPLATE = '''
=== 下注階段 ===
您的餘額: ${balance}

{current_bets}

選擇支持的馬匹:
1. ♠ 黑桃馬
2. ♥ 紅心馬
3. ♦ 方塊馬
4. ♣ 梅花馬
5. 完成下注
0. 返回主菜單

請選擇 (0-5): '''

CURRENT_BETS_TEMPLATE = '''
目前下注狀況:
{bet_lines}
總下注: ${total_bet}
剩餘餘額: ${remaining_balance}
'''
```

#### 5.2.4 結算界面模板
```python
SETTLEMENT_TEMPLATE = '''
=== 比賽結果 ===
🏆 獲勝者: {winner_suit} {winner_name}

您的下注結果:
{bet_results}

總盈虧: {profit_sign}${abs_profit}
目前餘額: ${current_balance}

按 Enter 繼續...
'''

BET_RESULT_LINE_WIN = "{suit} {name}: ${bet_amount} → 🎉 獲勝！贏得 ${winnings}"
BET_RESULT_LINE_LOSE = "{suit} {name}: ${bet_amount} → ❌ 失敗"
```

### 5.3 錯誤處理與用戶提示

#### 5.3.1 錯誤消息定義
```python
ERROR_MESSAGES = {
    "INVALID_INPUT": "輸入無效，請重新輸入",
    "INSUFFICIENT_BALANCE": "餘額不足，無法進行此操作",
    "NO_BETS_PLACED": "請至少下注一匹馬！",
    "INVALID_AMOUNT": "請輸入有效的金額數字",
    "GAME_INTERRUPTED": "遊戲被中斷",
    "DECK_EMPTY": "卡牌已用完，遊戲結束",
    "SYSTEM_ERROR": "系統錯誤，請重試"
}

SUCCESS_MESSAGES = {
    "BET_PLACED": "下注成功！{suit} {amount}元",
    "GAME_WON": "恭喜！您贏得了 ${amount}",
    "GAME_SAVED": "遊戲狀態已保存"
}

INFO_MESSAGES = {
    "GAME_START": "遊戲開始，祝您好運！",
    "DRAWING_CARD": "正在翻牌...",
    "RACE_FINISHED": "比賽結束！",
    "GOODBYE": "感謝遊玩！再見！"
}
```

#### 5.3.2 統一輸出函數
```python
class GameDisplay:
    @staticmethod
    def print_error(message: str) -> None:
        print(f"❌ 錯誤: {message}")
    
    @staticmethod
    def print_success(message: str) -> None:
        print(f"✅ {message}")
    
    @staticmethod
    def print_info(message: str) -> None:
        print(f"ℹ️ {message}")
    
    @staticmethod
    def print_warning(message: str) -> None:
        print(f"⚠️ 警告: {message}")
    
    @staticmethod
    def format_currency(amount: int) -> str:
        return f"${amount:,}"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        return f"{value:.1f}%"
```

## 6. 遊戲體驗設計

### 6.1 動畫效果
- 翻牌時短暫停頓增加懸念
- 馬匹移動時的簡單動畫效果
- 獲勝時的慶祝顯示

### 6.2 音效提示(可選)
- 翻牌音效
- 馬匹移動音效
- 獲勝音效

### 6.3 賠率設計
- 標準賠率 1:3 (下注 $100，獲勝得 $300 總計 $400)
- 可考慮根據即時賠率調整

## 7. 擴展功能

### 7.1 進階功能
- 多人遊戲模式
- 錦標賽模式
- 成就系統
- 排行榜功能

### 7.2 數據分析
- 每匹馬的歷史勝率
- 玩家投注模式分析
- 遊戲統計報告

### 7.3 自訂設定
- 賽道長度可調整
- 賠率可自訂
- 起始資金可設定

## 8. 品質標準與測試規範

### 8.1 性能要求
- 遊戲啟動時間 < 2秒
- 翻牌響應時間 < 0.5秒
- 記憶體使用 < 50MB
- 支援連續遊玩 1000+ 局不卡頓

### 8.2 穩定性要求
- 無記憶體洩漏
- 異常輸入處理完整
- 遊戲狀態保存可靠
- Ctrl+C 中斷處理正確

### 8.3 測試用例規範

#### 8.3.1 單元測試用例
```python
import unittest
from unittest.mock import patch, MagicMock

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(str(card), "♥A")
    
    def test_deck_initialization(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
        
    def test_deck_shuffle(self):
        deck = Deck()
        original_order = deck.cards.copy()
        deck.shuffle()
        # 洗牌後順序應該不同（機率極高）
        self.assertNotEqual(deck.cards, original_order)
    
    def test_deck_draw_card(self):
        deck = Deck()
        initial_count = len(deck.cards)
        card = deck.draw_card()
        self.assertIsNotNone(card)
        self.assertEqual(len(deck.cards), initial_count - 1)
        self.assertIn(card, deck.used_cards)

class TestHorse(unittest.TestCase):
    def test_horse_creation(self):
        horse = Horse(Suit.SPADES)
        self.assertEqual(horse.suit, Suit.SPADES)
        self.assertEqual(horse.position, 0)
        self.assertEqual(horse.name, "黑桃馬")
    
    def test_horse_movement(self):
        horse = Horse(Suit.HEARTS, track_length=10)
        horse.move_forward(3)
        self.assertEqual(horse.position, 3)
        self.assertFalse(horse.is_winner())
        
        horse.move_forward(7)
        self.assertEqual(horse.position, 10)  # 不應超過賽道長度
        self.assertTrue(horse.is_winner())
    
    def test_progress_bar_generation(self):
        horse = Horse(Suit.CLUBS, track_length=5)
        horse.position = 2
        bar = horse.get_progress_bar()
        expected = "|--🐎--|"  # 位置2上有馬
        self.assertEqual(bar, expected)

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player(1000)
        self.assertEqual(player.balance, 1000)
        self.assertEqual(player.bets, {})
        self.assertEqual(player.total_bet, 0)
    
    def test_place_bet_success(self):
        player = Player(1000)
        success, message = player.place_bet(Suit.HEARTS, 100)
        self.assertTrue(success)
        self.assertEqual(player.balance, 900)
        self.assertEqual(player.bets[Suit.HEARTS], 100)
        self.assertEqual(player.total_bet, 100)
    
    def test_place_bet_insufficient_balance(self):
        player = Player(50)
        success, message = player.place_bet(Suit.HEARTS, 100)
        self.assertFalse(success)
        self.assertIn("餘額不足", message)
        self.assertEqual(player.balance, 50)  # 餘額不變
    
    def test_calculate_winnings(self):
        player = Player(1000)
        player.place_bet(Suit.HEARTS, 100)
        player.place_bet(Suit.SPADES, 50)
        
        # 紅心馬獲勝
        net_profit = player.calculate_winnings(Suit.HEARTS, 3.0)
        self.assertEqual(net_profit, 150)  # 贏300，總下注150，淨利150
        self.assertEqual(player.balance, 1150)  # 1000-150+300

class TestInputValidation(unittest.TestCase):
    def test_validate_menu_choice(self):
        # 有效輸入
        valid, choice, msg = InputValidator.validate_menu_choice("2", range(1, 5))
        self.assertTrue(valid)
        self.assertEqual(choice, 2)
        
        # 無效輸入 - 超出範圍
        valid, choice, msg = InputValidator.validate_menu_choice("5", range(1, 5))
        self.assertFalse(valid)
        self.assertIn("請選擇", msg)
        
        # 無效輸入 - 非數字
        valid, choice, msg = InputValidator.validate_menu_choice("abc", range(1, 5))
        self.assertFalse(valid)
        self.assertIn("有效的數字", msg)
    
    def test_validate_bet_amount(self):
        # 有效金額
        valid, amount, msg = InputValidator.validate_bet_amount("100", 1000)
        self.assertTrue(valid)
        self.assertEqual(amount, 100)
        
        # 帶$符號的有效金額
        valid, amount, msg = InputValidator.validate_bet_amount("$250", 1000)
        self.assertTrue(valid)
        self.assertEqual(amount, 250)
        
        # 超出餘額
        valid, amount, msg = InputValidator.validate_bet_amount("1500", 1000)
        self.assertFalse(valid)
        self.assertIn("不能超過餘額", msg)
```

#### 8.3.2 整合測試用例
```python
class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        self.config = GameConfig()
        self.config.ANIMATION_DELAY = 0  # 測試時關閉動畫延遲
        self.game = HorseRacingGame(self.config)
    
    @patch('builtins.input', side_effect=['2', '100', '5'])  # 選擇紅心馬，下注100，完成下注
    @patch('random.shuffle')  # 模擬洗牌
    def test_complete_game_flow(self, mock_shuffle, mock_input):
        # 設定固定的牌組順序，讓紅心馬獲勝
        hearts_cards = [Card(Suit.HEARTS, rank) for rank in Rank]
        self.game.deck.cards = hearts_cards * 4  # 確保有足夠的紅心牌
        
        # 執行完整遊戲流程
        initial_balance = self.game.player.balance
        self.game.play_single_game()
        
        # 驗證結果
        self.assertGreater(self.game.player.balance, initial_balance)  # 應該贏錢
        self.assertEqual(len(self.game.player.game_history), 1)  # 應該有一局記錄
    
    def test_error_handling_invalid_input(self):
        # 測試各種無效輸入的處理
        test_cases = [
            ("abc", "請輸入有效的數字"),
            ("-50", "下注金額必須大於 0"),
            ("999999", "不能超過餘額")
        ]
        
        for invalid_input, expected_error in test_cases:
            success, message = self.game.player.place_bet(Suit.HEARTS, 
                                                         InputValidator.validate_bet_amount(invalid_input, 1000)[1])
            if not InputValidator.validate_bet_amount(invalid_input, 1000)[0]:
                self.assertFalse(success or True)  # 應該被驗證器攔截
```

### 8.4 驗收標準

#### 8.4.1 功能驗收標準
- [ ] 遊戲可以正常啟動並顯示主菜單
- [ ] 玩家可以成功下注並查看下注狀態
- [ ] 賽馬過程正確顯示，馬匹根據翻牌移動
- [ ] 正確檢測獲勝條件並進行結算
- [ ] 所有用戶輸入都有適當的驗證和錯誤處理
- [ ] 遊戲統計功能正常工作
- [ ] 可以進行多局遊戲而不出現錯誤

#### 8.4.2 性能驗收標準
- [ ] 遊戲啟動時間 < 2秒
- [ ] 翻牌動畫流暢，無明顯延遲
- [ ] 記憶體使用穩定，長時間運行無洩漏
- [ ] 支援 Ctrl+C 正確退出

#### 8.4.3 用戶體驗驗收標準
- [ ] 界面佈局清晰，信息易於理解
- [ ] 錯誤提示明確，幫助用戶糾正輸入
- [ ] 遊戲節奏合理，不會過快或過慢
- [ ] 支援中文顯示，無亂碼問題

## 9. 開發里程碑

### 9.1 第一階段 (MVP)
- 基本遊戲邏輯
- 簡單CLI界面
- 單局遊戲功能

### 9.2 第二階段
- 下注系統
- 資金管理
- 基本統計功能

### 9.3 第三階段
- 界面美化
- 動畫效果
- 擴展功能

### 9.4 第四階段
- 性能優化
- 錯誤處理完善
- 用戶體驗改善

## 10. 實現指導與最佳實踐

### 10.1 代碼結構建議

#### 10.1.1 文件組織結構
```
horse_racing_poker_cli/
├── main.py                 # 主程序入口
├── game/
│   ├── __init__.py
│   ├── card.py            # 卡牌相關類
│   ├── horse.py           # 馬匹相關類
│   ├── track.py           # 賽道相關類
│   ├── player.py          # 玩家相關類
│   └── engine.py          # 遊戲引擎
├── ui/
│   ├── __init__.py
│   ├── display.py         # 顯示相關函數
│   ├── input_handler.py   # 輸入處理
│   └── templates.py       # 界面模板
├── utils/
│   ├── __init__.py
│   ├── validator.py       # 輸入驗證
│   └── config.py          # 配置管理
├── tests/
│   ├── test_card.py
│   ├── test_horse.py
│   ├── test_player.py
│   └── test_integration.py
├── config.json            # 配置文件
└── README.md
```

#### 10.1.2 單文件實現版本
如果選擇單文件實現，建議按以下順序組織代碼：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
撲克牌賽馬遊戲 CLI 版本
單文件實現版本
"""

# 1. 導入標準庫
import os
import sys
import time
import random
from enum import Enum
from typing import List, Dict, Optional, Tuple

# 2. 常量定義
# 3. 枚舉定義 (Suit, Rank)
# 4. 配置類 (GameConfig)
# 5. 基礎類 (Card, Deck)
# 6. 遊戲邏輯類 (Horse, Track, Player)
# 7. 輸入驗證類 (InputValidator)
# 8. 顯示類 (GameDisplay)
# 9. 主遊戲類 (HorseRacingGame)
# 10. 主函數 (main)

if __name__ == "__main__":
    main()
```

### 10.2 錯誤處理最佳實踐

#### 10.2.1 異常處理策略
```python
class GameException(Exception):
    """遊戲基礎異常類"""
    pass

class InvalidInputException(GameException):
    """無效輸入異常"""
    pass

class InsufficientBalanceException(GameException):
    """餘額不足異常"""
    pass

class GameStateException(GameException):
    """遊戲狀態異常"""
    pass

# 使用示例
def safe_input(prompt: str, validator_func, max_retries: int = 3) -> any:
    """安全輸入函數，包含重試機制"""
    for attempt in range(max_retries):
        try:
            user_input = input(prompt).strip()
            return validator_func(user_input)
        except InvalidInputException as e:
            print(f"❌ {e}")
            if attempt < max_retries - 1:
                print(f"還有 {max_retries - attempt - 1} 次機會")
            else:
                print("重試次數用完，返回主菜單")
                raise
```

### 10.3 性能優化建議

#### 10.3.1 內存管理
```python
# 使用 __slots__ 減少內存使用
class Card:
    __slots__ = ['suit', 'rank']
    
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

# 對象池模式重用卡牌對象
class CardPool:
    _pool: Dict[Tuple[Suit, Rank], Card] = {}
    
    @classmethod
    def get_card(cls, suit: Suit, rank: Rank) -> Card:
        key = (suit, rank)
        if key not in cls._pool:
            cls._pool[key] = Card(suit, rank)
        return cls._pool[key]
```

#### 10.3.2 顯示優化
```python
# 緩存進度條避免重複計算
class TrackDisplayCache:
    _cache: Dict[Tuple[int, int], str] = {}
    
    @classmethod
    def get_progress_bar(cls, position: int, total_length: int) -> str:
        key = (position, total_length)
        if key not in cls._cache:
            cls._cache[key] = cls._generate_progress_bar(position, total_length)
        return cls._cache[key]
```

### 10.4 調試與日誌

#### 10.4.1 日誌配置
```python
import logging

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('HorseRacingGame')

# 在關鍵位置添加日誌
def draw_card(self) -> Optional[Card]:
    if not self.cards:
        logger.warning("嘗試從空牌組抽牌")
        return None
    
    card = self.cards.pop()
    logger.info(f"抽到卡牌: {card}")
    return card
```

### 10.5 國際化支持

#### 10.5.1 多語言支持框架
```python
class Localization:
    _translations = {
        'zh_TW': {
            'spades_horse': '黑桃馬',
            'hearts_horse': '紅心馬',
            'diamonds_horse': '方塊馬',
            'clubs_horse': '梅花馬',
            'game_title': '撲克牌賽馬遊戲',
            'balance': '餘額',
            'bet_amount': '下注金額',
            # ... 更多翻譯
        },
        'en_US': {
            'spades_horse': 'Spades Horse',
            'hearts_horse': 'Hearts Horse',
            'diamonds_horse': 'Diamonds Horse',
            'clubs_horse': 'Clubs Horse',
            'game_title': 'Poker Horse Racing',
            'balance': 'Balance',
            'bet_amount': 'Bet Amount',
            # ... 更多翻譯
        }
    }
    
    def __init__(self, language: str = 'zh_TW'):
        self.language = language
    
    def get(self, key: str) -> str:
        return self._translations.get(self.language, {}).get(key, key)
```

### 10.6 風險評估與緩解

#### 10.6.1 技術風險
- **隨機數生成公平性**: 使用 Python 標準庫的 `random` 模組，經過充分測試
- **跨平台兼容性**: 僅使用標準庫，避免平台特定功能
- **性能問題**: 實現對象池、顯示緩存等優化策略

#### 10.6.2 產品風險
- **遊戲平衡性**: 提供可配置的賠率和賽道長度
- **用戶體驗**: 充分的錯誤處理和輸入驗證
- **可維護性**: 清晰的代碼結構和充分的文檔

#### 10.6.3 緩解策略
- 編寫完整的單元測試和整合測試
- 提供詳細的錯誤日誌和調試信息
- 實現漸進式功能開發（MVP → 完整版本）
- 用戶反饋收集機制

## 11. AI 實現檢查清單

### 11.1 P0 功能（必須實現）
- [ ] 實現 Suit 和 Rank 枚舉
- [ ] 實現 Card 類別，包含 `__str__` 和 `__repr__` 方法
- [ ] 實現 Deck 類別，包含洗牌、抽牌、重置功能
- [ ] 實現 Horse 類別，包含移動和獲勝檢測
- [ ] 實現 Track 類別，包含賽道顯示和狀態管理
- [ ] 實現 Player 類別，包含下注和資金管理
- [ ] 實現 HorseRacingGame 主遊戲類
- [ ] 實現基本的 CLI 界面和輸入處理
- [ ] 實現完整的遊戲流程（下注→賽馬→結算）

### 11.2 P1 功能（高優先級）
- [ ] 實現 InputValidator 輸入驗證類
- [ ] 實現錯誤處理和異常管理
- [ ] 實現遊戲統計功能
- [ ] 實現多局遊戲支持
- [ ] 實現清屏和界面刷新
- [ ] 實現 Ctrl+C 中斷處理

### 11.3 P2 功能（中優先級）
- [ ] 實現界面模板系統
- [ ] 實現遊戲歷史記錄
- [ ] 實現配置文件支持
- [ ] 實現進度條美化
- [ ] 實現成功/錯誤消息系統

### 11.4 代碼質量檢查
- [ ] 所有類別都有適當的文檔字符串
- [ ] 所有方法都有類型標註
- [ ] 錯誤處理覆蓋所有可能的異常情況
- [ ] 輸入驗證覆蓋所有用戶輸入點
- [ ] 代碼符合 PEP 8 風格指南
- [ ] 沒有硬編碼的魔法數字
- [ ] 適當使用枚舉代替字符串常量

### 11.5 測試檢查
- [ ] 編寫單元測試覆蓋核心邏輯
- [ ] 測試邊界條件（餘額為0、牌組空等）
- [ ] 測試錯誤輸入處理
- [ ] 測試完整遊戲流程
- [ ] 手動測試所有用戶交互路徑

### 11.6 部署檢查
- [ ] 確保只使用 Python 標準庫
- [ ] 支援 Python 3.8+
- [ ] 跨平台兼容（Windows/macOS/Linux）
- [ ] 提供清晰的運行說明
- [ ] 處理編碼問題（UTF-8 支持）

---

*本PRD文檔版本: v2.0 (AI優化版)*  
*最後更新日期: 2024年*  
*目標: 為AI代碼生成提供詳細、明確的技術規範*