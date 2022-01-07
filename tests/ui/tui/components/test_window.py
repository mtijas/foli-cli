import unittest
import unittest.mock as mock
from unittest.mock import Mock

from src.folicli.ui.tui.components.window import Window


class DummyWindow(Window):
    def initial_render(self):
        pass


class TestWindow(unittest.TestCase):
    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def setUp(self, mocked_curses):
        self.mocked_curses_win = Mock()
        mocked_curses.newwin.return_value = self.mocked_curses_win
        self.mocked_curses = mocked_curses
        self.width = 100
        self.height = 100
        self.window = DummyWindow(self.height, self.width)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_window_width_height_limited(self, mocked_curses):
        """Window width and height should be at least 1"""
        window = DummyWindow(0, 0)

        self.assertEqual(window.height, 1)
        self.assertEqual(window.width, 1)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_window_y_x_limited(self, mocked_curses):
        """Window y and x should be zero or more"""
        window = DummyWindow(5, 5, -1, -1)

        self.assertEqual(window.y, 0)
        self.assertEqual(window.y, 0)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_set_bkgd_sets_bkgd_in_curses_window(self, mocked_curses):
        """Set background color should be available"""
        mocked_win = Mock()
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(5, 5)

        window.set_background_color(1)

        mocked_win.bkgd.assert_called_once()
        mocked_curses.color_pair.assert_called_once_with(1)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_refresh_refreshs_internal_window(self, mocked_curses):
        """Refresh should actually refresh internal curses window"""
        mocked_win = Mock()
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(5, 5)

        window.refresh()

        mocked_win.refresh.assert_called_once()

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_str_basic_text_added_fully(self, mocked_curses):
        """Fitting text should be fully added to desired row"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(10, 10)

        window.add_str(1, 1, "test")

        mocked_win.addnstr.assert_called_once_with(1, 1, "test", 8)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_str_text_does_not_overflow(self, mocked_curses):
        """Text must not overflow from the right"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(10, 10)

        window.add_str(1, 1, "testtesttest")

        mocked_win.addnstr.assert_called_once_with(1, 1, "testtesttest", 8)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_str_negative_y_adds_to_first_line(self, mocked_curses):
        """Negative y makes text appear in first line"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(10, 10)

        window.add_str(-1, 1, "test")

        mocked_win.addnstr.assert_called_once_with(0, 1, "test", 8)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_str_megalomaniac_y_adds_to_last_line(self, mocked_curses):
        """Megalomaniac y makes text appear in last line"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(10, 10)

        window.add_str(99, 1, "test")

        mocked_win.addnstr.assert_called_once_with(9, 1, "test", 8)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_str_negative_x_starts_from_first_char(self, mocked_curses):
        """Negative x makes text start from first character"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(10, 10)

        window.add_str(0, -1, "test")

        mocked_win.addnstr.assert_called_once_with(0, 0, "test", 9)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_str_megalomaniac_x_starts_from_last_char(self, mocked_curses):
        """Megalomaniac x makes text start from last character"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(10, 10)

        window.add_str(0, 100, "test")

        mocked_win.addnstr.assert_called_once_with(0, 9, "test", 0)

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_centered_str_test_1(self, mocked_curses):
        """Centered str test with texts from "" to overlong text"""
        tests = [
            {"text": "", "x": 5},
            {"text": "A", "x": 5},
            {"text": "AA", "x": 4},
            {"text": "AAA", "x": 4},
            {"text": "AAAA", "x": 3},
            {"text": "AAAAA", "x": 3},
            {"text": "AAAAAA", "x": 2},
            {"text": "AAAAAAA", "x": 2},
            {"text": "AAAAAAAA", "x": 1},
            {"text": "AAAAAAAAA", "x": 1},
            {"text": "AAAAAAAAAA", "x": 0},
            {"text": "OVERFLOWINGVALUE", "x": 0},
        ]
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        window = DummyWindow(10, 10)

        for test in tests:
            window.add_centered_str(0, test["text"])
            mocked_win.addnstr.assert_called_with(
                0, test["x"], test["text"], 9 - test["x"]
            )

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_str_with_color(self, mocked_curses):
        """Str should be added with color referencing color number"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        mocked_curses.color_pair.return_value = "color_pair"
        window = DummyWindow(10, 10)

        window.add_str(0, 0, "test", 1)

        mocked_win.addnstr.assert_called_once_with(0, 0, "test", 9, "color_pair")

    @mock.patch("src.folicli.ui.tui.components.window.curses")
    def test_add_centered_str_with_color(self, mocked_curses):
        """Centered str should be added with color referencing color number"""
        mocked_win = Mock()
        mocked_win.getmaxyx.return_value = (10, 10)
        mocked_curses.newwin.return_value = mocked_win
        mocked_curses.color_pair.return_value = "color_pair"
        window = DummyWindow(10, 10)

        window.add_centered_str(0, "test", 1)

        mocked_win.addnstr.assert_called_once_with(0, 3, "test", 6, "color_pair")
