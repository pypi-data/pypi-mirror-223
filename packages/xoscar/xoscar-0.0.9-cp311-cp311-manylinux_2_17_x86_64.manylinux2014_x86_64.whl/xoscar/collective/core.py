# Copyright 2022-2023 XProbe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import hashlib
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .. import Actor, actor_ref
from ..context import get_context
from .common import (
    INVOKE_ERROR_MESSAGE,
    RANK_ADDRESS_ENV_KEY,
    AllReduceAlgorithm,
    CollectiveReduceOp,
)
from .process_group import ProcessGroup, ProcessGroupGloo
from .utils import get_rank_address_via_env


class RankActor(Actor):
    def __init__(
        self,
        rank: int,
        world: int,
        backend: str = "gloo",
        pg_options: Optional[ProcessGroup.Options] = None,
        *args,
        **kwargs,
    ):
        self._rank = rank
        self._world = world
        self._backend = backend
        self.name_to_pg: Dict[str, Dict[str, "ProcessGroup"]] = defaultdict(dict)
        self._pg_options = pg_options

    @classmethod
    def default_uid(cls):
        return "RankActor"

    async def __post_create__(self):
        os.environ[RANK_ADDRESS_ENV_KEY] = self.address
        _ip = self._get_ip()
        if self._backend == "gloo":
            pg = ProcessGroupGloo(
                _ip,
                self._rank,
                self._world,
                group_name="default",
                pg_options=self._pg_options,
            )
            self.name_to_pg["gloo"]["default"] = pg
        else:
            raise NotImplementedError("Not impl other backends for now!")

    def process_group(self, pg_name: str) -> ProcessGroup:
        return self.name_to_pg[self._backend][pg_name]

    def rank(self) -> int:
        return self._rank

    def world(self) -> int:
        return self._world

    def backend(self) -> str:
        return self._backend

    def _get_ip(self) -> str:
        return self.address.split(":")[0]

    def _process_group_name(self, ranks: List[int]) -> str:
        return hashlib.sha1(
            bytes(self._backend + "_".join(map(str, ranks)), "utf-8")
        ).hexdigest()

    def new_group(
        self, ranks: List[int], pg_options: Optional[ProcessGroup.Options] = None
    ) -> Optional[str]:
        assert (
            len(ranks) <= self._world
        ), "``ranks`` in new_group cannot be larger than the world."
        assert all(
            [self._world > rank >= 0 for rank in ranks]
        ), "rank in ``ranks`` is illegal."
        assert len({rank for rank in ranks}) == len(
            ranks
        ), "there can be no duplicate ranks in the ``ranks``."
        if self._rank not in ranks:
            return None
        if len(ranks) == self._world:
            return "default"
        global_ranks = sorted(ranks)
        group_rank = global_ranks.index(self._rank)
        group_world = len(global_ranks)
        group_name = self._process_group_name(global_ranks)
        if group_name in self.name_to_pg[self._backend]:
            return group_name
        _ip = self._get_ip()
        pg = ProcessGroupGloo(
            _ip, group_rank, group_world, group_name=group_name, pg_options=pg_options
        )
        self.name_to_pg[self._backend][group_name] = pg
        return group_name

    def reduce(
        self,
        send_data: Any,
        recv_data: Any,
        op: CollectiveReduceOp = CollectiveReduceOp.SUM,
        root: Optional[int] = 0,
        tag: Optional[int] = 0,
        pg_name: str = "default",
    ):
        self.name_to_pg[self._backend][pg_name].reduce(
            send_data, recv_data, op=op, root=root, tag=tag
        )

    def allreduce(
        self,
        send_data: Any,
        recv_data: Any,
        op: CollectiveReduceOp = CollectiveReduceOp.SUM,
        algorithm: AllReduceAlgorithm = AllReduceAlgorithm.RING,
        tag: Optional[int] = 0,
        pg_name: str = "default",
    ):
        self.name_to_pg[self._backend][pg_name].allreduce(
            send_data, recv_data, op=op, algorithm=algorithm, tag=tag
        )

    def gather(
        self,
        send_data: Any,
        recv_data: Any,
        root: Optional[int] = 0,
        tag: Optional[int] = 0,
        pg_name: str = "default",
    ):
        self.name_to_pg[self._backend][pg_name].gather(
            send_data, recv_data, root=root, tag=tag
        )

    def allgather(
        self,
        send_data: Any,
        recv_data: Any,
        tag: Optional[int] = 0,
        pg_name: str = "default",
    ):
        self.name_to_pg[self._backend][pg_name].allgather(send_data, recv_data, tag=tag)

    def scatter(
        self,
        send_data: List[Any],
        recv_data: Any,
        root: Optional[int] = 0,
        tag: Optional[int] = 0,
        pg_name: str = "default",
    ):
        self.name_to_pg[self._backend][pg_name].scatter(
            send_data, recv_data, root=root, tag=tag
        )

    def reduce_scatter(
        self,
        send_data: Any,
        recv_data: Any,
        recv_elems: List[int],
        op: CollectiveReduceOp = CollectiveReduceOp.SUM,
        pg_name: str = "default",
    ):  # pragma: no cover
        self.name_to_pg[self._backend][pg_name].reduce_scatter(
            send_data, recv_data, recv_elems, op
        )

    def alltoall(
        self,
        send_data: Any,
        recv_data: Any,
        tag: Optional[int] = 0,
        pg_name: str = "default",
    ):
        self.name_to_pg[self._backend][pg_name].alltoall(send_data, recv_data, tag=tag)

    def broadcast(
        self,
        send_data: Any,
        recv_data: Any,
        root: Optional[int] = 0,
        tag: Optional[int] = 0,
        pg_name: str = "default",
    ):
        self.name_to_pg[self._backend][pg_name].broadcast(
            send_data, recv_data, root, tag=tag
        )


