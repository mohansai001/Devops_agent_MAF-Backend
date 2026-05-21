from contextvars import ContextVar

github_pat_ctx: ContextVar[str] = ContextVar("github_pat")