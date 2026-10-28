"""Site settings: the Tableau Public links the app embeds.

Paste each link between the quotes below (or set the matching environment
variable). Any form of Tableau Public link works:
    https://public.tableau.com/views/<Workbook>/<Dashboard>
    https://public.tableau.com/app/profile/<you>/viz/<Workbook>/<Dashboard>
    https://public.tableau.com/shared/<code>
"""
import os

TABLEAU_DASHBOARD_URL = os.environ.get("TABLEAU_DASHBOARD_URL", "https://public.tableau.com/views/T3dashboard/F1RaceIntelligenceDashboard")
TABLEAU_STORY_URL = os.environ.get("TABLEAU_STORY_URL", "https://public.tableau.com/views/T3Story/F1RaceIntelligenceStory")
