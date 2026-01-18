from termflow.ui.app import TermFlowApp
import sys

def main():
    """Entry point for TermFlow."""
    app = TermFlowApp()
    app.run()

if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("TermFlow requires Python 3.8 or higher.")
        sys.exit(1)
        
    main()
