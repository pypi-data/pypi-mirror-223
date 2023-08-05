from pathlib import Path
from geovisio_cli import model
import pytest


def test_Picture_toml():
    p = model.Picture(
        path="/tmp/1.jpg",
        id="blerg",
        location="http://api.geovisio.fr/blerg",
        status="ready",
    )
    assert p == model.Picture.from_toml(p.toml())


def test_Sequence_toml():
    pics = [
        model.Picture(
            path="/tmp/bla/1.jpg",
            id="bla1",
            location="http://api.geovisio.fr/bla/1",
            status="ready",
        ),
        model.Picture(
            path="/tmp/bla/2.jpg",
            id="bla2",
            location="http://api.geovisio.fr/bla/2",
            status="ready",
        ),
    ]
    s = model.Sequence(
        title="Bla",
        path="/tmp/bla",
        id="blabla",
        location="http://api.geovisio.fr/bla",
        producer="BBC (Bla Bla Corporation)",
        pictures=pics,
        sort_method=model.SortMethod.time_desc,
    )
    assert s == model.Sequence.from_toml(s.toml())


def test_ManySequences_toml(tmpdir):
    pics1 = [
        model.Picture(
            path="/tmp/bla/1.jpg",
            id="bla1",
            location="http://api.geovisio.fr/bla/1",
            status="ready",
        ),
        model.Picture(
            path="/tmp/bla/2.jpg",
            id="bla2",
            location="http://api.geovisio.fr/bla/2",
            status="ready",
        ),
    ]
    seq1 = model.Sequence(
        title="Bla",
        path="/tmp/bla",
        id="blabla",
        location="http://api.geovisio.fr/bla",
        producer="BBC (Bla Bla Corporation)",
        pictures=pics1,
        sort_method=model.SortMethod.time_desc,
    )
    pics2 = [
        model.Picture(
            path="/tmp/bla2/1.jpg",
            id="bla2-1",
            location="http://api.geovisio.fr/bla2/1",
            status="ready",
        ),
        model.Picture(
            path="/tmp/bla2/2.jpg",
            id="bla2-2",
            location="http://api.geovisio.fr/bla2/2",
            status="ready",
        ),
    ]
    seq2 = model.Sequence(
        title="Bla2",
        path="/tmp/bla2",
        id="blabla2",
        location="http://api.geovisio.fr/bla2",
        producer="BBC (Bla Bla Corporation)",
        pictures=pics2,
        sort_method=model.SortMethod.time_asc,
    )
    toml_file = tmpdir / model.SEQUENCE_TOML_FILE
    ms = model.ManySequences(toml_file=toml_file, sequences=[seq1, seq2])
    ms.persist()
    assert ms == model.ManySequences.read_from_file(toml_file)


def test_ManySequences_has_same_sort_method():
    toml_file = Path("some_file.toml")
    seq1 = model.Sequence(sort_method=model.SortMethod.time_asc)
    ms = model.ManySequences(toml_file=toml_file, sequences=[seq1])

    assert ms.has_same_sort_method(None)
    assert ms.has_same_sort_method(model.SortMethod.time_asc)
    assert not ms.has_same_sort_method(model.SortMethod.time_desc)

    ms = model.ManySequences(toml_file=toml_file, sequences=[])
    assert ms.has_same_sort_method(None)
    assert ms.has_same_sort_method(model.SortMethod.time_asc)


def test_ManySequences_is_empty():
    toml_file = Path("some_file.toml")
    ms = model.ManySequences(toml_file=toml_file, sequences=[])
    assert ms.is_empty()

    seq1 = model.Sequence()
    ms = model.ManySequences(toml_file=toml_file, sequences=[seq1])
    assert ms.is_empty()

    pic1 = model.Picture(path="/tmp/bla/1.jpg")
    seq1 = model.Sequence(pictures=[pic1])
    ms = model.ManySequences(toml_file=toml_file, sequences=[seq1])
    assert not ms.is_empty()


def test_ManySequences_has_valid_pictures():
    toml_file = Path("some_file.toml")
    ms = model.ManySequences(toml_file=toml_file, sequences=[])
    assert not ms.has_valid_pictures()

    pic1 = model.Picture(path="/tmp/bla/1.jpg", status="broken-metadata")
    seq1 = model.Sequence(pictures=[pic1])
    ms = model.ManySequences(toml_file=toml_file, sequences=[seq1])
    assert not ms.has_valid_pictures()

    pic1 = model.Picture(path="/tmp/bla/1.jpg")
    seq1 = model.Sequence(pictures=[pic1])
    ms = model.ManySequences(toml_file=toml_file, sequences=[seq1])
    assert ms.has_valid_pictures()


def test_rw_sequences_toml(tmp_path):
    s = model.Sequence(
        title="SEQUENCE",
        id="blab-blabla-blablabla",
        path=str(tmp_path),
        pictures=[
            model.Picture(
                id="blou-bloublou-bloubloublou-1", path=str(tmp_path / "1.jpg")
            ),
            model.Picture(
                id="blou-bloublou-bloubloublou-2", path=str(tmp_path / "2.jpg")
            ),
            model.Picture(
                id="blou-bloublou-bloubloublou-3", path=str(tmp_path / "3.jpg")
            ),
        ],
        sort_method=model.SortMethod.time_desc,
    )
    tomlFile = tmp_path / "_geovisio.toml"
    ms = model.ManySequences(tomlFile, sequences=[s])
    res = ms.persist()
    assert res == tomlFile

    res2 = model.ManySequences.read_from_file(tomlFile)
    assert ms == res2
