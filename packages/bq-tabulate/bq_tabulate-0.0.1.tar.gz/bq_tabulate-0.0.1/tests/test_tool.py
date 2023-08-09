import json
from textwrap import dedent

from bq_tabulate import tool


def test_arithmetic():
    with open("tests/example.json", "r") as infile:
        example_json = json.load(infile)
    actual = tool.bq_tabulate(example_json)
    expected = dedent("""\
    category                 f0_
    ---------------  -----------
    family           15681705594
    standard         13754806819
    ad-supported      9553476042
    trial-opt-out     7050298030
    duo               6826200648
    campaign          4218297356
    student           3639993696
    trial-opt-in      2338638547
    iap               1573221041
    bundle            1087830904
    non-subscriber     615196940
    premium-mini        96730190
    paygtorecurring     18341966
    basic                8765048
    spotify-plus         8303007
    unknown              1158804""")
    assert actual == expected
