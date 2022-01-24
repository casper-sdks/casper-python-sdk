import pycspr
from pycspr import serialisation1


def test_that_standard_payment_serialises_to_and_from_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        encoded = serialisation1.to_bytes(entity)
        assert encoded == vector["bytes"]["payment"]
        _, decoded = serialisation1.from_bytes(encoded, type(entity))
        assert entity == decoded


def test_that_standard_payment_serialises_to_and_from_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        encoded = serialisation1.to_json(entity)
        decoded = serialisation1.from_json(encoded, type(entity))
        assert entity == decoded


def test_that_transfer_session_serialises_to_and_from_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        encoded = serialisation1.to_bytes(entity)
        assert encoded == vector["bytes"]["session"]
        _, decoded = serialisation1.from_bytes(encoded, type(entity))
        assert entity == decoded


def test_that_transfer_session_serialises_to_and_from_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        encoded = serialisation1.to_json(entity)
        decoded = serialisation1.from_json(encoded, type(entity))
        assert entity == decoded
