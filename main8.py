import sqlite3
from random import randint, choice
from faker import Faker

con = sqlite3.connect('databasefile.db')
cur = con.cursor()
# SQL query that inserts a row of data in the relationships table.
for _ in range(100):
    add_relationship_query = """
        INSERT INTO relationships
        (
            person1_id,
            person2_id,
            type,
            start_date
        )
        VALUES (?, ?, ?, ?);
        """
    fake = Faker()
    # Randomly select first person in relationship
    person1_id = randint(1, 200)
    # Randomly select second person in relationship
    # Loop ensures person will not be in a relationship with themself
    person2_id = randint(1, 200)
    while person2_id == person1_id:
        person2_id = randint(1, 200)
    # Randomly select a relationship type
    rel_type = choice(('friend', 'spouse', 'partner', 'relative'))
    # Randomly select a relationship start date between now and 50 years ago
    start_date = fake.date_between(start_date='-50y', end_date='today')
    # Create tuple of data for the new relationship
    new_relationship = (person1_id, person2_id, rel_type, start_date)
    # Add the new relationship to the DB

    cur.execute(add_relationship_query, new_relationship)

all_relationships = """
    SELECT person1.name, person2.name, start_date, type FROM relationships
    JOIN people person1 ON person1_id = person1.id
    JOIN people person2 ON person2_id = person2.id;
"""
# Execute the query and get all results
cur.execute(all_relationships)
all_relationships = cur.fetchall()
# Print sentences describing each relationship
for person1, person2, start_date, type in all_relationships:
    print(f'{person1} has been a {type} of {person2} since {start_date}.')
con.commit()
con.close()
