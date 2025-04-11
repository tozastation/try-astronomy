import torch

# Check that MPS is available
if not torch.backends.mps.is_available():
    if not torch.backends.mps.is_built():
        print("MPS not available because the current PyTorch install was not "
              "built with MPS enabled.")
    else:
        print("MPS not available because the current MacOS version is not 12.3+ "
              "and/or you do not have an MPS-enabled device on this machine.")

mps_device = torch.device('mps')
print('device count: %d' % torch.mps.device_count())
print('memory occupied: %f GB' % (torch.mps.current_allocated_memory() / (1024 ** 3)))
print('memory allocated: %f GB' % (torch.mps.driver_allocated_memory() / (1024 ** 3)))
print('recommended max Working set size: %f GB' % (torch.mps.recommended_max_memory() / (1024 ** 3)))
