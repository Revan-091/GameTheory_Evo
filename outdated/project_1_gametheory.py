import nashpy as nash
import numpy as np




def main():
    #game1_mil()
  #  game2_eco()
   # game3_pol()

   
    
    #def game1_mil():
    mil_array = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])#Array values to be calculated historically accurate
    game1 = nash.Game(mil_array)
    
    sigma_row = [0, 1, 0]
    sigma_col = [0, 0, 1]
    payoff_mil = game1[sigma_row, sigma_col]
    points_row_player_1 = 0
    points_col_player_1 = 0

    print("\n")
    print("GAME 1(Military): ")
    print(game1)
    print("The strategies are:\n","Row Player: ", sigma_row, "Column player: ", sigma_col)
    print("\n The payoff is: ", payoff_mil)
    
    if payoff_mil[0] == all([1, -1]):
        points_row_player_1 += 1
        print("Points for row player: ", points_row_player_1)
        print("Points for column player", points_col_player_1)
    if payoff_mil[1] == all([-1, 1]):
        points_col_player_1 += 1
        print("Points for row player: ", points_row_player_1)
        print("Points for column player", points_col_player_1)
    else:
        print("hehehehe")

#def game2_eco():
    eco_array = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])#Array values to be calculated historically accurate
    game2 = nash.Game(eco_array)
    
    sigma_row = [0, 1, 0]
    sigma_col = [1, 0, 0]
    payoff_eco = game2[sigma_row, sigma_col]
    points_row_player_2 = 0
    points_col_player_2 = 0

    print("\n")
    print("GAME 2(Economics): ")
    print(game2)
    print("The strategies are:\n","Row Player: ", sigma_row, "Column player: ", sigma_col)
    print("\n The payoff is: ", payoff_eco)
    
    if payoff_eco[0] == all([1, -1]):
        points_row_player_2 += 1
        print("Points for row player: ", points_row_player_2)
        print("Points for column player", points_col_player_2)
    if payoff_eco[1] == all([-1, 1]):
        points_col_player_2 += 1
        print("Points for row player: ", points_row_player_2)
        print("Points for column player", points_col_player_2)
    else:
        print("hehehehe")


#def game3_pol():
    pol_array = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])#Array values to be calculated historically accurate
    game3 = nash.Game(pol_array)
    
    sigma_row = [0, 1, 0]
    sigma_col = [0, 0, 1]
    payoff_pol = game3[sigma_row, sigma_col]
    points_row_player_3 = 0
    points_col_player_3 = 0

    print("\n")
    print("GAME 3 (Politics): ")
    print(game3)
    print("The strategies are:\n","Row Player: ", sigma_row, "Column player: ", sigma_col)
    print("\n The payoff is: ", payoff_pol)
    
    if payoff_pol[0] == all([1, -1]):
        points_row_player_3 += 1
        print("Points for row player: ", points_row_player_3)
        print("Points for column player", points_col_player_3)
    if payoff_pol[1] == all([-1, 1]):
        points_col_player_3 += 1
        print("Points for row player: ", points_row_player_3)
        print("Points for column player", points_col_player_3)
    else:
        print("hehehehe")


    print("\n")
    Points_row_player = [points_row_player_1 + points_row_player_2 + points_row_player_3]
    print("Points for row player overall: ", Points_row_player)
    Points_col_player = [points_col_player_1 + points_col_player_2 + points_col_player_3]
    print("Points for column  player overall: ", Points_col_player)

    if Points_row_player > Points_col_player:
        print("\n")
        print("Row Player has won the conflict")
    elif Points_row_player < Points_col_player:
        print("\n")
        print("Column Player has won the conflict")
    elif Points_row_player == Points_col_player:
        print("\n")
        print("The conflict has resulted in a tie")
main()
