import uuid
from models import db

class Game(db.Model):
    __tablename__ = 'games'
    
    # UUID Primary Key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    latest_state_id = db.Column(db.String(36), db.ForeignKey('game_states.id'), nullable=True)
    current_state_order = db.Column(db.Integer, default=0)

    # Relationship to GameState

    game_states = db.relationship(
        'GameState',
        backref='game',
        lazy=True,
        primaryjoin='Game.id == GameState.game_id',
        foreign_keys='GameState.game_id'
    )

    def get_latest_state(self) -> 'GameState':
        print(f"{self.latest_state_id}")
        return GameState.query.get(self.latest_state_id)
    
    def __repr__(self):
        return f'<Game {self.id}>'


class GameState(db.Model):
    __tablename__ = 'game_states'
    
    # UUID Primary Key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Key to Game
    game_id = db.Column(db.String(36), db.ForeignKey('games.id'), nullable=False)
    
    # Order of the game state
    order = db.Column(db.Integer, nullable=False)
    
    # Board representation, you can use JSON or a string
    board = db.Column(db.JSON, nullable=False)
    
    # Ensure combination of game_id and order is unique
    __table_args__ = (db.UniqueConstraint('game_id', 'order', name='_game_order_uc'),)

    def __repr__(self):
        return f'<GameState {self.id}>'


