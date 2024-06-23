from pathlib import Path
from streamlit.source_util import (
    page_icon_and_name,
    calc_md5,
    get_pages,
    _on_pages_changed
)
def add_page(main_script_path_str, page_name):
    """
    Adds a new page to the Streamlit app by updating the pages dictionary with the new page's details.

    Parameters:
    - main_script_path_str (str): The path to the main script of the Streamlit app as a string.
    - page_name (str): The name of the page to be added. This function searches for a Python file that includes the page_name in its filename within the main script's directory or its 'Page' subdirectory.

    This function does not return any value but triggers the _on_pages_changed signal to refresh the app's page list.
    """
    pages = get_pages(main_script_path_str)
    main_script_path = Path(main_script_path_str)
    pages_dir = main_script_path.parent / "Page"
    script_path = [f for f in list(pages_dir.glob("*.py")) + list(main_script_path.parent.glob("*.py")) if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)
    psh = calc_md5(script_path_str)
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }
    _on_pages_changed.send()
def delete_page(main_script_path_str, page_name):
    """
    Deletes a page from the Streamlit app by removing it from the pages dictionary based on the page name.

    Parameters:
    - main_script_path_str (str): The path to the main script of the Streamlit app as a string.
    - page_name (str): The name of the page to be deleted.

    This function does not return any value but triggers the _on_pages_changed signal to refresh the app's page list.
    """
    current_pages = get_pages(main_script_path_str)
    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
    _on_pages_changed.send()

