#     Copyright 2016-present CERN – European Organization for Nuclear Research
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from pandas import Series


def cast_series(series: Series, output_type: type):
    """
    Casts the given series to another series type specified by output_type (e.g. casts container of type pd.Series
    to QFSeries).

    Parameters
    ----------
    series
        series to be casted
    output_type
        type to which series should be casted

    Returns
    -------
    casted_series
        new series of given type
    """
    return output_type(data=series.values, index=series.index).__finalize__(series)
