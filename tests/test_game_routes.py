from app.app import create_app
from pytest import fixture

@fixture
def client_app():
    app = create_app()
    app.testing = True
    return app.test_client()
    

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
        # mock_create_game.side_effect = Exception

        response = client_app.post('/create_game')

        mock_create_game.assert_called_once()

        assert response.status_code == 500
