import time
import os
import shutil
import json
import re
from qaseio.commons.models.result import Result
from qaseio.commons.models.run import Run
from qaseio.commons.models.attachment import Attachment
from qaseio.commons.utils import QaseUtils
from typing import Optional

class QaseReport:
    def __init__(
        self, 
        report_path: Optional[str] = "build/qase-report",
        format: Optional[str] = "json",
        environment: Optional[str] = None
    ):
        self.report_path = report_path
        if not format:
            self.format = "json"
        else:
            self.format = format
        
        self.start_time = None
        self.end_time = None
        self.run_id = None
        self.environment = environment

        pass

    def start_run(self):
        self._check_report_path()
        self.start_time = str(time.time())
        pass

    def complete_run(self, is_main: bool=True, exit_code = None):
        if (is_main):
            self.end_time = str(time.time())
            self._compile_report()
        else:
            pass

    def add_result(self, result: Result):
        result.set_run_id(self.run_id)
        for attachment in result.attachments:
            self._persist_attachment(attachment)

        if result.steps:
            self._persist_attachments_in_steps(result.steps)

        self._store_result(result)

    def _persist_attachment(self, attachment: Attachment):
        if attachment.content:
            if isinstance(attachment.content, str):
                mode = "w"
            if isinstance(attachment.content, bytes):
                mode = "wb"
            with open(f"{self.report_path}/attachments/{attachment.id}-{attachment.file_name}", mode) as f:
                f.write(attachment.content)
            # Clear content to save memory and avoid double writing
            attachment.content = None
        elif attachment.file_path:
            shutil.copy2(os.path.abspath(attachment.file_path), f"{self.report_path}/attachments/{attachment.id}-{attachment.file_name}")

    def _persist_attachments_in_steps(self, steps: list):
        for step in steps:
            if step.attachments:
                for attachment in step.attachments:
                    self._persist_attachment(attachment)
                if step.steps:
                    self._persist_attachments_in_steps(step.steps)

    def add_attachment(self, attachment: Attachment) -> None:
        self.attachments.append(attachment)

    # Method saves result to a file
    def _store_result(self, result: Result):
        self._store_object(result, self.report_path+"/results/", result.id)

    def _check_report_path(self):
        for path in [self.report_path, self.report_path+"/results/", self.report_path+"/attachments/"]:
            self._recreate_dir(path)

    def _recreate_dir(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    def _update_run_duration(self, time):
        self.duration += time
        
    # Method builds final report
    def _compile_report(self):
        run = Run(
            title = "Test run",
            start_time=float(self.start_time),
            end_time=float(self.end_time),
            environment=self.environment
        )
        for file in os.listdir(self.report_path+"/results"):
            with open(self.report_path+"/results/"+file, 'r') as source:
                result = self._read_object(source)
                run.add_result(result)

        run.add_host_data(QaseUtils.get_host_data())
        
        self._store_object(run, self.report_path, "report")

    # Saves a model to a file
    def _store_object(self, object, path, filename):
        data = object.to_json()
        if (self.format == 'jsonp'):
            data = f"qaseJsonp({data});"
        with open(f"{path}/{filename}.{self.format}", 'w', encoding='utf-8') as f:
            f.write(data)

    def _read_object(self, source):
        data = source.read()
        if (self.format == 'json'):
            return json.loads(data)
        elif (self.format == 'jsonp'):
            jsonp_pattern = r'\w+\(\s*({[\s\S]*})\s*\);'
            match = re.search(jsonp_pattern, data)
            if match:
                data = match.group(1)
                return json.loads(data)
            else:
                raise ValueError('Invalid JSONP format')
        raise ValueError('Unknown format')
