import random
class Tic_Tac_Toe_Elham:
    def __init__(self, num_of_rows=3):
        self.number_of_rows = num_of_rows
        self.game_matrix = [[0 for i in range(self.number_of_rows)] for j in range(self.number_of_rows)]
        self.flag_continue_game = True
        self.next_player= 'khar'
        
        self.number_of_turns = 0
        
    def play_game(self):
        number_of_rows = eval(input('please enter the size of the game? It will be the number of rows!'))
        self.build_matrix(number_of_rows)
        self.visualize_game()
        self.introduce_players()
        #print('ckecking winner', self.check_winner())
        while self.check_winner()==0:
            self.select_turn()
            row_number, column_number = self.choose_cell()
            self.update_matrix(row_number, column_number)
            #print('ckecking winner', self.check_winner())
            self.end_game()
        
    def build_matrix(self, num_of_rows=3):
        self.number_of_rows= num_of_rows
        self.game_matrix = [[0 for i in range(self.number_of_rows)] for j in range(self.number_of_rows)]
        
    def visualize_game(self):
        print(self.game_matrix)
        
    def introduce_players(self):
        confirm_O = str(input('player_1 you are playing with letter "O"!, please confirm that by entering the letter "O"')).upper()
        while confirm_O!= 'O':
            print('you are not entering letter "O"! your confirmation is needed before starting the game! :)')
            confirm_O = str(input('player_1 you are playing with letter "O"!, please confirm that by entering the letter "O"')).upper()
        print('Perfect')

        # A quick introduction with player two
        confirm_X = str(input('player_2 you are playing with letter "X"!, please confirm that by entering the letter "X"')).upper()
        while confirm_X!= 'X':
            print('you are not entering letter "X"! your confirmation is needed before starting the game! :)')
            confirm_X = str(input('player_2 you are playing with letter "X"!, please confirm that by entering the letter "X"')).upper()
        print('Perfect')
        
    def select_turn(self):
        
        
        if self.next_player== 'player_1':
            self.next_player ='player_2'
            
                
        elif self.next_player== 'player_2':
            self.next_player ='player_1'
            
                
        else:
            self.next_player= random.choice(['player_1', 'player_2'])
                   
        
        
    def choose_cell(self):
        print(self.next_player,'please enter a number between 1 and', self.number_of_rows, 'as a number of row')
        row_number= eval(input('please enter the number'))
        while int(row_number)< 1 or int(row_number)> int(self.number_of_rows):
            print('Your chosen number is out of range! you should enter a number between 1 and', self.number_of_rows)
            row_number= input('please enter the number')
        else:
            print('Thank you!')
            column_number= eval(input('Now, please enter another number in the same range as a number of column'))
            while int(column_number)< 1 or int(column_number)> int(self.number_of_rows):
                print('Your chosen number is out of range! you should enter a number between 1 and', self.number_of_rows)
                column_number= input('please enter the number')
        while self.game_matrix[int(row_number)-1][int(column_number)-1]!=0:
            print('your chosen cell has been selected before, please try another cell! please first enter the number of row')
            row_number= eval(input('please enter the number'))
            while int(row_number)< 1 or int(row_number)> int(self.number_of_rows):
                print('Your chosen number is out of range! you should enter a number between 1 and', self.number_of_rows)
                row_number= input('please enter the number')
            else:
                print('Thank you!')
                
                column_number= eval(input('Now, please enter another number in the same range as a number of column'))
                while int(column_number)< 1 or int(column_number)> int(self.number_of_rows):
                    print('Your chosen number is out of range! you should enter a number between 1 and', self.number_of_rows)
                    column_number= input('please enter the number')
        self.number_of_turns+=1
        return row_number, column_number
        
        
    def update_matrix(self, row_number, column_number):
        
        self.game_matrix[int(row_number)-1][int(column_number)-1]= 'O' if self.next_player =='player_1' else 'X'
        print(self.game_matrix)
        
    def check_winner(self):
        for i in range(self.number_of_rows):
            flag1=0
            flag2=0
            flag3=0
            flag4=0
            if self.game_matrix[i][0]==0:
                flag1=1
            if self.game_matrix[0][i]==0:    
                flag2=1
            if self.game_matrix[0][0]==0:    
                flag3=1
            if self.game_matrix[0][self.number_of_rows-1]==0:    
                flag4=1

            #print('f1:', flag1, 'f2:', flag2, 'f3:', flag3, 'f4:', flag4)
            for j in range(self.number_of_rows):
                if flag1==0 and self.game_matrix[i][j] != self.game_matrix[i][0]:
                    flag1=1
                if flag2==0 and self.game_matrix[j][i] != self.game_matrix[0][i]:
                    flag2=1
                if flag3==0 and i==j and self.game_matrix[0][0] != self.game_matrix[i][j]:
                    flag3=1
                if flag4==0 and j==self.number_of_rows-1-i and self.game_matrix[0][self.number_of_rows-1] != self.game_matrix[i][j]:
                    flag4=1
                #print('f1:', flag1, 'f2:', flag2, 'f3:', flag3, 'f4:', flag4)

            if (flag1==0 and self.game_matrix[i][0]=='O') or (flag2==0 and self.game_matrix[0][i]=='O'):
                return 1
            if (flag1==0 and self.game_matrix[0][i]=='X') or (flag2==0 and self.game_matrix[0][i]=='X'):
                return 2
            if self.number_of_turns==self.number_of_rows**2:
                return -1

        if (flag3==0 and self.game_matrix[0][0]=='O') or (flag4==0 and self.game_matrix[0][self.number_of_rows-1]=='O'):
            return 1
        if (flag3==0 and self.game_matrix[0][0]=='X') or (flag4==0 and self.game_matrix[0][self.number_of_rows-1]=='X'):
            return 2
        return 0    
    def end_game(self):
        res= self.check_winner()
        if res==1:
            print('player 1 you WON the game!')
        elif res==2:   
            print('player 2 you WON the game!')
        elif res==-1:
            print('The game has been ended in a draw')
            
            
            
