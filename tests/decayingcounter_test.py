"""Unit tests for decaying counter"""
import time

from hyapi.decayingcounter import DecayingCounter


def test_decay_check() -> None:
    """Ensures we are decaying"""
    dcounter = DecayingCounter(10, 3)

    for _ in range(5):
        dcounter.inc()
        time.sleep(0.5)

    assert dcounter.count
    tailing = dcounter._events[-1]

    while dcounter.count:
        assert dcounter._events[-1] == tailing

    assert dcounter.count == 0


def test_max_count() -> None:
    """Hold 10 items and only 10 items"""
    dcounter = DecayingCounter(10, 2)

    for _ in range(10):
        assert dcounter.inc()

    assert not dcounter.inc()

    for _ in range(1_000):
        dcounter.inc()
    assert dcounter.count == 10
