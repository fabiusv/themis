from pymstodo import ToDoConnection
from dotenv import load_dotenv, find_dotenv, set_key
import json
from datetime import datetime
import os
import pytz


class MS_Todo():
    def __init__(self):
        load_dotenv()
        client_id = os.getenv("client_id_ms_graph")
        client_secret = os.getenv("client_secret_ms_graph")
        token = json.loads(os.getenv("ms_graph_oauth"))
        self.todo_client = ToDoConnection(client_id=client_id, client_secret=client_secret, token=token)
    def get_lists(self):
        lists = self.todo_client.get_lists()
        ci = 0
        formatted_result = ""
        for list in lists:
            formatted_result += f"{list} / List Index: {ci}\n"
            ci += 1
        return lists

    def get_tasks(self, list_index=0, due_date_str="heute"):
        lists = self.todo_client.get_lists()
        task_list = lists[list_index]

        print(datetime.now(pytz.utc))
        if due_date_str == "heute":
            due_date_str = datetime.now(pytz.utc).replace(hour=23, minute=59, second=59)
            print(due_date_str)
        elif due_date_str == "morgen":
            due_date_str = (datetime.now(pytz.utc) + datetime.timedelta(days=1))
        elif due_date_str == "woche":
            due_date_str = (datetime.now(pytz.utc) + datetime.timedelta(days=7))
        elif due_date_str == "Monat":
            due_date_str = (datetime.now(pytz.utc) + datetime.timedelta(days=30))
        elif due_date_str == "überfällig":
            due_date_str = (datetime.now(pytz.utc) - datetime.timedelta(days=1))

        tasks = self.todo_client.get_tasks(task_list.list_id)
        
        #filter tasks by due date, aceppt only tasks that are due before due_date_str
        tasks = [task for task in tasks if task.due_date if task.due_date <= due_date_str]

        return tasks
    
#print(MS_Todo().get_tasks())