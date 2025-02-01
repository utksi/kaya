#include "symbol.inc"
  MODULE mopenacc_struct_def
#ifdef _OPENACC
  USE openacc

  PRIVATE

  PUBLIC :: ACC_ASYNC_SYNC,ACC_IS_PRESENT,ACC_PRESENT_COUNT, &
            ACC_ATTACH_ASYNC,ACC_DETACH_ASYNC

  INTEGER, PUBLIC :: ACC_ASYNC_Q=ACC_ASYNC_SYNC
!$OMP THREADPRIVATE(ACC_ASYNC_Q)

#ifndef ACC_DEBUG
  INTEGER, PARAMETER, PUBLIC :: ACC_ASYNC_ASYNC=1
#else
  INTEGER, PUBLIC            :: ACC_ASYNC_ASYNC=1
#endif
#endif
  !> Flags whether device-sided execution is allowed in principle
  LOGICAL, PUBLIC :: ACC_EXEC_ALLOW=.FALSE.
  !> Flags whether device-sided execution is momentarily activated
  LOGICAL, PUBLIC :: ACC_EXEC_ON=.FALSE.
  !> Total number of devices detected by the OpenACC runtime
  INTEGER, PUBLIC :: ACC_NUM_DEVICES
  !> Maximum number of MPI-ranks per device
  INTEGER, PUBLIC :: ACC_MAX_RANKS_PER_DEVICE
  !> compute capability of NVIDIA hardware
  INTEGER, PUBLIC :: ACC_NV_COMPUTE_CAPABILITY
#ifdef USENCCL
  !> Flags whether NCCL is used
  LOGICAL, PUBLIC :: LUSENCCL=.TRUE.
#endif
  END MODULE mopenacc_struct_def
