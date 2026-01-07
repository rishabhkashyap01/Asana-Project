import uuid
import random

class ProjectGenerator:
    def __init__(self):
        self.templates = {
            "Engineering": [
                "Infrastructure Migration 2026", "Mobile App - Sprint Backlog",
                "Security Audit & Remediation", "API Documentation Update",
                "Frontend Component Library", "Database Performance Tuning"
            ],
            "Marketing": [
                "Q1 Social Media Campaign", "Annual Brand Refresh",
                "Product Hunt Launch Strategy", "Content Marketing Pipeline"
            ],
            "Product": [
                "User Interview Insights", "Product Roadmap - H1 2026"
            ],
            "Sales": [
                "Enterprise Lead Tracking", "Q1 Sales Kickoff Planning"
            ],
            "Operations": [
                "New Hire Onboarding Flow", "IT Asset Management"
            ]
        }

    # --- RENAME THIS METHOD ---
    def generate_for_team(self, team_id, department):
        """
        Generates a realistic set of projects for a specific team.
        Matches the call in main.py
        """
        projects = []
        names_pool = self.templates.get(department, ["General Initiative", "Team Tasks"])
        
        num_projects = random.randint(2, 5)
        selected_names = random.sample(names_pool, min(num_projects, len(names_pool)))

        for name in selected_names:
            projects.append({
                "project_id": str(uuid.uuid4()),
                "name": name,
                "team_id": team_id,
                "project_type": department
            })
            
        return projects