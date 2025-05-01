from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
from bson import ObjectId
import pytz

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Limpar dados existentes
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Criar usuários
        users = [
            User.objects.create(_id=ObjectId(), name="thundergod", email="thundergod@mhigh.edu"),
            User.objects.create(_id=ObjectId(), name="metalgeek", email="metalgeek@mhigh.edu"),
            User.objects.create(_id=ObjectId(), name="zerocool", email="zerocool@mhigh.edu"),
            User.objects.create(_id=ObjectId(), name="crashoverride", email="crashoverride@mhigh.edu"),
            User.objects.create(_id=ObjectId(), name="sleeptoken", email="sleeptoken@mhigh.edu")
        ]

        # Criar times
        blue_team = Team.objects.create(_id=ObjectId(), name="Blue Team")
        gold_team = Team.objects.create(_id=ObjectId(), name="Gold Team")
        blue_team.members.set(users)

        # Criar atividades
        for user in users:
            Activity.objects.create(
                _id=ObjectId(),
                user=user,
                activity_type="Cycling" if user.name == "thundergod" else
                           "Crossfit" if user.name == "metalgeek" else
                           "Running" if user.name == "zerocool" else
                           "Strength" if user.name == "crashoverride" else
                           "Swimming",
                duration=3600 if user.name == "thundergod" else
                        7200 if user.name == "metalgeek" else
                        5400 if user.name == "zerocool" else
                        1800 if user.name == "crashoverride" else
                        4500,
                date=datetime.now(pytz.UTC).date()
            )

        # Criar entradas no leaderboard
        for i, user in enumerate(users):
            Leaderboard.objects.create(
                _id=ObjectId(),
                user=user,
                score=100 - (i * 5)
            )

        # Criar workouts
        workouts = [
            Workout.objects.create(
                _id=ObjectId(),
                name="Cycling Training",
                description="Training for a road cycling event",
                user=next(u for u in users if u.name == "thundergod"),
                duration=timedelta(hours=1)
            ),
            Workout.objects.create(
                _id=ObjectId(),
                name="Crossfit",
                description="Training for a crossfit competition",
                user=next(u for u in users if u.name == "metalgeek"),
                duration=timedelta(hours=2)
            ),
            Workout.objects.create(
                _id=ObjectId(),
                name="Running Training",
                description="Training for a marathon",
                user=next(u for u in users if u.name == "zerocool"),
                duration=timedelta(hours=1, minutes=30)
            ),
            Workout.objects.create(
                _id=ObjectId(),
                name="Strength Training",
                description="Training for strength",
                user=next(u for u in users if u.name == "crashoverride"),
                duration=timedelta(minutes=30)
            ),
            Workout.objects.create(
                _id=ObjectId(),
                name="Swimming Training",
                description="Training for a swimming competition",
                user=next(u for u in users if u.name == "sleeptoken"),
                duration=timedelta(hours=1, minutes=15)
            )
        ]

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))