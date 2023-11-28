import json
import logging
from io import StringIO

from auslib.log import configure_logging


def test_logger(caplog):
    stream = StringIO()
    configure_logging(stream=stream)

    logging.info("TEST OUTPUT")

    assert len(caplog.records) == 1
    r = caplog.records[0]
    assert r.levelno == 20
    assert r.message == "TEST OUTPUT"

    o = json.loads(stream.getvalue())
    assert o["Severity"] == 200
    assert o["Fields"]["message"] == "TEST OUTPUT"


def test_exception(caplog):
    stream = StringIO()
    configure_logging(stream=stream)

    try:
        raise ValueError("Oh noes!")
    except ValueError as e:
        logging.error("TEST OUTPUT", exc_info=e)

    assert len(caplog.records) == 1
    r = caplog.records[0]
    assert r.levelno == 40
    assert r.message == "TEST OUTPUT"
    assert r.exc_info

    o = json.loads(stream.getvalue())
    assert o["Severity"] == 500
    assert o["Fields"]["message"] == "TEST OUTPUT"
    assert o["Fields"]["error"].startswith("ValueError")


def test_extra(caplog):
    configure_logging()

    # We need to explicitly create a new logger here so that the BalrogLogger is instantiated
    logger = logging.getLogger("{}.{}".format(__name__, "test_extra"))

    logger.info("TEST OUTPUT", extra={"foo": "bar"})

    assert len(caplog.records) == 1
    r = caplog.records[0]
    assert r.message == "TEST OUTPUT"
    assert r.foo == "bar"
    assert r.requestid == "None"


def test_noextra(caplog):
    configure_logging()

    # We need to explicitly create a new logger here so that the BalrogLogger is instantiated
    logger = logging.getLogger("{}.{}".format(__name__, "test_onextra"))

    logger.info("TEST OUTPUT")

    assert len(caplog.records) == 1
    r = caplog.records[0]
    assert r.message == "TEST OUTPUT"
    assert r.requestid == "None"


def test_json_output(caplog):
    stream = StringIO()
    configure_logging(stream=stream)

    logging.info('{"foo": "bar"}')

    assert len(caplog.records) == 1
    r = caplog.records[0]

    assert r.levelno == 20
    assert r.message == '{"foo": "bar"}'

    o = json.loads(stream.getvalue())
    assert "message" not in o["Fields"]


def test_no_message(caplog):
    stream = StringIO()
    configure_logging(stream=stream)

    logging.info("")

    assert len(caplog.records) == 1
    r = caplog.records[0]

    assert r.levelno == 20

    o = json.loads(stream.getvalue())
    assert "message" not in o["Fields"]


def test_not_serializable(caplog):
    stream = StringIO()
    configure_logging(stream=stream)

    logging.info("", extra={"type": bytes, "data": b""})

    assert len(caplog.records) == 1
    r = caplog.records[0]

    assert r.levelno == 20

    o = json.loads(stream.getvalue())
    assert set(o["Fields"]) == {"type", "data"}
