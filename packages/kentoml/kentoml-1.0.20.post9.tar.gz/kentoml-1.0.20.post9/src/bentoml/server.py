from __future__ import annotations

import sys
import typing as t
import logging
import textwrap
import subprocess
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from simple_di import inject
from simple_di import Provide

from .exceptions import BentoMLException
from ._internal.tag import Tag
from ._internal.bento import Bento
from ._internal.service import Service
from ._internal.configuration.containers import BentoMLContainer

if TYPE_CHECKING:
    from types import TracebackType

    from ._internal.client import Client
    from ._internal.client import GrpcClient
    from ._internal.client import HTTPClient

    _FILE: t.TypeAlias = None | int | t.IO[t.Any]


logger = logging.getLogger(__name__)

__all__ = ["Server", "GrpcServer", "HTTPServer"]


class Server(ABC):
    servable: str | Bento | Tag | Service
    host: str
    port: int

    args: list[str]

    process: subprocess.Popen[bytes] | None = None
    timeout: float = 10
    _client: Client | None = None

    def __init__(
        self,
        servable: str | Bento | Tag | Service,
        serve_cmd: str,
        reload: bool,
        production: bool,
        env: t.Literal["conda"] | None,
        host: str,
        port: int,
        working_dir: str | None,
        api_workers: int | None,
        backlog: int,
        bento: str | Bento | Tag | Service | None = None,
    ):
        if bento is not None:
            if not servable:
                logger.warning(
                    "'bento' is deprecated, either remove it as a kwargs or pass '%s' as the first positional argument",
                    bento,
                )
                servable = bento
            else:
                raise BentoMLException(
                    "Cannot use both 'bento' and 'servable' as kwargs as 'bento' is deprecated."
                )

        self.servable = servable
        # backward compatibility
        self.bento = servable

        working_dir = None
        if isinstance(servable, Bento):
            bento_str = str(servable.tag)
        elif isinstance(servable, Tag):
            bento_str = str(servable)
        elif isinstance(servable, Service):
            if not servable.is_service_importable():
                raise BentoMLException(
                    "Cannot use 'bentoml.Service' as a server if it is defined in interactive session or Jupyter Notebooks."
                )
            bento_str, working_dir = servable.get_service_import_origin()
        else:
            bento_str = servable

        args: list[str] = [
            sys.executable,
            "-m",
            "bentoml",
            serve_cmd,
            bento_str,
            "--host",
            host,
            "--port",
            str(port),
            "--backlog",
            str(backlog),
        ]

        if working_dir:
            args.extend(["--working-dir", working_dir])
        if not production:
            args.append("--development")
        if reload:
            args.append("--reload")
        if env:
            args.extend(["--env", env])

        if api_workers is not None:
            args.extend(["--api-workers", str(api_workers)])
        if working_dir is not None:
            args.extend(["--working-dir", str(working_dir)])

        self.args = args
        self.host = "127.0.0.1" if host == "0.0.0.0" else host
        self.port = port

    def start(
        self,
        blocking: bool = False,
        env: dict[str, str] | None = None,
        stdin: _FILE = None,
        stdout: _FILE = None,
        stderr: _FILE = None,
        text: bool | None = None,
    ):
        """Start the server programmatically.

        To get the client, use the context manager.

        .. note::
           ``blocking=True`` and using ``start()`` as a context manager is mutually exclusive.

        Args:
            blocking: If True, the server will block until it is stopped.
            env: A dictionary of environment variables to pass to the server. Default to ``None``.
            stdin: The stdin to pass to the server. Default to ``None``.
            stdout: The stdout to pass to the server. Default to ``None``.
            stderr: The stderr to pass to the server. Default to ``None``.
            text: Whether to output as text or bytes for stdout and stderr. Default to ``None``.
        """

        class _Manager:
            def __init__(__inner_self):
                logger.debug(f"Starting server with arguments: {self.args}")
                default_io_descriptor = None if blocking else subprocess.PIPE
                if text is None:
                    logger.warning(
                        "Setting text to True will be the default behaviour for bentoml 2.x. Please set it explicitly to avoid breaking changes.\n"
                        + '    Example: "server.start(text=False, ...)"',
                    )
                self.process = subprocess.Popen(
                    self.args,
                    stdout=stdout if stdout is not None else default_io_descriptor,
                    stderr=stderr if stderr is not None else default_io_descriptor,
                    stdin=stdin if stdin is not None else default_io_descriptor,
                    env=env,
                    # TODO: Make this default to True in 2.x
                    text=text if text is not None else False,
                )

                if blocking:
                    try:
                        self.process.wait()
                    except KeyboardInterrupt:
                        pass

            def __enter__(__inner_self):
                return self.get_client()

            def __exit__(
                __inner_self,
                exc_type: type[BaseException] | None,
                exc_value: BaseException | None,
                traceback: TracebackType | None,
            ):
                self.stop()

        return _Manager()

    @abstractmethod
    def get_client(self) -> Client | None:
        pass

    def stop(self) -> None:
        if self.process is None:
            logger.warning("Attempted to stop a BentoML server that was not running!")
            return
        assert self.process is not None
        out_code = self.process.poll()
        if out_code == 0:
            logger.warning(
                "Attempted to stop a BentoML server that has already exited!"
            )
        elif out_code is not None:
            logs = "Attempted to stop a BentoML server that has already exited with an error!\nServer Output:\n"
            if self.process.stdout is not None and not self.process.stdout.closed:
                s = self.process.stdout.read()
                logs += textwrap.indent(
                    s.decode("utf-8") if isinstance(s, bytes) else s, " " * 4
                )
            if self.process.stderr is not None and not self.process.stderr.closed:
                logs += "\nServer Error:\n"
                s = self.process.stderr.read()
                logs += textwrap.indent(
                    s.decode("utf-8") if isinstance(s, bytes) else s, " " * 4
                )
            logger.warning(logs)

        self.process.terminate()
        # NOTE: Need to call communicate to avoid zombie processes
        self.process.communicate()

    def __enter__(self):
        logger.warning(
            "Using bentoml.Server as a context manager is deprecated, use bentoml.Server.start instead."
        )

        return self

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback_type: TracebackType,
    ):
        try:
            self.stop()
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error stopping server: {e}", exc_info=e)


