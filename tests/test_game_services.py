from unittest.mock import patch, PropertyMock
from models.game import Game, GameState
from app.services.game_services import GameService
import pytest
from app.app import create_app


from app.constants import GameStatuses


# @pytest.fixture
# def app_context():
#     app = create_app()
#     with app.app_context():
#         # yield is a fancy way of using the with block and doing nothing but waiting
#         yield

# @pytest.fixture
# def game1():
#     game_state = GameState(board=['9', '4', '2', '1'])
#     game = Game()
#     print(game_state)
#     print(game)
#     game.latest_state_id=game_state.id
#     game.current_state_order=game_state.order
#     assert game.current_state_order == 0

#     return game

# @pytest.fixture
# def mock_game_with_state_factory(mocker):
#     def _create(board: list[str]):
#         sample_game = Game(id="65c83135-18a7-4556-9bd2-d15b77532133")
#         sample_game_state = GameState(board=board)

#         mocker.patch.object(Game, 'latest_state', new_callable=PropertyMock, return_value = sample_game_state)         
#         mocker.patch("app.services.game_services.GameService._create_game_state")
        
#         return sample_game
#     return _create
        

class TestGameService():
    

    def test_create_game_service(self, mocker):
        game_mock = mocker.Mock()
        game_mock.id = "65c83135-18a7-4556-9bd2-d15b77532133"
        game_mock.latest_state.board = ['9', '2', '3', '1']

        
        game_state_mock = mocker.Mock()
        game_state_mock.id = "ddd1bde8-5edc-4419-b290-3c42915c63b9" 

        mocker.patch("app.services.game_services.Game", return_value=game_mock)
        mocker.patch("app.services.game_services.GameState", return_value=game_state_mock)

        session_add_mock = mocker.patch("models.db.session.add")
        session_flush_mock = mocker.patch("models.db.session.flush")
        session_commit_mock = mocker.patch("models.db.session.commit")

        response = GameService.create_game()

        assert session_add_mock.call_count == 2
        assert session_flush_mock.call_count == 1
        assert session_commit_mock.call_count == 2

        assert response == {
            'board': ['9', '2', '3', '1'],
            'game_id': "65c83135-18a7-4556-9bd2-d15b77532133",
            'message': "Game Successfully Created",
            "status": "in_progress"
        }

    @pytest.mark.parametrize(
        "initial_board, number1, number2, operator, updated_board, expected_status",
        [
            (['10', '8', '7', '2'], '10', '8', 'add', ['7', '2', '18'], GameStatuses.IN_PROGRESS.value),
            (['10', '8', '7', '2'], '8', '2', 'div', ['10', '7', '4.0'], GameStatuses.IN_PROGRESS.value)
        ]
    ) 
    def test_make_move_service_happy_paths(self, mocker, initial_board, number1, number2, operator, updated_board, expected_status):
        sample_game = Game(id="65c83135-18a7-4556-9bd2-d15b77532133")
        sample_game_initial = GameState(board=initial_board)
        sample_game_updated = GameState(board=updated_board)

        # new callable needs to be callable so wrap it around a lambda
        mocker.patch.object(Game, 'latest_state', new_callable=lambda:PropertyMock(side_effect=[sample_game_initial, sample_game_updated]))

        # needed for a few reasons, but if you don't mock then the function will actually get called, and will use the mocker object as Game
        mock_create_game_state = mocker.patch("app.services.game_services.GameService._create_game_state")

        response = GameService.make_move(game=sample_game, number1=number1, number2=number2, operator=operator)

        # This verifies new_board is calculated correctly
        mock_create_game_state.assert_called_with(game=sample_game, board=updated_board)

        assert response == {
            "board": updated_board,
            "game_id": "65c83135-18a7-4556-9bd2-d15b77532133",
            "message": "move made successfully",
            "status": expected_status
        }

        

    # def test_make_move_service_divide_non_divisible(self, mock_game_with_state_factory):
    #     sample_game = mock_game_with_state_factory(board=['10', '8', '7', '2'])

    #     with pytest.raises(Exception) as exc_info:
    #         GameService.make_move(game=sample_game, number1="8", number2="7", operator="div")
        
    #     assert  "Can't divide evenly" in str(exc_info)

        



        















        # fake_game = mocker.Mock()
        # fake_game.id = "65c83135-18a7-4556-9bd2-d15b77532133"

        # fake_state = mocker.Mock()
        # fake_state.id = "ddd1bde8-5edc-4419-b290-3c42915c63b9"
        
        # mock_session = mocker.patch("services.game_services.db.session")
        # mock_session.flush.return_value = None
        # mock_session.add.return_value = None
        # mock_session.commit.return_value = None

        # mocker.patch("services.game_services.Game", return_value=fake_game)
        # mocker.patch("services.game_services.GameState", return_value=fake_state)

        # GameService.create_game()

        
        # mock_session.add.assert_any_call(fake_state)
        # mock_session.add.assert_any_call(fake_game)
        # mock_session.flush.assert_called_once()
        # mock_session.commit.assert_called()
        # mock_format_response.assert_called_once_with(
        #     game=fake_game,
        #     message="Game Successfully Created",
        #     status=GameStatuses.IN_PROGRESS
        # )

        
    
    
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




    
