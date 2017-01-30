# coding: utf-8
import click
from stock import models, query
from .main import cli, AliasedGroup


@cli.group(cls=AliasedGroup)
def db():
    pass


@db.command(help="Show env")
def env():
    models.create_all()
    tables = ", ".join(models.engine.table_names())
    summary = """\
url: {engine.url}
echo: {engine.echo}
name: {engine.name}
tables: {tables}
""".format(engine=models.engine, tables=tables)
    click.echo(summary)


@db.command(help="Create new all tables")
def create():
    models.create_all()


@db.command(help="Drop all tables")
@click.option("-y", "--yes", is_flag=True, default=False)
def drop(yes):
    if yes or click.confirm("Drop all tables. Are you sure?"):
        models.drop_all()


@db.command(name="dummy")
def dummy():
    session = models.Session()
    import datetime
    today = datetime.date.today()
    for i in range(100):
        n = today + datetime.timedelta(days=i)
        session.add(models.Price(date=n, close=i, quandl_code="test"))
    for i in range(100):
        c = i * (1 if i % 2 == 0 else -1)
        n = today + datetime.timedelta(days=i)
        session.add(models.Price(date=n, close=c, quandl_code="test2"))
    session.commit()


@db.command(name="quandl_codes", help="Store and show quandl code")
def quandl_codes():
    click.secho(", ".join(c for c in query.quandl_codes()))