class HTTPServer(Server):
    _client: HTTPClient | None = None

    @inject
    def __init__(
        self,
        bento: str | Bento | Tag | Service,
        reload: bool = False,
        production: bool = True,
        env: t.Literal["conda"] | None = None,
        host: str = Provide[BentoMLContainer.http.host],
        port: int = Provide[BentoMLContainer.http.port],
        working_dir: str | None = None,
        api_workers: int | None = Provide[BentoMLContainer.api_server_workers],
        backlog: int = Provide[BentoMLContainer.api_server_config.backlog],
        ssl_certfile: str | None = Provide[BentoMLContainer.ssl.certfile],
        ssl_keyfile: str | None = Provide[BentoMLContainer.ssl.keyfile],
        ssl_keyfile_password: str
        | None = Provide[BentoMLContainer.ssl.keyfile_password],
        ssl_version: int | None = Provide[BentoMLContainer.ssl.version],
        ssl_cert_reqs: int | None = Provide[BentoMLContainer.ssl.cert_reqs],
        ssl_ca_certs: str | None = Provide[BentoMLContainer.ssl.ca_certs],
        ssl_ciphers: str | None = Provide[BentoMLContainer.ssl.ciphers],
    ):
        # hacky workaround to prevent bentoml.serve being overwritten immediately
        from .serve import construct_ssl_args

        super().__init__(
            bento,
            "serve-http",
            reload,
            production,
            env,
            host,
            port,
            working_dir,
            api_workers,
            backlog,
        )

        ssl_args: dict[str, t.Any] = {
            "ssl_certfile": ssl_certfile,
            "ssl_keyfile": ssl_keyfile,
            "ssl_ca_certs": ssl_ca_certs,
        }
        ssl_args.update(
            ssl_keyfile_password=ssl_keyfile_password,
            ssl_version=ssl_version,
            ssl_cert_reqs=ssl_cert_reqs,
            ssl_ciphers=ssl_ciphers,
        )

        self.args.extend(construct_ssl_args(**ssl_args))

        if api_workers is not None:
            self.args.extend(["--api-workers", str(api_workers)])
        if working_dir is not None:
            self.args.extend(["--working-dir", str(working_dir)])

    def client(self) -> HTTPClient | None:
        logger.warning(
            "'Server.client()' is deprecated, use 'Server.get_client()' instead."
        )
        return self.get_client()

    def get_client(self) -> HTTPClient | None:
        if self.process is None:
            logger.warning(
                "Attempted to get a client for a BentoML server that was not running! Try running 'bentoml.*Server.start()' first."
            )
            return
        assert self.process is not None
        out_code = self.process.poll()
        if out_code == 0:
            logger.warning(
                "Attempted to get a client from a BentoML server that has already exited! You can run '.start()' again to restart it."
            )
            return
        elif out_code is not None:
            logs = "Attempted to get a client from a BentoML server that has already exited with an error!\nServer Output:\n"
            if self.process.stdout is not None and not self.process.stdout.closed:
                s = self.process.stdout.read()
                logs += textwrap.indent(
                    s.decode("utf-8") if isinstance(s, bytes) else s, " " * 4
                )
            if self.process.stderr is not None and not self.process.stderr.closed:
                logs += "\nServer Error:\n"
                s = self.process.stderr.read()
                logs += textwrap.indent(
                    s.decode("utf-8") if isinstance(s, bytes) else s, " " * 4
                )
            logger.warning(logs)
            return

        if self._client is None:
            from .client import HTTPClient

            HTTPClient.wait_until_server_ready(
                host=self.host, port=self.port, timeout=self.timeout
            )
            self._client = HTTPClient.from_url(f"http://{self.host}:{self.port}")
        return self._client


