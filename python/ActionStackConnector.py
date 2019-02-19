""" Used by the Rosie Agent to print information about the tasks Rosie is performing """
import sys
import vim
import traceback

from string import digits
from pysoarlib import AgentConnector

from VimWriter import VimWriter

def task_to_string(task_id):
    task_handle = task_id.GetChildString("task-handle")
    arg1_id = task_id.GetChildId("arg1")
    arg2_id = task_id.GetChildId("arg2")

    task = task_handle + "("
    if arg1_id != None:
        task += task_arg_to_string(arg1_id)
    if arg2_id != None:
        if arg1_id != None:
            task += ", "
        task += task_arg_to_string(arg2_id)
    task += ")"

    return task

def task_arg_to_string(arg_id):
    arg_type = arg_id.GetChildString("arg-type")
    if arg_type == "object":
        return obj_arg_to_string(arg_id.GetChildId("id"))
    elif arg_type == "predicate":
        handle_str = arg_id.GetChildString("handle")
        obj2_str = obj_arg_to_string(arg_id.GetChildId("2"))
        return "%s(%s)" % ( handle_str, obj2_str )
    elif arg_type == "waypoint":
        wp_id = arg_id.GetChildId("id")
        return wp_id.GetChildString("handle")
    elif arg_type == "concept":
        return arg_id.GetChildString("handle")
    return "?"

def obj_arg_to_string(obj_id):
    pred_order = [ ["size"], ["color"], ["name", "shape", "category"] ]
    preds_id = obj_id.GetChildId("predicates")
    obj_desc = ""
    for pred_list in pred_order:
        for pred in pred_list:
            pred_str = preds_id.GetChildString(pred)
            if pred_str:
                obj_desc += pred_str + " "
                break
    if len(obj_desc) > 0:
        obj_desc = obj_desc[:-1]

    return obj_desc.translate(str.maketrans('', '', digits))

class ActionStackConnector(AgentConnector):
    def __init__(self, agent, writer):
        AgentConnector.__init__(self, agent, print_handler=lambda message: writer.write(message, VimWriter.MAIN_PANE, clear=False, scroll=True))

        self.print_task = lambda message: writer.write(message, VimWriter.SIDE_PANE_MID, clear=False, scroll=True, strip=False)

        self.add_output_command("started-task")
        self.add_output_command("completed-task")

    def on_init_soar(self):
        pass

    def on_input_phase(self, input_link):
        pass

    def on_output_event(self, command_name, root_id):
        if command_name == "started-task":
            self.process_started_task(root_id)
        elif command_name == "completed-task":
            self.process_completed_task(root_id)

    def process_started_task(self, root_id):
        try:
            seg_id = root_id.GetChildId("segment")
            padding = "  " * (seg_id.GetChildInt("depth") - 1)
            task_id = seg_id.GetChildId("task-operator")
            self.print_task(padding + ">" + task_to_string(task_id))
        except:
            self.print_handler("Error Parsing Started Task")
            self.print_handler(traceback.format_exc())
        root_id.CreateStringWME("handled", "true")

    def process_completed_task(self, root_id):
        try:
            seg_id = root_id.GetChildId("segment")
            padding = "  " * (seg_id.GetChildInt("depth") - 1)
            task_id = seg_id.GetChildId("task-operator")
            self.print_task(padding + "<" + task_to_string(task_id))
        except:
            self.print_handler("Error Parsing Completed Task")
            self.print_handler(traceback.format_exc())
        root_id.CreateStringWME("handled", "true")
