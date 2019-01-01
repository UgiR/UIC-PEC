'''
Custom types in models
Import this file in migrations/script.py.mako

and edit migrations/env.py:

def run_migrations_online():

    context.configure(connection=connection,
                      ...
                      user_module_prefix='migration_types.',
                      ...
'''

import sqlalchemy_utils
