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

from ondewo.vtsi import projects_pb2
from ondewo.vtsi.projects_pb2_grpc import ProjectsStub


class Projects(BaseServicesInterface):

    @property
    def stub(self) -> ProjectsStub:
        stub: ProjectsStub = ProjectsStub(channel=self.grpc_channel)
        return stub

    def create_vtsi_project(
        self,
        request: projects_pb2.CreateVtsiProjectRequest
    ) -> projects_pb2.CreateVtsiProjectResponse:
        return self.stub.CreateVtsiProject(request=request)

    def get_vtsi_project(
        self,
        request: projects_pb2.GetVtsiProjectRequest
    ) -> projects_pb2.VtsiProject:
        return self.stub.GetVtsiProject(request=request)

    def update_vtsi_project(
        self,
        request: projects_pb2.UpdateVtsiProjectRequest
    ) -> projects_pb2.UpdateVtsiProjectResponse:
        return self.stub.UpdateVtsiProject(request=request)

    def delete_vtsi_project(
        self,
        request: projects_pb2.DeleteVtsiProjectRequest
    ) -> projects_pb2.DeleteVtsiProjectResponse:
        return self.stub.DeleteVtsiProject(request=request)

    def deploy_vtsi_project(
        self,
        request: projects_pb2.DeployVtsiProjectRequest
    ) -> projects_pb2.DeployVtsiProjectResponse:
        return self.stub.DeployVtsiProject(request=request)

    def undeploy_vtsi_project(
        self,
        request: projects_pb2.UndeployVtsiProjectRequest
    ) -> projects_pb2.UndeployVtsiProjectResponse:
        return self.stub.UndeployVtsiProject(request=request)

    def list_vtsi_projects(
        self,
        request: projects_pb2.ListVtsiProjectsRequest
    ) -> projects_pb2.ListVtsiProjectsResponse:
        return self.stub.ListVtsiProjects(request=request)
