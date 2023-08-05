import os
import pytest

import geovisio_cli.sequences.status
import geovisio_cli.sequences.upload
from ..conftest import FIXTURE_DIR
from pathlib import Path
import requests
from geovisio_cli import exception, model
from datetime import timedelta
import toml


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_valid_upload(geovisio_with_token, datafiles):
    uploadReports = geovisio_cli.sequences.upload.upload(
        path=Path(datafiles),
        geovisio=geovisio_with_token,
        title="some title",
        pictureUploadTimeout=20,
    )
    assert len(uploadReports) == 1
    assert len(uploadReports[0].uploaded_pictures) == 3
    assert len(uploadReports[0].errors) == 0

    collection = model.Sequence(location=uploadReports[0].location)
    with requests.session() as s:
        geovisio_cli.sequences.status.wait_for_sequence(
            s, collection, timeout=timedelta(minutes=1)
        )
        status = geovisio_cli.sequences.status.get_status(s, collection)
        sequence_info = geovisio_cli.sequences.status.info(s, collection)
    # 3 pictures should have been uploaded
    assert len(status.pictures) == 3

    for i in status.pictures:
        assert i.status == "ready"

    # the collection should also have 3 items
    collection = requests.get(f"{collection.location}/items")
    collection.raise_for_status()

    features = collection.json()["features"]
    assert len(features) == 3

    assert sequence_info.title == "some title"
    assert sequence_info.interior_orientation == [
        model.InteriorOrientation(make="SONY", model="FDR-X1000V", field_of_view=None)
    ]

    # Check generated TOML file
    tomlFile = datafiles / model.SEQUENCE_TOML_FILE
    with open(tomlFile, "r") as f:
        tomlFileContent = f.read()
        seqToml = toml.loads(tomlFileContent)
        assert seqToml["1"]["sequence"]["id"] == sequence_info.id
        assert seqToml["1"]["pictures"]["e1.jpg"]["id"] == features[0]["id"]
        assert seqToml["1"]["pictures"]["e2.jpg"]["id"] == features[1]["id"]
        assert seqToml["1"]["pictures"]["e3.jpg"]["id"] == features[2]["id"]


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_resume_upload(geovisio_with_token, datafiles):
    # Make e2 not valid to have a partial upload
    picE2 = datafiles / "e2.jpg"
    picE2bak = datafiles / "e2.bak"
    os.rename(picE2, picE2bak)
    with open(picE2, "w") as picE2file:
        picE2file.write("")
        picE2file.close()

    # Start upload -> 2 uploaded pics + 1 failure
    uploadReports = geovisio_cli.sequences.upload.upload(
        path=Path(datafiles),
        geovisio=geovisio_with_token,
        title="some title",
        sortMethod=model.SortMethod.filename_asc,
        pictureUploadTimeout=20,
    )
    assert len(uploadReports) == 1
    assert len(uploadReports[0].uploaded_pictures) == 2
    assert len(uploadReports[0].errors) == 1
    assert uploadReports[0].errors[0].position == 2

    # Check TOML file -> e2 has no ID but broken status
    tomlFile = datafiles / model.SEQUENCE_TOML_FILE
    with open(tomlFile, "r") as f:
        tomlFileContent = f.read()
        f.close()
        seqToml = toml.loads(tomlFileContent)
        assert seqToml["1"]["pictures"]["e2.jpg"].get("id") is None
        assert seqToml["1"]["pictures"]["e2.jpg"]["status"] == "broken"

    # Make e2 valid
    os.remove(picE2)
    os.rename(picE2bak, picE2)

    # Launch again upload : 1 uploaded pic + 0 failure
    uploadReports2 = geovisio_cli.sequences.upload.upload(
        path=Path(datafiles),
        geovisio=geovisio_with_token,
        title="some title",
        sortMethod=model.SortMethod.filename_asc,
        pictureUploadTimeout=20,
    )
    assert uploadReports2[0].location == uploadReports[0].location
    assert len(uploadReports2[0].uploaded_pictures) == 1
    assert len(uploadReports2[0].errors) == 0

    # Check TOML file -> everything has ID and looks like a charm
    with open(tomlFile, "r") as f:
        tomlFileContent = f.read()
        f.close()
        seqToml2 = toml.loads(tomlFileContent)
        assert seqToml2["1"]["sequence"]["id"] == seqToml["1"]["sequence"]["id"]
        assert (
            seqToml2["1"]["pictures"]["e1.jpg"]["id"]
            == seqToml["1"]["pictures"]["e1.jpg"]["id"]
        )
        assert seqToml2["1"]["pictures"]["e2.jpg"]["id"] is not None
        assert seqToml2["1"]["pictures"]["e2.jpg"].get("status") is None
        assert (
            seqToml2["1"]["pictures"]["e3.jpg"]["id"]
            == seqToml["1"]["pictures"]["e3.jpg"]["id"]
        )


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_upload_twice(geovisio_with_token, datafiles):
    """Uploading twice the same sequence, should result of nothing done in the second upload"""
    # Start upload -> 2 uploaded pics + 1 failure
    uploadReports = geovisio_cli.sequences.upload.upload(
        path=Path(datafiles),
        geovisio=geovisio_with_token,
        title="some title",
        pictureUploadTimeout=20,
    )
    assert len(uploadReports) == 1
    assert len(uploadReports[0].uploaded_pictures) == 3
    assert len(uploadReports[0].errors) == 0

    # Launch again upload : 1 uploaded pic + 0 failure
    uploadReports2 = geovisio_cli.sequences.upload.upload(
        path=Path(datafiles),
        geovisio=geovisio_with_token,
        title="some title",
        pictureUploadTimeout=20,
    )
    assert len(uploadReports2) == 1
    assert uploadReports2[0].location == uploadReports[0].location
    assert len(uploadReports2[0].uploaded_pictures) == 0
    assert len(uploadReports2[0].errors) == 0


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_on_invalid_url_host(datafiles):
    with pytest.raises(exception.CliException) as e:
        geovisio_cli.sequences.upload.upload(
            path=Path(datafiles),
            geovisio=model.Geovisio(url="http://some_invalid_url"),
            title="some title",
            pictureUploadTimeout=20,
        )
    msg = str(e.value)
    assert msg.startswith(
        """The API is not reachable. Please check error and used URL below, and retry later if the URL is correct.

[bold]Used URL:[/bold] http://some_invalid_url/api
[bold]Error:[/bold]"""
    )
    assert "Failed to establish a new connection:" in msg


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_on_invalid_url_path(geovisio_with_token, datafiles):
    with pytest.raises(exception.CliException) as e:
        geovisio_cli.sequences.upload.upload(
            path=Path(datafiles),
            geovisio=model.Geovisio(
                url=geovisio_with_token.url + "/some_additional_path"
            ),
            title=None,
            pictureUploadTimeout=20,
        )
    msg = str(e.value)
    assert msg.startswith(
        f"""The API URL is not valid.

Note that your URL should be the API root (something like https://geovisio.fr, https://panoramax.ign.fr or any other geovisio instance).
Please make sure you gave the correct URL and retry.

[bold]Used URL:[/bold] {geovisio_with_token.url}/some_additional_path/api
[bold]Error:[/bold]"""
    )


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
)
def test_upload_on_invalid_url_schema(datafiles):
    with pytest.raises(exception.CliException) as e:
        geovisio_cli.sequences.upload.upload(
            path=Path(datafiles),
            geovisio=model.Geovisio(url="a non valid url at all"),
            title=None,
            pictureUploadTimeout=20,
        )
    assert str(e.value).startswith(
        """Error while connecting to the API. Please check error and used URL below

[bold]Used URL:[/bold] a non valid url at all/api
[bold]Error:[/bold]"""
    )
