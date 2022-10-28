# Top level CLI group
# All other spawner commands belong to this group
import click


@click.group(help="CLI tool for spawning lightweight virtualization systems")
@click.option(
    '-i', '--instances',
    type=int,
    help='Number of instances to spawn as part of the experiment',
    required=True,
)
@click.option(
    '-n', '--name',
    type=str,
    help='Name of image to use',
    required=True,
)
@click.pass_context
def spawner(ctx, instances, name):
    ctx.ensure_object(dict)

    ctx.obj['instances'] = instances
    ctx.obj['name'] = name
