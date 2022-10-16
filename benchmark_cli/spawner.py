import click

from docker_spawner import docker_spawner
from unikraft_spawner import unikraft_spawner
from top_level_spawner import spawner

# Docker spawner command
@spawner.command()
@click.option(
    '--clean_flag',
    is_flag=True,
    help='Flag to specify whether to skip cleaning containers after experiment',
)
@click.pass_context
def docker(ctx, clean_flag):
    docker_spawner(
        instances=ctx.obj['instances'],
        name=ctx.obj['name'],
        clean_flag=clean_flag,
    )

# Unikraft spawner command
@spawner.command()
@click.pass_context
def unikraft(ctx):
	unikraft_spawner(
		instances=ctx.obj['instances'],
		name=ctx.obj['name'],
	)

if __name__ == '__main__':
	spawner(obj={})