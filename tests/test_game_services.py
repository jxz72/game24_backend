from unittest.mock import patch, PropertyMock
from models.game import Game, GameState
from app.services.game_services import GameService
import pytest
from app.app import create_app

from app.constants import GameStatuses

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

    @pytest.mark.parametrize(
        "initial_board, number1, number2, operator, expected_error",
        [
            (['10', '8', '7', '2'], '10', '8', 'div', Exception("Can't divide evenly")),
            (['10', '8', '7', '2'], 'hey', '2', 'div', Exception("number isn't a valid number"))
        ]
    ) 
    def test_make_move_service_errors(self, mocker, initial_board, number1, number2, operator, expected_error):
        game = Game(id="65c83135-18a7-4556-9bd2-d15b77532133")

        with pytest.raises(Exception) as exc_info:
            GameService.make_move(game=game, number1=number1, number2=number2, operator=operator)
        print(exc_info.value)
        assert str(exc_info.value) == str(expected_error)

