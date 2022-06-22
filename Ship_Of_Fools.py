

import random as rd


class Die:
    '''
Die: Responsible for handling randomly generated integer values between 1 and 6.
'''
    def __init__(self):
        self._value = 0
    def get_value(self) -> int:
        return self._value
    def roll(self):
        '''rolling the die'''
        self._value = rd.randint(1, 6)
    
    
    

class DiceCup:
    '''DiceCup: Handles five objects (dice) of class Die. Has the ability to bank and
release dice individually. Can also roll dice that are not banked.'''
    def __init__(self):
        self._dice = [Die() for i in range(5)]
        self._banked = [False for i in range(5)]
        
    def value(self, index) -> int:
        return self._dice[index]
        
    def bank(self, index):
        '''Banking the dice'''
        self._banked[index] = True
        
    def is_banked(self, index) -> bool:
        '''Checking if dice value is Banked'''
        return self._banked[index]
    
    def release(self, index):
        '''Releasing dice values'''
        self._banked[index] = False
        self._dice[index]._value = 0
        
    def release_all(self):
        '''Releasing all dice values'''
        for index in range(5):
            self.release(index)

    def roll(self):
        '''Rolling unbanked dices'''
        for index in range(5):
            if self._banked[index] == False:
                self._dice[index].roll()
  

class ShipOfFoolsGame:
    '''ShipOfFoolsGame: Responsible for the game logic and has the ability to play a
round of the game resulting in a score. Also has a property that tells what
accumulated score results in a winning state, for example 21.'''
    def __init__(self):
        self._cup = DiceCup()
        self.winning_score = 21
        
    def round(self) -> int:
        ## Releasing all the die
        self._cup.release_all()

        has_ship, has_captain, has_crew = False, False, False
        # This will be the sum of the remaining dice, i.e., the score.
        crew = 0
        
        die_values = [] 
        for index in range(5):
            die_values.append(self._cup._dice[index].get_value())
        print('Initial Die Values',die_values)
        
        self._cup.roll()
        # Repeat three times
        for game_round in range(3):
            
            die_values = [] 
            for index in range(5):
                die_values.append(self._cup._dice[index].get_value())
                
            print(die_values)
            if not (has_ship) and (6 in die_values):
                has_ship = True
                self._cup.bank(die_values.index(6)) # Fixing the Ship Die Value
                #print('Ship Index',die_values.index(6))
                    
            if (has_ship) and not (has_captain) and (5 in die_values):
                has_captain = True
                self._cup.bank(die_values.index(5)) # Fixing the Captian Die Value
                #print('Cap Index',die_values.index(5))
               
            if has_captain and not has_crew and (4 in die_values):
                has_crew = True
                self._cup.bank(die_values.index(4)) # Fixing the Crew Die Value
                #print('Crew Index',die_values.index(4))
            
            if has_ship and has_captain and has_crew:
                # Now we got all needed dice, and can bank the ones we like to save.
                if game_round < 2:
                    for index in range(5):
                        if self._cup._dice[index].get_value()>3:
                            self._cup.bank(index)
                        
                elif game_round == 2:
                    for index in range(5):
                        if not self._cup.is_banked(index):
                            self._cup.bank(index)
            else:
                self._cup.roll()
                
            sum_of_dice = sum(die_values)
           
        # If we have a ship, captain and crew (sum 15),
        # calculate the sum of the two remaining.
        if has_ship and has_captain and has_crew:
            crew = sum_of_dice - 15
        print('value', crew)
        return crew


class Player:
    '''Player: Responsible for the score of the individual player. Has the ability, given a
game logic, play a round of a game. The gained score is accumulated in the attribute
score.'''
    def __init__(self, name):
        self.set_name(name)
        self._score = 0
        
    def set_name(self, namestring):
        self._name = namestring
        
    def current_score(self):
        return self._score
    
    def reset_score(self):
        self._score = 0
        
    def play_round(self, game:ShipOfFoolsGame):
        self._score += game.round()


class PlayRoom:    
    '''PlayRoom: Responsible for handling a number of players and a game. Every round the room lets each player play, and afterwards check if any player have reached the winning score.'''
    def __init__(self):
        self._players = []
    
    def set_game(self, game:ShipOfFoolsGame):
        self.game = game
        
    def add_player(self, player:Player):
        '''Add player to room'''
        self._players.append(player)
    
    def reset_scores(self):
        for player in self._players:
            player.reset_score()
    
    def game_finished(self) -> bool:
        ''' returns True or Flase'''
        status = False
        scores = []
        
        for player in self._players:
            scores.append(player.current_score())
            
        if max(scores) >= self.game.winning_score:
            status = True
        
        return status
    
    def play_round(self):
        for player in self._players:
            #print(f"Now {player._name}'s turn")
            #print(player._name,'\n','-'*10)
            player.play_round(self.game)
            
    
    def print_scores(self):
        for player in self._players:
            print(f'Player: {player._name} has Scored: {player.current_score()}')
    
    def print_winner(self):
        scores = []
        for player in self._players:
            scores.append(player.current_score())
            
        if max(scores) >= self.game.winning_score:
            player = self._players[scores.index(max(scores))]
            print(f'Winner of the game: {player._name}')


if __name__ == "__main__":
    
    
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player('Ling'))
    room.add_player(Player('Chang'))
    room.add_player(Player('Kavya'))
    room.reset_scores()
    rounds = 1
    while not room.game_finished():
        print("round:",rounds)
        print('*'*10)
        room.play_round()
        room.print_scores()
        rounds+= 1
        
    
    room.print_winner()
    
