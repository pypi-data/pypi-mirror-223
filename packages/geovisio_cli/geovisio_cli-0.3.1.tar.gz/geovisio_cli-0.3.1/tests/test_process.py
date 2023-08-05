import pytest
import os
from geovisio_cli.sequences.process import standard
from .conftest import FIXTURE_DIR
from pathlib import Path, PurePath


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "not_a_pic.md"),
)
def test_upload_with_invalid_file(datafiles):
    ms = standard.process(path=Path(datafiles), title=None)

    assert len(ms.sequences) == 1
    s = ms.sequences[0]
    assert len(s.pictures) == 3
    assert [PurePath(p.path).stem for p in s.pictures] == ["e1", "e2", "e3"]
    assert s.title == Path(datafiles).name
