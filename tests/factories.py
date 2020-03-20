# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Test Factory makes fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Inventory
import random

class InventoryFactory(factory.Factory):
    """ Creates fake inventory items """

    class Meta:
        model = Inventory

    id = factory.Sequence (lambda n: n)
    name = factory.Faker("first_name")
    sku = factory.Faker("last_name") 
    quantity = random.randint(0,100)
    if random.random() < .5: #Only set some, adjust % as needed.
        restockLevel = random.randint(0,10) # OPTIONAL Level at which we will need to restock the item.

if __name__ == "__main__":
    for _ in range(10):
        inventory = InventoryFactory()
        print(inventory.serialize())