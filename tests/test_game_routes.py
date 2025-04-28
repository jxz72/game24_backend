from app.app import create_app

class TestGameRoutes:
    def test_create_game_route(self, mocker):
        mock_create_game = mocker.patch('app.services.game_services.GameService.create_game')
        expected_game_id = "65c83135-18a7-4556-9bd2-d15b77532133"
        mock_create_game.return_value = expected_game_id
        app = create_app()

        client = app.test_client()
        response = client.post('/create_game')

        mock_create_game.assert_called_once()
        
        assert response.status_code == 200 
        assert response.data.decode() == expected_game_id
