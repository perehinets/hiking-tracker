from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Hiker, Hike, Route, Difficulty


@admin.register(Hiker)
class HikerAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "gender",
                        "birth_date",
                    )
                },
            ),
        )
    )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ("difficulty",)
    list_display = ("name", "location", "difficulty", "distance", "elevation")


@admin.register(Hike)
class HikeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ("route",)
    list_display = ("name", "date", "max_hikers")


admin.site.register(Difficulty)
