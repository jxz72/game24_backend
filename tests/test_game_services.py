from unittest.mock import patch
from models.game import Game, GameState
from app.services.game_services import GameService
import pytest
from app.app import create_app

from app.constants import GameStatuses


@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        # yield is a fancy way of using the with block and doing nothing but waiting
        yield

@pytest.fixture
def game1():
    game_state = GameState(board=['9', '4', '2', '1'])
    game = Game()
    print(game_state)
    print(game)
    game.latest_state_id=game_state.id
    game.current_state_order=game_state.order
    assert game.current_state_order == 0

    return game

    
class TestGameService():
    pass
    
    # def test_format_response(self, game1):
        # sample_message = "Sample Message Here"

        # response = GameService._format_response(
        #     game=game1,
        #     status=GameStatuses.IN_PROGRESS,
        #     message=sample_message,
        # )
        # assert response == {
        #     "game_id": game1.id,
        #     "status": GameStatuses.value,
        #     "message": sample_message,
        #     "board": game1.board
        # }


    # @pytest.fixture(autouse=True)
    # def test_transaction(app_context):
    #     from app.models import db
    #     connection = db


    # @patch("app.services.game_services.db.session.add")
    # @patch("app.services.game_services.db.session.flush")
    # @patch("app.services.game_services.db.session.commit")
    # def test_create_game(self, mock_commit, mock_flush, mock_add, app_context):
    #     mock_commit.return_value = None
    #     mock_add.return_value = None

    #     json_response = GameService.create_game()
        
    #     print(json_response)




    
