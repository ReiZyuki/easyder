import inspect

from .parser import parse, STAGES


COOKIE_VARIABLE = "Cooki"


class EasyDer:

    def __init__(self, cookies=None):
        import os
        from .downloader import Downloader

        self.downloader = Downloader()
        self.cookies = cookies or []

    def _get_working_cookie(self, url):
        if not self.cookies:
            return None

        print("Checking cookies...")

        for cookie in self.cookies:
            if not cookie:
                continue

            if not self.downloader.cookie_exists(cookie):
                print(f"❌ Cookie file not found: {cookie}")
                print("   → Continuing...")
                continue

            try:
                print(f"🔍 Testing cookie: {cookie}")

                self.downloader.test_cookie(
                    url,
                    cookie
                )

                print(f"✅ Cookie works: {cookie}")
                return cookie

            except Exception as e:
                print(f"❌ Cookie failed: {cookie}")
                print(f"   → {e}")
                print("   → Continuing...")

        print("⚠️ No working cookie found.")
        return None

    def execute(self, expression, url=None, progress_callback=None):
        config = parse(expression)

        if url is not None:
            config["url"] = url

        if not config["url"]:
            raise ValueError("URL missing")

        try:
            return self.downloader.execute(
                config,
                cookies=None,
                progress_callback=progress_callback
            )

        except Exception as normal_error:
            print("\n⚠️ Normal request failed.")

            working_cookie = self._get_working_cookie(
                config["url"]
            )

            if working_cookie is None:
                print("❌ No working cookie available.")
                raise normal_error

            print(
                f"🍪 Using working cookie: "
                f"{working_cookie}"
            )

            return self.downloader.execute(
                config,
                cookies=working_cookie,
                progress_callback=progress_callback
            )

    def __call__(
        self,
        expression,
        url=None,
        progress_callback=None
    ):
        return self.execute(
            expression,
            url,
            progress_callback
        )


def _get_user_cookies():
    frame = inspect.currentframe()

    try:
        if frame is None:
            return []

        caller = frame.f_back

        while caller is not None:
            cookies = caller.f_locals.get(
                COOKIE_VARIABLE
            )

            if cookies is None:
                cookies = caller.f_globals.get(
                    COOKIE_VARIABLE
                )

            if cookies is not None:
                if isinstance(cookies, str):
                    return [cookies]

                if isinstance(cookies, (list, tuple)):
                    return list(cookies)

            caller = caller.f_back

        return []

    finally:
        del frame


def rz(
    expression,
    url=None,
    progress_callback=None
):
    cookies = _get_user_cookies()

    handler = EasyDer(cookies)

    return handler.execute(
        expression,
        url,
        progress_callback
    )
