from classes.LedColor import LedColor


def test_interpolate_rgb_val_1_0():
    c1 = [0, 0, 0]
    c2 = [255, 255, 255]

    ACTUAL_VALUE_CORRECT = LedColor.interpolate_rgb(c1, c2, 1)
    ACTUAL_VALUE_WRONG = LedColor.interpolate_rgb(c1, c2, 0.5)
    assert ACTUAL_VALUE_CORRECT == c2
    assert not ACTUAL_VALUE_WRONG == c2

    ACTUAL_VALUE_ZERO = LedColor.interpolate_rgb(c1, c2, 0)
    assert ACTUAL_VALUE_ZERO == c1


def test_interpolate_rgb_half():
    c1 = [0, 0, 0]
    c2 = [255, 255, 255]

    ACTUAL_VALUE_HALF = LedColor.interpolate_rgb(c1, c2, 0.5)
    EXPECTED_VALUE_HALF = [128, 128, 128]

    assert ACTUAL_VALUE_HALF == EXPECTED_VALUE_HALF


def test_can_get_color_as_list():
    ACTUAL_VALUE = LedColor.get_rgb_value(LedColor.lightOrange)
    EXPECTED_RETURN_VALUE = [180, 45, 0]

    assert ACTUAL_VALUE == EXPECTED_RETURN_VALUE


def test_can_convert_list_to_color():
    ACTUAL_VALUE = LedColor.rgb([180, 45, 0])
    EXPECTED_RETURN_VALUE = LedColor.lightOrange

    assert ACTUAL_VALUE == EXPECTED_RETURN_VALUE


def test_can_get_random_color():
    """Checks to make sure it can get a random color. Colors should be an int value."""
    ACTUAL = LedColor.get_random()
    
    assert type(ACTUAL) == int
