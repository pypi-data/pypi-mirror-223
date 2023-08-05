# *****************************************************************************
# *
# * Authors:     Federico P. de Isidro Gomez (fp.deisidro@cnb.csic.es) [1]
# *
# * [1] Centro Nacional de Biotecnologia, CSIC, Spain
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# *****************************************************************************

from pyworkflow.tests import DataSet

DataSet(name='tomo-em',
        folder='tomo-em',
        files={
            'ts1': 'tutorialData/BBa.st',
            'ts2': 'tutorialData/BBb.st',
            'excludeViewsFile': 'tutorialData/excludeViewsFile.txt',
            'tm1': 'tutorialData/BBa.prexg',
            'tm2': 'tutorialData/BBb.prexg'
        })

DataSet(name='tutorialDataImodCTF',
        folder='tutorialDataImodCTF',
        files={
            'tsCtf1': 'WTI042413_1series4.st',
            'inputCtfFile': 'WTI042413_1series4.defocus'
        })
