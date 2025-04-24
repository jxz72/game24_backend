from unittest.mock import patch
from models.game import Game
from app.services.game_services import GameService
import pytest
from app.app import create_app


@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        # yield is a fancy way of using the with block and doing nothing but waiting
        yield

@pytest.fixture
def game1():
    game = Game(board=["6", "4", "3", "8"])
    
class TestGameService():
    pass
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




    
