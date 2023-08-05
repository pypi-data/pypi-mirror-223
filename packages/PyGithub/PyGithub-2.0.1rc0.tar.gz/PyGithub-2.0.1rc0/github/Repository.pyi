from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union, overload, Iterable

from github.Artifact import Artifact
from github.AuthenticatedUser import AuthenticatedUser
from github.Autolink import Autolink
from github.Branch import Branch
from github.CheckRun import CheckRun
from github.CheckSuite import CheckSuite
from github.Clones import Clones
from github.Commit import Commit
from github.CommitComment import CommitComment
from github.Comparison import Comparison
from github.ContentFile import ContentFile
from github.Deployment import Deployment
from github.Download import Download
from github.Environment import Environment
from github.EnvironmentDeploymentBranchPolicy import (
    EnvironmentDeploymentBranchPolicyParams,
)
from github.EnvironmentProtectionRuleReviewer import ReviewerParams
from github.Event import Event
from github.GitBlob import GitBlob
from github.GitCommit import GitCommit
from github.GithubObject import CompletableGithubObject, _NotSetType
from github.GitRef import GitRef
from github.GitRelease import GitRelease
from github.GitReleaseAsset import GitReleaseAsset
from github.GitTag import GitTag
from github.GitTree import GitTree
from github.Hook import Hook
from github.InputGitAuthor import InputGitAuthor
from github.InputGitTreeElement import InputGitTreeElement
from github.Invitation import Invitation
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.IssueEvent import IssueEvent
from github.Label import Label
from github.Milestone import Milestone
from github.NamedUser import NamedUser
from github.Notification import Notification
from github.Organization import Organization
from github.PaginatedList import PaginatedList
from github.Path import Path
from github.Permissions import Permissions
from github.Project import Project
from github.PublicKey import PublicKey
from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from github.Referrer import Referrer
from github.RepositoryAdvisory import RepositoryAdvisory
from github.RepositoryAdvisoryCredit import RepositoryAdvisoryCredit
from github.RepositoryAdvisoryVulnerability import (
    RepositoryAdvisoryVulnerability,
    AdvisoryVulnerability,
)
from github.RepositoryKey import RepositoryKey
from github.RepositoryPreferences import RepositoryPreferences
from github.SelfHostedActionsRunner import SelfHostedActionsRunner
from github.SourceImport import SourceImport
from github.Stargazer import Stargazer
from github.StatsCodeFrequency import StatsCodeFrequency
from github.StatsCommitActivity import StatsCommitActivity
from github.StatsContributor import StatsContributor
from github.StatsParticipation import StatsParticipation
from github.StatsPunchCard import StatsPunchCard
from github.Tag import Tag
from github.Team import Team
from github.View import View
from github.Workflow import Workflow
from github.WorkflowRun import WorkflowRun

