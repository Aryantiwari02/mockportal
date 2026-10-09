from rest_framework.throttling import SimpleRateThrottle


class AgentRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls from AI Agents to prevent denial-of-service
    or excessive automated polling.
    """

    scope = "agent_api"

    def get_cache_key(self, request, view):
        agent_user = getattr(request, "user", None)
        if agent_user and getattr(agent_user, "is_agent", False):
            ident = getattr(agent_user, "prefix", "agent")
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }


class AgentPublicRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of public scheme queries by agents.
    """

    scope = "agent_public"

    def get_cache_key(self, request, view):
        agent_user = getattr(request, "user", None)
        if agent_user and getattr(agent_user, "is_agent", False):
            ident = getattr(agent_user, "prefix", "agent")
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }
