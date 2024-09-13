"""Script to generate data for example organogram."""
import os
import pandas as pd
import random

# Set the random seed for reproducibility
random.seed(42)

# Create lists of sample names, teams, and divisions
names = ["Aisha", "Liam", "Yuki", "Sofia", "Raj", "Zoe", "Chen", "Fatima", "Diego", "Priya",
         "Kwame", "Ingrid", "Hassan", "Mei", "Alejandro", "Olga", "Jamal", "Sven", "Amara", "Nadia",
         "Ravi", "Astrid", "Tariq", "Valentina", "Kenji", "Aaliyah", "Magnus", "Zara", "Mateo", "Leila",
         "Dmitri", "Chiara", "Kwesi", "Yara", "Sanjay", "Freya", "Takeshi", "Amina", "Luca", "Anika",
         "Xavier", "Ines", "Rahul", "Nia", "Esteban", "Mia", "Hiroshi", "Soraya", "Thabo", "Emilia"]
teams = ["Sales", "Marketing", "Engineering", "HR", "Finance", "Customer Support", "Product", "Legal", "Operations"]
divisions = ["North America", "Europe", "Asia Pacific", "Latin America", "Global"]

# Hard-coded teams with their leaders
teams = {
    "Executive": ["CEO"],
    "Sales": ["Sales Director", "Sales Manager", "Sales Representative"],
    "Marketing": ["Marketing Director", "Marketing Manager", "Marketing Specialist"],
    "Engineering": ["CTO", "Engineering Manager", "Software Engineer"],
    "HR": ["HR Director", "HR Manager", "HR Specialist"],
    "Finance": ["CFO", "Finance Manager", "Accountant"],
}


# Function to generate a unique ID (unchanged)
def generate_id():
    return f"EMP{random.randint(1000, 9999)}"

# Create the DataFrame
data = []

# Add CEO first
ceo_id = generate_id()
ceo_name = random.choice(names)
ceo_division = random.choice(divisions)
data.append([ceo_id, ceo_name, "Executive", "CEO", ceo_division, "", ""])

# Process other roles
for team, roles in teams.items():
    for role in roles:
        if role == "CEO":
            continue  # Skip CEO as it's already added
        
        id = generate_id()
        name = random.choice(names)
        division = random.choice(divisions)
        
        if role.endswith("Director") or role in ["CTO", "CFO"]:
            manager_name = ceo_name
            manager_id = ceo_id
        else:
            potential_managers = [emp for emp in data if emp[2] == team and emp[3] != role]
            if potential_managers:
                manager = random.choice(potential_managers)
                manager_name = manager[1]
                manager_id = manager[0]
            else:
                # If no manager found, use the team leader (Director/CTO/CFO) as manager
                team_leader = next(emp for emp in data if emp[2] == team and (emp[3].endswith("Director") or emp[3] in ["CTO", "CFO"]))
                manager_name = team_leader[1]
                manager_id = team_leader[0]
        
        data.append([id, name, team, role, division, manager_name, manager_id])


# Fill remaining positions
while len(data) < 50:
    team, roles = random.choice(list(teams.items()))
    if team == "Executive":
        continue  # Skip Executive team as we don't want to add more CEOs
    
    # Choose a non-leadership role
    non_leadership_roles = [role for role in roles if not role.endswith("Director") and role not in ["CTO", "CFO"]]
    if not non_leadership_roles:
        continue  # Skip if no non-leadership roles available
    
    role = random.choice(non_leadership_roles)
    id = generate_id()
    name = random.choice(names)
    division = random.choice(divisions)
    
    # Find a manager in the same team
    potential_managers = [emp for emp in data if emp[2] == team and emp[3] != role]
    if not potential_managers:
        continue  # Skip if no potential managers found
    
    manager = random.choice(potential_managers)
    manager_name = manager[1]
    manager_id = manager[0]
    
    data.append([id, name, team, role, division, manager_name, manager_id])

# Ensure we have exactly 50 employees
while len(data) > 50:
    non_leadership = [emp for emp in data if not emp[3].endswith("Director") and emp[3] not in ["CEO", "CTO", "CFO"]]
    if non_leadership:
        data.remove(random.choice(non_leadership))
    else:
        break  # Avoid infinite loop if we can't remove any more employees

# Create the DataFrame
df = pd.DataFrame(data, columns=["ID", "name", "team", "role", "division", "manager_name", "managerID"])

pickle_path = os.path.join("data", "example_employee_data.pkl")
df.to_pickle(pickle_path)
