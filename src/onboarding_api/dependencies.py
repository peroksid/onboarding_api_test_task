from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends

from .db import ConnectionPool, get_pool


PoolDep = Annotated[ConnectionPool, Depends(get_pool)]
UUID4Dep = Annotated[UUID, Depends(uuid4)]
