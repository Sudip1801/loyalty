import multiprocessing
import sys

import gunicorn.app.wsgiapp  # type: ignore
from dishka.integrations.flask import setup_dishka
from flask import Flask

from loyalty.bootstrap.di.container import get_container
from loyalty.presentation.web.flask_api.root import include_root

flask_app = Flask(__name__)


def main(_args: list[str]) -> None:
    include_root(flask_app)

    setup_dishka(container=get_container(), app=flask_app, auto_inject=True)
    sys.argv = [  # ugly hack
        "gunicorn",
        "-b",
        "0.0.0.0:5000",
        "-w",
        str(multiprocessing.cpu_count() * 2),
        "loyalty.bootstrap.entrypoint.flask_api:flask_app",
    ]
    gunicorn.app.wsgiapp.run()


if __name__ == "__main__":
    main(sys.argv)
