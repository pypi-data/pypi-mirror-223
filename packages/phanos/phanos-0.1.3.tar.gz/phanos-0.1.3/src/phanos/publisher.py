""" """
from __future__ import annotations

import inspect
import logging
import sys
import threading
import typing
from abc import abstractmethod

from . import (
    log,
    types,
    messaging,
)
from .metrics import MetricWrapper, TimeProfiler, ResponseSize
from .tree import MethodTreeNode

TIME_PROFILER = "time_profiler"
RESPONSE_SIZE = "response_size"


class OutputFormatter:
    """class for converting Record type into profiling string"""

    @staticmethod
    def record_to_str(name: str, record: types.Record) -> str:
        """converts Record type into profiling string

        :param name: name of profiler
        :param record: metric record which to convert
        """
        value = record["value"][1]
        if not record.get("labels"):
            return f"profiler: {name}, " f"method: {record.get('method')}, " f"value: {value} {record.get('units')}"
        # format labels as this "key=value, key2=value2"
        labels = ", ".join(f"{k}={v}" for k, v in record["labels"].items())
        return (
            f"profiler: {name}, "
            f"method: {record.get('method')}, "
            f"value: {value} {record.get('units')}, "
            f"labels: {labels}"
        )


class BaseHandler:
    """base class for record handling"""

    handler_name: str

    def __init__(self, handler_name: str) -> None:
        """
        :param handler_name: name of handler. used for managing handlers"""
        self.handler_name = handler_name

    @abstractmethod
    def handle(
        self,
        records: typing.List[types.Record],
        profiler_name: str = "profiler",
    ) -> None:
        """
        method for handling records

        :param profiler_name: name of profiler
        :param records: list of records to handle
        """
        raise NotImplementedError


class ImpProfHandler(BaseHandler):
    """RabbitMQ record handler"""

    publisher: messaging.BlockingPublisher
    logger: typing.Optional[log.LoggerLike]

    def __init__(
        self,
        handler_name: str,
        host: str = "127.0.0.1",
        port: int = 5672,
        user: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        heartbeat: int = 47,
        timeout: float = 23,
        retry_delay: float = 0.137,
        retry: int = 3,
        exchange_name: str = "profiling",
        exchange_type: str = "fanout",
        logger: typing.Optional[log.LoggerLike] = None,
        **kwargs,
    ) -> None:
        """Creates `messaging.BlockingPublisher` instance (connection not established yet),
         sets logger and create time profiler and response size profiler

        :param handler_name: name of handler. used for managing handlers
        :param host: rabbitMQ server host
        :param port: rabbitMQ server port
        :param user: rabbitMQ login username
        :param password: rabbitMQ user password
        :param exchange_name: exchange name to bind queue with
        :param exchange_type: exchange type to bind queue with
        :param logger: loging object to use
        :param retry: how many times to retry publish event
        :param int|float retry_delay: Time to wait in seconds, before the next
        :param timeout: If not None,
            the value is a non-negative timeout, in seconds, for the
            connection to remain blocked (triggered by Connection.Blocked from
            broker); if the timeout expires before connection becomes unblocked,
            the connection will be torn down, triggering the adapter-specific
            mechanism for informing client app about the closed connection (
            e.g., on_close_callback or ConnectionClosed exception) with
            `reason_code` of `InternalCloseReasons.BLOCKED_CONNECTION_TIMEOUT`.
        :param kwargs: other connection params, like `timeout goes here`
        :param logger: logger
        """
        super().__init__(handler_name)

        self.logger = logger or logging.getLogger(__name__)
        self.publisher = messaging.BlockingPublisher(
            host=host,
            port=port,
            user=user,
            password=password,
            heartbeat=heartbeat,
            timeout=timeout,
            retry_delay=retry_delay,
            retry=retry,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            logger=logger,
            **kwargs,
        )
        try:
            self.publisher.connect()
        except messaging.NETWORK_ERRORS as err:
            self.logger.error(f"ImpProfHandler cannot connect to RabbitMQ because of {err}")
            raise RuntimeError("Cannot connect to RabbitMQ") from err

        self.logger.info("ImpProfHandler created successfully")
        self.publisher.close()

    def handle(
        self,
        records: typing.List[types.Record],
        profiler_name: str = "profiler",
    ) -> None:
        """Sends list of records to rabitMq queue

        :param profiler_name: name of profiler (not used)
        :param records: list of records to publish
        """

        _ = profiler_name
        for record in records:
            _ = self.publisher.publish(record)


