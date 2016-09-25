"""A collection of tests for tenpy.linalg.charges"""

import tenpy.linalg.charges as charges
import numpy as np
import numpy.testing as npt
import nose.tools as nst
import itertools as it

# charges for comparison
# unsorted
qflat_us = np.array([-6, -6, -6, -4, -4, -4, 4, 4, -4, -4, -4, -4, -2, -2, -2, -2, -2, -2, -2, -2,
                     -2, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2, -2, 0, 0, 0, 0, 2, 2, 2,
                     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 6, 6]).reshape((-1, 1))
qind_us = np.array([[0, 3, -6],
                    [3, 6, -4],
                    [6, 8, 4],
                    [8, 12, -4],
                    [12, 23, -2],
                    [23, 34, 0],
                    [34, 37, -2],
                    [37, 41, 0],
                    [41, 55, 2],
                    [55, 59, 4],
                    [59, 61, 6]])   # yapf: disable
# sorted
qflat_s = np.sort(qflat_us, axis=0)
qind_s = np.array([[ 0,  3, -6],
                   [ 3, 10, -4],
                   [10, 24, -2],
                   [24, 39,  0],
                   [39, 53,  2],
                   [53, 59,  4],
                   [59, 61,  6]])    # yapf: disable

qdict_s = {(-6,): slice(0,  3),
           (-4,): slice(3,  10),
           (-2,): slice(10, 24),
           (0,) : slice(24, 39),
           (2,) : slice(39, 53),
           (4,) : slice(53, 59),
           (6,) : slice(59, 61)}    # yapf: disable

ch_1 = charges.ChargeInfo([1])


def test_ChargeInfo():
    trivial = charges.ChargeInfo()
    trivial.test_sanity()
    print "trivial: ", trivial
    nst.eq_(trivial.qnumber, 0)
    chinfo = charges.ChargeInfo([3, 1], ['some', ''])
    print "nontrivial chinfo: ", chinfo
    nst.eq_(chinfo.qnumber, 2)
    qs = [[0, 2], [2, 0], [5, 3], [-2, -3]]
    is_valid = [True, True, False, False]
    for q, valid in zip(qs, is_valid):
        nst.eq_(chinfo.check_valid(q), valid)
    qs_valid = np.array([chinfo.make_valid(q) for q in qs])
    npt.assert_equal(qs_valid, chinfo.make_valid(qs))


def test__find_row_differences():
    for qflat in [qflat_us, qflat_s]:
        diff = charges._find_row_differences(qflat)
        comp = [0] + [i for i in range(1, len(qflat))
                      if np.any(qflat[i - 1] != qflat[i])] + [len(qflat)]
        npt.assert_equal(diff, comp)


def test_LegCharge():
    for (qflat, qind) in [(qflat_s, qind_s), (qflat_us, qind_us)]:
        lc = charges.LegCharge.from_qflat(ch_1, qflat)
        npt.assert_equal(lc.qind, qind)  # check qflat -> qind
        npt.assert_equal(lc.to_qflat(), qflat)  # check qind -> qflat
    lc = charges.LegCharge.from_qdict(ch_1, qdict_s)
    npt.assert_equal(lc.qind, qind_s)  # qdict -> qflat
    npt.assert_equal(lc.to_qdict(), qdict_s)  # qflat -> qdict