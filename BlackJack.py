import random
import time
import sys

suits = ('Hearts(♥)', 'Diamonds(♦)', 'Spades(♠)', 'Clubs(♣)')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

# Displays text with a typwriter effect
# This func is just for "enhanced" UI
def typewriter(text, delay=0.02, end=""):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(end, end="" )  

# This class all card attributes such as: rank, suit, and card value
class Card:
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
# This class simulates a card deck and has a func to shuffle it    
class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))
    
    def __str__(self):
        cards = 0
        for i in self.deck:
            print(i)
            cards += 1
        return(f"Remaining cards in the deck: {cards}") 
    
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        one_card = self.deck.pop()
        return one_card

# Class that accepts player's cards
# Ace is adjusted from 11 to 1 if total card value exceeds 21
class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1 
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
# Class that holds players chips and bets
class Chips:
    
    def __init__(self):
        self.total = 1000
        self.bet = 0 
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet
    
    
# Ask player to make a bet
def take_bet(chips): 
    
    while True:
        typewriter("\nMake your bet: ")
        bet = input()
        
        if bet.isnumeric() == False:
            
            typewriter("The bet you have put is not a value.\nPlease try again.")
            
        
        if bet.isnumeric() == True:
            
            if chips.total < int(bet):
                typewriter(f"You are betting more than you currently have. \nYour current balance is: {chips.total}\n\nUse a smaller bet.")
            
            if int(bet) == 0:
                typewriter("Let's see some money...")
            
            else:
                typewriter(f"\nPlayer bets {bet} Belly\n")
                break
    
    return int(bet)

# Call to hit
def hit(deck, hand): 
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    print("\n")
    print("_"*35)
    

# Asks player to hit or stand    
def hit_or_stand(deck, hand, dealer):
    while True:
        print("_"*35)
        typewriter("Do you want to hit or stand?\n (h/s) ")
        response = input()
        print("_"*35)
        
        if response.lower() == "h":
            typewriter("Player hits.")
            hit(deck, hand)
            show_some(player, dealer)
            if hand.value > 21:
                player_busts(player, player_chips)
                return False #Player is busted     
            return True
        
        elif response.lower() == "s":
            typewriter("Player stands.\n")
            print("_"*35)
            return False #Player stands
        else:
            print("Invalid input.")

#SHOWS ALL CARDS OF PLAYER, ONE OF DEALER
def show_some(player,dealer): 
    print("_"*35)
    typewriter("\nPlayer's Hand:\n\n")
    for card in player.cards:
        print(card)
    typewriter(f"Total Value: {player.value}")
    print("\n")
    print("_ "*17)
    
    typewriter("Dealer's Hand:\n\n ")
    print("*card hidden*")
    print(dealer.cards[1])
    
# This function will be used when it's the dealer's turn to draw cards
# Shows all cards of the dealer    
def show_dealer(dealer):
    print("_"*35)
    typewriter("Dealer's Hand:\n\n")
    for card in dealer.cards:
        print(card)
    time.sleep(3)

# Shows all cards of both parties
def show_all(player,dealer): 
    print("_"*35)
    typewriter("\n\t\t\tEND RESULT")
    typewriter("\nPlayer's Hand:\n\n")
    for card in player.cards:
        print(card)
    print("_ "*17)    
    typewriter(f"Total Value: {player.value}")
    print("\n")
    print("_"*35)
    
    typewriter("Dealer's Hand:\n\n")
    for card in dealer.cards:
        print(card)
    print("_ "*17)
    typewriter(f"Total Value: {dealer.value}\n")

# Winning/Losing calls
def player_busts(player, chips):
    time.sleep(1.5)
    print("_"*35)
    print("\nPLAYER BUSTS!")
    print("_"*35)
    chips.lose_bet()
    
def player_wins(chips):
    time.sleep(1.5)
    print("_"*35)
    print("\nPLAYER WINS!")
    print("_"*35)
    chips.win_bet()

def dealer_busts(chips):
    time.sleep(1.5)
    print("_"*35)
    print("\nDEALER BUSTS!")
    print("_"*35)
    chips.win_bet()
    
def dealer_wins(chips):
    time.sleep(1.5)
    print("_"*35)
    print("\nDEALER WINS!")
    print("_"*35)
    chips.lose_bet()

    
def push(chips):
    print("_"*35)
    print("IT'S A PUSH!\nPlayer's bet is returned...")
    print("_"*35)
    
    
# Function asks player whether to play again or not
def play_again(chips):
    while True:
        typewriter("Do you want to play again? (y/n):")
        decs = input()
        
        if chips.total == 0:
            typewriter("You went BANKRUPT...!",delay = 0.2)
            time.sleep(2)
            typewriter("\n\t\t\tGAME OVER", delay=0.15)
            return False
        elif decs.lower() not in ["y", "n"]:
            typewriter("Not the right answer.")
        elif decs.lower() == "y":
            typewriter("Starting new round\n")
            return True
        else:
            return False
        

# Building up the game...
"""                        Black Jack - GAME                                """
# Set up the Player's chips
player_chips = Chips()
        

while True:
    hits = True
    
    typewriter("The game is about to begin...\n\t\tGood luck!")
    
    time.sleep(1)
    deck = Deck() #Create the deck
    
    # Create & shuffle the deck, deal two cards to each player
    
    deck.shuffle()
    # Create the hands of the parties
    player = Hand()
    dealer = Hand()
    
    # Deal the cards to each player + dealer
    for i in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
    
    #Show amount of chips to the player
    print(f"\n*** Current Chips: {player_chips.total} Belly")
    time.sleep(1)
    
    # Prompt the Player for their bet
    player_bet = take_bet(player_chips)
    player_chips.bet = player_bet
    
    # Show cards (but keep one dealer card hidden)
    time.sleep(1.5)
    show_some(player, dealer)
    
    while True:  
        
        # Prompt for Player to Hit or Stand
        time.sleep(2)
        if not hit_or_stand(deck, player, dealer):
            break
 
        
        # When player's hand exceeds 21, player_busts() runs and breaks out of loop
        if player.value > 21:
            player_busts(player, player_chips)
            
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        time.sleep(1.5)
        while dealer.value <= 17:
            hit(deck, dealer)
            show_dealer(dealer)
        
        #Show all cards
        show_all(player, dealer)
        
        #Remaining winning/losing scenarios
        if dealer.value > 21:
            dealer_busts(player_chips)

        elif player.value > dealer.value:
            player_wins(player_chips)

        elif player.value < dealer.value:
            dealer_wins(player_chips)
            

        elif player.value == dealer.value:
            push(player_chips)


        
    time.sleep(2)    
    # Inform Player of their chips total
    print("\n")
    print("*"*35) 
    typewriter(f"\nTotal Chips:\n {player_chips.total}\n\n")
    print("*"*35) 
    
    # Ask player to play again
    game = play_again(player_chips)
    if not game:
        break