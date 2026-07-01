import sys
import traceback
import flet as ft

from app.bootstrap import configure_app


# Global exception logger
def log_exception(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions to file and stdout."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # Write to file
    with open('debug_global_exception.log', 'a', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(f"GLOBAL EXCEPTION: {exc_type.__name__}\n")
        f.write("="*70 + "\n")
        f.write(tb)
        f.write("\n")
    
    # Print to console
    print("\n" + "="*70)
    print(f"GLOBAL EXCEPTION: {exc_type.__name__}")
    print("="*70)
    print(tb)
    print("="*70 + "\n")


sys.excepthook = log_exception


def main(page: ft.Page) -> None:
    """Initialize the app shell for Sprint 01 Epic 1."""
    try:
        configure_app(page)
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        with open('debug_main_error.log', 'w', encoding='utf-8') as f:
            f.write(tb)
        print("\nERROR IN main():")
        print(tb)
        raise


if __name__ == "__main__":
    ft.run(main)
