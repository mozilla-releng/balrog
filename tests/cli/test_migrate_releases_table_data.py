from copy import deepcopy
from traceback import print_exception

import pytest
from click.testing import CliRunner
from sqlalchemy import select

from auslib.blobs.base import createBlob
from auslib.cli.migrate_releases_table_data import cmd
from auslib.global_state import dbo


@pytest.fixture(scope="function")
def no_conflict_database(tmp_path, db_schema, insert_release, firefox_56_0_build1, firefox_64_0_build1, cdm_16, cdm_17):
    dburi = f"sqlite:///{tmp_path}/test.db"
    dbo.setDb(dburi)
    db_schema.create_all(dbo.engine)
    dbo.releases.t.insert().execute(
        name="Firefox-56.0-build1", product="Firefox", data_version=1, read_only=False, data=createBlob(firefox_56_0_build1),
    )
    insert_release(firefox_64_0_build1, "Firefox", history=False)
    dbo.releases.t.insert().execute(
        name="CDM-16", product="CDM", data_version=1, read_only=True, data=createBlob(cdm_16),
    )
    insert_release(cdm_17, "CDM", history=False)

    yield dburi


@pytest.fixture(scope="function")
def conflict_database(tmp_path, db_schema, insert_release, firefox_56_0_build1, firefox_64_0_build1, cdm_16, cdm_17):
    dburi = f"sqlite:///{tmp_path}/test.db"
    dbo.setDb(dburi)
    db_schema.create_all(dbo.engine)
    dbo.releases.t.insert().execute(
        name="Firefox-56.0-build1", product="Firefox", data_version=1, read_only=False, data=createBlob(firefox_56_0_build1),
    )
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["hashFunction"] = "sha1024"
    insert_release(firefox_56_0_build1, "Firefox", history=False)
    insert_release(firefox_64_0_build1, "Firefox", history=False)
    dbo.releases.t.insert().execute(
        name="CDM-16", product="CDM", data_version=1, read_only=True, data=createBlob(cdm_16),
    )
    cdm_16 = deepcopy(cdm_16)
    cdm_16["hashFunction"] = "sha1024"
    insert_release(cdm_16, "CDM", history=False)
    insert_release(cdm_17, "CDM", history=False)

    yield dburi


def test_migrate_no_conflict_dryrun(no_conflict_database):
    runner = CliRunner()
    ret = runner.invoke(cmd, [no_conflict_database])
    assert ret.exit_code == 0
    assert "Would migrate Firefox-56.0-build1" in ret.output
    assert "Would migrate CDM-16" in ret.output

    with dbo.begin() as trans:
        names = set([r["name"] for r in trans.execute(select([dbo.releases_json.name])).fetchall()])
        assert names == set(["Firefox-64.0-build1", "CDM-17"])
        names = set([r["name"] for r in trans.execute(select([dbo.release_assets.name])).fetchall()])
        assert names == set(["Firefox-64.0-build1"])


def test_migrate_no_conflict_migrate(no_conflict_database):
    runner = CliRunner()
    ret = runner.invoke(cmd, ["--migrate", no_conflict_database])
    if ret.exit_code != 0:
        print_exception(*ret.exc_info)
        assert False
    assert "Migrating Firefox-56.0-build1…" in ret.output
    assert "Migrating CDM-16…" in ret.output

    with dbo.begin() as trans:
        names = set([r["name"] for r in trans.execute(select([dbo.releases_json.name])).fetchall()])
        assert names == set(["Firefox-56.0-build1", "Firefox-64.0-build1", "CDM-16", "CDM-17"])
        names = set([r["name"] for r in trans.execute(select([dbo.release_assets.name])).fetchall()])
        assert names == set(["Firefox-56.0-build1", "Firefox-64.0-build1"])


