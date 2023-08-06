import click
from click.core import Context as ClickContext
import os


@click.command(hidden=True)
@click.pass_context
def env(ctx: ClickContext):
    """Prints the environment variables which can be used to configure Gable"""
    env_vars = ["GABLE_API_ENDPOINT", "GABLE_API_KEY"]
    for env_var in env_vars:
        click.echo(f"{env_var}={os.environ.get(env_var, '<Not Set>')}")
    click.echo(
        "Note: these can be overridden by passing command line arguments to gable."
    )
