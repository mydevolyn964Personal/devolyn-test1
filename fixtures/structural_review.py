"""Working pipeline example whose abstraction needs product-context review."""

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class Request:
    text: str
    tags: list[str] = field(default_factory=list)


Stage = Callable[[Request], Request]


class RequestPipeline:
    def __init__(self) -> None:
        self._stages: list[tuple[str, Stage]] = []

    def register(self, name: str, stage: Stage) -> None:
        self._stages.append((name, stage))

    def run(self, request: Request) -> Request:
        for _, stage in self._stages:
            request = stage(request)
        return request


def trim_text(request: Request) -> Request:
    request.text = request.text.strip()
    return request


def add_content_tag(request: Request) -> Request:
    if request.text:
        request.tags.append("has-content")
    return request


def build_request_pipeline() -> RequestPipeline:
    pipeline = RequestPipeline()
    pipeline.register("trim", trim_text)
    pipeline.register("tag-content", add_content_tag)
    return pipeline


if __name__ == "__main__":
    result = build_request_pipeline().run(Request("  Example input  "))
    print(result)
