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

from .MLaaSException import MLaaSException


class BlockchainException(MLaaSException):
    """Base exception for Blockchain client."""

    pass


class ContractException(BlockchainException):
    """Base exception for smart contract interactions."""

    pass


class ContractNotFoundException(ContractException):
    def __init__(self, address):
        message = (
            "Smart contract was not found in the blockchain instance.\n"
            f"Contract address: {address}"
        )
        self.address = address
        super().__init__(message)


class ContractVerificationException(ContractException):
    def __init__(self, address):
        message = (
            "Exception occurred when trying to veify the smart contract (may have already been verified).\n"
            f"Contract address: {address}"
        )
        self.address = address
        super().__init__(message)


class ContractDeploymentException(ContractException):
    def __init__(self, payload):
        message = (
            "Exception occurred when trying to deploy smart contract.\n"
            f"Contract payload: {payload}"
        )
        self.payload = payload
        super().__init__(message)
