from flask import Blueprint, request
from models.game import Game, GameState
from models import db
from app.constants import VALID_OPERATIONS
from app.services.game_services import GameService

bp = Blueprint("call", __name__)
@bp.route('/create_game', methods=['GET', 'POST'])
def create_game():
    try:
        game_id = GameService.create_game()
        return game_id
    except:
        raise Exception("Game could not be created")

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
    
    game = Game.query.get(game_id)

    if game is None:
        raise Exception("Game ID not found")

    return GameService.make_move(game=game, number1=number1, number2=number2, operator=operator)