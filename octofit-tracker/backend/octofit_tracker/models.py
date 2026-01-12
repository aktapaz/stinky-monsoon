from djongo import models


class Team(models.Model):
    _id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.JSONField(default=list)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    alias = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_points = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Activity(models.Model):
    user_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    points = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f'{self.activity_type} - {self.duration} mins'


class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField()
    exercises = models.JSONField(default=list)
    category = models.CharField(max_length=100)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    rank = models.IntegerField()
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100)
    total_points = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f'{self.rank}. {self.name} - {self.total_points} points'
