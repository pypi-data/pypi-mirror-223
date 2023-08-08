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


class SharingException(MLaaSException):
    """Base exception for Model Sharing client."""

    pass


class ModelException(SharingException):
    """Base exception for ML model instances."""

    pass


class DatasetException(SharingException):
    """Base exception for dataset instances."""

    pass


class ModelNotFoundException(ModelException):
    def __init__(self, id):
        message = "Model was not found in the platform.\n" f"Model UUID: {id}"
        self.id = id
        super().__init__(message)


class DatasetNotFoundException(DatasetException):
    def __init__(self, id):
        message = "Dataset was not found in the platform.\n" f"Dataset UUID: {id}"
        self.id = id
        super().__init__(message)


class ModelRegistrationException(ModelException):
    def __init__(self):
        message = "Exception occurred when trying to register model."
        super().__init__(message)


class DatasetRegistrationException(DatasetException):
    def __init__(self):
        message = "Exception occurred when trying to register dataset."
        super().__init__(message)


class ModelUpdateException(ModelException):
    def __init__(self, id):
        message = (
            "Exception occurred when trying to update model with training results.\n"
            f"Model UUID: {id}"
        )
        self.id = id
        super().__init__(message)
