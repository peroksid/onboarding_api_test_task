from typing import Annotated, Callable
from uuid import UUID, uuid4

from fastapi import Depends

from .db import ConnectionPool, get_pool
from .storage import save_file


PoolDep = Annotated[ConnectionPool, Depends(get_pool)]
SaveFileDep = Annotated[Callable, Depends(save_file)]
UUID4Dep = Annotated[UUID, Depends(uuid4)]
