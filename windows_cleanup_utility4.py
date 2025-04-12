import os
import shutil
import logging
import subprocess
import ctypes

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

skipped_files = []  # List to track files that couldn't be cleared


def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


# ------------------------------
# Core Cleanup Functions
# ------------------------------

def clear_temp_files():
    """Clear temporary files."""
    temp_dir = os.getenv('TEMP', "C:\\Windows\\Temp")
    logging.info("Clearing temporary files...")
    if os.path.exists(temp_dir):
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    logging.info(f"Cleared: {os.path.join(root, file)}")
                except Exception as e:
                    logging.warning(f"Skipped: {os.path.join(root, file)} ({e})")
                    skipped_files.append(os.path.join(root, file))
    logging.info(f"Completed clearing temporary files in {temp_dir}.")


def clear_prefetch_files():
    """Clear prefetch files."""
    prefetch_dir = "C:\\Windows\\Prefetch"
    logging.info("Clearing prefetch files...")
    if os.path.exists(prefetch_dir):
        for file in os.listdir(prefetch_dir):
            try:
                os.remove(os.path.join(prefetch_dir, file))
                logging.info(f"Cleared: {os.path.join(prefetch_dir, file)}")
            except Exception as e:
                logging.warning(f"Skipped: {os.path.join(prefetch_dir, file)} ({e})")
                skipped_files.append(os.path.join(prefetch_dir, file))
    logging.info("Completed clearing prefetch files.")


def clear_memory_dump_files():
    """Clear memory dump files."""
    logging.info("Clearing memory dump files...")
    dump_dirs = [r"C:\Windows\Minidump", r"C:\Windows\MEMORY.DMP"]
    for dump_dir in dump_dirs:
        if os.path.exists(dump_dir):
            if os.path.isfile(dump_dir):
                try:
                    os.remove(dump_dir)
                    logging.info(f"Cleared: {dump_dir}")
                except Exception as e:
                    logging.warning(f"Skipped: {dump_dir} ({e})")
                    skipped_files.append(dump_dir)
            else:
                for file in os.listdir(dump_dir):
                    try:
                        os.remove(os.path.join(dump_dir, file))
                        logging.info(f"Cleared: {os.path.join(dump_dir, file)}")
                    except Exception as e:
                        logging.warning(f"Skipped: {os.path.join(dump_dir, file)} ({e})")
                        skipped_files.append(os.path.join(dump_dir, file))
    logging.info("Finished clearing memory dump files.")


def clear_windows_error_reporting_files():
    """Clear Windows Error Reporting files."""
    logging.info("Clearing Windows Error Reporting files...")
    error_dirs = [
        r"C:\ProgramData\Microsoft\Windows\WER\ReportQueue",
        r"C:\ProgramData\Microsoft\Windows\WER\ReportArchive",
    ]
    for dir_path in error_dirs:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                logging.info(f"Cleared: {dir_path}")
            except Exception as e:
                logging.warning(f"Failed to clear error reports in {dir_path}: {e}")
                skipped_files.append(dir_path)
    logging.info("Completed clearing Windows Error Reporting files.")


def clear_windows_update_cache():
    """Clear Windows Update Cache."""
    update_cache_dir = "C:\\Windows\\SoftwareDistribution\\Download"
    logging.info("Clearing Windows Update Cache...")
    if os.path.exists(update_cache_dir):
        try:
            shutil.rmtree(update_cache_dir)
            os.makedirs(update_cache_dir)
            logging.info("Windows Update Cache cleared successfully.")
        except Exception as e:
            logging.error(f"Failed to clear Windows Update Cache: {e}")
            skipped_files.append(update_cache_dir)


