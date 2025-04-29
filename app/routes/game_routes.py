from flask import Blueprint, request, jsonify
from models.game import Game, GameState
from models import db
from app.constants import VALID_OPERATIONS
from app.services.game_services import GameService

bp = Blueprint("call", __name__)
@bp.route('/create_game', methods=['GET', 'POST'])
def create_game():
    game_id = GameService.create_game()
    return jsonify({"game_id": game_id})

@bp.route('/game', methods=['GET'])
def view_game():
    game_id = request.args.get("game_id")
    game = GameService.get_game(game_id=game_id)
    
    curr_board = game.latest_state.board

    return {
        "game_id": game_id,
        "board": curr_board,
    }


# This should just be a post request
@bp.route('/move', methods=['POST', 'GET'])
def make_move():
    game_id = request.args.get("game_id")
    number1 = request.args.get("number1")
    number2 = request.args.get("number2")
    operator = request.args.get("operator")

    if game_id is None:
        raise Exception("Game ID required")
    if number1 is None:
        raise Exception("Number1 required")
    if number2 is None:
        raise Exception("Number2 required")
    if operator is None:
        raise Exception("Operator required")    
    
    game = GameService.get_game(game_id=game_id)

    return GameService.make_move(game=game, number1=number1, number2=number2, operator=operator)

@bp.route('/undo', methods=['POST', 'GET'])
def undo_move():
    game_id = request.args.get("game_id")

    if game_id is None:
        raise Exception("Game ID invalid")

    game = GameService.get_game(game_id=game_id)

    return GameService.undo(game)