#include "symbol.inc"
MODULE bse_struct
  USE prec
  IMPLICIT NONE

  TYPE banddesc
    INTEGER :: VBMIN, VBMAX      ! band index for the VB minimum and VB maximum
    INTEGER :: CBMIN, CBMAX      ! band index for the CB minimum and CB maximum
    INTEGER :: CBMIN4, CBMAX4    ! band index for the CB minimum and CB maximum for n4
                                 ! this might be reduced for parallelization over bands
    INTEGER :: NGLB              ! block size for conduction bands = total number of conduction bands
    INTEGER :: NGLB4             ! block size for conduction bands for fourth index (N4 usually)
                                 ! [ N4 is distributed over nodes when band parallelization is used
                                 !   in this case NGLB4 is equal NGLB/ number of nodes]
  END TYPE banddesc

  TYPE bse_matrix_index
    INTEGER :: NCV
    INTEGER, ALLOCATABLE ::  N1(:)  ! valence band index
    INTEGER, ALLOCATABLE ::  N3(:)  ! conduction band index
    INTEGER, ALLOCATABLE ::  NK(:)  ! k-point index
    INTEGER, ALLOCATABLE ::  ISP(:) ! spin index
    INTEGER, ALLOCATABLE ::  INDEX(:,:,:,:) ! yield index into Hamilton matrix for given valence, conduction, k-point and spin
  END TYPE bse_matrix_index


  TYPE selfenergy_from_bse 
     INTEGER :: NOMEGA
     INTEGER :: NBANDS
     INTEGER :: NKPTS
     INTEGER :: ISPIN
     REAL(q), POINTER :: OMEGA(:)  => NULL()
     REAL(q), POINTER :: REAL_PART(:,:,:,:) => NULL() !1st index over frequencies, 2nd index over bands
     REAL(q), POINTER :: IMAG_PART(:,:,:,:) => NULL()!3rd index over kpoints, 4th index over spin 
     COMPLEX(q), POINTER :: CELNEW(:,:,:) => NULL()  !bands, kpoints, spin 
  END TYPE selfenergy_from_bse

END MODULE bse_struct
