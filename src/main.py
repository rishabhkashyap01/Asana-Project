import os
import uuid
import random
import logging
from utils.db_helpers import DatabaseHelper
from generators.users import UserGenerator
from generators.projects import ProjectGenerator
from generators.tasks import TaskGenerator

class AsanaSimulationOrchestrator:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        output_dir = os.path.join(base_dir, "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        db_path = os.path.join(output_dir, "asana_simulation.sqlite")
        self.db = DatabaseHelper(db_path=db_path)
        
        self.user_gen = UserGenerator()
        self.proj_gen = ProjectGenerator()
        self.task_gen = TaskGenerator()

    def initialize_env(self):
        if os.path.exists(self.db.db_path):
            os.remove(self.db.db_path)
            print(f"Removed existing database.")
        
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schema.sql")
        self.db.execute_script(schema_path)

    def run(self, user_count=5000):
        print(f"🚀 Starting Simulation for {user_count} users...")
        self.initialize_env()

        # 1. Create Organization
        org_id = str(uuid.uuid4())
        self.db.execute("INSERT INTO organizations (organization_id, name, domain) VALUES (?, ?, ?)",
                        (org_id, "Acme Global Tech", "acme-tech.ai"))
        
        # 2. Generate Global Tags
        tags = [("Urgent", "red"), ("Blocked", "yellow"), ("Refactor", "blue"), ("Low Priority", "green")]
        tag_ids = []
        for name, color in tags:
            tid = str(uuid.uuid4())
            self.db.execute("INSERT INTO tags (tag_id, name, color) VALUES (?, ?, ?)", (tid, name, color))
            tag_ids.append(tid)

        # 3. Generate Users
        users = self.user_gen.generate_batch(user_count)
        user_ids = [] # Initialize outside the block
        if users:
            columns = users[0].keys()
            data_list = [list(u.values()) for u in users]
            self.db.batch_insert("users", columns, data_list)
            user_ids = [u['user_id'] for u in users] # Now accessible to Step 4

        # 4. Create Teams & Memberships
        team_definitions = [("Engineering", "Core Product"), ("Marketing", "Growth"), ("Sales", "Enterprise")]
        for t_name, t_desc in team_definitions:
            t_id = str(uuid.uuid4())
            self.db.execute("INSERT INTO teams (team_id, organization_id, name, description) VALUES (?,?,?,?)",
                            (t_id, org_id, t_name, t_desc))
            
            # Use min() to prevent sampling more users than exist
            team_users = random.sample(user_ids, min(20, len(user_ids)))
            for u_id in team_users:
                self.db.execute("INSERT INTO team_memberships (membership_id, team_id, user_id) VALUES (?,?,?)",
                                (str(uuid.uuid4()), t_id, u_id))

            # 5. Create Projects & Sections
            projects = self.proj_gen.generate_for_team(t_id, t_name)
            for p in projects:
                self.db.execute("INSERT INTO projects (project_id, team_id, name, project_type) VALUES (?,?,?,?)",
                                (p['project_id'], t_id, p['name'], t_name))
                
                section_ids = []
                for s_name in ["Backlog", "In Progress", "Review", "Done"]:
                    s_id = str(uuid.uuid4())
                    self.db.execute("INSERT INTO sections (section_id, project_id, name) VALUES (?,?,?)",
                                    (s_id, p['project_id'], s_name))
                    section_ids.append(s_id)

                # 6. Generate Tasks, Subtasks, and Associations
                tasks, tag_links = self.task_gen.create_tasks_for_project(
                    p['project_id'], t_name, team_users, section_ids, tag_ids
                )
                
                if tasks:
                    # Explicitly define columns to match schema.sql
                    task_cols = ["task_id", "project_id", "section_id", "assignee_id", "parent_task_id", "name", "description", "priority", "due_date"]
                    self.db.batch_insert("tasks", task_cols, [list(t.values()) for t in tasks])

                if tag_links:
                    self.db.batch_insert("task_tags", ["task_id", "tag_id"], [list(link.values()) for link in tag_links])

        self._audit_and_report()

    def _audit_and_report(self):
        def q(sql): 
            with self.db.get_connection() as conn:
                res = conn.execute(sql).fetchone()
                return res[0] if res else 0
        
        counts = {
            "orgs": q("SELECT COUNT(*) FROM organizations"),
            "users": q("SELECT COUNT(*) FROM users"),
            "teams": q("SELECT COUNT(*) FROM teams"),
            "memberships": q("SELECT COUNT(*) FROM team_memberships"),
            "projects": q("SELECT COUNT(*) FROM projects"),
            "sections": q("SELECT COUNT(*) FROM sections"),
            "tasks": q("SELECT COUNT(*) FROM tasks WHERE parent_task_id IS NULL"),
            "subtasks": q("SELECT COUNT(*) FROM tasks WHERE parent_task_id IS NOT NULL"),
            "tags": q("SELECT COUNT(*) FROM tags"),
            "comments": q("SELECT COUNT(*) FROM comments"),
            "task_tags": q("SELECT COUNT(*) FROM task_tags")
        }
        self._print_summary(counts)

    def _print_summary(self, counts):
        print("✅ WORK GRAPH SIMULATION COMPLETE")
        print(" ="*25)
        for key, val in counts.items():
            print(f"{key.capitalize():<25} {val}")
        print("-" * 45)
        print(f"{'Database Engine:':<25} SQLite 3")
        print(f"{'Output Path:':<25} {self.db.db_path}")
        print(" ="*25 + "\n")

if __name__ == "__main__":
    orchestrator = AsanaSimulationOrchestrator()
    orchestrator.run(user_count=5000)