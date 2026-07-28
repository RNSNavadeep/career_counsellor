from .ai_engineer import AI_ENGINEER
from .data_scientist import DATA_SCIENTIST
from .data_analyst import DATA_ANALYST
from .ml_engineer import ML_ENGINEER
from .frontend import FRONTEND_DEVELOPER
from .backend import BACKEND_DEVELOPER
from .fullstack import FULLSTACK_DEVELOPER
from .cybersecurity import CYBERSECURITY_ENGINEER
from .devops import DEVOPS_ENGINEER
from .cloud import CLOUD_ENGINEER

from .ui_ux_designer import UI_UX_DESIGNER
from .graphic_designer import GRAPHIC_DESIGNER
from .digital_marketer import DIGITAL_MARKETER
from .business_analyst import BUSINESS_ANALYST
from .financial_analyst import FINANCIAL_ANALYST

# Standardize domains across all careers
_raw_careers = [
    (AI_ENGINEER, "Tech"),
    (DATA_SCIENTIST, "Tech"),
    (DATA_ANALYST, "Tech"),
    (ML_ENGINEER, "Tech"),
    (FRONTEND_DEVELOPER, "Tech"),
    (BACKEND_DEVELOPER, "Tech"),
    (FULLSTACK_DEVELOPER, "Tech"),
    (CYBERSECURITY_ENGINEER, "Tech"),
    (DEVOPS_ENGINEER, "Tech"),
    (CLOUD_ENGINEER, "Tech"),
    (UI_UX_DESIGNER, "Arts & Design"),
    (GRAPHIC_DESIGNER, "Arts & Design"),
    (DIGITAL_MARKETER, "Commerce & Business"),
    (BUSINESS_ANALYST, "Commerce & Business"),
    (FINANCIAL_ANALST := FINANCIAL_ANALYST, "Commerce & Business"),
]

career_data = {}
for item, default_domain in _raw_careers:
    if "domain" not in item:
        item["domain"] = default_domain
    career_data[item["career"]] = item

CAREER_DOMAINS = {
    "All": list(career_data.keys()),
    "Tech": [c for c, d in career_data.items() if d.get("domain") == "Tech"],
    "Arts & Design": [c for c, d in career_data.items() if d.get("domain") == "Arts & Design"],
    "Commerce & Business": [c for c, d in career_data.items() if d.get("domain") == "Commerce & Business"],
}