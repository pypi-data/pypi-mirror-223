import os

from ciocore.validator import Validator
from ciokatana.v1.model import jobs_model
from ciokatana.v1 import const as k
from cioseq.sequence import Sequence

        
from ciocore import data as coredata
from ciokatana.v1.model import hardware_model
        
# class ValidateSceneExists(Validator):
#     def run(self, _):
#         filepath = rt.maxFilePath + rt.maxFileName
#         if not filepath:
#             self.add_error("This file has never been saved. Please give it a name and try again.")

class ValidateInstanceType(Validator):
    def run(self, _):
        hardware = coredata.data()["instance_types"]
        instance_type_name = hardware_model.get_value(self._submitter)
        instance_type = hardware.find(instance_type_name)
        gpu = instance_type.get("gpu")
        desc = instance_type.get("description")
        if gpu:
            self.add_warning("You have selected a GPU instance type ({}), but the selected renderer cannot make use of a graphics card. This is likely to incur unwanted costs. Please consider using a CPU instance type instead.".format(desc)) 


class ValidateTasks(Validator):
    def run(self, _):
        frame_data = list(jobs_model.resolve_overrides(self._submitter))
        self._validate_chunk_size(frame_data)
        self._validate_task_count(frame_data)

    def _validate_chunk_size(self, frame_data):
        high_chunk_nodes = []
        for data in frame_data:
            if data["chunk_size"] > 1:
                high_chunk_nodes.append(data["render_node"])
        if high_chunk_nodes:
            nodes = ", ".join([n.getName() for n in high_chunk_nodes])
            msg = (
                "The following nodes have a chunk size greater than 1:\n[{}]\n".format(
                    nodes
                )
            )
            msg += "Your render may take longer than necessary."
            msg += "We recommend setting chunk size to 1 for 3D work."
            self.add_notice(msg)

    def _validate_task_count(self, frame_data):
        high_task_count_messages = []
        for data in frame_data:
            sequence = Sequence.create(
                data["frame_spec"], chunk_size=data["chunk_size"]
            )
            num_tasks = len(sequence.chunks())
            if num_tasks > k.MAX_TASKS:
                high_task_count_messages.append(
                    f"{data['render_node'].getName() }: ({num_tasks} tasks)"
                )

        if high_task_count_messages:
            msg = (
                f"The following nodes have more than the maximum ({k.MAX_TASKS}) tasks:"
            )
            high_task_count_messages = [msg] + high_task_count_messages
            high_task_count_messages.append(
                "Please increase the chunk size or reduce the number of frames."
            )
            high_task_count_messages = "\n".join(high_task_count_messages)
            self.add_error(high_task_count_messages)


# class ValidateDummy(Validator):
#     def run(self, _):
#         self.add_notice("This is a notice about nothing.")
#         self.add_warning("This is a warning about nothing.")
#         # self.add_error("This is an error about nothing.")



# Implement more validators here
####################################
####################################


def run(dialog):
    validators = [plugin(dialog) for plugin in Validator.plugins()]

    for validator in validators:
        validator.run(None)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices
