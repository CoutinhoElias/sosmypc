# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 22:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160315_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qualificacaoprofissoespessoa',
            old_name='profissaopessoa',
            new_name='profissao',
        ),
        migrations.AlterUniqueTogether(
            name='qualificacaoprofissoespessoa',
            unique_together=set([('profissao', 'qualificacao')]),
        ),
    ]
