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


class Region(BaseRegisteredSeedTypeClass):
    def __init__(self, args, session):
        self.opentack = OpenstackHelper(args, session)
   
    def seed(self, spec):
        logging.info('seeding regions')
        if 'regions' in spec:
            # seed parent regions
            for region in spec['regions']:
                if 'parent_region' not in region:
                    self._seed_region(region)
            # seed child regions
            for region in spec['regions']:
                if 'parent_region' in region:
                    self._seed_region(region)

    def _seed_region(self, region):
        """ seed a keystone region """
        logging.debug("seeding region %s" % region)

        region = self.opentack.sanitize(region,
                        ('id', 'description', 'parent_region'))
        if 'id' not in region or not region['id']:
            logging.warn(
                "skipping region '%s', since it is misconfigured" % region)
            return

        try:
            result = self.openstack.get_keystone().regions.get(region['id'])
        except self.openstack.get_keystone().exception.NotFound:
            result = None

        if not result:
            logging.info("create region '%s'" % region['id'])
            self.openstack.get_keystone().regions.create(**region)
        else:  # wtf: why can't they deal with parent_region(_id) consistently
            wtf = region.copy()
            if 'parent_region' in wtf:
                wtf['parent_region_id'] = wtf.pop('parent_region')
            for attr in list(wtf.keys()):
                if wtf[attr] != result._info.get(attr, ''):
                    logging.info(
                        "%s differs. update region '%s'" % (attr, region))
                    self.openstack.get_keystone().regions.update(result.id, **region)
                    break