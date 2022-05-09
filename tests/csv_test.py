"This tests for SCV files"


def test_csv_upload(client):
    "Tes for CSV upload after login"
    response = client.get("/songs/upload")
    assert response.status_code == 302
