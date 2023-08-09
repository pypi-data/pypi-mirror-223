
import sqlite3
from  datetime import datetime

class MeetingManager:
    def __init__(self, db_path="meeting_manager.db"):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY, name TEXT, active BOOLEAN)")
        cursor.execute("CREATE TABLE IF NOT EXISTS meetings (id INTEGER PRIMARY KEY, acta_person_id INTEGER, dynamizer_person_id INTEGER, meeting_datetime TEXT, FOREIGN KEY(acta_person_id) REFERENCES people(id), FOREIGN KEY(dynamizer_person_id) REFERENCES people(id))")
        connection.commit()
        connection.close()

    def add_person(self, name, active=True):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO people (name, active) VALUES (?, ?)", (name, active))
        connection.commit()
        connection.close()

    def update_person(self, person_id, name, active):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("UPDATE people SET name = ?, active = ? WHERE id = ?", (name, active, person_id))
        connection.commit()
        connection.close()

    def delete_person(self, person_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM people WHERE id = ?", (person_id,))
        connection.commit()
        connection.close()

    def get_people(self, active=False):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        if active:
            cursor.execute("SELECT * FROM people WHERE active = 1")
        else:
            cursor.execute("SELECT * FROM people")
        people = cursor.fetchall()
        connection.close()
        return people

    def next_meeting(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        # Get active persons
        
        active_persons = [p[0] for p in self.get_people(active=True)]
        print(active_persons)
        if len(active_persons) < 2:
            raise ValueError("Not enough active persons to schedule a meeting")
        # Find previous meeting's acta and dynamizer persons
        cursor.execute("SELECT acta_person_id, dynamizer_person_id FROM meetings ORDER BY id DESC LIMIT 1")
        prev_meeting = cursor.fetchone()
        if prev_meeting:
            prev_acta_person_id, prev_dynamizer_person_id = prev_meeting
            acta_person_id = self.find_next_person_id(prev_acta_person_id, active_persons)
            dynamizer_person_id = self.find_next_person_id(prev_dynamizer_person_id, active_persons, [acta_person_id])
        else:
            acta_person_id, dynamizer_person_id = active_persons[0], active_persons[1]
        # Insert new meeting
        meeting_datetime = datetime.now().isoformat()
        cursor.execute("INSERT INTO meetings (acta_person_id, dynamizer_person_id, meeting_datetime) VALUES (?, ?, ?)", (acta_person_id, dynamizer_person_id, meeting_datetime))
        connection.commit()
        connection.close()

    def find_next_person_id(self, person_id, active_persons, exclude_ids=[]):
        if person_id in active_persons:
            next_index = (active_persons.index(person_id) + 1) % len(active_persons)
        else:
            next_index = 0

        next_person_id = active_persons[next_index]
        while next_person_id in exclude_ids:
            next_index = (next_index + 1) % len(active_persons)
            next_person_id = active_persons[next_index]

        return next_person_id


    def get_current_meeting(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM meetings ORDER BY id DESC LIMIT 1")
        meeting = cursor.fetchone()
        connection.close()
        if meeting:
            acta_person_id, dynamizer_person_id, meeting_datetime = meeting[1], meeting[2], meeting[3]
            acta_person = self.get_person_name(acta_person_id)
            dynamizer_person = self.get_person_name(dynamizer_person_id)
            previous_acta_person_name, previous_dyna_person, previous_meeting_time = self.get_previous_meeting()
            
            return acta_person, dynamizer_person,meeting_datetime,previous_acta_person_name, previous_dyna_person, previous_meeting_time
        return None, None, None, None, None, None

    def delete_most_recent_meeting(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM meetings WHERE id = (SELECT MAX(id) FROM meetings)")
        connection.commit()
        connection.close()

    def get_person(self, person_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name, active FROM people WHERE id = ?", (person_id,))
        person = cursor.fetchone()
        connection.close()
        return person if person else None


    def get_person_name(self, person_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM people WHERE id = ?", (person_id,))
        name = cursor.fetchone()
        connection.close()
        return name if name else None

    def toggle_active(self, person_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT active FROM people WHERE id = ?", (person_id,))
        active = cursor.fetchone()[0]
        cursor.execute("UPDATE people SET active = ? WHERE id = ?", (not active, person_id))
        connection.commit()
        connection.close()

    def get_previous_meeting(self):
        """
        Retrieves the details of the previous meeting from the database.

        Returns:
            acta_person (str): The name of the person in charge of the minutes in the previous meeting.
            dynamizer_person (str): The name of the person acting as the dynamizer in the previous meeting.
            meeting_time (str): The date and time of the previous meeting.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        # Explicitly selecting the necessary columns
        cursor.execute("SELECT acta_person_id, dynamizer_person_id, meeting_datetime FROM meetings ORDER BY id DESC LIMIT 1 OFFSET 1")
        meeting = cursor.fetchone()
        connection.close()

        if meeting:
            acta_person = self.get_person_name(meeting[0]) or "-"
            minutes_person = [acta_person[0] if acta_person else "-"]
            minutestring = ''.join(minutes_person) # Cooode smeeeelllll!
            dyna_person = self.get_person_name(meeting[1])
            dynastring = ''.join(dyna_person) # Cooode smeeeelllll!
            dynamizer_person = [dyna_person[0] if dyna_person else "-"]

            meeting_time = meeting[2]
            return minutestring, dynastring, meeting_time

        return None, None, None

