import random
from replit import db

class menu:
    def __init__(self):
        self.player_names = []
        self.num_players = 0
        self.num_games = 0
        self.games_played = 0

    def game_menu(self):
        while True:
            if (self.num_games == 0 and self.games_played != 0):
                print("Thank You For Playing!")
                print("Final Scores:")
                print("------------------")
                print(
                    f"Player 1 ({self.player_names[0]}) has {self.points1} total points"
                )
                print(
                    f"Player 2 ({self.player_names[1]}) has {self.points2} total points"
                )
                print("------------------")
                exit()
            if (self.games_played == 0):
                print(
                    "Welcome to the Game of UNO\n1) Play Game\n2) View Statistics\n3) Exit Program"
                )
                option = int(input("Please enter an option: "))
            else:
                print(
                    f"This is round {self.games_played+1}\n1) Play Game\n2) View Statistics\n3) Exit Program"
                )
                option = int(input("Please enter an option: "))
            if (option == 1):
                if (self.num_players == 0):
                    self.take_inputs()
                self.randomize_cards()
                self.start_board()
                self.place_card()
                break
            elif (option == 2):
                self.statistics()
                break
            elif (option == 3):
                exit()
            else:
                print("Only options are numbers 1-3")

    def statistics(self):
        print()
        if (len(self.player_names) == 0):
            print("No statistics have been found!")
        else:
            while True:
                print(
                    "Choose an option below\n1) Player points\n2) Games Played\n3) Return to main_menu"
                )
                option = int(input("Please enter an option: "))
                print()
                if (option == 3):
                    self.game_menu()
                else:
                    print("------------------")
                    if (option == 1):
                        for i in range(len(db["names"])):
                            name = db["names"][i][0]
                            points = db["names"][i][1]
                            print(f"{name} has {points} points")
                    elif (option == 2):
                        played = db["games"]
                        print(f"Games played is {played}")
                    else:
                        print("Only options are 1-3")
                    print("------------------")
                print()
        print()
        self.game_menu()

    def get_number_of_players(self):
        while True:
            self.num_players = int(
                input("How many players to play the game? "))
            if (self.num_players != 2):
                print("Only 2 players can play at once!")
                continue
            else:
                break

    def get_player_names(self):
        i = 1
        while (i <= self.num_players):
            name = input(f"Enter Player {i} Name: ")
            if (name.isalpha() == False):
                print("Please enter a valid name for Player!")
            else:
                self.player_names.append(name)
                i += 1

    def get_number_of_games(self):
        while True:
            self.num_games = int(
                input(
                    "How many games do you want to play choose an odd number? "
                ))
            if (self.num_games % 2 == 0):
                print("Please enter an odd integer for number of games!")
                continue
            else:
                break

    def take_inputs(self):
        self.get_number_of_players()
        self.get_player_names()
        self.get_number_of_games()


