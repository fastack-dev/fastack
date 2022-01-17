import os
import shutil
import sys
import textwrap


def sync_api_docs():
    """
    Syncs the API docs from source
    """

    print("Syncing API docs")
    try:
        input(
            "This will delete all content that is in the docs/api. Press CTRL-C to cancel"
        )
    except KeyboardInterrupt:
        exit(1)

    api_dir = os.path.join("docs", "api")
    shutil.rmtree(api_dir)
    excluded_files = [
        os.path.join("fastack", "globals.py"),
        os.path.join("fastack", "__main__.py"),
    ]
    for root, dirs, files in os.walk("fastack"):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith(".py") and filepath not in excluded_files:
                outdir = os.path.join(api_dir, root)
                os.makedirs(outdir, exist_ok=True)
                print(f"Syncing {filepath}")
                outfile = os.path.splitext(file)[0] + ".md"
                py_module = filepath.replace(os.sep, ".").replace(".py", "")
                with open(os.path.join(outdir, outfile), "w") as fp:
                    content = textwrap.dedent(
                        f"""\
                    # {py_module}
                    ::: {py_module}
                    """
                    )
                    fp.write(content)


def main():
    handlers = {"sync_api_docs": sync_api_docs}
    try:
        arg = sys.argv[1]
    except IndexError:
        print("No command specified")
        exit(1)

    func = handlers.get(arg)
    if not func:
        print(f"Invalid command: {arg}")
        exit(1)

    func()


if __name__ == "__main__":
    main()
