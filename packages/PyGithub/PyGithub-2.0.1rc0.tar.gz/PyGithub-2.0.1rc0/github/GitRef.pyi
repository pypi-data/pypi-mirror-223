from typing import Any, Dict, Union

from github.GithubObject import CompletableGithubObject, _NotSetType
from github.GitObject import GitObject

class GitRef(CompletableGithubObject):
    def __repr__(self) -> str: ...
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    def delete(self) -> None: ...
    def edit(self, sha: str, force: Union[bool, _NotSetType] = ...) -> None: ...
    @property
    def object(self) -> GitObject: ...
    @property
    def ref(self) -> str: ...
    @property
    def url(self) -> str: ...