class LoggerHandler(BaseHandler):
    """logger handler"""

    logger: log.LoggerLike
    formatter: OutputFormatter
    level: int

    def __init__(
        self,
        handler_name: str,
        logger: typing.Optional[log.LoggerLike] = None,
        level: int = 10,
    ) -> None:
        """

        :param handler_name: name of handler. used for managing handlers
        :param logger: logger instance if none -> creates new with name PHANOS
        :param level: level of logger in which prints records. default is DEBUG
        """
        super().__init__(handler_name)
        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger("PHANOS")
            self.logger.setLevel(10)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(10)
            self.logger.addHandler(handler)
        self.level = level
        self.formatter = OutputFormatter()

    def handle(self, records: typing.List[types.Record], profiler_name: str = "profiler") -> None:
        """logs list of records

        :param profiler_name: name of profiler
        :param records: list of records
        """
        for record in records:
            self.logger.log(self.level, self.formatter.record_to_str(profiler_name, record))


class NamedLoggerHandler(BaseHandler):
    """Logger handler initialised with name of logger rather than passing object"""

    logger: log.LoggerLike
    formatter: OutputFormatter
    level: int

    def __init__(
        self,
        handler_name: str,
        logger_name: str,
        level: int = logging.DEBUG,
    ) -> None:
        """
        Initialise handler and find logger by name.

        :param handler_name: name of handler. used for managing handlers
        :param logger_name: find this logger `logging.getLogger(logger_name)`
        :param level: level of logger in which prints records. default is DEBUG
        """
        super().__init__(handler_name)
        self.logger = logging.getLogger(logger_name)
        self.level = level
        self.formatter = OutputFormatter()

    def handle(self, records: typing.List[types.Record], profiler_name: str = "profiler") -> None:
        """logs list of records

        :param profiler_name: name of profiler
        :param records: list of records
        """
        for record in records:
            self.logger.log(self.level, self.formatter.record_to_str(profiler_name, record))


class StreamHandler(BaseHandler):
    """Stream handler of Records."""

    formatter: OutputFormatter
    output: typing.TextIO
    _lock: threading.Lock

    def __init__(self, handler_name: str, output: typing.TextIO = sys.stdout) -> None:
        """

        :param handler_name: name of profiler
        :param output: stream output. Default 'sys.stdout'
        """
        super().__init__(handler_name)
        self.output = output
        self.formatter = OutputFormatter()
        self._lock = threading.Lock()

    def handle(self, records: typing.List[types.Record], profiler_name: str = "profiler") -> None:
        """logs list of records

        :param profiler_name: name of profiler
        :param records: list of records
        """
        for record in records:
            with self._lock:
                print(
                    self.formatter.record_to_str(profiler_name, record),
                    file=self.output,
                    flush=True,
                )


