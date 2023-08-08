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

from typing import Literal, Union

from .base import BaseClient
from ..exceptions.blockchain import *
from ..models import DatasetContract, ModelContract, ModelContractUnverified

import requests


class BlockchainClient(BaseClient):
    def __init__(self, blockchain_endpoint: str, secure: bool = False):
        super().__init__(blockchain_endpoint, secure)

    def read_contract(
        self,
        contract_type: Literal["model", "model_unverified", "dataset"],
        contract_address: str,
    ) -> Union[DatasetContract, ModelContract, ModelContractUnverified]:
        try:
            res = requests.get(
                self.build_url("contract", contract_type, contract_address)
            ).content
            match contract_type:
                case "model":
                    return ModelContract.parse_raw(res)
                case "model_unverified":
                    return ModelContractUnverified.parse_raw(res)
                case "dataset":
                    return DatasetContract.parse_raw(res)
                case _:
                    raise ContractNotFoundException(contract_address)
        except requests.exceptions.RequestException as e:
            raise ContractNotFoundException(contract_address)

    def verify_contract(self, contract_address: str, res_hash: str) -> None:
        try:
            requests.post(
                self.build_url("contract", contract_address, "verify"),
                params={"res_hash": res_hash},
            )
        except requests.exceptions.RequestException as e:
            raise ContractVerificationException(contract_address)

    def deploy_contract(
        self,
        contract_type: Literal["model", "model_unverified", "dataset"],
        payload: Union[
            DatasetContract, ModelContract, ModelContractUnverified
        ],
    ) -> str:
        try:
            return requests.post(
                self.build_url("contract", contract_type),
                json=payload.dict(exclude_none=True),
            ).json()["contract_address"]
        except requests.exceptions.RequestException as e:
            raise ContractDeploymentException(payload)