def test_migrate_conflict_dryrun(conflict_database):
    runner = CliRunner()
    ret = runner.invoke(cmd, [conflict_database])
    assert ret.exit_code == 1
    assert "Not migrating because of conflicts" in ret.output
    assert "Conflict: Firefox-56.0-build1 is in releases and releases_json" in ret.output
    assert "Conflict: CDM-16 is in releases and releases_json" in ret.output

    with dbo.begin() as trans:
        names = set([r["name"] for r in trans.execute(select([dbo.releases_json.name])).fetchall()])
        assert names == set(["Firefox-56.0-build1", "Firefox-64.0-build1", "CDM-16", "CDM-17"])
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "Firefox-56.0-build1")).fetchone()["data"]
        assert release["hashFunction"] == "sha1024"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-56.0-build1")).fetchall()) == 19
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "CDM-16")).fetchone()["data"]
        assert release["hashFunction"] == "sha1024"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "CDM-16")).fetchall()) == 0


def test_migrate_conflict_dryrun_overwrite(conflict_database):
    runner = CliRunner()
    ret = runner.invoke(cmd, ["--overwrite", conflict_database])
    assert ret.exit_code == 0
    assert "Conflict: Firefox-56.0-build1 is in releases and releases_json" in ret.output
    assert "Conflict: CDM-16 is in releases and releases_json" in ret.output
    assert "Ignoring conflicts because overwrite is True" in ret.output
    assert "Would migrate Firefox-56.0-build1" in ret.output
    assert "Would migrate CDM-16" in ret.output

    with dbo.begin() as trans:
        names = set([r["name"] for r in trans.execute(select([dbo.releases_json.name])).fetchall()])
        assert names == set(["Firefox-56.0-build1", "Firefox-64.0-build1", "CDM-16", "CDM-17"])
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "Firefox-56.0-build1")).fetchone()["data"]
        assert release["hashFunction"] == "sha1024"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-56.0-build1")).fetchall()) == 19
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "CDM-16")).fetchone()["data"]
        assert release["hashFunction"] == "sha1024"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "CDM-16")).fetchall()) == 0


def test_migrate_conflict_migrate_abort(conflict_database):
    runner = CliRunner()
    ret = runner.invoke(cmd, ["--migrate", conflict_database])
    assert ret.exit_code == 1
    assert "Conflict: Firefox-56.0-build1 is in releases and releases_json" in ret.output
    assert "Conflict: CDM-16 is in releases and releases_json" in ret.output
    assert "Not migrating because of conflicts" in ret.output

    with dbo.begin() as trans:
        names = set([r["name"] for r in trans.execute(select([dbo.releases_json.name])).fetchall()])
        assert names == set(["Firefox-56.0-build1", "Firefox-64.0-build1", "CDM-16", "CDM-17"])
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "Firefox-56.0-build1")).fetchone()["data"]
        assert release["hashFunction"] == "sha1024"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-56.0-build1")).fetchall()) == 19
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "CDM-16")).fetchone()["data"]
        assert release["hashFunction"] == "sha1024"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "CDM-16")).fetchall()) == 0


def test_migrate_conflict_migrate_overwrite(conflict_database):
    runner = CliRunner()
    ret = runner.invoke(cmd, ["--migrate", "--overwrite", conflict_database])
    assert ret.exit_code == 0, ret.output
    assert "Conflict: Firefox-56.0-build1 is in releases and releases_json" in ret.output
    assert "Conflict: CDM-16 is in releases and releases_json" in ret.output
    assert "Ignoring conflicts because overwrite is True" in ret.output
    assert "Migrating Firefox-56.0-build1…" in ret.output
    assert "Migrating CDM-16…" in ret.output

    with dbo.begin() as trans:
        names = set([r["name"] for r in trans.execute(select([dbo.releases_json.name])).fetchall()])
        assert names == set(["Firefox-56.0-build1", "Firefox-64.0-build1", "CDM-16", "CDM-17"])
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "Firefox-56.0-build1")).fetchone()["data"]
        assert release["hashFunction"] == "sha512"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-56.0-build1")).fetchall()) == 19
        release = trans.execute(select([dbo.releases_json.data]).where(dbo.releases_json.name == "CDM-16")).fetchone()["data"]
        assert release["hashFunction"] == "sha512"
        assert len(trans.execute(dbo.release_assets.t.select().where(dbo.release_assets.name == "CDM-16")).fetchall()) == 0
