from enum import Enum


class StudyType(Enum):
	BBROWSER=0
	H5_10X=1
	H5AD=2
	MTX_10X=3
	BCS=4
	RDS=5
	TSV=6
	DSP=7
	VISIUM=8
	VIZGEN=9
	COSMX=10
	XENIUM=11
	VISIUM_RDS=12
	VISIUM_ANN=13
	VIZGEN_V2=14
	TILE_DB=15
	PROTEOMICS_QPTIFF=16
	PROTEOMICS_OME_TIF=17
	PROTEOMICS_TIFF=18


class TechnologyType(Enum):
	SINGLE_CELL='SC'
	LENS_SC='LENS_SC'
	VISIUM='VISIUM'
	DSP='DSP'
	PROTEOMICS='PROTEOMICS'


class Species(Enum):
  HUMAN='human'
  MOUSE='mouse'
  NON_HUMAN_PRIMATE='primate'
  OTHERS='others'


class InputMatrixType(Enum):
  RAW='raw'
  NORMALIZED='normalized'


UNIT_RAW = 'raw'
UNIT_LOGNORM = 'lognorm'
