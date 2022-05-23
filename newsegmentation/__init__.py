# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
from ._algorithms import fbbcm as default_lcm
from ._algorithms import pbmm as default_sdm
from ._architecture import NewsSegmentation
from ._databasetrans import default_dbt
from ._slm import slm as default_slm
from ._structures import Leaf
from ._structures import TreeStructure
from ._gtreader import gtreader


def info():
	__text = f'News segmentation package:\n' \
	         f'--------------------------------------------\n' \
	         f'FAST USAGE:\n' \
	         f'--------------------------------------------\n' \
	         f'PATH_TO_MY_FILE = <PAHT>\n' \
	         f'import newsegmentation as ns\n' \
	         f'news = ns.NewsSegmentation(PATH_TO_MY_FILE)\n' \
	         f'for pon in news:\n' \
	         f'\tprint(pon)\n' \
	         f'--------------------------------------------\n'
	print(__text)
	return __text


def about():
	__text = f'Institution:\n' \
	         f'------------------------------------------------------\n' \
	         f'Universidad de Alcalá.\n' \
	         f'Escuela Politécnica Superior.\n' \
	         f'Departamento de Teoría De la Señal y Comunicaciones.\n' \
	         f'Cátedra ISDEFE.\n' \
	         f'------------------------------------------------------\n' \
	         f'Author: Alberto Palomo Alonso\n' \
	         f'------------------------------------------------------\n'
	print(__text)
	return __text


class Segmentation(NewsSegmentation):
	@staticmethod
	def _spatial_manager(r, param):
		return default_sdm(r, param)

	@staticmethod
	def _specific_language_model(s):
		return default_slm(s)

	@staticmethod
	def _later_correlation_manager(lm, s, t, param):
		return default_lcm(lm, s, t, param)

	@staticmethod
	def _database_transformation(path, op):
		return default_dbt(path, op)
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
