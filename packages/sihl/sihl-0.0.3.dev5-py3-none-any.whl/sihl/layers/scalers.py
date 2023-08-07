from torch import Tensor, nn
from torch.nn.functional import interpolate

from sihl.layers.convblocks import ConvNormRelu


class StridedDownscaler(ConvNormRelu):
    def __init__(self, num_channels: int, **kwargs):  # type: ignore
        super().__init__(num_channels, num_channels, stride=2, **kwargs)


class BilinearUpscaler(nn.Module):
    def forward(self, x: Tensor) -> Tensor:
        return interpolate(x, scale_factor=2.0, mode="bilinear")  # type: ignore


# class BilinearAdditiveUpscaler(nn.Module):
