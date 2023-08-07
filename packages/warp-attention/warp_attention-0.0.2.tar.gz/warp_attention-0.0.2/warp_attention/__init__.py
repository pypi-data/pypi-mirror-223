try:
  import torch
except ImportError:
  print("pytorch is not installed.")
  exit()

from torch import Tensor
from typing import Optional
from pathlib import Path

try:
  from warp_attention.warp_attention_torch_cpp import create_module

  _proj_dir = Path(__file__).resolve().parent
  _kernel_dir = _proj_dir / "kernel"

  _kernel_map = {
    "8.0": f"{_kernel_dir}/warp_attn_forward_sm80.cubin",
    "8.6": f"{_kernel_dir}/warp_attn_forward_sm86.cubin",
  }
  _kernel_config = torch.load(_kernel_dir / "kernel_config.pt")
  _kernel_module = create_module(_kernel_config, _kernel_map)

  def _warp_attention_forward(
      query: Tensor,
      key: Tensor,
      value: Tensor,
      scale: Optional[float] = None,
      out: Optional[Tensor] = None,
      version: int = 0,
      speed_level: int = 3,
    ):
    if out is None:
      out = torch.zeros_like(query)
    if scale is None:
      scale = query.shape[-1] ** (-0.5)

    stream = torch.cuda.current_stream()

    _kernel_module.run(
      query, key, value, out, 
      scale, speed_level, version, stream.cuda_stream
    )

except ImportError:
  print("warp_attention is installed incorrectly.")