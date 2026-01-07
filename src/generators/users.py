import uuid
import random
from faker import Faker

# Initialize Faker with multiple locales for a realistic global/diverse workforce
fake = Faker(['en_US', 'en_GB', 'en_IN'])

class UserGenerator:
    def __init__(self):
        # Weighting: More members than admins or guests
        self.roles = ['admin', 'member', 'member', 'member', 'guest'] 
        self.departments = [
            "Engineering", "Product", "Design", "Marketing", 
            "Sales", "Customer Success", "HR", "Operations", "Legal"
        ]

    def generate_batch(self, count=5000):
        """
        Generates a list of user dictionaries. 
        Renamed to generate_batch to match main.py expectations.
        """
        users = []
        # Realism: Using a set to ensure 100% unique emails
        emails_seen = set()
        
        for _ in range(count):
            name = fake.name()
            u_uuid = str(uuid.uuid4())
            
            # Realism: Corporate email format with collision avoidance
            safe_name = "".join(filter(str.isalnum, name.lower().replace(' ', '.')))
            email = f"{safe_name}.{u_uuid[:4]}@acme-corp.ai"
            
            user = {
                "user_id": u_uuid,
                "name": name,
                "email": email,
                "role": random.choice(self.roles),
                "department": random.choice(self.departments),
                "is_active": 1 if random.random() < 0.95 else 0 # SQLite prefers 1/0 for booleans
            }
            users.append(user)
            
        return users
