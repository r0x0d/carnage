# MIT License
#
# Copyright (c) 2022, Rodolfo Olivieri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module that implements the Aligment Route."""

from sanic import Request
from sanic_ext import validate
from carnage.api.routes.base import BaseRoute
from carnage.api.schemas.aligment import (
    CreateAligmentSchema,
    ListAligmentSchema,
    UpdateAligmentSchema,
)
from carnage.database.repository.aligment import AligmentRepository


class AligmentRoute(BaseRoute):
    """Class that overrides the base routes for an API request."""

    name: str = "aligment"

    def __init__(
        self,
        repository: type[AligmentRepository] = AligmentRepository,
    ) -> None:
        """Constructor for HTTP API route.

        :param repository: The repository that may be used to query
            information.
        """
        super().__init__(
            repository=repository,
        )

    @validate(json=CreateAligmentSchema)
    async def post(self, request: Request, body: CreateAligmentSchema) -> None:
        """Async method that represents a post request to this API.

        :param request: The data send throught the request.
        """
        return await super().post(body)

    async def get(self) -> list[ListAligmentSchema]:
        """Async method that represents a normal get request to this API."""
        return await super().get()

    async def get_by_id(self, identifier: str) -> ListAligmentSchema:
        """Async method that represents a normal get to this API.

        This instance of get request is meant to be used with an identifier to
        filter for a specific result.

        :param identifier: The unique identifier used in the query.
        """
        return await super().get_by_id(identifier)

    @validate(json=UpdateAligmentSchema)
    async def put(
        self,
        request: Request,
        body: UpdateAligmentSchema,
        identifier: str,
    ) -> None:
        """Async method that update data for this API.

        :param request: The data send throught the request.
        :param identifier: The unique identifier used in the query.
        """
        return await super().put(body, identifier)
