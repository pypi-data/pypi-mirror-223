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

class RpcNoDefaultErrorCodeApiRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ft', '2015-03-03', 'RpcNoDefaultErrorCodeApi')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_HttpMe(self): # String
		return self.get_query_params().get('HttpMe')

	def set_HttpMe(self, HttpMe):  # String
		self.add_query_param('HttpMe', HttpMe)
	def get_HttpStatusCode(self): # String
		return self.get_query_params().get('HttpStatusCode')

	def set_HttpStatusCode(self, HttpStatusCode):  # String
		self.add_query_param('HttpStatusCode', HttpStatusCode)
	def get_SetUser(self): # String
		return self.get_query_params().get('SetUser')

	def set_SetUser(self, SetUser):  # String
		self.add_query_param('SetUser', SetUser)
	def get_Code(self): # String
		return self.get_query_params().get('Code')

	def set_Code(self, Code):  # String
		self.add_query_param('Code', Code)
	def get_Success(self): # String
		return self.get_query_params().get('Success')

	def set_Success(self, Success):  # String
		self.add_query_param('Success', Success)
	def get_Message(self): # String
		return self.get_query_params().get('Message')

	def set_Message(self, Message):  # String
		self.add_query_param('Message', Message)
