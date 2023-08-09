import pytest
import os
from meeting_roles.meeting_manager import MeetingManager


def setup_function():
    # Delete any existing test database before each test
    if os.path.exists("test_meeting_manager.db"):
        os.remove("test_meeting_manager.db")

def test_initialization_and_table_creation():
    mm = MeetingManager("test_meeting_manager.db")
    assert os.path.exists("test_meeting_manager.db") == True

def test_adding_people():
    mm = MeetingManager("test_meeting_manager.db")
    mm.add_person("Alice")
    people = mm.get_people()
    assert len(people) == 1
    assert people[0][1] == "Alice"
    assert people[0][2] == True

def test_updating_people():
    mm = MeetingManager("test_meeting_manager.db")
    mm.add_person("Alice")
    mm.update_person(1, "Alicia", False)
    person = mm.get_people()[0]
    assert person[1] == "Alicia"
    assert person[2] == False

def test_deleting_people():
    mm = MeetingManager("test_meeting_manager.db")
    mm.add_person("Alice")
    mm.delete_person(1)
    assert len(mm.get_people()) == 0

def test_getting_people():
    mm = MeetingManager("test_meeting_manager.db")
    mm.add_person("Alice")
    mm.add_person("Bob")
    assert len(mm.get_people()) == 2

def test_next_meeting():
    mm = MeetingManager("test_meeting_manager.db")
    mm.add_person("Alice")
    mm.add_person("Bob")
    mm.next_meeting() # Should not raise an error

def test_next_meeting_not_enough_people():
    mm = MeetingManager("test_meeting_manager.db")
    mm.add_person("Alice")
    with pytest.raises(ValueError):
        mm.next_meeting()
