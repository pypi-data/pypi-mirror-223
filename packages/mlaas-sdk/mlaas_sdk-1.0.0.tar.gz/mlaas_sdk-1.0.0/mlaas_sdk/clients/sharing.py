# Copyright 2023, Atos Spain S.A.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from .base import BaseClient
from ..exceptions.sharing import *
from ..models import DatasetContract, ModelContract, ModelContractUnverified

import requests


class SharingClient(BaseClient):
    def __init__(self, sharing_endpoint: str, secure: bool = False):
        super().__init__(sharing_endpoint, secure)

    def get_model(self, model_id: str) -> requests.Response:
        try:
            return requests.get(self.build_url("model", model_id), stream=True)
        except requests.exceptions.RequestException as e:
            raise ModelNotFoundException(model_id)

    def get_dataset(self, dataset_id: str) -> requests.Response:
        try:
            return requests.get(
                self.build_url("dataset", dataset_id), stream=True
            )
        except requests.exceptions.RequestException as e:
            raise DatasetNotFoundException(dataset_id)

    def get_model_metadata(self, model_id: str) -> ModelContract:
        try:
            return ModelContract.parse_raw(
                requests.get(
                    self.build_url("model", model_id, "metadata")
                ).content
            )
        except requests.exceptions.RequestException as e:
            raise ModelException(model_id)

    def add_model(self, model: ModelContract) -> str:
        try:
            return requests.post(
                self.build_url("model"),
                json=model.dict(exclude_none=True),
            ).json()["model_id"]
        except requests.exceptions.RequestException as e:
            raise ModelRegistrationException()

    def add_model_unverified(self, model: ModelContractUnverified) -> str:
        try:
            return requests.post(
                self.build_url("model", "unverified"),
                json=model.dict(exclude_none=True),
            ).json()["model_id"]
        except requests.exceptions.RequestException as e:
            raise ModelRegistrationException()

    def add_dataset(self, dataset: DatasetContract) -> str:
        try:
            return requests.post(
                self.build_url("dataset"),
                json=dataset.dict(exclude_none=True),
            ).json()["dataset_id"]
        except requests.exceptions.RequestException as e:
            raise DatasetRegistrationException()

    def update_model(self, model_id: str, model: str) -> None:
        try:
            requests.put(
                self.build_url("model", model_id),
                files={
                    "model": (model.split("/")[-1], open(model, "rb")),
                },
            )
        except requests.exceptions.RequestException as e:
            raise ModelUpdateException(model_id)
