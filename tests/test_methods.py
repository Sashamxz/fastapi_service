
# Relative Import
import sys
sys.path.append("..")
# END Relative Import

from app.methods import get_file_size


def test_get_file_size():
    # assert isinstance(get_file_size('test.txt', '../uploaded_files/'), int) == True
    assert isinstance(get_file_size('test.txt', './'), int) == True


