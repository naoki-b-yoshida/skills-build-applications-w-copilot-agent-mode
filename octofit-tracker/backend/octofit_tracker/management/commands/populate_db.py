from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # コレクション全削除
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.workouts.delete_many({})
        db.leaderboard.delete_many({})

        # サンプルユーザー
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers'},
            {'username': 'spiderman', 'email': 'spidey@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'username': 'superman', 'email': 'superman@dc.com', 'first_name': 'Clark', 'last_name': 'Kent'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]
        marvel_user_ids = db.users.insert_many(marvel_heroes).inserted_ids
        dc_user_ids = db.users.insert_many(dc_heroes).inserted_ids

        # チーム
        marvel_team = {'name': 'Marvel', 'members': marvel_user_ids}
        dc_team = {'name': 'DC', 'members': dc_user_ids}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # アクティビティ
        for user_id in marvel_user_ids + dc_user_ids:
            db.activities.insert_one({'user_id': user_id, 'activity_type': 'Running', 'duration': 30, 'calories_burned': 300, 'date': '2024-04-01'})
            db.activities.insert_one({'user_id': user_id, 'activity_type': 'Cycling', 'duration': 45, 'calories_burned': 400, 'date': '2024-04-02'})

        # ワークアウト
        for user_id in marvel_user_ids + dc_user_ids:
            db.workouts.insert_one({'user_id': user_id, 'name': 'Morning Routine', 'description': 'Pushups and situps', 'date': '2024-04-01'})
            db.workouts.insert_one({'user_id': user_id, 'name': 'Evening Cardio', 'description': 'Jogging and stretching', 'date': '2024-04-02'})

        # リーダーボード
        db.leaderboard.insert_one({'team_id': marvel_team_id, 'score': 900})
        db.leaderboard.insert_one({'team_id': dc_team_id, 'score': 850})

        # emailユニークインデックス
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Test data population completed.'))
