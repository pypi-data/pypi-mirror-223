import os

from pytest import MonkeyPatch

from tons import settings


def test_settings_extra_config_path(tons_workdir):
    # SETUP
    extra_config_path = str(tons_workdir / "extra_config.yaml")
    with MonkeyPatch.context() as monkeypatch_context:
        # SETUP
        monkeypatch_context.setenv("TONS_CONFIG_PATH", extra_config_path)
        monkeypatch_context.setattr(settings, "GLOBAL_CONFIG_PATH", [tons_workdir / "config.yaml"])
        monkeypatch_context.setattr(settings, "CUSTOM_CONFIG_PATH", None)

        import importlib
        importlib.reload(settings)

        # ASSERT
        assert os.environ.get("TONS_CONFIG_PATH") == extra_config_path
        assert settings.CUSTOM_CONFIG_PATH == extra_config_path
