# services/users/manage.py

import unittest
import coverage


from flask.cli import FlaskGroup
from project import create_app, db

from project.api.models import User

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app = create_app) 

@cli.command('seed_db')
def seed_db():
    """Sembrando en la base de datos"""
    db.session.add(User(username='jorge', email='jorgepaz@upeu.edu.pe'))
    db.session.add(User(username='missael', email='pazmissael@gmail.com'))
    db.session.commit()

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Ejecutar los tests sin covertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de cobertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)




if __name__ == '__main__':
    cli()
