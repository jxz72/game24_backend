import copy
from models import db
from models.game import Game, GameState
from app.constants import VALID_OPERATIONS, GameStatuses

class GameService:
    @classmethod
    def create_game(cls) -> str:
        """
        Creates new game
        Returns ID of the game
        """
        game = Game()
        db.session.add(game)
        db.session.flush()

        new_game_state_1 = GameState(
            game_id=game.id,  # Link the game state to the new game
            order=0,
            board=["9", '6', '4', '1'],
        )
        db.session.add(new_game_state_1)
        db.session.commit()

        game.latest_state_id = new_game_state_1.id
        db.session.commit()

        return cls._format_response(game=game, message="Game Successfully Created", status=GameStatuses.IN_PROGRESS)

    @classmethod
    def get_game(cls, game_id: str):
        try:
            return Game.query.get(game_id)
        except:
            raise Exception("Game ID not valid")

    @classmethod
    def make_move(cls, game: Game, number1: str, number2: str, operator: str) -> list:
        try:
            number1_int = int(number1)
            number2_int = int(number2)
        except:
            raise Exception("number isn't a valid number")

        if operator not in VALID_OPERATIONS:
            raise Exception("Invalid operation passed in")

        if operator == 'div' and number1_int / number2_int != number1_int // number2_int:
            raise Exception("Can't divide evenly")
        
        curr_game_state: GameState = game.latest_state
        curr_board = curr_game_state.board

        #handle frequency too. 
        if number1 not in curr_board or number2 not in curr_board:
            raise Exception("Number not in board")
        

        new_board = copy.deepcopy(curr_board)
        new_board.remove(number1)
        new_board.remove(number2)

        op = VALID_OPERATIONS[operator]
        new_number = op(number1_int, number2_int)
        new_board.append(str(new_number))

        new_board_list = list(new_board)
        cls._create_game_state(game=game, board=new_board_list)

        return cls._format_response(game=game, message="move made successfully", status=GameStatuses.IN_PROGRESS)


    @classmethod
    def undo(cls, game: Game):
        if game.current_state_order == 0:
            return cls._format_response(game=game, status=GameStatuses.IN_PROGRESS, message="There are no steps to undo")

        current_state = GameState.query.get(game.latest_state_id)

        previous_state = (
                GameState.query
                .filter_by(game_id=game.id, order=game.current_state_order-1)
                .first()
            )
                
        if current_state and previous_state:
            db.session.delete(current_state)

            game.latest_state_id = previous_state.id
            game.current_state_order = previous_state.order

            db.session.commit()
        else:
            raise Exception("Alert, undo attempted but not updated")
        
        
        return cls._format_response(game=game, status=GameStatuses.IN_PROGRESS, message="Undo Completed")

    def _create_game_state(game: Game, board: list):
        new_order = game.current_state_order + 1
        new_game_state = GameState(
            game_id = game.id,
            order=new_order,
            board = board
        )
        db.session.add(new_game_state)
        db.session.flush()

        game.current_state_order = new_order
        game.latest_state_id = new_game_state.id

        db.session.commit()
    
    def _format_response(game: Game, status: GameStatuses, message: str):
        return {
            "game_id": game.id,
            "status": status.value,
            "message": message,
            "board": game.latest_state.board
        }