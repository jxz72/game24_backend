from app.app import create_app

class TestGameRoutes:
    # This is using the pytest-mock mocker fixture
    def test_create_game_route(self, mocker):
        mock_create_game = mocker.patch('app.services.game_services.GameService.create_game')
        mock_create_game.return_value = "65c83135-18a7-4556-9bd2-d15b77532133"
        app = create_app()

        client = app.test_client()
        response = client.post('/create_game')

        mock_create_game.assert_called_once()
    
        assert response.data.decode() == "65c83135-18a7-4556-9bd2-d15b77532133"
