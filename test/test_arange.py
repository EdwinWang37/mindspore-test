import pytest
import numpy as np
import torch
import mindspore as ms
from mindspore import mint, Tensor

input_data = [[1, 6, 2, 4], [7, 3, 8, 2], [2, 9, 11, 5]]
dtype_ms_list = [ms.int8, ms.int16, ms.int32, ms.int64, ms.uint8, ms.uint16, ms.uint32, ms.uint64, ms.float16,
                 ms.float32, ms.float64, ms.bfloat16, ms.bool_]
dtype_torch_list = [torch.int8, torch.int16, torch.int32, torch.int64, torch.uint8, torch.uint16, torch.uint32,
                    torch.uint64, torch.float16, torch.float32, torch.float64, torch.bfloat16, torch.bool]

@pytest.mark.parametrize('mode', [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
def test_arange_different_dtypes(mode):
    """测试不同数据类型下，MindSpore和PyTorch的数据类型的支持度，若支持度相同的场景，比较运算结果是否一致"""
    ms.set_context(mode=mode)

    for dtype_ms, dtype_torch in zip(dtype_ms_list, dtype_torch_list):
        start, end, step = 0, 10, 2

        try:
            ms_result = mint.arange(start=start, end=end, step=step, dtype=dtype_ms)
        except Exception as e:
            ms_result = str(e)

        try:
            torch_result = torch.arange(start=start, end=end, step=step, dtype=dtype_torch)
        except Exception as e:
            torch_result = str(e)

        if isinstance(ms_result, ms.Tensor) and isinstance(torch_result, torch.Tensor):
            assert np.allclose(ms_result.asnumpy(), torch_result.numpy(), atol=1e-3), \
                f"Results do not match for dtype_ms: {dtype_ms} and dtype_torch: {dtype_torch}"
        else:
            assert str(ms_result) == str(torch_result), \
                f"Mismatch in error messages for dtype_ms: {dtype_ms} and dtype_torch: {dtype_torch}. " \
                f"MindSpore error: {ms_result}, PyTorch error: {torch_result}"

@pytest.mark.parametrize('mode', [ms.GRAPH_MODE, ms.PYNATIVE_MODE])
def test_arange_wrong_input(mode):
    """测试无效输入时，MindSpore和PyTorch的错误处理的异常对比"""
    ms.set_context(mode=mode)

    invalid_inputs = [
        ("start", "end", "step"),  # start, end, step 不是int或float类型
        (0, 10, 0),  # step = 0
        (10, 5, 2),  # step > 0 且 start >= end
        (5, 10, -1)  # step < 0 且 start <= end
    ]

    for start, end, step in invalid_inputs:
        # MindSpore
        try:
            ms_result = mint.arange(start=start, end=end, step=step)
        except Exception as e:
            ms_result = str(e)

        # PyTorch
        try:
            torch_result = torch.arange(start=start, end=end, step=step)
        except Exception as e:
            torch_result = str(e)

        print(f"MindSpore error: {ms_result}")
        print(f"PyTorch error: {torch_result}")