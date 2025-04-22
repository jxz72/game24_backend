from flask import Blueprint, render_template, request
from models.game import Game, GameState
from models import db


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
        board={"number1": "9", 
               "number2": '6',
               "number3": '3',
               "number4": '1'},  
    )
    db.session.add(new_game_state_1)
    db.session.commit()

    print(f"Game {new_game.id} created with states:")
    for state in new_game.game_states:
        print(state)

    return "sucesss"


