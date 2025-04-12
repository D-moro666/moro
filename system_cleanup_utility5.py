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
# Individual Cleanup Functions
# ------------------------------

def clear_temp_files():
    """Clear temporary files."""
    temp_dir = os.getenv('TEMP', "C:\\Windows\\Temp")
    logging.info("Clearing temporary files...")
    if os.path.exists(temp_dir):
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    logging.info(f"Cleared: {file_path}")
                except Exception as e:
                    logging.warning(f"Skipped: {file_path} ({e})")
                    skipped_files.append(file_path)
    logging.info(f"Completed clearing temporary files in {temp_dir}.")


def clear_prefetch_files():
    """Clear prefetch files."""
    prefetch_dir = "C:\\Windows\\Prefetch"
    logging.info("Clearing prefetch files...")
    if os.path.exists(prefetch_dir):
        for file in os.listdir(prefetch_dir):
            file_path = os.path.join(prefetch_dir, file)
            try:
                os.remove(file_path)
                logging.info(f"Cleared: {file_path}")
            except Exception as e:
                logging.warning(f"Skipped: {file_path} ({e})")
                skipped_files.append(file_path)
    logging.info("Completed clearing prefetch files.")


def clear_memory_dump_files():
    """Clear system memory dump files."""
    logging.info("Clearing memory dump files...")
    dump_dirs = [
        r"C:\Windows\Minidump",  # Mini dump files directory
        r"C:\Windows\MEMORY.DMP"  # System memory dump file
    ]
    for dump_dir in dump_dirs:
        if os.path.exists(dump_dir):
            if os.path.isfile(dump_dir):  # Case for MEMORY.DMP
                try:
                    os.remove(dump_dir)
                    logging.info(f"Cleared: {dump_dir}")
                except Exception as e:
                    logging.warning(f"Skipped: {dump_dir} ({e})")
                    skipped_files.append(dump_dir)
            else:  # Case for directories like Minidump
                for file in os.listdir(dump_dir):
                    file_path = os.path.join(dump_dir, file)
                    try:
                        os.remove(file_path)
                        logging.info(f"Cleared: {file_path}")
                    except Exception as e:
                        logging.warning(f"Skipped: {file_path} ({e})")
                        skipped_files.append(file_path)
    logging.info("Finished clearing memory dump files.")


def clear_application_cache():
    """Clear cache files for various applications."""
    logging.info("Clearing application caches...")
    chrome_cache = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache")
    if os.path.exists(chrome_cache):
        try:
            shutil.rmtree(chrome_cache)
            logging.info("Cleared Chrome cache.")
        except Exception as e:
            logging.warning(f"Failed to clear Chrome cache. ({e})")
            skipped_files.append(chrome_cache)

    firefox_cache = os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles")
    if os.path.exists(firefox_cache):
        for profile in os.listdir(firefox_cache):
            cache_path = os.path.join(firefox_cache, profile, "cache2")
            if os.path.exists(cache_path):
                try:
                    shutil.rmtree(cache_path)
                    logging.info(f"Cleared Firefox cache for profile: {profile}")
                except Exception as e:
                    logging.warning(f"Failed to clear Firefox cache for profile {profile}. ({e})")
                    skipped_files.append(cache_path)
    logging.info("Completed clearing application caches.")


def clear_cookies():
    """Clear browser cookies."""
    logging.info("Clearing browser cookies...")
    chrome_cookies = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies")
    if os.path.exists(chrome_cookies):
        try:
            os.remove(chrome_cookies)
            logging.info("Cleared Chrome cookies.")
        except Exception as e:
            logging.warning(f"Failed to clear Chrome cookies. ({e})")
            skipped_files.append(chrome_cookies)

    firefox_profiles = os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles")
    if os.path.exists(firefox_profiles):
        for profile in os.listdir(firefox_profiles):
            cookies_file = os.path.join(firefox_profiles, profile, "cookies.sqlite")
            if os.path.exists(cookies_file):
                try:
                    os.remove(cookies_file)
                    logging.info(f"Cleared Firefox cookies for profile: {profile}")
                except Exception as e:
                    logging.warning(f"Failed to clear Firefox cookies for profile {profile}. ({e})")
                    skipped_files.append(cookies_file)
    logging.info("Completed clearing browser cookies.")


def clear_unused_windows_install_files():
    """Remove unused Windows installation files."""
    logging.info("Removing unused Windows installation files...")
    try:
        subprocess.check_call(["dism", "/online", "/cleanup-image", "/StartComponentCleanup", "/ResetBase"])
        logging.info("Successfully removed unused Windows installation files.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to remove unused Windows installation files: {e}")


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


def clear_dns_cache():
    """Flush the DNS cache."""
    logging.info("Flushing DNS cache...")
    try:
        os.system("ipconfig /flushdns")
        logging.info("DNS cache flushed successfully.")
    except Exception as e:
        logging.error(f"Error flushing DNS cache: {e}")


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


# ------------------------------
# Main Execution Routine
# ------------------------------

def main():
    """Main function for running cleanup tasks."""
    if not is_admin():
        logging.error("You must run this script as an administrator.")
        return

    # Execute cleanup tasks
    clear_temp_files()
    clear_prefetch_files()
    clear_memory_dump_files()
    clear_application_cache()
    clear_cookies()
    clear_unused_windows_install_files()
    clear_system_logs()
    clear_dns_cache()
    clear_recycle_bin()

    # Display summary of skipped/deleted files.
    logging.info("\n--- Cleanup Summary ---")
    if skipped_files:
        logging.warning("The following files or tasks were skipped (locked or in use):")
        for file in skipped_files:
            logging.warning(f"  - {file}")
    else:
        logging.info("All cleanup tasks completed successfully!")


# Entry point for script execution
if __name__ == "__main__":
    main()