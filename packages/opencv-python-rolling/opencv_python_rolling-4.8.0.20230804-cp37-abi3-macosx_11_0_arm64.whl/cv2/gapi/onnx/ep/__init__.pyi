__all__: list[str] = []

import typing


# Classes
class CUDA:
    # Functions
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, dev_id: int) -> None: ...


class TensorRT:
    # Functions
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, dev_id: int) -> None: ...


class OpenVINO:
    # Functions
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, dev_type: str) -> None: ...

    def cfgCacheDir(self, dir: str) -> OpenVINO: ...

    def cfgNumThreads(self, nthreads: int) -> OpenVINO: ...

    def cfgEnableOpenCLThrottling(self) -> OpenVINO: ...

    def cfgEnableDynamicShapes(self) -> OpenVINO: ...


class DirectML:
    # Functions
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, device_id: int) -> None: ...



