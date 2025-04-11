from django.contrib.sitemaps import Sitemap


class CommonSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return [
            "/",
            "/about/",
            "/program/",
            "/discover/moods/",
            "/discover/tracks/",
            "/discover/playlists/",
            "/discover/artists/",
            "/discover/editors/",
            "/reception/",
            "/faq/",
            "/about/",
            "/donate/",
            "/imprint/",
            "/imprint/",
        ]

    def location(self, item):
        return item