class Repository(CompletableGithubObject):
    def __repr__(self) -> str: ...
    def _hub(
        self, mode: str, event: str, callback: str, secret: Union[str, _NotSetType]
    ) -> None: ...
    @property
    def _identity(self) -> str: ...
    def _initAttributes(self) -> None: ...
    def _legacy_convert_issue(self, attributes: Dict[str, Any]) -> Dict[str, Any]: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    @property
    def allow_merge_commit(self) -> bool: ...
    @property
    def allow_rebase_merge(self) -> bool: ...
    @property
    def allow_squash_merge(self) -> bool: ...
    @property
    def archived(self) -> bool: ...
    def add_to_collaborators(
        self,
        collaborator: Union[str, NamedUser],
        permission: Union[str, _NotSetType] = ...,
    ) -> None: ...
    @property
    def archive_url(self) -> str: ...
    @property
    def assignees_url(self) -> str: ...
    @property
    def blobs_url(self) -> str: ...
    @property
    def branches_url(self) -> str: ...
    @property
    def clone_url(self) -> str: ...
    @property
    def collaborators_url(self) -> str: ...
    @property
    def comments_url(self) -> str: ...
    @property
    def commits_url(self) -> str: ...
    def compare(self, base: str, head: str) -> Comparison: ...
    @property
    def compare_url(self) -> str: ...
    @property
    def contents_url(self) -> str: ...
    @property
    def contributors_url(self) -> str: ...
    def create_autolink(self, key_prefix: str, url_template: str) -> Autolink: ...
    def create_check_run(
        self,
        name: str,
        head_sha: str,
        details_url: Union[_NotSetType, str] = ...,
        external_id: Union[_NotSetType, str] = ...,
        status: Union[_NotSetType, str] = ...,
        started_at: Union[_NotSetType, datetime] = ...,
        conclusion: Union[_NotSetType, str] = ...,
        completed_at: Union[_NotSetType, datetime] = ...,
        output: Union[
            _NotSetType, Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]
        ] = ...,
        actions: Union[_NotSetType, List[Dict[str, str]]] = ...,
    ) -> CheckRun: ...
    def create_check_suite(self, head_sha: str) -> CheckSuite: ...
    def create_deployment(
        self,
        ref: str,
        task: Union[str, _NotSetType] = ...,
        auto_merge: Union[bool, _NotSetType] = ...,
        required_contexts: Union[List[str], _NotSetType] = ...,
        payload: Union[Dict[str, Any], _NotSetType] = ...,
        environment: Union[str, _NotSetType] = ...,
        description: Union[str, _NotSetType] = ...,
        transient_environment: Union[bool, _NotSetType] = ...,
        production_environment: Union[bool, _NotSetType] = ...,
    ) -> Deployment: ...
    def get_repository_advisories(self) -> PaginatedList[RepositoryAdvisory]: ...
    def get_repository_advisory(self, ghsa: str) -> RepositoryAdvisory: ...
    def create_environment(
        self,
        environment_name: str,
        wait_timer: int = ...,
        reviewers: List[ReviewerParams] = ...,
        deployment_branch_policy: Optional[
            EnvironmentDeploymentBranchPolicyParams
        ] = ...,
    ) -> Environment: ...
    def create_file(
        self,
        path: str,
        message: str,
        content: str,
        branch: Union[str, _NotSetType] = ...,
        committer: Union[InputGitAuthor, _NotSetType] = ...,
        author: Union[InputGitAuthor, _NotSetType] = ...,
    ) -> Dict[str, Union[ContentFile, Commit]]: ...
    def create_git_blob(self, content: str, encoding: str) -> GitBlob: ...
    def create_git_commit(
        self,
        message: str,
        tree: GitTree,
        parents: List[GitCommit],
        author: Union[InputGitAuthor, _NotSetType] = ...,
        committer: Union[InputGitAuthor, _NotSetType] = ...,
    ) -> GitCommit: ...
    def create_git_ref(self, ref: str, sha: str) -> GitRef: ...
    def create_git_release(
        self,
        tag: str,
        name: str,
        message: str,
        draft: bool = ...,
        prerelease: bool = ...,
        generate_release_notes: bool = ...,
        target_commitish: Union[str, _NotSetType] = ...,
    ) -> GitRelease: ...
    def create_git_tag(
        self,
        tag: str,
        message: str,
        object: str,
        type: str,
        tagger: Union[InputGitAuthor, _NotSetType] = ...,
    ) -> GitTag: ...
    def create_git_tag_and_release(
        self,
        tag: str,
        tag_message: str,
        release_name: str,
        release_message: str,
        object: str,
        type: str,
        tagger: Union[InputGitAuthor, _NotSetType] = ...,
        draft: bool = ...,
        prerelease: bool = ...,
        generate_release_notes: bool = ...,
    ) -> GitRelease: ...
    def create_git_tree(
        self,
        tree: List[InputGitTreeElement],
        base_tree: Union[GitTree, _NotSetType] = ...,
    ) -> GitTree: ...
    def create_hook(
        self,
        name: str,
        config: Dict[str, str],
        events: Union[_NotSetType, List[str]] = ...,
        active: Union[bool, _NotSetType] = ...,
    ) -> Hook: ...
    def create_issue(
        self,
        title: str,
        body: Union[str, _NotSetType] = ...,
        assignee: Union[NamedUser, str, _NotSetType] = ...,
        milestone: Union[Milestone, _NotSetType] = ...,
        labels: Union[List[Label], _NotSetType, List[str]] = ...,
        assignees: Union[_NotSetType, List[str], List[NamedUser]] = ...,
    ) -> Issue: ...
    def create_key(
        self, title: str, key: str, read_only: bool = ...
    ) -> RepositoryKey: ...
    def create_label(
        self, name: str, color: str, description: Union[str, _NotSetType] = ...
    ) -> Label: ...
    def create_milestone(
        self,
        title: str,
        state: Union[str, _NotSetType] = ...,
        description: Union[str, _NotSetType] = ...,
        due_on: Union[date, _NotSetType] = ...,
    ) -> Milestone: ...
    def create_project(
        self, name: str, body: Union[str, _NotSetType] = ...
    ) -> Project: ...
    @overload
    def create_pull(
        self,
        title: str,
        body: str,
        base: str,
        head: str,
        maintainer_can_modify: Union[bool, _NotSetType] = _NotSetType(),
        draft: bool = False,
        issue: _NotSetType = _NotSetType(),
    ) -> PullRequest: ...
    @overload
    def create_pull(
        self,
        title: _NotSetType,
        body: _NotSetType,
        base: str,
        head: str,
        maintainer_can_modify: _NotSetType,
        issue: Issue,
    ) -> PullRequest: ...
    def create_repository_advisory(
        self,
        summary: str,
        description: str,
        severity_or_cvss_vector_string: str,
        cve_id: Optional[str] = ...,
        vulnerabilities: Optional[Iterable[AdvisoryVulnerability]] = ...,
        cwe_ids: Optional[Iterable[str]] = ...,
        credits: Optional[Iterable[RepositoryAdvisoryCredit]] = ...,
    ) -> RepositoryAdvisory: ...
    def report_security_vulnerability(
        self,
        summary: str,
        description: str,
        severity_or_cvss_vector_string: str,
        cve_id: Optional[str] = ...,
        vulnerabilities: Optional[Iterable[AdvisoryVulnerability]] = ...,
        cwe_ids: Optional[Iterable[str]] = ...,
        credits: Optional[Iterable[RepositoryAdvisoryCredit]] = ...,
    ) -> RepositoryAdvisory: ...
    def create_repository_dispatch(
        self, event_type: str, client_payload: Union[Dict[str, Any], _NotSetType] = ...
    ) -> bool: ...
    def create_secret(self, secret_name: str, unencrypted_value: str) -> bool: ...
    def delete_secret(self, secret_name: str) -> bool: ...
    def create_source_import(
        self,
        vcs: str,
        vcs_url: str,
        vcs_username: Union[str, _NotSetType] = ...,
        vcs_password: Union[str, _NotSetType] = ...,
    ) -> SourceImport: ...
    @property
    def created_at(self) -> datetime: ...
    @property
    def default_branch(self) -> str: ...
    def delete(self) -> None: ...
    def delete_environment(self, environment_name: str) -> None: ...
    def delete_file(
        self,
        path: str,
        message: str,
        sha: str,
        branch: Union[str, _NotSetType] = ...,
        committer: Union[InputGitAuthor, _NotSetType] = ...,
        author: Union[InputGitAuthor, _NotSetType] = ...,
    ) -> Dict[str, Union[Commit, _NotSetType]]: ...
    @property
    def delete_branch_on_merge(self) -> bool: ...
    @property
    def deployments_url(self) -> str: ...
    @property
    def description(self) -> str: ...
    def disable_automated_security_fixes(self) -> bool: ...
    def disable_vulnerability_alert(self) -> bool: ...
    @property
    def downloads_url(self) -> str: ...
    def edit(
        self,
        name: Optional[str] = ...,
        description: Union[str, _NotSetType] = ...,
        homepage: Union[str, _NotSetType] = ...,
        private: Union[bool, _NotSetType] = ...,
        has_issues: Union[bool, _NotSetType] = ...,
        has_projects: Union[bool, _NotSetType] = ...,
        has_wiki: Union[bool, _NotSetType] = ...,
        has_downloads: Union[bool, _NotSetType] = ...,
        default_branch: Union[str, _NotSetType] = ...,
        allow_forking: Union[bool, _NotSetType] = ...,
        allow_squash_merge: Union[bool, _NotSetType] = ...,
        allow_merge_commit: Union[bool, _NotSetType] = ...,
        allow_rebase_merge: Union[bool, _NotSetType] = ...,
        delete_branch_on_merge: Union[bool, _NotSetType] = ...,
        allow_update_branch: Union[bool, _NotSetType] = ...,
        archived: Union[bool, _NotSetType] = ...,
    ) -> None: ...
    def enable_automated_security_fixes(self) -> bool: ...
    def enable_vulnerability_alert(self) -> bool: ...
    @property
    def events_url(self) -> str: ...
    @property
    def fork(self) -> bool: ...
    @property
    def forks(self) -> int: ...
    @property
    def forks_count(self) -> int: ...
    @property
    def forks_url(self) -> str: ...
    @property
    def full_name(self) -> str: ...
    def get_archive_link(
        self, archive_format: str, ref: Union[str, _NotSetType] = ...
    ) -> str: ...
    def get_artifact(self, artifact_id: int) -> Artifact: ...
    def get_artifacts(
        self, name: Union[str, _NotSetType] = ...
    ) -> PaginatedList[Artifact]: ...
    def get_assignees(self) -> PaginatedList[NamedUser]: ...
    def get_autolinks(self) -> PaginatedList[Autolink]: ...
    def get_branch(self, branch: str) -> Branch: ...
    def rename_branch(self, branch: Union[str, Branch], new_name: str) -> bool: ...
    def get_branches(self) -> PaginatedList[Branch]: ...
    def get_check_run(self, check_run_id: int) -> CheckRun: ...
    def get_check_suite(self, check_suite_id: int) -> CheckSuite: ...
    def get_clones_traffic(
        self, per: Union[str, _NotSetType] = ...
    ) -> Dict[str, Union[int, List[Clones]]]: ...
    def get_collaborator_permission(
        self, collaborator: Union[str, NamedUser]
    ) -> str: ...
    def get_collaborators(
        self, affiliation: Union[str, _NotSetType] = ...
    ) -> PaginatedList[NamedUser]: ...
    def get_comment(self, id: int) -> CommitComment: ...
    def get_comments(self) -> PaginatedList[CommitComment]: ...
    def get_commit(self, sha: str) -> Commit: ...
    def get_commits(
        self,
        sha: Union[str, _NotSetType] = ...,
        path: Union[str, _NotSetType] = ...,
        since: Union[_NotSetType, datetime] = ...,
        until: Union[_NotSetType, datetime] = ...,
        author: Union[AuthenticatedUser, NamedUser, str, _NotSetType] = ...,
    ) -> PaginatedList[Commit]: ...
    def get_contents(
        self, path: str, ref: Union[str, _NotSetType] = ...
    ) -> Union[List[ContentFile], ContentFile]: ...
    def get_contributors(
        self, anon: Union[str, _NotSetType] = ...
    ) -> PaginatedList[NamedUser]: ...
    def get_deployment(self, id_: int) -> Deployment: ...
    def get_deployments(
        self,
        sha: Union[str, _NotSetType] = ...,
        ref: Union[str, _NotSetType] = ...,
        task: Union[str, _NotSetType] = ...,
        environment: Union[str, _NotSetType] = ...,
    ) -> PaginatedList[Deployment]: ...
    def get_dir_contents(
        self, path: str, ref: Union[str, _NotSetType] = ...
    ) -> List[ContentFile]: ...
    def get_download(self, id: int) -> Download: ...
    def get_downloads(self) -> PaginatedList[Download]: ...
    def get_environments(self) -> PaginatedList[Environment]: ...
    def get_environment(self, environment_name: str) -> Environment: ...
    def get_events(self) -> PaginatedList[Event]: ...
    def get_forks(self) -> PaginatedList[Repository]: ...
    def create_fork(
        self,
        organization: Union[Organization, str, _NotSetType] = ...,
        name: Union[str, _NotSetType] = ...,
        default_branch_only: Union[str, _NotSetType] = ...,
    ) -> Repository: ...
    def get_git_blob(self, sha: str) -> GitBlob: ...
    def get_git_commit(self, sha: str) -> GitCommit: ...
    def get_git_matching_refs(self, ref: str) -> PaginatedList[GitRef]: ...
    def get_git_ref(self, ref: str) -> GitRef: ...
    def get_git_refs(self) -> PaginatedList[GitRef]: ...
    def get_git_tag(self, sha: str) -> GitTag: ...
    def get_git_tree(
        self, sha: str, recursive: Union[bool, _NotSetType] = ...
    ) -> GitTree: ...
    def get_hook(self, id: int) -> Hook: ...
    def get_hooks(self) -> PaginatedList[Hook]: ...
    def get_issue(self, number: int) -> Issue: ...
    def get_issues(
        self,
        milestone: Union[Milestone, str, _NotSetType] = ...,
        state: Union[str, _NotSetType] = ...,
        assignee: Union[NamedUser, str, _NotSetType] = ...,
        mentioned: Union[_NotSetType, NamedUser] = ...,
        labels: Union[List[str], List[Label], _NotSetType] = ...,
        sort: Union[str, _NotSetType] = ...,
        direction: Union[str, _NotSetType] = ...,
        since: Union[_NotSetType, datetime] = ...,
        creator: Union[NamedUser, _NotSetType] = ...,
    ) -> PaginatedList[Issue]: ...
    def get_issues_comments(
        self,
        sort: Union[str, _NotSetType] = ...,
        direction: Union[str, _NotSetType] = ...,
        since: Union[_NotSetType, datetime] = ...,
    ) -> PaginatedList[IssueComment]: ...
    def get_issues_event(self, id: int) -> IssueEvent: ...
    def get_issues_events(self) -> PaginatedList[IssueEvent]: ...
    def get_key(self, id: int) -> RepositoryKey: ...
    def get_keys(self) -> PaginatedList[RepositoryKey]: ...
    def get_label(self, name: str) -> Label: ...
    def get_labels(self) -> PaginatedList[Label]: ...
    def get_languages(self) -> Dict[str, int]: ...
    def get_latest_release(self) -> GitRelease: ...
    def get_license(self) -> ContentFile: ...
    def get_milestone(self, number: int) -> Milestone: ...
    def get_milestones(
        self,
        state: Union[str, _NotSetType] = ...,
        sort: Union[str, _NotSetType] = ...,
        direction: Union[str, _NotSetType] = ...,
    ) -> PaginatedList[Milestone]: ...
    def get_network_events(self) -> PaginatedList[Event]: ...
    def get_notifications(
        self,
        all: Union[bool, _NotSetType] = ...,
        participating: Union[bool, _NotSetType] = ...,
        since: Union[datetime, _NotSetType] = ...,
        before: Union[datetime, _NotSetType] = ...,
    ) -> PaginatedList[Notification]: ...
    def get_pending_invitations(self) -> PaginatedList[Invitation]: ...
    def get_projects(
        self, state: Union[str, _NotSetType] = ...
    ) -> PaginatedList[Project]: ...
    def get_public_key(self) -> PublicKey: ...
    def get_pull(self, number: int) -> PullRequest: ...
    def get_pulls(
        self,
        state: Union[str, _NotSetType] = ...,
        sort: Union[str, _NotSetType] = ...,
        direction: Union[str, _NotSetType] = ...,
        base: Union[str, _NotSetType] = ...,
        head: Union[str, _NotSetType] = ...,
    ) -> PaginatedList[PullRequest]: ...
    def get_pulls_comments(
        self,
        sort: Union[str, _NotSetType] = ...,
        direction: Union[str, _NotSetType] = ...,
        since: Union[_NotSetType, datetime] = ...,
    ) -> PaginatedList[PullRequestComment]: ...
    def get_pulls_review_comments(
        self,
        sort: Union[str, _NotSetType] = ...,
        direction: Union[str, _NotSetType] = ...,
        since: Union[_NotSetType, datetime] = ...,
    ) -> PaginatedList[PullRequestComment]: ...
    def get_readme(self, ref: Union[str, _NotSetType] = ...) -> ContentFile: ...
    def get_release(self, id: Union[int, str]) -> GitRelease: ...
    def get_release_asset(self, id: int) -> GitReleaseAsset: ...
    def get_releases(self) -> PaginatedList[GitRelease]: ...
    def get_self_hosted_runner(self, runner_id: int) -> SelfHostedActionsRunner: ...
    def get_self_hosted_runners(self) -> PaginatedList[SelfHostedActionsRunner]: ...
    def get_source_import(self) -> SourceImport: ...
    def get_stargazers(self) -> PaginatedList[NamedUser]: ...
    def get_stargazers_with_dates(self) -> PaginatedList[Stargazer]: ...
    def get_stats_code_frequency(self) -> Optional[List[StatsCodeFrequency]]: ...
    def get_stats_commit_activity(self) -> Optional[List[StatsCommitActivity]]: ...
    def get_stats_contributors(self) -> Optional[List[StatsContributor]]: ...
    def get_stats_participation(self) -> Optional[StatsParticipation]: ...
    def get_stats_punch_card(self) -> Optional[StatsPunchCard]: ...
    def get_subscribers(self) -> PaginatedList[NamedUser]: ...
    def get_tags(self) -> PaginatedList[Tag]: ...
    def get_teams(self) -> PaginatedList[Team]: ...
    def get_top_paths(self) -> List[Path]: ...
    def get_top_referrers(self) -> List[Referrer]: ...
    def get_topics(self) -> List[str]: ...
    def get_views_traffic(
        self, per: Union[str, _NotSetType] = ...
    ) -> Dict[str, Union[int, List[View]]]: ...
    def get_vulnerability_alert(self) -> bool: ...
    def get_watchers(self) -> PaginatedList[NamedUser]: ...
    def get_workflow(self, id_or_name: Union[str, int]) -> Workflow: ...
    def get_workflows(self) -> PaginatedList[Workflow]: ...
    def get_workflow_run(self, id_: int) -> WorkflowRun: ...
    def get_workflow_runs(
        self,
        actor: Union[NamedUser, _NotSetType] = ...,
        branch: Union[Branch, _NotSetType] = ...,
        event: Union[str, _NotSetType] = ...,
        status: Union[str, _NotSetType] = ...,
        exclude_pull_requests: Union[bool, _NotSetType] = ...,
        head_sha: Union[str, _NotSetType] = ...,
    ) -> PaginatedList[WorkflowRun]: ...
    def update_check_suites_preferences(
        self, auto_trigger_checks: List[Dict[str, Union[bool, int]]]
    ) -> RepositoryPreferences: ...
    @property
    def git_commits_url(self) -> str: ...
    @property
    def git_refs_url(self) -> str: ...
    @property
    def git_tags_url(self) -> str: ...
    @property
    def git_url(self) -> str: ...
    @property
    def has_downloads(self) -> bool: ...
    def has_in_assignees(self, assignee: Union[str, NamedUser]) -> bool: ...
    def has_in_collaborators(self, collaborator: Union[str, NamedUser]) -> bool: ...
    @property
    def has_issues(self) -> bool: ...
    @property
    def has_pages(self) -> bool: ...
    @property
    def has_projects(self) -> bool: ...
    @property
    def has_wiki(self) -> bool: ...
    @property
    def homepage(self) -> str: ...
    @property
    def hooks_url(self) -> str: ...
    @property
    def html_url(self) -> str: ...
    @property
    def id(self) -> int: ...
    @property
    def is_template(self) -> bool: ...
    @property
    def issue_comment_url(self) -> str: ...
    @property
    def issue_events_url(self) -> str: ...
    @property
    def issues_url(self) -> str: ...
    @property
    def keys_url(self) -> str: ...
    @property
    def labels_url(self) -> str: ...
    @property
    def language(self) -> str: ...
    @property
    def languages_url(self) -> str: ...
    def legacy_search_issues(self, state: str, keyword: str) -> List[Issue]: ...
    def mark_notifications_as_read(self, last_read_at: datetime = ...) -> None: ...
    @property
    def master_branch(self) -> Optional[str]: ...
    def merge(
        self, base: str, head: str, commit_message: Union[str, _NotSetType] = ...
    ) -> Optional[Commit]: ...
    @property
    def merges_url(self) -> str: ...
    @property
    def milestones_url(self) -> str: ...
    @property
    def mirror_url(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def network_count(self) -> int: ...
    @property
    def notifications_url(self) -> str: ...
    @property
    def open_issues(self) -> int: ...
    @property
    def open_issues_count(self) -> int: ...
    @property
    def organization(self) -> Organization: ...
    @property
    def owner(self) -> NamedUser: ...
    @property
    def parent(self) -> Repository: ...
    @property
    def permissions(self) -> Permissions: ...
    @property
    def private(self) -> bool: ...
    @property
    def pulls_url(self) -> str: ...
    @property
    def pushed_at(self) -> datetime: ...
    @property
    def releases_url(self) -> str: ...
    def remove_autolink(self, autolink: Union[Autolink, int]) -> bool: ...
    def remove_from_collaborators(
        self, collaborator: Union[str, NamedUser]
    ) -> None: ...
    def remove_self_hosted_runner(
        self, runner: Union[SelfHostedActionsRunner, int]
    ) -> bool: ...
    def remove_invitation(self, invite_id: int) -> None: ...
    def replace_topics(self, topics: List[str]) -> None: ...
    @property
    def size(self) -> int: ...
    @property
    def source(self) -> Optional[Repository]: ...
    @property
    def ssh_url(self) -> str: ...
    @property
    def stargazers_count(self) -> int: ...
    @property
    def stargazers_url(self) -> str: ...
    @property
    def statuses_url(self) -> str: ...
    def subscribe_to_hub(
        self, event: str, callback: str, secret: Union[str, _NotSetType] = ...
    ) -> None: ...
    @property
    def subscribers_count(self) -> int: ...
    @property
    def subscribers_url(self) -> str: ...
    @property
    def subscription_url(self) -> str: ...
    @property
    def svn_url(self) -> str: ...
    @property
    def tags_url(self) -> str: ...
    @property
    def teams_url(self) -> str: ...
    @property
    def topics(self) -> List[str]: ...
    @property
    def trees_url(self) -> str: ...
    def unsubscribe_from_hub(self, event: str, callback: str) -> None: ...
    def update_environment(
        self,
        environment_name: str,
        wait_timer: int = ...,
        reviewers: List[ReviewerParams] = ...,
        deployment_branch_policy: Optional[
            EnvironmentDeploymentBranchPolicyParams
        ] = ...,
    ) -> Environment: ...
    def update_file(
        self,
        path: str,
        message: str,
        content: Union[bytes, str],
        sha: str,
        branch: Union[_NotSetType, str] = ...,
        committer: Union[_NotSetType, InputGitAuthor] = ...,
        author: Union[_NotSetType, InputGitAuthor] = ...,
    ) -> Dict[str, Union[ContentFile, Commit]]: ...
    @property
    def updated_at(self) -> datetime: ...
    @property
    def url(self) -> str: ...
    @property
    def visibility(self) -> str: ...
    @property
    def watchers(self) -> int: ...
    @property
    def watchers_count(self) -> int: ...
