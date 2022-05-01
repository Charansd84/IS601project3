"""This tests the Locations page"""


def song_page_content(client):
    response = client.get("/locations_datatables/")
    assert "Upload Locations" in response.data
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/welcome"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data