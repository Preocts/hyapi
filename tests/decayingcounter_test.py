"""Unit tests for decaying counter"""
import time

from hyapi.decayingcounter import DecayingCounter


def test_two_second_check() -> None:
    """Ensures we are decaying"""
    dcounter = DecayingCounter(2, 200)
    loop_count = 0

    while dcounter.count < 100:
        time.sleep(0.01)
        dcounter.inc()
        loop_count += 1

        assert dcounter.count == loop_count

    time.sleep(2)

    assert dcounter.count == 0


def test_max_count() -> None:
    """Hold 10 items and only 10 items"""
    dcounter = DecayingCounter(2, 10)

    for _ in range(10):
        assert dcounter.inc()

    assert not dcounter.inc()

    for _ in range(1_000):
        dcounter.inc()
    assert dcounter.count == 10
