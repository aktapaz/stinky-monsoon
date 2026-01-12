from django.test import TestCase
from .models import Team, User, Activity, Workout, Leaderboard

class ModelTests(TestCase):
    def test_team_creation(self):
        team = Team.objects.create(_id='test_team', name='Test Team', description='Test', members=[])
        self.assertEqual(team.name, 'Test Team')

    def test_user_creation(self):
        user = User.objects.create(name='Test User', email='test@example.com', alias='Tester', team_id='test_team')
        self.assertEqual(user.email, 'test@example.com')

    def test_activity_creation(self):
        activity = Activity.objects.create(user_id='test_user', activity_type='Running', duration=30, points=3, date='2026-01-12T00:00:00Z')
        self.assertEqual(activity.activity_type, 'Running')

    def test_workout_creation(self):
        workout = Workout.objects.create(name='Test Workout', description='Desc', difficulty='Easy', duration=20, exercises=['Run'], category='Cardio')
        self.assertEqual(workout.name, 'Test Workout')

    def test_leaderboard_creation(self):
        entry = Leaderboard.objects.create(rank=1, user_id='test_user', name='Test User', team_id='test_team', total_points=100)
        self.assertEqual(entry.rank, 1)