async def init_process_group(
    rank: int, world_size: int, backend: str = "gloo", address: Optional[str] = None
):
    address = address or os.environ.get(RANK_ADDRESS_ENV_KEY, None)
    if address is None:
        raise RuntimeError(
            "Cannot decide which process to involve in the collective communication."
        )
    ctx = get_context()
    await ctx.create_actor(
        RankActor, rank, world_size, backend=backend, address=address, uid="RankActor"
    )


async def new_group(
    ranks: List[int], pg_options: Optional[ProcessGroup.Options] = None
):
    address = os.environ.get(RANK_ADDRESS_ENV_KEY, None)
    if address is None:
        raise RuntimeError(INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    return await ref.new_group(ranks, pg_options)


async def reduce(
    send_data: Any,
    recv_data: Any,
    op: CollectiveReduceOp = CollectiveReduceOp.SUM,
    root: Optional[int] = 0,
    tag: Optional[int] = 0,
    group_name: str = "default",
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    await ref.reduce(
        send_data, recv_data, op=op, root=root, tag=tag, pg_name=group_name
    )


async def allreduce(
    send_data: Any,
    recv_data: Any,
    op: CollectiveReduceOp = CollectiveReduceOp.SUM,
    algorithm: AllReduceAlgorithm = AllReduceAlgorithm.RING,
    tag: Optional[int] = 0,
    group_name: str = "default",
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid="RankActor")
    await ref.allreduce(
        send_data, recv_data, op=op, algorithm=algorithm, tag=tag, pg_name=group_name
    )


async def gather(
    send_data: Any,
    recv_data: Any,
    root: Optional[int] = 0,
    tag: Optional[int] = 0,
    group_name: str = "default",
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    await ref.gather(send_data, recv_data, root=root, tag=tag, pg_name=group_name)


async def allgather(
    send_data: Any, recv_data: Any, tag: Optional[int] = 0, group_name: str = "default"
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    await ref.allgather(send_data, recv_data, tag=tag, pg_name=group_name)


async def scatter(
    send_data: List[Any],
    recv_data: Any,
    root: Optional[int] = 0,
    tag: Optional[int] = 0,
    group_name: str = "default",
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    await ref.scatter(send_data, recv_data, root=root, tag=tag, pg_name=group_name)


async def reduce_scatter(
    send_data: Any,
    recv_data: Any,
    recv_elems: List[int],
    op: CollectiveReduceOp = CollectiveReduceOp.SUM,
    group_name: str = "default",
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    await ref.reduce_scatter(send_data, recv_data, recv_elems, op, pg_name=group_name)


async def alltoall(
    send_data: Any, recv_data: Any, tag: Optional[int] = 0, group_name: str = "default"
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    await ref.alltoall(send_data, recv_data, tag=tag, pg_name=group_name)


async def broadcast(
    send_data: Any,
    recv_data: Any,
    root: Optional[int] = 0,
    tag: Optional[int] = 0,
    group_name: str = "default",
):
    address = get_rank_address_via_env(RANK_ADDRESS_ENV_KEY, INVOKE_ERROR_MESSAGE)
    ref = await actor_ref(address=address, uid=f"RankActor")
    await ref.broadcast(send_data, recv_data, root, tag, pg_name=group_name)
