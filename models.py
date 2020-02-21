from app import db


class Player(db.Model):
    __table_args__ = {'schema': 'hockey'}
    id = db.Column(db.Integer, primary_key=True, index=True)
    slug = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    position = db.Column(db.String(2))
    shoots = db.Column(db.String(120))
    height = db.Column(db.String(4))
    weight = db.Column(db.Integer)
    dob = db.Column(db.Date)
    is_hof = db.Column(db.Boolean)
    #nationality = db.Column(db.String(50))

    def __init__(self, slug, name, position, shoots, height, weight, dob, is_hof):

        self.slug = slug
        self.name = name
        self.position = position
        self.shoots = shoots
        self.height = height
        self.weight = weight
        self.dob = dob
        self.is_hof = is_hof
        #self.nationality = nationality


class SkaterSeason(db.Model):
    __table_args__ = {'schema': 'hockey'}

    id = db.Column(db.Integer, primary_key=True, index=True)
    player_id = db.Column(db.Integer, db.ForeignKey('hockey.player.id'))
    season = db.Column(db.String(7))
    age = db.Column(db.Integer)
    team = db.Column(db.String(3))
    league = db.Column(db.String(4))
    games_played = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    points = db.Column(db.Integer)
    penalty_minutes = db.Column(db.Integer)
    even_strength_goals = db.Column(db.Integer)
    power_play_goals = db.Column(db.Integer)
    short_handed_goals = db.Column(db.Integer)
    game_winning_goals = db.Column(db.Integer)
    even_strength_assists = db.Column(db.Integer)
    power_play_assists = db.Column(db.Integer)
    short_handed_assists = db.Column(db.Integer)
    shots = db.Column(db.Integer)
    shot_percentage = db.Column(db.Float)
    time_on_ice = db.Column(db.Integer)
    average_time_on_ice = db.Column(db.Integer)
    awards = db.Column(db.String)
    is_playoffs = db.Column(db.Boolean)
    won_cup = db.Column(db.Boolean)

    def __init__(self, player_id, season, age, team, league, games_played, goals, assists, points, penalty_minutes, even_strength_goals, power_play_goals, short_handed_goals, game_winning_goals, even_strength_assists, power_play_assists, short_handed_assists, shots, shot_percentage, time_on_ice, average_time_on_ice, awards, is_playoffs, won_cup):

        self.player_id = player_id
        self.season = season
        self.age = age
        self.team = team
        self.league = league
        self.games_played = games_played
        self.goals = goals
        self.assists = assists
        self.points = points
        self.penalty_minutes = penalty_minutes 
        self.even_strength_goals = even_strength_goals
        self.power_play_goals = power_play_goals
        self.short_handed_goals = short_handed_goals
        self.game_winning_goals = game_winning_goals
        self.even_strength_assists = even_strength_assists
        self.power_play_assists = power_play_goals
        self.short_handed_assists = short_handed_assists
        self.shots = shots
        self.shot_percentage = shot_percentage
        self.time_on_ice = time_on_ice
        self.average_time_on_ice = average_time_on_ice
        self.awards = awards
        self.is_playoffs = is_playoffs
        self.won_cup = won_cup

class GoalieSeason(db.Model):
    __table_args__ = {'schema': 'hockey'}

    id = db.Column(db.Integer, primary_key=True, index=True)
    player_id = db.Column(db.Integer, db.ForeignKey('hockey.player.id'))
    season = db.Column(db.String(7))
    age = db.Column(db.Integer)
    team = db.Column(db.String(3))
    league = db.Column(db.String(4))
    games_played = db.Column(db.Integer)
    games_started = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses =  db.Column(db.Integer)
    tie_overtime_shootout_losses = db.Column(db.Integer)
    goals_against = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    save_percentage = db.Column(db.Float)
    goals_against_average = db.Column(db.Float)
    shutout = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    quality_starts = db.Column(db.Integer)
    quality_start_percentage = db.Column(db.Float)
    really_bad_starts = db.Column(db.Integer)
    goals_saved_above_average = db.Column(db.Float)
    adjusted_goals_against_average = db.Column(db.Float)
    goalie_point_share = db.Column(db.Float)
    goals = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    points = db.Column(db.Integer)
    penalty_minutes = db.Column(db.Integer)
    is_playoffs = db.Column(db.Boolean)
    won_cup = db.Column(db.Boolean)

    def __init__(self, player_id, season, age, team, league, games_played, games_started, wins, losses, tie_overtime_shootout_losses, goals_against, saves, save_percentage, goals_against_average, shutout, minutes, quality_starts, quality_start_percentage, really_bad_starts, goals_saved_above_average, adjusted_goals_against_average, goalie_point_share, goals, assists, points, penalty_minutes, awards, is_playoffs, won_cup):

        self.player_id = player_id
        self.season = season
        self.age = age
        self.team = team
        self.league = league
        self.games_played = games_played
        self.games_started = games_started
        self.wins = wins
        self.losses =  losses
        self.tie_overtime_shootout_losses = tie_overtime_shootout_losses 
        self.goals_against = goals_against
        self.saves = saves
        self.save_percentage = save_percentage
        self.goals_against_average = goals_against_average
        self.shutout = shutout
        self.minutes = minutes
        self.quality_starts = quality_starts
        self.quality_start_percentage = quality_start_percentage
        self.really_bad_starts = really_bad_starts
        self.goals_saved_above_average = goals_saved_above_average
        self.adjusted_goals_against_average = adjusted_goals_against_average
        self.goalie_point_share = goalie_point_share
        self.goals = goals
        self.assists = assists
        self.points = points
        self.penalty_minutes = penalty_minutes 
        self.awards = awards
        self.is_playoffs = is_playoffs
        self.won_cup = won_cup