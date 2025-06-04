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
"""Module that implements the Base Route defaults methods."""

from pydantic import BaseModel

from carnage.database.repository.base import BaseRepository
from sanic.views import HTTPMethodView
from sanic import Request


class BaseRoute(HTTPMethodView):
    """Class that implements the base routes for an API request."""

    name: str = "base"

    def __init__(
        self,
        repository: type[BaseRepository] = BaseRepository,
    ) -> None:
        """Base constructor for all API routes.

        In the base class we define how the routes should look like and the
        methods that are associated with each endpoint. Those methods can (and
        are) overriden in each class that inherits from this base.

        :param repository: The repository that is used in queries.
        """
        self.repository = repository()

    async def post(self, request: Request) -> None:
        """Async method that represents a post request to this API.

        :param request: The data send throught the request.
        """
        self.repository.insert(values=request.json)

    async def get(self) -> list[BaseModel]:
        """Async method that represents a normal get request to this API."""
        result = self.repository.select()
        return [self.list_schema.from_orm(item) for item in result]

    async def get_by_id(self, identifier: str) -> BaseModel:
        """Async method that represents a normal get to this API.

        This instance of get request is meant to be used with an identifier to
        filter for a specific result.

        :param identifier: The unique identifier used in the query.
        """
        result = self.repository.select_by_id(identifier=identifier)
        return self.list_schema.from_orm(result[0])

    async def put(self, request: Request, identifier: str) -> None:
        """Async method that update data for this API.

        :param request: The data send throught the request.
        :param identifier: The unique identifier used in the query.
        """
        self.repository.update(values=request.json, identifier=identifier)

    async def delete(self, identifier: str) -> None:
        """Async method that deletes an entry for this API.

        :param identifier: The unique identifier used in the query.
        """
        self.repository.delete(identifier=identifier)
