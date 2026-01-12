from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        self.stdout.write(self.style.SUCCESS('Connected to MongoDB'))
        
        # Drop existing collections to start fresh
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        
        self.stdout.write(self.style.SUCCESS('Cleared existing collections'))
        
        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))
        
        # Insert Teams
        teams = [
            {
                '_id': 'team_marvel',
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.now(),
                'members': []
            },
            {
                '_id': 'team_dc',
                'name': 'Team DC',
                'description': 'Justice League Heroes',
                'created_at': datetime.now(),
                'members': []
            }
        ]
        db.teams.insert_many(teams)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams)} teams'))
        
        # Insert Users (Superheroes)
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'team': 'team_marvel', 'alias': 'Tony Stark'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'team': 'team_marvel', 'alias': 'Steve Rogers'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'team': 'team_marvel', 'alias': 'Thor Odinson'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'team': 'team_marvel', 'alias': 'Natasha Romanoff'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'team': 'team_marvel', 'alias': 'Bruce Banner'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'team': 'team_marvel', 'alias': 'Peter Parker'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'team': 'team_dc', 'alias': 'Clark Kent'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'team': 'team_dc', 'alias': 'Bruce Wayne'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'team': 'team_dc', 'alias': 'Diana Prince'},
            {'name': 'Flash', 'email': 'barry.allen@dc.com', 'team': 'team_dc', 'alias': 'Barry Allen'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'team': 'team_dc', 'alias': 'Arthur Curry'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'team': 'team_dc', 'alias': 'Hal Jordan'},
        ]
        
        users = []
        user_ids = []
        for hero in marvel_heroes + dc_heroes:
            user_doc = {
                'name': hero['name'],
                'email': hero['email'],
                'alias': hero['alias'],
                'team_id': hero['team'],
                'created_at': datetime.now(),
                'total_points': 0,
                'active': True
            }
            users.append(user_doc)
        
        result = db.users.insert_many(users)
        user_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users)} users'))
        
        # Update teams with member references
        marvel_user_ids = [uid for i, uid in enumerate(user_ids) if i < len(marvel_heroes)]
        dc_user_ids = [uid for i, uid in enumerate(user_ids) if i >= len(marvel_heroes)]
        
        db.teams.update_one({'_id': 'team_marvel'}, {'$set': {'members': marvel_user_ids}})
        db.teams.update_one({'_id': 'team_dc'}, {'$set': {'members': dc_user_ids}})
        
        # Insert Activities
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing']
        activities = []
        
        for user_id in user_ids:
            # Create 5-10 activities per user
            for _ in range(random.randint(5, 10)):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)  # minutes
                points = duration // 10  # 1 point per 10 minutes
                
                activity = {
                    'user_id': user_id,
                    'activity_type': activity_type,
                    'duration': duration,
                    'points': points,
                    'date': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'notes': f'Great {activity_type.lower()} session!'
                }
                activities.append(activity)
                
                # Update user's total points
                db.users.update_one(
                    {'_id': user_id},
                    {'$inc': {'total_points': points}}
                )
        
        db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities)} activities'))
        
        # Insert Workouts (suggested workouts)
        workouts = [
            {
                'name': 'Hero Strength Training',
                'description': 'Build superhuman strength with this intense workout',
                'difficulty': 'Advanced',
                'duration': 60,
                'exercises': ['Bench Press', 'Squats', 'Deadlifts', 'Pull-ups'],
                'category': 'Strength'
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Channel your inner speedster',
                'difficulty': 'Intermediate',
                'duration': 45,
                'exercises': ['Sprint Intervals', 'Jump Rope', 'High Knees', 'Burpees'],
                'category': 'Cardio'
            },
            {
                'name': 'Zen Warrior Yoga',
                'description': 'Find balance and flexibility like a true warrior',
                'difficulty': 'Beginner',
                'duration': 30,
                'exercises': ['Sun Salutation', 'Warrior Pose', 'Tree Pose', 'Meditation'],
                'category': 'Flexibility'
            },
            {
                'name': 'Aquatic Power Swim',
                'description': 'Master the waters with powerful strokes',
                'difficulty': 'Intermediate',
                'duration': 50,
                'exercises': ['Freestyle', 'Backstroke', 'Butterfly', 'Underwater Breathing'],
                'category': 'Swimming'
            },
            {
                'name': 'Vigilante Combat Training',
                'description': 'Fight crime with advanced combat techniques',
                'difficulty': 'Advanced',
                'duration': 75,
                'exercises': ['Shadow Boxing', 'Kickboxing', 'Grappling', 'Agility Drills'],
                'category': 'Combat'
            }
        ]
        
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts)} workouts'))
        
        # Create Leaderboard
        # Get all users sorted by total_points
        all_users = list(db.users.find().sort('total_points', -1))
        
        leaderboard_entries = []
        for rank, user in enumerate(all_users, start=1):
            entry = {
                'rank': rank,
                'user_id': user['_id'],
                'name': user['name'],
                'team_id': user['team_id'],
                'total_points': user['total_points'],
                'updated_at': datetime.now()
            }
            leaderboard_entries.append(entry)
        
        db.leaderboard.insert_many(leaderboard_entries)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_entries)} leaderboard entries'))
        
        # Display summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {db.teams.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {db.users.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {db.activities.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {db.workouts.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {db.leaderboard.count_documents({})}'))
        
        # Display top 3 from leaderboard
        self.stdout.write(self.style.SUCCESS('\n=== Top 3 Heroes ==='))
        for entry in leaderboard_entries[:3]:
            self.stdout.write(self.style.SUCCESS(
                f'{entry["rank"]}. {entry["name"]} - {entry["total_points"]} points'
            ))
        
        client.close()
