from flask import Blueprint

from CTFd.models import Challenges, Fails, Solves, db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.utils.user import get_ip


class TimerChallengeModel(Challenges):
    id = db.Column(
        db.Integer,
        db.ForeignKey("challenges.id", ondelete="CASCADE"),
        primary_key=True
    )

    def __init__(self, *args, **kwargs):
        super(TimerChallengeModel, self).__init__(**kwargs)


class TimerChallenge(BaseChallenge):
    id = "timer"  # Unique identifier used to register challenges
    name = "timer"  # Name of a challenge type
    templates = {  # Handlebars templates used for each aspect of challenge editing & viewing
        "create": "/plugins/timer_challenges/assets/create.html",
        "update": "/plugins/timer_challenges/assets/update.html",
        "view": "/plugins/timer_challenges/assets/view.html",
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/timer_challenges/assets/create.js",
        "update": "/plugins/timer_challenges/assets/update.js",
        "view": "/plugins/timer_challenges/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/timer_challenges/assets/"
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        "timer_challenges",
        __name__,
        template_folder="templates",
        static_folder="assets",
    )
    challenge_model = TimerChallengeModel

    @classmethod
    def read(cls, challenge):
        challenge = TimerChallengeModel.query.filter_by(id=challenge.id).first()
        data = {
            "id": challenge.id,
            "name": challenge.name,
            "value": challenge.value,
            "description": challenge.description,
            "category": challenge.category,
            "state": challenge.state,
            "max_attempts": challenge.max_attempts,
            "type": challenge.type,
            "type_data": {
                "id": cls.id,
                "name": cls.name,
                "templates": cls.templates,
                "scripts": cls.scripts,
            },
        }
        return data


def load(app):
    app.db.create_all()
    CHALLENGE_CLASSES["timer"] = TimerChallenge
    register_plugin_assets_directory(
        app,
        base_path="/plugins/timer_challenges/assets/"
    )
