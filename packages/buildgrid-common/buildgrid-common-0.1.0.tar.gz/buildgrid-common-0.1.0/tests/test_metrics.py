import logging

from buildgrid.common.metrics.log_metric_publisher import LogMetricPublisher


def test_common_metrics(caplog):
    caplog.set_level(logging.INFO)
    publisher = LogMetricPublisher("dev")

    with publisher.common_metrics("test_metric"):
        pass

    assert len(caplog.record_tuples) == 2
    tuples = caplog.record_tuples
    assert tuples[0] == ("buildgrid.common.metrics.log_metric_publisher", logging.INFO, "dev.test_metric=1")
    assert tuples[1][2].endswith("ms")


def test_common_metrics_error(caplog):
    caplog.set_level(logging.INFO)
    publisher = LogMetricPublisher("dev")

    try:
        with publisher.common_metrics("test_metric"):
            raise RuntimeError()
    except Exception:
        pass

    assert len(caplog.record_tuples) == 3
    tuples = caplog.record_tuples
    assert tuples[0] == ("buildgrid.common.metrics.log_metric_publisher", logging.INFO, "dev.test_metric=1")
    assert tuples[2] == ("buildgrid.common.metrics.log_metric_publisher", logging.INFO, "dev.test_metric.error=1")
    assert tuples[1][2].endswith("ms")
