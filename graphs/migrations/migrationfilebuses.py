# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlparse
from django.db import models, migrations


def load_stores_from_sql():
    from mysite.settings import BASE_DIR
    import os
    # print os.path.join(BASE_DIR,'graph/sql/vertices.sql')
    sql_statements = open(os.path.join(BASE_DIR,'graphs/sql/bus.sql'), 'r').read()
    return sql_statements

class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(load_stores_from_sql()),
    ]