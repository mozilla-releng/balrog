import os
import sys

import click
from sqlalchemy import select

from ..global_state import dbo
from ..services import releases


@click.command()
@click.option("--migrate", is_flag=True, default=False, help="When passed, data will actually be migrated.")
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite releases_json releases with releases version. If not passed and a release exists in both tables, this command will fail.",
)
@click.argument("dburi", default=os.environ.get("DBURI"))
def cmd(dburi, migrate, overwrite):
    dbo.setDb(dburi)

    with dbo.begin() as trans:
        releases_names = set([r["name"] for r in trans.execute(select([dbo.releases.name])).fetchall()])
        releases_json_names = set([r["name"] for r in trans.execute(select([dbo.releases_json.name])).fetchall()])
        in_both = releases_names & releases_json_names

        if in_both:
            for r in in_both:
                click.echo(f"Conflict: {r} is in releases and releases_json")

            if not overwrite:
                click.echo("Not migrating because of conflicts, and overwrite is False")
                sys.exit(1)

            click.echo("Ignoring conflicts because overwrite is True")

        for r in sorted(releases_names):
            if not migrate:
                click.echo(f"Would migrate {r}")
                continue

            click.echo(f"Migrating {r}…")
            release = trans.execute(dbo.releases.t.select().where(dbo.releases.name == r)).fetchone()
            base, assets = releases.split_release(release["data"], release["data"]["schema_version"])
            if r in in_both:
                trans.execute(
                    dbo.releases_json.t.update(
                        values=dict(
                            name=release["name"],
                            product=release["product"],
                            read_only=release["read_only"],
                            data_version=release["data_version"],
                            data=release["data"],
                        )
                    ).where(dbo.releases_json.name == release["name"])
                )
            else:
                trans.execute(
                    dbo.releases_json.t.insert(
                        values=dict(
                            name=release["name"],
                            product=release["product"],
                            read_only=release["read_only"],
                            data_version=release["data_version"],
                            data=release["data"],
                        )
                    )
                )

            for path, item in assets:
                path = "." + ".".join(path)
                if r in in_both:
                    trans.execute(
                        dbo.release_assets.t.update(values=dict(name=release["name"], path=path, data_version=release["data_version"], data=item,))
                        .where(dbo.release_assets.name == release["name"])
                        .where(dbo.release_assets.path == path)
                    )
                else:
                    trans.execute(dbo.release_assets.t.insert(values=dict(name=release["name"], path=path, data_version=release["data_version"], data=item,)))
