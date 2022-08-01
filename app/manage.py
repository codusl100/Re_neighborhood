import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from __init__ import create_app
from app import db
from models import Fcuser

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
	app.run()

@manager.command
def test():
	"""Runs the unit tests."""
	tests = unittest.TestLoader().discover('/', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		return 0
	return 1

if __name__ == '__main__':
	manager.run()