class PhanosProfiler(log.InstanceLoggerMixin):
    """Class responsible for sending records to IMP_prof RabbitMQ publish queue"""

    metrics: typing.Dict[str, MetricWrapper]

    _root: MethodTreeNode
    current_node: MethodTreeNode

    time_profile: typing.Optional[TimeProfiler]
    resp_size_profile: typing.Optional[ResponseSize]

    before_func: typing.Optional[typing.Callable]
    after_func: typing.Optional[typing.Callable]
    before_root_func: typing.Optional[typing.Callable]
    after_root_func: typing.Optional[typing.Callable]

    handlers: typing.Dict[str, BaseHandler]
    handle_records: bool
    job: str
    error_occurred: bool

    def __init__(self) -> None:
        """Initialize ProfilesPublisher

        Initialization just creates new instance!!

        """

        self.metrics = {}
        self.handlers = {}
        self.job = ""
        self.error_occurred = False

        self.resp_size_profile = None
        self.time_profile = None

        self.before_func = None
        self.after_func = None
        self.before_root_func = None
        self.after_root_func = None

        super().__init__(logged_name="phanos")

    def config(
        self,
        logger=None,
        job: str = "",
        time_profile: bool = True,
        request_size_profile: bool = False,
        handle_records: bool = True,
    ) -> None:
        """configure PhanosProfiler
        :param job: name of job
        :param logger: logger instance
        :param time_profile: should create instance time profiler
        :param request_size_profile: should create instance of request size profiler
        :param handle_records: should handle recorded records
        """
        self.logger = logger or logging.getLogger(__name__)
        self.job = job
        if time_profile:
            self.create_time_profiler()
        if request_size_profile:
            self.create_response_size_profiler()
        self.handle_records = handle_records

        self._root = MethodTreeNode(None, self.logger)
        self.current_node = self._root

    def dict_config(self, settings: dict[str, typing.Any]) -> None:
        """
        Configure profiler instance with dictionary config.
        Set up profiling from config file, instead fo changing code for various environments.

        Example:
            ```
            {
                "job": "my_app",
                "logger": "my_app_debug_logger",
                "time_profile": True,
                "handle_records": True,
                "handlers": {
                    "stdout_handler": {
                        "class": "phanos.publisher.StreamHandler",
                        "handler_name": "stdout_handler",
                        "output": "ext://sys.stdout",
                    }
                }
            }
            ```

        :param settings: dictionary of desired profiling set up
        """
        from . import config as phanos_config

        if "logger" in settings:
            self.logger = logging.getLogger(settings["logger"])
        else:
            self.logger = logging.getLogger(__name__)
        if "job" in settings:
            self.job = settings["job"]
        if settings.get("time_profile"):
            self.create_time_profiler()
        self.handle_records = settings.get("handle_records", True)
        if "handlers" in settings:
            named_handlers = phanos_config.create_handlers(settings["handlers"])
            for handler in named_handlers.values():
                self.add_handler(handler)

        self._root = MethodTreeNode(None, self.logger)
        self.current_node = self._root

    def create_time_profiler(self) -> None:
        """Create time profiling metric"""
        self.time_profile = TimeProfiler(TIME_PROFILER, job=self.job, logger=self.logger)
        self.add_metric(self.time_profile)
        self.debug("Phanos - time profiler created")

    def create_response_size_profiler(self) -> None:
        """create response size profiling metric"""
        self.resp_size_profile = ResponseSize(RESPONSE_SIZE, job=self.job, logger=self.logger)
        self.add_metric(self.resp_size_profile)
        self.debug("Phanos - response size profiler created")

    def delete_metric(self, item: str) -> None:
        """deletes one metric instance
        :param item: name of the metric instance
        :raises KeyError: if metric does not exist
        """
        try:
            _ = self.metrics.pop(item)
        except KeyError:
            self.error(f"{self.delete_metric.__qualname__}: metric {item} do not exist")
            raise KeyError(f"metric {item} do not exist")

        if item == "time_profiler":
            self.time_profile = None
        if item == "response_size":
            self.resp_size_profile = None
        self.debug(f"metric {item} deleted")

    def delete_metrics(self, rm_time_profile: bool = False, rm_resp_size_profile: bool = False) -> None:
        """deletes all custom metric instances

        :param rm_time_profile: should pre created time_profiler be deleted
        :param rm_resp_size_profile: should pre created response_size_profiler be deleted
        """
        names = list(self.metrics.keys())
        for name in names:
            if (name != TIME_PROFILER or rm_time_profile) and (name != RESPONSE_SIZE or rm_resp_size_profile):
                self.delete_metric(name)

    def clear(self):
        """clear all records from all metrics and clear method tree"""
        for metric in self.metrics.values():
            metric.cleanup()

        self.current_node = self._root
        self._root.clear_tree()

    def add_metric(self, metric: MetricWrapper) -> None:
        """adds new metric to profiling

        :param metric: metric instance
        """
        if self.metrics.get(metric.name, None):
            self.warning(f"Metric {metric.name} already exist. Overwriting with new metric")
        self.metrics[metric.name] = metric
        self.debug(f"Metric {metric.name} added to phanos profiler")

    def add_handler(self, handler: BaseHandler) -> None:
        """Add handler to profiler

        :param handler: handler instance
        """
        if self.handlers.get(handler.handler_name, None):
            self.warning(f"Handler {handler.handler_name} already exist. Overwriting with new handler")
        self.handlers[handler.handler_name] = handler
        self.debug(f"Handler {handler.handler_name} added to phanos profiler")

    def delete_handler(self, handler_name: str) -> None:
        """Delete handler from profiler

        :param handler_name: name of handler:
        :raises KeyError: if handler do not exist
        """
        try:
            _ = self.handlers.pop(handler_name)
        except KeyError:
            self.error(f"{self.delete_handler.__qualname__}: handler {handler_name} do not exist")
            raise KeyError(f"handler {handler_name} do not exist")
        self.debug(f"handler {handler_name} deleted")

    def delete_handlers(self) -> None:
        """delete all handlers"""
        self.handlers.clear()
        self.debug("all handlers deleted")

    def profile(self, func: typing.Callable) -> typing.Callable:
        """
        Decorator specifying which methods should be profiled.
        Default profiler is time profiler which measures execution time of decorated methods

        Usage: decorate methods which you want to be profiled

        :param func: method or function which should be profiled
        """

        def before_function_handling(args, kwargs):
            """Handlers profiling before profiled function execution (records start time)

            Saves method context into MethodTreeNode, calls _before_root_func, _before_func
            """
            if self.handlers and self.handle_records:
                if self.current_node == self._root:
                    self.error_occurred = False
                self.current_node = self.current_node.add_child(MethodTreeNode(func, self.logger))

                if self.current_node.parent == self._root:
                    self._before_root_func(func, args, kwargs)
                self._before_func(func, args, kwargs)

        def after_function_handling(result, args, kwargs):
            """Handles profiling after profiled function execution (records stop time)

            Deletes method context from MethodTreeNode, calls _after_root_func, _after_func and handle records
            if root function was executed
            """
            if self.handlers and self.handle_records:
                self._after_func(result, args, kwargs)

                if self.current_node.parent == self._root:
                    self._after_root_func(result, args, kwargs)
                    self.handle_records_clear()
                if self.current_node.parent and not self.error_occurred:
                    self.current_node = self.current_node.parent
                    self.current_node.delete_child()
                elif not self.error_occurred:
                    self.error(f"{self.profile.__qualname__}: node {self.current_node.context!r} have no parent.")
                    raise ValueError(f"{self.current_node.context!r} have no parent")

        async def async_inner(*args, **kwargs) -> typing.Any:
            """async decorator version"""
            before_function_handling(args, kwargs)
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                # in case of exception handle measured records, cleanup and reraise
                self.force_handle_records_clear()
                self.error_occurred = True
                raise e
            after_function_handling(result, args, kwargs)
            return result

        def sync_inner(*args, **kwargs) -> typing.Any:
            """sync decorator version"""
            before_function_handling(args, kwargs)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                # in case of exception handle measured records, cleanup and reraise
                self.force_handle_records_clear()
                self.error_occurred = True
                raise e
            after_function_handling(result, args, kwargs)
            return result

        if inspect.iscoroutinefunction(func):
            return async_inner
        return sync_inner

    def _before_root_func(self, func, args, kwargs) -> None:
        """method executing before root function

        :param func: root function
        """
        # users custom metrics operation recording
        if callable(self.before_root_func):
            self.before_root_func(func, args, kwargs)
        # place for phanos metrics if needed

    def _after_root_func(self, fn_result: typing.Any, args, kwargs) -> None:
        """method executing after the root function


        :param fn_result: result of function
        """
        # phanos metrics
        if self.resp_size_profile:
            self.resp_size_profile.store_operation(
                method=self.current_node.context, operation="rec", value=fn_result, label_values={}
            )
        # users custom metrics operation recording
        if callable(self.after_root_func):
            self.after_root_func(fn_result, args, kwargs)

    def _before_func(self, func, args, kwargs) -> None:
        # users custom metrics operation recording
        if callable(self.before_func):
            self.before_func(func, args, kwargs)
        # phanos metrics
        if self.time_profile:
            self.time_profile.start()

    def _after_func(self, fn_result, args, kwargs) -> None:
        # phanos metrics
        if self.time_profile and not self.error_occurred:
            self.time_profile.store_operation(method=self.current_node.context, operation="stop", label_values={})
        # users custom metrics operation recording
        if callable(self.after_func):
            self.after_func(fn_result, args, kwargs)

    def handle_records_clear(self) -> None:
        """Pass records to each registered Handler and clear stored records
        method DO NOT clear MethodContext tree
        """
        # send records and log em
        for metric in self.metrics.values():
            records = metric.to_records()
            for handler in self.handlers.values():
                self.debug(f"handler %s handling metric %s", handler.handler_name, metric.name)
                handler.handle(records, metric.name)
            metric.cleanup()

    def force_handle_records_clear(self) -> None:
        """Method to force records handling

        forces record handling. As side effect clears all metrics and clears MethodContext tree
        """
        # send records and log em
        self.debug("Forcing record handling")
        self.handle_records_clear()
        self.current_node = self._root
        self._root.clear_tree()
