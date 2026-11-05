import sqlite3

import click
from flask import current_app, g


def get_db():
    """Open a SQLite connection for the current request/application context."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(error=None):
    """Close the database connection at the end of the application context."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create all tables defined in schema.sql."""
    db = get_db()
    with current_app.open_resource("schema.sql") as schema_file:
        db.executescript(schema_file.read().decode("utf-8"))
    db.commit()


@click.command("init-db")
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database handlers and CLI commands on the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
