﻿"""_5508.py

CouplingConnectionCompoundMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.mbd_analyses import _5358
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5535
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CouplingConnectionCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundMultibodyDynamicsAnalysis',)


class CouplingConnectionCompoundMultibodyDynamicsAnalysis(_5535.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis):
    """CouplingConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_5358.CouplingConnectionMultibodyDynamicsAnalysis]':
        """List[CouplingConnectionMultibodyDynamicsAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_5358.CouplingConnectionMultibodyDynamicsAnalysis]':
        """List[CouplingConnectionMultibodyDynamicsAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
