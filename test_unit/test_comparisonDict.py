from comparison_dict import ComparisonDict


class TestComparisonDict:
    def test_simple_comparisons(self):
        a = ComparisonDict((('name', 'Foonyor   '), ('valid', '1'), ('count', '  1')))
        b = ComparisonDict((('name', 'Foonyor   '), ('valid', '1'), ('count', '  1')))
        # not equal:
        c = ComparisonDict((('name', 'Foonyor   '), ('valid', '1'), ('count', '  9')))
        d = ComparisonDict((('name', 'Foonyos   '), ('valid', '1'), ('count', '  9')))
        e = ComparisonDict((('name', 'Foonyos   '), ('valid', '0'), ('count', '  9')))
        f = ComparisonDict((('name', 'Foonyor   '), ('valid', '1'), ('count', '  1'),
                            ('new_val', '0')))
        g = ComparisonDict((('name', 'Jack'),))

        assert a == b
        assert b == a

        assert a != c
        assert a != d
        assert a != e
        assert a != f
        assert a != g and b != g