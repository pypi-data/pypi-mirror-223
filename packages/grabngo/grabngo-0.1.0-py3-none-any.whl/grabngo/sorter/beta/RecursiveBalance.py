from collections import deque

import torch
from torch import Tensor

from absl import logging
from overrides import overrides

from grabngo.sorter.SorterBase import SorterBase


class RecursiveBalance(SorterBase):
    idx: int

    # acc: running partial sum of shape (d,)
    acc: Tensor

    left: "RecursiveBalance" = None
    right: "RecursiveBalance" = None

    # Only the leaf node keeps track of the orders.
    is_root: bool = False
    is_leaf: bool = False

    # root specific
    # m: stale mean of shape (d,)
    run_sum: Tensor
    run_sum_next: Tensor

    # leaf specific
    positives: deque = None
    negatives: deque = None

    def __init__(
        self, n: int, d: int, depth: int = 5, is_root: bool = True, *args, **kwargs
    ):
        """

        :param n:
        :param d:
        :param depth: the maximum depth of the recursive tree. Note that the
            depth of a tree starts from 0, so a tree with maximum depth 3
            actually has 4 "layers".
        :param random_first_epoch:
        :param prob_balance:
        :param prob_balance_c:
        :param device:
        """
        # Gary: only the root init the random projection matrix and record
        # herding if needed
        if not is_root:
            kwargs["random_projection"] = False
            kwargs["record_herding"] = False
            kwargs["record_norm"] = False

        super().__init__(n, d, *args, **kwargs)

        self.is_leaf = depth == 0
        self.is_root = is_root

        if self.is_root:
            logging.info(f"Creating RecursiveBalance with depth {depth}")

        # Init in a way that self.reset_epoch is always called at the start of
        # each epoch
        self.idx = -1

        self.acc = torch.zeros(self.d, dtype=self.dtype, device=self.device)

        if self.is_root:
            self.run_sum = torch.zeros_like(self.acc)
            self.run_sum_next = torch.zeros_like(self.acc)
        else:
            del self.orders
            del self.next_orders

        if not self.is_leaf:
            self.left = RecursiveBalance(
                n, d, depth=depth - 1, is_root=False, *args, **kwargs
            )
            self.right = RecursiveBalance(
                n, d, depth=depth - 1, is_root=False, *args, **kwargs
            )
        else:
            self.positives = deque()
            self.negatives = deque()

    def get_orders(self) -> list[int]:
        return (
            [*self.positives, *self.negatives]
            if self.is_leaf
            else self.left.get_orders() + self.right.get_orders()
        )

    @overrides
    def _reset_epoch(self):
        # TODO: no guarantee that the entire dataset is looped during an epoch
        # let's assert it is for now.

        # For recursive balance, the orders are not updated on the fly, we have
        # to update it at the beginning of reset_epoch() in the root

        if self.is_root:
            # hack: it's not before the start of 1st epoch
            if self.idx != -1:
                self.orders = torch.tensor(self.get_orders(), dtype=torch.int64)

            logging.debug(len(self.orders))
            logging.debug(self.orders)

            assert len(self.orders) == self.n, (
                "The sampler is not updated with all examples during last "
                "epoch. Aborted."
            )

        self.idx = 0

        self.acc.zero_()

        if self.is_root:
            self.run_sum = self.run_sum_next / self.n
            self.run_sum_next.zero_()

        if not self.is_leaf:
            self.left._reset_epoch()
            self.right._reset_epoch()
        else:
            self.positives.clear()
            self.negatives.clear()

    @torch.no_grad()
    def single_step(self, g: Tensor, idx: int):
        """

        :param g: normalized per sample gradient
        :param idx: the index of the example in dataset
        :return:
        """
        # It's crucial here to work on a clone of grad.
        # Don't modify grad in-place

        # if epsilon_{k,t} == +1
        if self.balance(g, self.acc):
            self.acc += g
            if self.is_leaf:
                self.positives.append(idx)
            else:
                self.left.single_step(g, idx)
        else:
            self.acc -= g
            if self.is_leaf:
                self.negatives.appendleft(idx)
            else:
                self.right.single_step(g, idx)

    @torch.no_grad()
    @overrides
    def _step(self, grads: Tensor, b: int):
        assert self.is_root, "Only the root of sampler should call this function."

        self.run_sum_next += grads.sum(dim=0)
        grads = grads - self.run_sum

        for i in range(b):
            self.single_step(grads[i], self.orders[self.idx])
            self.idx += 1
