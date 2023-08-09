import sys

import pytest

from mTEL import mTEL
from eTEL import eTEL


def test_eTEL():
    eTEL.run(['-f', 'tests/resources/s228c_orf_cds.fasta', '-psm', 'tests/resources/psm.tsv', '-o', 'tests/output', '-decoy', 'rev_', '-p', 'substitutions', '-tol', '0.005', '-TEST', '-1'])
    assert True


def test_mTEL():
    mTEL.run(['-f', 'tests/resources/results_ionquant2', '-r', 'tests/resources/tRNA_count/yeast_tRNA_count.csv', '-o', 'tests/output', '-s', '250', '-p', '100', '-c', '4.2e-17', '-t', '10', '-b', '100', '-nb', '-1', '-a', 'n'])
    assert True
