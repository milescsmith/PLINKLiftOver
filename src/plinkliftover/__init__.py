# type: ignore[attr-defined]
"""`plinkliftover` Converts genotype data stored in plink's PED+MAP format from one genome build to another, using liftOver"""
try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
