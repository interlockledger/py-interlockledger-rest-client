# Copyright (c) 2024, InterlockLedger Network
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from unittest import TestCase
from src.pyil2.client import IL2Client
import os


class BaseApiTest(TestCase):
    def setUp(self):
        self.filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.password = os.environ.get('TEST_CERTIFICATE_PASS')
        self.host = os.environ.get('TEST_HOST')
        self.default_chain = os.environ.get('TEST_DEFAULT_CHAIN')
        self.second_chain = os.environ.get('TEST_SECOND_CHAIN')

        if not self.filepath or not self.password or not self.host or not self.default_chain:
            self.skipTest(
                'Skipping TEST_CERTIFICATE_PATH or TEST_CERTIFICATE_PASS or TEST_HOST or TEST_DEFAULT_CHAIN are not set as environment variables.')

        self.client = IL2Client(
            host=self.host,
            cert_filepath=self.filepath,
            cert_password=self.password,
            timeout=100,
            verify_ca=False,
        )
