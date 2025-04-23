from flask import Blueprint, request
from models.game import Game, GameState
from models import db
from app.constants import VALID_OPERATIONS


bp = Blueprint("call", __name__)
@bp.route('/create_game', methods=['GET', 'POST'])
def create_game():

    print("JZ Inside Create Game")
    new_game = Game()
    print("JZ made new game")
    db.session.add(new_game)
    db.session.flush()  # 👈 This line is crucial

    print("JZ added game to session")

    new_game_state_1 = GameState(
        game_id=new_game.id,  # Link the game state to the new game
        order=0,
        board=["9", '6', '3', '1'],
    )
    db.session.add(new_game_state_1)
    db.session.commit()

    new_game.latest_state_id = new_game_state_1.id
    db.session.commit()


    print(f"Game {new_game.id} created with states:")
    for state in new_game.game_states:
        print(state)

    return "sucesss"

# This should just be a post request
@bp.route('/move', methods=['POST', 'GET'])
def make_move():
    game_id = request.args.get("game_id")
    number1 = request.args.get("number1")
    number2 = request.args.get("number2")
    operator = request.args.get("operator")

    if game_id is None:
        raise Exception("Game ID invalid")
    if number1 is None:
        raise Exception("Number1 is invalid")
    if number2 is None:
        raise Exception("Number2 is invalid")
    if operator is None:
        raise Exception("Operator is invalid")

    print(f"{game_id=}")
    print(f"{number1=}")
    print(f"{number2=}")
    print(f"{operator=}")
    if operator not in VALID_OPERATIONS:
        raise Exception("Invalid operation passed in")
    
    try:
        number1_int = int(number1)
        number2_int = int(number2)
    except:
        raise Exception

    
    if operator == '/' and number1_int / number2_int != number1_int // number2_int:
        raise Exception("Can't divide evenly")

    game = Game.query.get(game_id)

    if game is None:
        raise Exception("Game ID not found")

    curr_game_state: GameState = game.get_latest_state()

    board_set = set(curr_game_state.board)

    # Next is to get the set logic working
    return list(board_set)

    

    
