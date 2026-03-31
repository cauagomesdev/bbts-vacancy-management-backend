"""
connectors/base.py
──────────────────
Contrato de conector de perfis externos.
Sprints futuras implementarão: GupyConnector, GoogleTalentConnector, EmpregaNetConnector.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ExternalProfile:
    """Perfil normalizado retornado por qualquer conector externo."""
    external_id: str
    full_name: str
    headline: str
    location: str
    skills: list[str]
    languages: list[str]
    certifications: list[str]
    education: list[str]
    raw_data: dict[str, Any]  # payload original do provider


@dataclass
class VacancyContext:
    """Contexto mínimo da vaga enviado ao conector para filtragem."""
    vacancy_id: int
    title: str
    location: str
    requirements: list[dict]  # [{type, name, mandatory, weight}]


class ProfileConnector(ABC):
    """
    Interface base para conectores de sourcing de candidatos.

    Cada integração externa deve herdar esta classe e implementar
    `fetch_profiles`. O sistema de ranking irá consumir os perfis
    retornados e calcular score internamente.
    """

    @abstractmethod
    async def fetch_profiles(self, vacancy: VacancyContext) -> list[ExternalProfile]:
        """
        Busca candidatos externos compatíveis com a vaga.

        Args:
            vacancy: Contexto da vaga aprovada.

        Returns:
            Lista de ExternalProfile normalizados.

        Raises:
            ConnectorError: Falha na comunicação com o provider.
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Verifica disponibilidade do provider externo."""
        ...


class ConnectorError(Exception):
    """Erro de comunicação com provider externo."""
    pass


# ── Stub / Mock connector (usado em Sprint 1) ──────────────────────────────────

class MockConnector(ProfileConnector):
    """
    Conector mock para Sprint 1.
    Retorna lista vazia — candidatos são fornecidos via seed.
    Substituir por GupyConnector, GoogleTalentConnector, etc. nas próximas sprints.
    """

    async def fetch_profiles(self, vacancy: VacancyContext) -> list[ExternalProfile]:
        # TODO Sprint 2: implementar integração real
        return []

    async def health_check(self) -> bool:
        return True
