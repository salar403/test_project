from django.db import models


class Leader(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)


class User(models.Model):
    MALE = 1
    FEMALE = 2
    NON_BINARY = 3
    GENDER_NOT_LISTED = 4

    GENDERS = [
        (MALE,"male"),
        (FEMALE,"female"),
        (NON_BINARY,"non_binary"),
        (GENDER_NOT_LISTED,"not_listed"),
    ]

    EAST_ASIAN = 1
    SOUTH_ASIAN = 2
    SOUTH_EAST_ASIAN = 3
    HISPANIC = 4
    LATINO = 5
    MIDDLE_EASTERN = 6
    MULTI_RACIAL = 7
    NATIVE_AMERICAN = 8
    WHITE = 9
    RACE_NOT_LISTED = 10

    RACES = [
        (EAST_ASIAN,"east_asian"),
        (SOUTH_ASIAN,"south_asian"),
        (SOUTH_EAST_ASIAN,"south_east_asian"),
        (HISPANIC,"hispanic"),
        (MIDDLE_EASTERN,"middle_eastern"),
        (MULTI_RACIAL,"multi_racial"),
        (NATIVE_AMERICAN,"native_american"),
        (WHITE,"white"),
        (RACE_NOT_LISTED,"not_listed"),
    ]
    name = models.CharField(max_length=50)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField(null=False)
    gender = models.IntegerField(choices=GENDERS, default=GENDER_NOT_LISTED)
    race = models.IntegerField(choices=RACES, default=RACE_NOT_LISTED)
    leader = models.ForeignKey(Leader, on_delete=models.SET_NULL, null=True, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    TOP = 1
    RIGHT = 2
    LEFT = 3

    TYPES = [
        (TOP, "top"),
        (RIGHT, "right"),
        (LEFT, "left"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="images")
    image = models.ImageField(upload_to="userimages/", null=False)
    attemp = models.IntegerField(default=0)
    type = models.IntegerField(choices=TYPES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Logins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logins")
    token = models.CharField(max_length=36, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
