import unittest
import unittest.mock as mock
from unittest.mock import Mock

from src.folicli.ui.tui.components.window import Window


class DummyWindow(Window):
    def static_render(self):
        pass

    def dynamic_render(self):
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
