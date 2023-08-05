# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkft.endpoint import endpoint_data

class CreateInsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ft', '2015-03-03', 'CreateIns')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_newparam1(self): # String
		return self.get_query_params().get('new-param-1')

	def set_newparam1(self, newparam1):  # String
		self.add_query_param('new-param-1', newparam1)
	def get_Bind(self): # String
		return self.get_query_params().get('Bind')

	def set_Bind(self, Bind):  # String
		self.add_query_param('Bind', Bind)
	def get_Test(self): # String
		return self.get_query_params().get('Test')

	def set_Test(self, Test):  # String
		self.add_query_param('Test', Test)
	def get_Success(self): # String
		return self.get_query_params().get('Success')

	def set_Success(self, Success):  # String
		self.add_query_param('Success', Success)
