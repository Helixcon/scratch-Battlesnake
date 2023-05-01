# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Heloixcon",  # TODO: Your Battlesnake Username
        "color": "#FF5555",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")
  


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}


    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_head = game_state['you']['body'][0]
    
    is_move_safe = {
        "up": my_head["y"] < board_height - 1,
        "down": my_head["y"] > 0,
        "left": my_head["x"] > 0,
        "right": my_head["x"] < board_width - 1
    }

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']
    my_body = game_state['you']['body']
    
    # Check if any of the safe moves will collide with our body
    for move, isSafe in is_move_safe.items():
        if isSafe:
            # Calculate the next position of our head if we make this move
            next_pos = {
                "x": my_head["x"],
                "y": my_head["y"]
            }
            if move == "up":
                next_pos["y"] += 1
            elif move == "down":
                next_pos["y"] -= 1
            elif move == "left":
                next_pos["x"] -= 1
            elif move == "right":
                next_pos["x"] += 1

            # Check if the next position collides with our body
            if next_pos in my_body:
                is_move_safe[move] = False
    

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']
    opponents = game_state['board']['snakes']

    for opponent in opponents:
      for body_part in opponent['body']:
        if my_head['x'] == body_part['x'] and my_head['y'] == body_part['y']:
          if my_head['y'] < body_part['y']:
              is_move_safe["down"] = False
          elif my_head['y'] > body_part['y']:
              is_move_safe["up"] = False
          elif my_head['x'] < body_part['x']:
              is_move_safe["right"] = False
          elif my_head['x'] > body_part['x']:
              is_move_safe["left"] = False
          break
  # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
  
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
  
    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    def get_safe_moves(state, my_snake):
      # Get all possible moves
      all_moves = ['up', 'down', 'left', 'right']
      safe_moves = []
      
      # Calculate the coordinates of the snake's head
      head_x, head_y = my_snake['head']['x'], my_snake['head']['y']
      
      # Check if each move is safe by looking at adjacent squares
      for move in all_moves:
          # Calculate the new coordinates of the snake's head if it makes this move
          if move == 'up':
              new_x, new_y = head_x, head_y - 1
          elif move == 'down':
              new_x, new_y = head_x, head_y + 1
          elif move == 'left':
              new_x, new_y = head_x - 1, head_y
          elif move == 'right':
              new_x, new_y = head_x + 1, head_y
          
          # Check if the new coordinates are within the bounds of the board
          if new_x < 0 or new_x >= state['board']['width'] or new_y < 0 or new_y >= state['board']['height']:
              continue
          
          # Check if the new coordinates would collide with any other snakes
          collision = False
          for snake in state['board']['snakes']:
              for i in range(len(snake['body'])):
                  if new_x == snake['body'][i]['x'] and new_y == snake['body'][i]['y']:
                      collision = True
                      break
              if collision:
                  break
        
          # If the move is safe, add it to the list of safe moves
          if not collision:
              safe_moves.append(move)
      
      return safe_moves

    def manhattan_distance(point1, point2):
      return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
  
      my_snake = {'head': (5, 5)}
      enemy_snakes = [{'head': (3, 8)}, {'head': (9, 2)}, {'head': (4, 4)}]
      
      distances = [manhattan_distance(my_snake['head'], enemy['head']) for enemy in enemy_snakes]
      
      print(distances)

    def get_squares_controlled(board, player):
      # Create an empty set to store the controlled squares
      controlled_squares = set()
      
      # Iterate over each square on the board
      for i in range(len(board)):
          for j in range(len(board[i])):
              # Check if the square is controlled by the player
              if board[i][j] == player:
                  # Check each direction from the square
                  for dx, dy in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                      x, y = i, j
                      # Iterate in the direction until an empty square is reached
                      while 0 <= x < len(board) and 0 <= y < len(board[x]) and board[x][y] == player:
                          # Add the square to the set of controlled squares
                          controlled_squares.add((x, y))
                          x += dx
                          y += dy
      
      # Return the set of controlled squares
      return controlled_squares

    def heuristic(state, my_snake_id):
      my_snake = None
      enemy_snakes = []
      for snake in state['board']['snakes']:
          if snake['id'] == my_snake_id:
              my_snake = snake
          else:
              enemy_snakes.append(snake)
  
      # Check if the enemy snake has died
      for enemy in enemy_snakes:
          if not enemy['health']:
              return float('inf')
  
      # Check if my snake has died
      if not my_snake['health']:
          return float('-inf')
  
      # Calculate the distance to the nearest food
      distances_to_food = [manhattan_distance(my_snake['head'], food) for food in state['board']['food']]
      min_distance_to_food = min(distances_to_food)
  
      # Calculate the number of move options available
      num_move_options = len(get_safe_moves(state, my_snake))
  
      # Calculate the number of squares controlled by my snake
      num_squares_controlled = len(get_squares_controlled(state, my_snake))
  
      # Calculate the length of each snake
      my_snake_length = len(my_snake['body'])
      enemy_snake_lengths = [len(enemy['body']) for enemy in enemy_snakes]
  
      # Calculate the health of my snake
      my_snake_health = my_snake['health']
  
      # Calculate the distance to the nearest enemy snake
      distances_to_enemy_snakes = [manhattan_distance(my_snake['head'], enemy['head']) for enemy in enemy_snakes]
      min_distance_to_enemy_snake = min(distances_to_enemy_snakes)
  
      # Calculate the overall score based on the above attributes
      score = (my_snake_length * 100) + (num_squares_controlled * 10) + (num_move_options * 10) + (my_snake_health * 5) - (min_distance_to_food * 10) - (min_distance_to_enemy_snake * 5) - (sum(enemy_snake_lengths) * 5)
  
      return score

    def minimax(gameState, depth, maximizingPlayer):
      # Check if depth is 0 or gameState is terminal
      if depth == 0 or gameState.is_terminal():
          return gameState.get_score(), None
      
      # If maximizing player
      if maximizingPlayer:
          max_value = float('-inf')
          best_move = None
          for move_option in gameState.get_possible_moves():
              new_state = gameState.apply_move(move_option)
              value, _ = minimax(new_state, depth-1, False)
              if value > max_value:
                  max_value = value
                  best_move = move_option
          return max_value, best_move
      
      # If minimizing player
      else:
          min_value = float('inf')
          best_move = None
          for move_option in gameState.get_possible_moves():
              new_state = gameState.apply_move(move_option)
              value, _ = minimax(new_state, depth-1, True)
              if value < min_value:
                  min_value = value
                  best_move = move_option
          return min_value, best_move


    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
