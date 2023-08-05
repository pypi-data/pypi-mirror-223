from typing import Any, Dict, List

from datetime import datetime
from github.GithubObject import CompletableGithubObject
from github.NamedUser import NamedUser

class GithubApp(CompletableGithubObject):
    def __repr__(self) -> str: ...
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def slug(self) -> str: ...
    @property
    def url(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    @property
    def external_url(self) -> str: ...
    @property
    def html_url(self) -> str: ...
    @property
    def created_at(self) -> datetime: ...
    @property
    def updated_at(self) -> datetime: ...
    @property
    def owner(self) -> NamedUser: ...
    @property
    def permissions(self) -> Dict[str, str]: ...
    @property
    def events(self) -> List[str]: ...
