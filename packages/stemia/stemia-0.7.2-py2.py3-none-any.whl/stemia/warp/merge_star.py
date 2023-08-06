import click


@click.command()
@click.argument('star_files', nargs=-1, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('-o', '--star-output', required=True, type=click.Path(dir_okay=False, resolve_path=True),
              help='where to put the merged star file')
@click.option('-f', '--overwrite', is_flag=True, help='overwrite output if exists')
def cli(star_files, star_output, overwrite):
    """
    Merge star files ignoring optic groups and ensuring columns for warp.
    """
    from pathlib import Path

    import starfile
    import numpy as np
    import pandas as pd
    from scipy.interpolate import splprep, splev
    from rich.progress import track
    from rich import print

    if Path(star_output).is_file() and not overwrite:
        raise click.UsageError(f'{star_output} exists but "-f" flag was not passed')

    data = []
    for f in track(star_files, description='Reading star files...'):
        df = starfile.read(f)
        if isinstance(df, dict):
            df = df['particles']
        df.rename(columns={'experiment_id': 'rlnMicrographName'}, inplace=True)
        df.rename(columns={'rlnTomoName': 'rlnMicrographName'}, inplace=True)
        data.append(df)

    data = pd.concat(data, ignore_index=True)
    starfile.write(data, star_output, overwrite=overwrite)
    print("You may have to edit the micrograph name column to match Warp's tomostar file names.")
