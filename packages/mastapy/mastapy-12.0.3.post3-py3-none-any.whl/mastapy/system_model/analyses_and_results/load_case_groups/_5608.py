﻿"""_5608.py

SubGroupInSingleDesignState
"""


from mastapy.system_model.analyses_and_results.static_loads import _6736
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.load_case_groups import _5599
from mastapy._internal.python_net import python_net_import

_SUB_GROUP_IN_SINGLE_DESIGN_STATE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'SubGroupInSingleDesignState')


__docformat__ = 'restructuredtext en'
__all__ = ('SubGroupInSingleDesignState',)


class SubGroupInSingleDesignState(_5599.AbstractDesignStateLoadCaseGroup):
    """SubGroupInSingleDesignState

    This is a mastapy class.
    """

    TYPE = _SUB_GROUP_IN_SINGLE_DESIGN_STATE

    def __init__(self, instance_to_wrap: 'SubGroupInSingleDesignState.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def remove_static_load(self, static_load: '_6736.StaticLoadCase'):
        """ 'RemoveStaticLoad' is the original name of this method.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """

        self.wrapped.RemoveStaticLoad(static_load.wrapped if static_load else None)