class game(menu):
    def __init__(self):
        super().__init__()
        self.playing_cards_colors = ["Red", "Blue", "Yellow", "Green"]
        self.playing_cards_numbers = [i for i in range(1, 10)] + ['Skip', 'Reverse', 'DrawTwo']
        self.deck = ([(i, j) for i in self.playing_cards_colors for j in self.playing_cards_numbers]) * 2 + [('DrawFour'), ('ColorChange')] * 4 + ([(i, j) for i in self.playing_cards_colors for j in range(1)])
        self.player_cards = {}
        self.current_card = ()
        self.player_turn = 0
        self.card_option = 0
        self.current_color = ""
        self.current_value = 0
        self.points1 = 0
        self.points2 = 0

    def randomize_cards(self):
        arr = []
        loop = 7 * len(self.player_names)
        for i in range(loop):
            randnum = random.randint(0, len(self.deck) - 1)
            arr.append(self.deck[randnum])
            self.deck.pop(randnum)
        size = len(arr) // len(self.player_names)
        for i in range(len(self.player_names)):
            self.player_cards[self.player_names[i]] = arr[:size]
            arr = arr[size:]

    def start_board(self):
        while self.current_card == ():
            randnum = random.randint(0, len(self.deck) - 1)
            if (type(self.deck[randnum][-1]) == int):
                self.current_card = self.deck[randnum]
                self.deck.pop(randnum)
                break
        self.current_color = self.current_card[0]
        self.current_value = self.current_card[1]
        print()

    def new_deck(self):
        self.deck = ([(i, j) for i in self.playing_cards_colors for j in self.playing_cards_numbers]) * 2 + [('DrawFour'), ('ColorChange')] * 4 + ([(i, j) for i in self.playing_cards_colors for j in range(1)])

    def pickup(self):
        randnum = random.randint(0, len(self.deck) - 1)
        temp = (self.deck[randnum], )
        print(f"Your new card is {self.deck[randnum]}")
        self.player_cards[self.player_names[self.player_turn]] += temp
        self.deck.pop(randnum)
        print(len(self.deck))
        if (len(self.deck) == 0):
            self.new_deck()
        print()
        if self.player_turn == 1:
            self.player_turn = 0
        else:
            self.player_turn = 1
        self.place_card()

    def place_card(self):
        if (len(self.player_cards[self.player_names[0]]) == 0):
            self.winner(0)
            self.game_menu()
        if (len(self.player_cards[self.player_names[1]]) == 0):
            self.winner(1)
            self.game_menu()
        print(f"{self.player_names[self.player_turn]} it is your turn!")
        if (self.current_card == "ColorChange" or self.current_card == "DrawFour"):
            print(
                f"The current card on the deck is {self.current_card}, the color chosen is {self.current_color}"
            )
        else:
            print(f"The current card on the deck is {self.current_card}")
        print("------------------")
        print(f"Your deck is: ")
        for i in range(
                len(self.player_cards[self.player_names[self.player_turn]])):
            print(
                f"{i+1}) {self.player_cards[self.player_names[self.player_turn]][i]}"
            )
        print("------------------")
        print()
        print(f"1) Play from hand")
        print(f"2) Pick up card")
        while True:
            num = int(input("Choose an option: "))
            if (num == 1 or num == 2):
                break
            else:
                print("Only inputs are 1 and 2!")
        if (num == 1):
            self.card_option = int(
                input("Choose which card you want to play: "))
            print()
            self.player_move()
        else:
            self.pickup()

    def player_move(self):
        if ((self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1][1]) == "DrawTwo"):
            self.current_card = self.player_cards[self.player_names[
                self.player_turn]][self.card_option - 1]
            self.current_color = self.player_cards[self.player_names[
                self.player_turn]][self.card_option - 1][0]
            del self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1]
            if self.player_turn == 1:
                self.player_turn = 0
            else:
                self.player_turn = 1
            self.draw_cards(2, self.player_turn)
            self.place_card()
        if ((self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1][1]) == "Skip"
                or (self.player_cards[self.player_names[self.player_turn]][
                    self.card_option - 1][1]) == "Reverse"):
            self.current_card = self.player_cards[self.player_names[
                self.player_turn]][self.card_option - 1]
            self.current_color = self.player_cards[self.player_names[
                self.player_turn]][self.card_option - 1][0]
            del self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1]
            self.place_card()
        if (self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1][0] == self.current_color
                or (self.player_cards[self.player_names[self.player_turn]][
                    self.card_option - 1][1] == self.current_value)):
            self.current_color = self.player_cards[self.player_names[
                self.player_turn]][self.card_option - 1][0]
            self.current_value = self.player_cards[self.player_names[
                self.player_turn]][self.card_option - 1][1]
            self.current_card = self.player_cards[self.player_names[
                self.player_turn]][self.card_option - 1]
            del self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1]
            if self.player_turn == 1:
                self.player_turn = 0
            else:
                self.player_turn = 1
            self.place_card()
        elif (self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1] == "DrawFour"):
            del self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1]
            if self.player_turn == 1:
                self.player_turn = 0
            else:
                self.player_turn = 1
            self.draw_cards(4, self.player_turn)
            self.choose_colors("DrawFour")
        elif (self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1] == "ColorChange"):
            del self.player_cards[self.player_names[self.player_turn]][
                self.card_option - 1]
            if self.player_turn == 1:
                self.player_turn = 0
            else:
                self.player_turn = 1
            self.choose_colors("ColorChange")
        else:
            print("Invalid card! Try again.")
            self.place_card()

    def choose_colors(self, card):
        for i in range(len(self.playing_cards_colors)):
            print(f"{i+1}) {self.playing_cards_colors[i]}")
        newColor = int(input("What colour would you like to choose? "))
        print()
        self.current_color = self.playing_cards_colors[newColor - 1]
        self.current_card = card
        self.place_card()

    def draw_cards(self, numCards, player):
        for i in range(numCards):
            randnum = random.randint(0, len(self.deck) - 1)
            temp = (self.deck[randnum], )
            self.player_cards[self.player_names[player]] += temp
            self.deck.pop(randnum)
        if self.player_turn == 1:
            self.player_turn = 0
        else:
            self.player_turn = 1

    def winner(self, player):
        points = 0
        if (player == 0):
            for i in range(len(self.player_cards[self.player_names[1]])):
                if self.player_cards[self.player_names[1]][i][
                        1] == "Skip" or self.player_cards[self.player_names[
                            1]][i][1] == "Reverse" or self.player_cards[
                                self.player_names[1]][i][1] == "DrawTwo":
                    points += 20
                    self.points1 += 20
                elif self.player_cards[self.player_names[1]][
                        i] == "DrawFour" or self.player_cards[
                            self.player_names[1]][i] == "ColorChange":
                    points += 50
                    self.points1 += 50
                else:
                    points += self.player_cards[self.player_names[1]][i][1]
                    self.points1 += self.player_cards[
                        self.player_names[1]][i][1]
            print(
                f"Congratulations {self.player_names[player]} you are the winner of round {self.games_played+1}"
            )
            print(f"You earned {points} points")
            points = 0
        else:
            for i in range(len(self.player_cards[self.player_names[0]])):
                if self.player_cards[self.player_names[0]][i][
                        1] == "Skip" or self.player_cards[self.player_names[
                            0]][i][1] == "Reverse" or self.player_cards[
                                self.player_names[0]][i][1] == "DrawTwo":
                    points += 20
                    self.points2 += 20
                elif self.player_cards[self.player_names[0]][
                        i] == "DrawFour" or self.player_cards[
                            self.player_names[0]][i] == "ColorChange":
                    points += 50
                    self.points2 += 50
                else:
                    points += self.player_cards[self.player_names[0]][i][1]
                    self.points2 += self.player_cards[
                        self.player_names[0]][i][1]
            print(
                f"Congratulations {self.player_names[player]} you are the winner of round {self.games_played+1}"
            )
            print(f"You earned {points} points")
            points = 0
        print()
        db["names"] = (self.player_names[0],
                       self.points1), (self.player_names[1], self.points2)
        db["games"] = self.games_played + 1
        self.num_games -= 1
        self.games_played += 1


def main():
    game().game_menu()


if __name__ == '__main__':
    main()
