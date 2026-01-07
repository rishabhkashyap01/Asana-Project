import uuid
import random
import time
from utils.llm_helper import LLMHelper

class TaskGenerator:
    def __init__(self):
        self.llm = LLMHelper()
        self.priorities = ["High", "Medium", "Low", "None"]

    def create_tasks_for_project(self, project_id, p_type, user_ids, section_ids, tag_ids):
        tasks_to_insert = []
        tag_links_to_insert = [] # New: To handle many-to-many relationships
        
        for i in range(20):  # 20 Main Tasks per project
            task_id = str(uuid.uuid4())
            assignee = random.choice(user_ids)
            section = random.choice(section_ids)
            
            # Realism: Better task naming
            name = f"{p_type} Phase {random.randint(1,5)}: Task {i+1}"
            
            # Main Task
            main_task = {
                "task_id": task_id,
                "project_id": project_id,
                "section_id": section,
                "assignee_id": assignee,
                "parent_task_id": None,
                "name": name,
                "description": self.llm.generate_task_description(name, p_type) if i < 1 else "Standard task.",
                "priority": random.choice(self.priorities),
                "due_date": "2026-03-15" # You can add date logic here later
            }
            tasks_to_insert.append(main_task)

            # 7. Relational Consistency: Subtasks
            if random.random() > 0.7:
                for j in range(random.randint(1, 3)):
                    sub_id = str(uuid.uuid4())
                    tasks_to_insert.append({
                        "task_id": sub_id,
                        "project_id": project_id,
                        "section_id": section,
                        "assignee_id": random.choice(user_ids),
                        "parent_task_id": task_id,
                        "name": f"Subtask {j+1}: {name}",
                        "description": "Granular action item for parent task.",
                        "priority": random.choice(self.priorities),
                        "due_date": None
                    })

            # 8. Task-Tag Association (Many-to-Many)
            # Logic: Assign 1-2 random tags to each main task
            selected_tags = random.sample(tag_ids, random.randint(1, 2))
            for t_id in selected_tags:
                tag_links_to_insert.append({
                    "task_id": task_id,
                    "tag_id": t_id
                })

        return tasks_to_insert, tag_links_to_insert # Return both lists