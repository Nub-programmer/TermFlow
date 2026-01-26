"""Resource path resolution using importlib.resources and platformdirs."""

from pathlib import Path
from importlib.resources import files
import platformdirs


def get_resource_path(filename: str) -> Path:
    """
    Get the absolute path to a packaged resource file (e.g., HELP.md, INFO.md).
    
    Handles both installed and development modes:
    - Installed mode: uses importlib.resources to access files from the data package
    - Development mode: falls back to relative paths from project root
    
    Args:
        filename: Name of the resource file (e.g., "HELP.md", "INFO.md")
    
    Returns:
        Path to the resource file
    """
    # Try importlib.resources for installed packages (files in termflow/data/)
    try:
        resource = files("termflow.data") / filename
        # Verify the resource exists by attempting to read it
        if hasattr(resource, '__fspath__'):
            path = Path(str(resource))
            if path.exists():
                return path
        # For contexts package (e.g., zip files), still return the resource
        with files("termflow.data").joinpath(filename).open('r'):
            pass
        return Path(str(resource))
    except (FileNotFoundError, TypeError, AttributeError, IsADirectoryError):
        pass
    
    # Fallback for development mode: check both termflow/data/ and project root
    data_dir = Path(__file__).parent.parent / "data"
    resource_path = data_dir / filename
    if resource_path.exists():
        return resource_path
    
    # Fallback: also check project root for development
    package_root = Path(__file__).parent.parent.parent
    resource_path = package_root / filename
    if resource_path.exists():
        return resource_path
    
    # Final fallback: return the expected path in data dir even if it doesn't exist
    # (caller should check existence)
    return data_dir / filename


def get_ui_resource_path(filename: str) -> Path:
    """
    Get the absolute path to a UI resource file (e.g., styles.tcss).
    
    Handles both installed and development modes.
    
    Args:
        filename: Name of the UI resource file (e.g., "styles.tcss")
    
    Returns:
        Path to the resource file in the data package
    """
    # Try importlib.resources for installed packages (files in termflow/data/)
    try:
        resource = files("termflow.data") / filename
        if hasattr(resource, '__fspath__'):
            path = Path(str(resource))
            if path.exists():
                return path
        # For packaged contexts, return the resource object as Path
        with files("termflow.data").joinpath(filename).open('r'):
            pass
        return Path(str(resource))
    except (FileNotFoundError, TypeError, AttributeError, IsADirectoryError):
        pass
    
    # Fallback for development mode: check termflow/data/
    data_dir = Path(__file__).parent.parent / "data"
    resource_path = data_dir / filename
    if resource_path.exists():
        return resource_path
    
    # Also check ui directory for backward compatibility during development
    ui_dir = Path(__file__).parent.parent / "ui"
    resource_path = ui_dir / filename
    if resource_path.exists():
        return resource_path
    
    # Final fallback: return expected path in data dir
    return Path(__file__).parent.parent / "data" / filename


def get_user_data_dir() -> Path:
    """
    Get the platform-appropriate directory for user data (config, todos, etc.).
    
    Uses platformdirs to ensure compatibility across Windows, macOS, and Linux.
    On Windows: typically C:\\Users\\<user>\\AppData\\Local\\termflow
    On macOS: typically ~/Library/Application Support/termflow
    On Linux: typically ~/.local/share/termflow
    
    Returns:
        Path object pointing to the user data directory (created if needed)
    """
    data_dir = Path(platformdirs.user_data_dir("termflow", "termflow"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_user_data_file(filename: str) -> Path:
    """
    Get the path to a user data file within the user data directory.
    
    Args:
        filename: Name of the data file (e.g., "todos.json", "config.toml")
    
    Returns:
        Path object for the file (file may not exist yet)
    """
    data_dir = get_user_data_dir()
    return data_dir / filename


def get_package_data_dir() -> Path:
    """
    Get the path to the package data directory (for development mode).
    
    This is primarily used as a fallback during development.
    In production, user data should use get_user_data_dir() instead.
    
    Returns:
        Path object pointing to termflow/data directory
    """
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
