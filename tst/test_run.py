import click

from run import run


def test_run():
    ctx = click.Context(run)
    assert run.list_commands(ctx) == ["api", "webapp"]

    # TODO(PC): run both servers to check they are viable and stop them afterwards
