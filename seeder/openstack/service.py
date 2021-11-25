"""
 Copyright 2021 SAP SE
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import logging
from seeder.seed_type_registry import BaseRegisteredSeedTypeClass
from seeder.openstack.openstack_helper import OpenstackHelper
from urllib.parse import urlparse

class Service(BaseRegisteredSeedTypeClass):
    def __init__(self, args, session):
        self.opentack = OpenstackHelper(args, session)

    def seed(self, spec):
        logging.info('seeding services')
        if 'services' in spec:
            for service in spec['services']:
                self.seed_service(service)


    def seed_service(service, keystone):
        """ seed a keystone service """