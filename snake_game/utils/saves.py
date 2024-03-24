from config import save_dir


def get_latest_save_file():
    """Get the latest save file."""
    return max(save_dir.glob("*.pkl"), key=lambda x: x.stat().st_ctime, default=None)
