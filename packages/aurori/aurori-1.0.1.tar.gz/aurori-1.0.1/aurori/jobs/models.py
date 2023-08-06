from datetime import datetime
from aurori import db, bcrypt
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

from datetime import datetime
from sqlalchemy_utils import ArrowType

from aurori.types.jsonDict import JsonDict


class JobExecute(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default="")
    workspace = db.Column(db.String(120), default="")
    job = db.Column(db.String(120), default="")
    state = db.Column(db.String(120), default="")
    triggered_on = db.Column(db.DateTime, default=datetime.utcnow)
    triggered_by = db.Column(db.String(120), default="")
    lifetime = db.Column(db.Integer, default=0)
    args = db.Column(JsonDict)
    results = db.Column(JsonDict)

    def __repr__(self):
        return '<Job {} for {}/{} >'.format(self.name, self.workspace,
                                            self.job)
