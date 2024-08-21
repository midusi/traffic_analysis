from backend import create_app
from pathlib import Path

static_folder = Path(__file__).parent.joinpath("static")

app = create_app(env="development", static_folder=static_folder)

if __name__ == '__main__':
	app.run()