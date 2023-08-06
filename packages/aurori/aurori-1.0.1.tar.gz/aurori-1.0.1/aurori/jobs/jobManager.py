"""
The aurori project

Copyright (C) 2022  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "aurori@fabba.space"
__credits__ = []
__license__ = "AGPLv3+"

import logging
from datetime import datetime
from apscheduler.schedulers.asyncio  import AsyncIOScheduler

from aurori.logs import logManager

class JobManager(object):
    """ The JobManager ...
    """
    def __init__(self, ):
        # preparation to instanciate
        self.config = None
        self.workspaceManager = None
        self.job_counter = 0
        self.jobs = {}
        self.scheduler = AsyncIOScheduler()
        logging.getLogger('apscheduler.scheduler').name = "SCHEDULER"
        logging.getLogger('apscheduler.executors.default').name = "EXECUTOR"

    def init_manager(self, config):
        self.config = config

    def get_jobs(self):
        return self.jobs

    def register_job(self, workspace, job_class, log_in_db=False):
        print("jobManager.register_job not implemented yet")

    def run_job(self,
                user,
                jobkey,
                args,
                date,
                max_instances=10,
                log_trigger=False):
        print("jobManager.run_job not implemented yet")