def clear_edge_browser_data():
    """Clear Microsoft Edge browser data."""
    logging.info("Clearing Microsoft Edge browser data...")
    edge_cache_dir = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache")
    if os.path.exists(edge_cache_dir):
        try:
            shutil.rmtree(edge_cache_dir)
            logging.info("Cleared Edge Cache.")
        except Exception as e:
            logging.warning(f"Failed to clear Edge Cache: {e}")
            skipped_files.append(edge_cache_dir)

    edge_cookies = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cookies")
    if os.path.exists(edge_cookies):
        try:
            os.remove(edge_cookies)
            logging.info("Cleared Edge Cookies.")
        except Exception as e:
            logging.warning(f"Failed to clear Edge Cookies: {e}")
            skipped_files.append(edge_cookies)
    logging.info("Completed clearing Microsoft Edge browser data.")


def clear_unused_windows_install_files():
    """Remove unused Windows installation files."""
    logging.info("Removing unused Windows installation files...")
    try:
        subprocess.check_call(["dism", "/online", "/cleanup-image", "/StartComponentCleanup", "/ResetBase"])
        logging.info("Successfully removed unused Windows installation files.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to remove unused Windows installation files: {e}")


def clean_registry():
    """Placeholder for cleaning the registry."""
    logging.info("Cleaning Windows registry using external tools or commands...")
    # This function can integrate with tools like CCleaner or PowerShell scripts to clean the registry.
    logging.info("Registry cleanup is a placeholder. Please use tools like CCleaner for this task.")


def clear_system_logs():
    """Clear Windows System Event Logs."""
    logging.info("Clearing Windows System Event Logs...")
    log_types = ["System", "Application", "Security", "Setup"]
    for log_type in log_types:
        try:
            os.system(f"wevtutil cl {log_type}")
            logging.info(f"Cleared {log_type} logs.")
        except Exception as e:
            logging.error(f"Error clearing {log_type} logs: {e}")


def clear_recycle_bin():
    """Empty Recycle Bin."""
    logging.info("Emptying Recycle Bin...")
    try:
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 3)
        if result == 0:
            logging.info("Recycle Bin emptied.")
        elif result == 2:
            logging.info("Recycle Bin was already empty.")
        else:
            logging.warning("Failed to empty Recycle Bin.")
    except Exception as e:
        logging.error(f"Error emptying Recycle Bin: {e}")


def clear_old_restore_points():
    """Clear old system restore points."""
    logging.info("Clearing old system restore points...")
    try:
        os.system("vssadmin delete shadows /for=C: /oldest /quiet")
        logging.info("Old Restore Points cleared successfully.")
    except Exception as e:
        logging.warning(f"Failed to clear old restore points: {e}")


def optimize_storage():
    """Perform disk optimization (defragmentation)."""
    logging.info("Optimizing storage...")
    try:
        os.system("defrag C: /O")
        logging.info("Optimization completed.")
    except Exception as e:
        logging.error(f"Storage optimization failed: {e}")


def flush_dns_cache():
    """Flush DNS cache."""
    logging.info("Flushing DNS cache...")
    try:
        os.system("ipconfig /flushdns")
        logging.info("DNS Cache flushed successfully.")
    except Exception as e:
        logging.error(f"Error flushing DNS cache: {e}")


# ------------------------------
# Main Execution
# ------------------------------

def main():
    if not is_admin():
        logging.error("You must run this script as an administrator.")
        return

    # Core cleanup tasks
    clear_temp_files()
    clear_prefetch_files()
    clear_memory_dump_files()
    clear_windows_update_cache()
    clear_windows_error_reporting_files()
    clear_edge_browser_data()
    clear_unused_windows_install_files()
    clear_system_logs()
    clear_recycle_bin()
    clear_old_restore_points()

    # Maintenance tasks
    optimize_storage()
    flush_dns_cache()

    # Registry cleaning task (placeholder)
    clean_registry()

    # Final summary
    if skipped_files:
        logging.warning("The following files or tasks were skipped:")
        for file in skipped_files:
            logging.warning(f"  - {file}")
    else:
        logging.info("All cleaning tasks were completed successfully!")


if __name__ == "__main__":
    main()