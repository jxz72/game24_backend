import copy
from models import db
from models.game import Game, GameState
from app.constants import VALID_OPERATIONS

class GameService:
    @classmethod
    def create_game(cls) -> str:
        """
        Creates new game
        Returns ID of the game
        """
        new_game = Game()
        db.session.add(new_game)
        db.session.flush()

        new_game_state_1 = GameState(
            game_id=new_game.id,  # Link the game state to the new game
            order=0,
            board=["9", '6', '4', '1'],
        )
        db.session.add(new_game_state_1)
        db.session.commit()

        new_game.latest_state_id = new_game_state_1.id
        db.session.commit()


        print(f"Game {new_game.id} created with states:")
        for state in new_game.game_states:
            print(state)

        return new_game.id

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
        
        curr_game_state: GameState = game.get_latest_state()
        curr_board = set(curr_game_state.board)

        if number1 not in curr_board or number2 not in curr_board:
            raise Exception("Number not in board")
        

        new_board = copy.deepcopy(curr_board)
        new_board.remove(number1)
        new_board.remove(number2)

        op = VALID_OPERATIONS[operator]
        new_number = op(number1_int, number2_int)
        new_board.add(str(new_number))

        new_board_list = list(new_board)
        cls._create_game_state(game=game, board=new_board_list)

        return new_board_list 


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

    @classmethod
    def undo(cls, game: Game):
        if game.current_state_order == 0:
            return "There are no steps to undo."

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
        
        
        return previous_state.board
            

