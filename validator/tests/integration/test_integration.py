# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import traceback
import unittest
import os

from txnintegration.integer_key_load_cli import IntKeyLoadTest
from txnintegration.validator_network_manager import get_default_vnm

ENABLE_OVERNIGHT_TESTS = False
if os.environ.get("ENABLE_OVERNIGHT_TESTS", False) == "1":
    ENABLE_OVERNIGHT_TESTS = True


class TestIntegration(unittest.TestCase):
    @unittest.skipUnless(ENABLE_OVERNIGHT_TESTS, "integration test")
    def test_intkey_load_ext(self):
        vnm = None
        try:
            print "Launching validator network."
            vnm = get_default_vnm(5)
            vnm.do_genesis()
            vnm.launch()
            print "Testing transaction load."
            test = IntKeyLoadTest()
            test.setup(vnm.urls(), 10)
            test.run(1)
            test.run_with_missing_dep(1)
            test.validate()
        finally:
            if vnm is not None:
                vnm.shutdown(archive_name="TestIntegrationResults_0")

    @unittest.skipUnless(ENABLE_OVERNIGHT_TESTS,
                         "limit of missing dependencies test")
    def test_missing_dependencies(self):
        vnm = None
        try:
            print "Launching validator network."
            vnm = get_default_vnm(5)
            vnm.do_genesis()
            vnm.launch()

            print "Testing limit of missing dependencies."
            test = IntKeyLoadTest()
            test.setup(vnm.urls(), 10)
            test.run(1)
            test.run_with_limit_txn_dependencies(1)
            test.validate()
        finally:
            if vnm is not None:
                vnm.shutdown(archive_name="TestIntegrationResults_1")
