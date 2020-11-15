from pathlib import Path
import click


@click.command()
@click.option('--root_path', default='/mnt/Data/scratch',
              show_default=True,
              help='Delete files in all subdirectories')
@click.option('--extensions', default=['.py', '.ipynb', '.java'],
              help='Exclude files with given extension',
              show_default=True,
              multiple=True)
@click.option('--dry-run/--no-dry-run', default=True, show_default=True,
              help='List files to be deleted')
def clean(root_path, extensions, dry_run):
    for file in Path(root_path).glob(f"**/*"):
        if file.is_file():
            if file.suffix not in extensions:
                print(file)
                if (not dry_run):
                    file.unlink()
