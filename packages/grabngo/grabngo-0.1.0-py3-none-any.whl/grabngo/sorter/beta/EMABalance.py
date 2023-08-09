import torch
from torch import Tensor
from overrides import overrides

from grabngo.sorter.SorterBase import SorterBase


class EMABalance(SorterBase):
    idx: int

    # acc: running partial sum of shape (d,)
    acc: Tensor
    # m: stale mean of shape (d,)
    run_sum: Tensor

    left: int
    right: int

    def __init__(
        self, n: int, d: int, ema_decay: float = 0.1, *args, **kwargs  # EMA decay rate
    ):
        super().__init__(n, d, *args, **kwargs)

        # Init in a way that self.reset_epoch is always called at the start of
        # each epoch
        self.idx = self.n
        self.left = self.n
        self.right = self.n - 1

        self.ema_decay = ema_decay

        self.acc = torch.zeros(self.d, dtype=self.dtype, device=self.device)

        # The run sum will be inited in the first step
        # self.run_sum = torch.zeros_like(self.acc)

        self.inited_ema = (
            False  # the first time we call single_step, we need to init ema
        )

    @overrides
    def _reset_epoch(self):
        # TODO: no guarantee that the entire dataset is looped during an epoch
        # let's assert it is for now.
        assert self.left > self.right
        assert self.idx == self.n

        self.idx = 0
        self.orders.copy_(self.next_orders)
        self.next_orders.zero_()

        self.left = 0
        self.right = self.n - 1

        self.acc.zero_()

    @torch.no_grad()
    @overrides
    def single_step(self, grad: Tensor) -> None:
        """

        :param grad: per sample gradient
        :return:
        """
        if not self.inited_ema:
            ema = grad.clone()
            self.inited_ema = True
        else:
            ema = (1 - self.ema_decay) * self.run_sum + self.ema_decay * grad
            # It's crucial here to work on a clone of grad.
            # Don't modify grad in-place
            grad = grad - self.run_sum

        self.run_sum = ema

        # if epsilon_{k,t} == +1
        if self.balance(grad, self.acc):
            self.next_orders[self.left] = self.orders[self.idx]
            self.acc += grad
            self.left += 1
        else:
            self.next_orders[self.right] = self.orders[self.idx]
            self.acc -= grad
            self.right -= 1

        self.idx += 1
