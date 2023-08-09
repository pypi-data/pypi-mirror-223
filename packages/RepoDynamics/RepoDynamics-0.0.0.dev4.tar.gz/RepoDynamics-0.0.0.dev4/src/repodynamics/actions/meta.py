import sys

from markitup import html, md

from repodynamics.ansi import SGR

def meta(
    cache_hit: bool,
    force_update: str,
    metadata_filepath: str,
    cache_filepath: str,
    github_token: str,
) -> tuple[dict, str]:

    if force_update not in ["all", "core", "none"]:
        print(
           SGR.format(
                f"ERROR! Invalid input for 'force_update': '{force_update}'.",
                styles=SGR.style(background_color="red"),
           )
        )
        sys.exit(1)

    if force_update != "none" or not cache_hit:
        from repodynamics.metadata import Metadata
        metadata = Metadata(
            path_cache=cache_filepath,
            update_cache=force_update == "all",
            github_token=github_token,
        )
        metadata_str = metadata.json()
        metadata_str_pretty = metadata.json(indent=4)
        metadata.json(write_to_file=True, output_filepath=metadata_filepath)
    else:
        import json
        with open(metadata_filepath) as f:
            metadata_dict = json.load(f)
        metadata_str = json.dumps(metadata_dict)
        metadata_str_pretty = json.dumps(metadata_dict, indent=4)

    output = {"json": metadata_str}

    force_update_emoji = "✅" if force_update == "all" else ("❌" if force_update == "none" else "☑️")
    cache_hit_emoji = "✅" if cache_hit else "❌"
    if not cache_hit or force_update == "all":
        result = "Updated all metadata"
    elif force_update == "core":
        result = "Updated core metadata but loaded API metadata from cache"
    elif force_update == "none":
        result = "Loaded all metadata from cache"
    else:
        raise ValueError(f"Unknown force_update value: {force_update}")

    metadata_details = html.details(
        content=md.code_block(metadata_str_pretty, "json"),
        summary="🖥 Metadata",
        content_indent=""
    )
    results_list = html.ul(
        [
            f"{force_update_emoji}  Force update (input: {force_update})",
            f"{cache_hit_emoji}  Cache hit",
            f"➡️ {result}",
        ],
        content_indent="",
    )
    log = f"<h2>Repository Metadata</h2>{results_list}<br>\n{metadata_details}"
    return output, log