class GrpcServer(Server):
    _client: GrpcClient | None = None

    @inject
    def __init__(
        self,
        bento: str | Bento | Tag | Service,
        reload: bool = False,
        production: bool = True,
        env: t.Literal["conda"] | None = None,
        host: str = Provide[BentoMLContainer.grpc.host],
        port: int = Provide[BentoMLContainer.grpc.port],
        working_dir: str | None = None,
        api_workers: int | None = Provide[BentoMLContainer.api_server_workers],
        backlog: int = Provide[BentoMLContainer.api_server_config.backlog],
        enable_reflection: bool = Provide[BentoMLContainer.grpc.reflection.enabled],
        enable_channelz: bool = Provide[BentoMLContainer.grpc.channelz.enabled],
        max_concurrent_streams: int
        | None = Provide[BentoMLContainer.grpc.max_concurrent_streams],
        ssl_certfile: str | None = Provide[BentoMLContainer.ssl.certfile],
        ssl_keyfile: str | None = Provide[BentoMLContainer.ssl.keyfile],
        ssl_ca_certs: str | None = Provide[BentoMLContainer.ssl.ca_certs],
        grpc_protocol_version: str | None = None,
    ):
        from .serve import construct_ssl_args

        super().__init__(
            bento,
            "serve-grpc",
            reload,
            production,
            env,
            host,
            port,
            working_dir,
            api_workers,
            backlog,
        )

        ssl_args: dict[str, t.Any] = {
            "ssl_certfile": ssl_certfile,
            "ssl_keyfile": ssl_keyfile,
            "ssl_ca_certs": ssl_ca_certs,
        }

        self.args.extend(construct_ssl_args(**ssl_args))

        if enable_reflection:
            self.args.append("--enable-reflection")
        if enable_channelz:
            self.args.append("--enable-channelz")
        if max_concurrent_streams is not None:
            self.args.extend(["--max-concurrent-streams", str(max_concurrent_streams)])

        if grpc_protocol_version is not None:
            self.args.extend(["--protocol-version", str(grpc_protocol_version)])

    def get_client(self) -> GrpcClient | None:
        if self.process is None:
            logger.warning(
                "Attempted to get a client for a BentoML server that was not running! Try running 'bentoml.*Server.start()' first."
            )
            return
        assert self.process is not None
        out_code = self.process.poll()
        if out_code == 0:
            logger.warning(
                "Attempted to get a client from a BentoML server that has already exited! You can run '.start()' again to restart it."
            )
            return
        elif out_code is not None:
            logs = "Attempted to get a client from a BentoML server that has already exited with an error!\nServer Output:\n"
            if self.process.stdout is not None and not self.process.stdout.closed:
                s = self.process.stdout.read()
                logs += textwrap.indent(
                    s.decode("utf-8") if isinstance(s, bytes) else s, " " * 4
                )
            if self.process.stderr is not None and not self.process.stderr.closed:
                logs += "\nServer Error:\n"
                s = self.process.stderr.read()
                logs += textwrap.indent(
                    s.decode("utf-8") if isinstance(s, bytes) else s, " " * 4
                )
            logger.warning(logs)
            return

        if self._client is None:
            from .client import GrpcClient

            GrpcClient.wait_until_server_ready(
                host=self.host, port=self.port, timeout=self.timeout
            )
            self._client = GrpcClient.from_url(f"{self.host}:{self.port}")
        return self._client
