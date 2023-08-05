from typing import Optional, Union

import hammock

from orkg.common import Hosts
from orkg.out import OrkgResponse

from .classes import ClassesClient
from .comparisons import ComparisonsClient
from .contribution_comparisons import ContributionComparisonsClient
from .contributions import ContributionsClient
from .dummy import DummyClient
from .harvesters import HarvestersClient
from .json import JSONClient
from .literals import LiteralsClient
from .objects import ObjectsClient
from .papers import PapersClient
from .predicates import PredicatesClient
from .resources import ResourcesClient
from .statements import StatementsClient
from .stats import StatsClient
from .templates import TemplatesClient


class ORKG(object):
    host: Optional[Union[str, Hosts]] = None
    simcomp_host: Optional[str] = None
    token: str = None

    def __init__(
        self,
        host: Optional[Union[str, Hosts]] = None,
        simcomp_host: Optional[str] = None,
        creds: Optional[tuple] = None,
        **kwargs,
    ):
        self._set_host(host)
        self._set_simcomp_host(simcomp_host)
        self.core = hammock.Hammock(self.host)
        if self.simcomp_available:
            self.simcomp = hammock.Hammock(self.simcomp_host)
        self.token = None
        if creds is not None and len(creds) == 2:
            self.__authenticate(creds[0], creds[1])
        self.backend = self.core.api
        self.resources = ResourcesClient(self)
        self.predicates = PredicatesClient(self)
        self.classes = ClassesClient(self)
        self.literals = LiteralsClient(self)
        self.stats = StatsClient(self)
        self.statements = StatementsClient(self)
        self.papers = PapersClient(self)
        self.comparisons = ComparisonsClient(self)
        self.contributions = ContributionsClient(self)
        self.objects = ObjectsClient(self)
        self.dummy = DummyClient(self)
        self.json = JSONClient(self)
        self.templates = TemplatesClient(self)
        self.contribution_comparisons = ContributionComparisonsClient(self)
        self.harvesters = HarvestersClient(self)

    @property
    def simcomp_available(self):
        return self.simcomp_host is not None

    def _set_host(self, host):
        if isinstance(host, Hosts):
            host = host.value
        if host is not None and not host.startswith("http"):
            if "host" not in host.lower():
                raise ValueError("host must begin with http or https")
            else:
                raise ValueError(
                    "the host name was not recognized -- use Hosts.PRODUCTION, Hosts.SANDBOX, or Hosts.INCUBATING without quotes"
                )
        if host is not None and host[-1] == "/":
            host = host[:-1]
        self.host = host if host is not None else "https://sandbox.orkg.org"

    def _set_simcomp_host(self, simcomp_host):
        if simcomp_host is not None and not simcomp_host.startswith("http"):
            raise ValueError("simcomp host must begin with http or https")
        if simcomp_host is None and "orkg" in self.host:
            simcomp_host = self.host + "/simcomp"
        self.simcomp_host = simcomp_host

    def __authenticate(self, email, password):
        data = {
            "username": email,
            "grant_type": "password",
            "client_id": "orkg-client",
            "password": password,
        }
        resp = self.core.oauth.token.POST(
            data=data, headers={"Authorization": "Basic b3JrZy1jbGllbnQ6c2VjcmV0"}
        )
        if resp.status_code == 200:
            self.token = resp.json()["access_token"]
        else:
            raise IOError(
                f"Please check the credentials provided!, got the error {resp.content}"
            )

    def ping(self):
        pass  # TODO: see how to ping ORKG host to know if it is alive

    # FIXME: remove after system stabling
    def pagination_activated(self) -> bool:
        self.backend._append_slash = True
        return "pageable" in self.backend.resources.GET().json()

    def wrap_response(
        self,
        response=None,
        status_code: str = None,
        content: Union[list, dict] = None,
        url: str = None,
    ) -> OrkgResponse:
        is_paged = self.pagination_activated()
        return OrkgResponse(
            client=self,
            response=response,
            status_code=status_code,
            content=content,
            url=url,
            paged=is_paged,
        )
