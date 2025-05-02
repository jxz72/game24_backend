from app.app import create_app
from pytest import fixture
from unittest.mock import MagicMock, PropertyMock

@fixture
def client_app():
    app = create_app()
    app.testing = True
    return app.test_client()

@fixture
def mock_game():
    game = MagicMock()

    mock_state = MagicMock()
    mock_state.board = ["9", "3", "1", "10"]

    type(game).latest_state = PropertyMock(return_value=mock_state)

    return game


class TestGameRoutes:
    def test_create_game_route(self, client_app, mocker):
        mock_create_game = mocker.patch('app.services.game_services.GameService.create_game')
        expected_game_id = "65c83135-18a7-4556-9bd2-d15b77532133"
        mock_create_game.return_value = expected_game_id
    
        response = client_app.post('/create_game')

        mock_create_game.assert_called_once()
        
        assert response.status_code == 200 
        assert response.get_json() == {"game_id": expected_game_id}

    def test_create_game_route_fail(self, mocker, client_app):
        mock_create_game = mocker.patch(
            'app.services.game_services.GameService.create_game',
            side_effect=Exception("Random Exception Message here!")
        )

        response = client_app.post('/create_game')

        mock_create_game.assert_called_once()

        assert response.status_code == 500
        assert response.get_json() == {'error': 'Random Exception Message here!'}

    def test_view_game_route(self, client_app, mock_game, mocker):
        mock_get_game = mocker.patch(
            'app.services.game_services.GameService.get_game'
        )

        mock_get_game.return_value = mock_game

        response = client_app.get('/game?game_id=65c83135-18a7-4556-9bd2-d15b77532133')
        assert response.status_code == 200
        assert response.get_json() == {'board': ['9', '3', '1', '10'], 'game_id': "65c83135-18a7-4556-9bd2-d15b77532133"}
    
    def test_view_game_route_fail(self, mocker, client_app):
        mock_get_game = mocker.patch(
            'app.services.game_services.GameService.get_game',
            side_effect=Exception("There was a problem with mock get game")
        )
        response = client_app.get('/game?game_id=65c83135-18a7-4556-9bd2-d15b77532133')
        mock_get_game.assert_called_once()
        assert response.status_code == 500
        assert response.get_json() == {'error': 'There was a problem with mock get game'}

    def test_view_game_route_no_game_id(self, mocker, client_app):
        response = client_app.get('/game')
        assert response.status_code == 400
        assert response.get_json() == {'error': "Game ID not provided"}



        



        
