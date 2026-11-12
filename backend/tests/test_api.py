def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy"}


def test_blogs_seeded(client):
    r = client.get("/api/v1/blogs")
    assert r.status_code == 200
    assert r.json()["total"] > 0


def test_blog_crud(client):
    payload = {
        "title": "CI post",
        "excerpt": "excerpt",
        "content": "content",
        "author": "ci",
        "date": "2026-01-01",
        "category": "Test",
        "image_url": "https://example.com/x.jpg",
    }
    r = client.post("/api/v1/blogs", json=payload)
    assert r.status_code == 201, r.text
    post_id = r.json()["id"]

    assert client.get(f"/api/v1/blogs/{post_id}").status_code == 200
    assert client.delete(f"/api/v1/blogs/{post_id}").status_code == 204
    assert client.get(f"/api/v1/blogs/{post_id}").status_code == 404


def test_recommend_returns_stay22_links(client):
    r = client.post(
        "/api/v1/recommendations/recommend",
        json={"user_demand": "hotel in Paris for 2 adults"},
    )
    assert r.status_code == 200, r.text
    data = r.json()

    assert data["extracted_parameters"]["location"] == "Paris"
    assert data["matched_hotels"], "mock data should yield hotels"
    for hotel in data["matched_hotels"]:
        assert hotel["url"].startswith("https://www.stay22.com/allez/roam?aid=testaid")

    assert data["stay22_map_url"].startswith("https://www.stay22.com/embed/gm?aid=testaid")
