from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CountryConfig:
    code: str
    label: str
    flag: str
    annual_frequency: float
    contracts: List[str]
    bonus_incidence: List[str]
    extras: Dict[str, List[str]] = field(default_factory=dict)


COUNTRIES: Dict[str, CountryConfig] = {
    "br": CountryConfig(
        code="br",
        label="Brasil",
        flag="assets/img/bandeiras/br.svg",
        annual_frequency=13.33,
        contracts=["CLT", "Estatutário", "Autônomo"],
        bonus_incidence=[
            "Não sofre incidência",
            "Incidência apenas IRRF",
            "Incidência total: FGTS, 13º, férias, IRRF, INSS",
        ],
        extras={
            "previdencia": ["PGBL (deduz IR)", "VGBL (não deduz IR)", "FGBL (não deduz IR)"],
        },
    ),
    "cl": CountryConfig(
        code="cl",
        label="Chile",
        flag="assets/img/bandeiras/chile.svg",
        annual_frequency=13.0,
        contracts=["Contrato indefinido", "Honorários"],
        bonus_incidence=["Afecto solo a impuestos", "Afecto a AFP + Salud", "Exento"],
        extras={
            "salud": ["FONASA (7%)", "ISAPRE (plano privado)"],
        },
    ),
    "ar": CountryConfig(
        code="ar",
        label="Argentina",
        flag="assets/img/bandeiras/argentina.svg",
        annual_frequency=13.0,
        contracts=["Indeterminado", "Plazo fijo", "Autónomo"],
        bonus_incidence=["Afecto a impuestos", "Exento hasta tope legal"],
    ),
    "co": CountryConfig(
        code="co",
        label="Colômbia",
        flag="assets/img/bandeiras/colombia.svg",
        annual_frequency=13.0,
        contracts=[
            "Indefinido",
            "Termo Fijo",
            "Prestação de Serviços (sem benefícios sociais)",
        ],
        bonus_incidence=["Só imposto", "Imposto + Seguridade Social", "Isento"],
    ),
    "mx": CountryConfig(
        code="mx",
        label="México",
        flag="assets/img/bandeiras/mexico.svg",
        annual_frequency=13.0,
        contracts=["Tiempo Indeterminado", "Tiempo Determinado", "Honorarios"],
        bonus_incidence=["Solo ISR", "ISR + IMSS", "Exento hasta tope legal"],
        extras={
            "estados": [
                "CDMX",
                "Estado de México",
                "Jalisco",
                "Nuevo León",
                "Puebla",
                "Otros",
            ]
        },
    ),
    "us": CountryConfig(
        code="us",
        label="Estados Unidos",
        flag="assets/img/bandeiras/usa.svg",
        annual_frequency=12.0,
        contracts=["Full-time (W2)", "Part-time (W2)", "Contractor (1099)"],
        bonus_incidence=[
            "Flat IRS Supplemental Rate (22%)",
            "Flat IRS High Earner Rate (37%)",
            "Combined Federal + State",
            "Employer Custom Rule",
        ],
        extras={
            "states": [
                "Florida",
                "Texas",
                "Nevada",
                "Washington",
                "Tennessee",
                "New York",
                "California",
                "New Jersey",
                "Illinois",
                "Massachusetts",
            ],
            "filing_status": [
                "Single",
                "Married Filing Jointly",
                "Married Filing Separately",
                "Head of Household",
            ],
        },
    ),
    "ca": CountryConfig(
        code="ca",
        label="Canadá",
        flag="assets/img/bandeiras/canada.svg",
        annual_frequency=12.0,
        contracts=[
            "Full-time Employment",
            "Part-time Employment",
            "Contractor (T4A / sem EI padrão)",
        ],
        bonus_incidence=[
            "Apenas Federal",
            "Federal + Provincial",
            "Federal + Provincial + CPP/EI",
            "Exento",
        ],
        extras={
            "provinces": [
                "Ontario",
                "British Columbia",
                "Alberta",
                "Québec",
                "Manitoba",
                "Saskatchewan",
                "Nova Scotia",
                "New Brunswick",
                "Prince Edward Island",
                "Newfoundland & Labrador",
                "Northwest Territories",
                "Yukon",
                "Nunavut",
            ]
        },
    ),
}


DEFAULT_COUNTRY = COUNTRIES["br"]


def country_options() -> List[str]:
    return [cfg.label for cfg in COUNTRIES.values()]


def find_country_by_label(label: str) -> Optional[CountryConfig]:
    for cfg in COUNTRIES.values():
        if cfg.label.lower() == label.lower():
            return cfg
    return None
