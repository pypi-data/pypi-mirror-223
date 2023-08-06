# Copyright 2021 ONDEWO GmbH
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
from ondewo.utils.base_services_interface import BaseServicesInterface

from ondewo.vtsi import calls_pb2
from ondewo.vtsi.calls_pb2_grpc import CallsStub


class Calls(BaseServicesInterface):

    @property
    def stub(self) -> CallsStub:
        stub: CallsStub = CallsStub(channel=self.grpc_channel)
        return stub

    def start_caller(
        self,
        request: calls_pb2.StartCallerRequest
    ) -> calls_pb2.StartCallerResponse:
        return self.stub.StartCaller(request=request)

    def start_callers(
        self,
        request: calls_pb2.StartCallersRequest
    ) -> calls_pb2.StartCallersResponse:
        return self.stub.StartCallers(request=request)

    def start_listener(
        self,
        request: calls_pb2.StartListenerRequest
    ) -> calls_pb2.StartListenerResponse:
        return self.stub.StartListener(request=request)

    def start_listeners(
        self,
        request: calls_pb2.StartListenersRequest
    ) -> calls_pb2.StartListenersResponse:
        return self.stub.StartListeners(request=request)

    def start_scheduled_caller(
        self,
        request: calls_pb2.StartScheduledCallerRequest
    ) -> calls_pb2.StartScheduledCallerResponse:
        return self.stub.StartScheduledCaller(request=request)

    def start_scheduled_callers(
        self, request: calls_pb2.StartScheduledCallersRequest
    ) -> calls_pb2.StartScheduledCallersResponse:
        return self.stub.StartScheduledCallers(request=request)

    def stop_call(
        self,
        request: calls_pb2.StopCallRequest
    ) -> calls_pb2.StopCallResponse:
        return self.stub.StopCall(request=request)

    def stop_calls(
        self, request:
        calls_pb2.StopCallsRequest
    ) -> calls_pb2.StopCallsResponse:
        return self.stub.StopCalls(request=request)

    def stop_all_calls(
        self,
        request: calls_pb2.StopAllCallsRequest
    ) -> calls_pb2.StopCallsResponse:
        return self.stub.StopAllCalls(request=request)

    def transfer_call(
        self,
        request: calls_pb2.TransferCallRequest
    ) -> calls_pb2.TransferCallResponse:
        return self.stub.TransferCall(request=request)

    def transfer_calls(
        self,
        request: calls_pb2.TransferCallsRequest
    ) -> calls_pb2.TransferCallsResponse:
        return self.stub.TransferCalls(request=request)

    def get_vtsi_call_info(
        self,
        request: calls_pb2.GetCallInfoRequest
    ) -> calls_pb2.GetCallInfoResponse:
        return self.stub.GetCallInfo(request=request)

    def list_vtsi_call_info(
        self,
        request: calls_pb2.ListCallInfoRequest
    ) -> calls_pb2.ListCallInfoResponse:
        return self.stub.ListCallInfo(request=request)

    def get_audio_file(
        self,
        request: calls_pb2.GetAudioFileRequest
    ) -> calls_pb2.GetAudioFileResponse:
        return self.stub.GetAudioFile(request=request)

    def get_full_conversation_audio_file(
        self,
        request: calls_pb2.GetFullConversationAudioFileRequest
    ) -> calls_pb2.GetFullConversationAudioFileResponse:
        return self.stub.GetFullConversationAudioFile(request=request)
