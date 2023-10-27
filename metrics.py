def get_tags():
    import socket
    tags = [
        f"host={socket.getfqdn()}",
        f"instance={instance}",
        f"borg_repository_id={borg_repository_id}",
    ]
    return ','.join(tags)


def get_fields(borg_data):
    from datetime import datetime

    borg_repository_id = borg_data['repository']['id']
    # borg_rc = borg_data['archive']['rc'] # Does not exist in JSON.
    # borg_archive_name = borg_data['archive']['id'] # TODO
    borg_duration_seconds = borg_data['archive']['duration']
    borg_archive_id = borg_data['archive']['id']

    borg_archive_compressed_size_bytes = borg_data['archive']['stats']['compressed_size']
    borg_archive_deduplicated_size_bytes = borg_data['archive']['stats']['deduplicated_size']
    borg_archive_original_size_bytes = borg_data['archive']['stats']['original_size']
    borg_archive_files_count = borg_data['archive']['stats']['nfiles']
    # Total chunks
    borg_cache_total_chunks_count = borg_data['cache']['stats']['total_chunks']
    # Unique chunks
    borg_cache_total_unique_chunks_count = borg_data['cache']['stats']['total_unique_chunks']
    # All archives: Original size
    borg_cache_total_size_bytes = borg_data['cache']['stats']['total_size']
    # All archives: Compressed size
    borg_cache_total_compressed_size_bytes = borg_data['cache']['stats']['total_csize']
    # All archives: Deduplicated size
    borg_cache_unique_compressed_size_bytes = borg_data['cache']['stats']['unique_csize']
    # Not shown in human-readable output; "Uncompressed size of all chunks" which is not a too useful information.
    borg_cache_unique_size_bytes = borg_data['cache']['stats']['unique_size']

    fields = [
        f"begin={datetime.now().isoformat()}",  # TODO: err, that's stupid
        f"end={datetime.now().isoformat()}",
        f"durationSeconds=0",  # TODO: err, that's stupid
        f"durationMinutes=0",  # TODO: err, that's stupid

        f"borg_repository_id={borg_repository_id}",
        f"borg_exit_code={borg_rc}",  # TODO
        f"borg_repository={borg_repository}",  # TODO
        f"borg_archive_name={borg_archive_name}",  # TODO
        f"borg_upload_ratelimit={borg_upload_ratelimit}",  # TODO
        f"borg_duration_seconds={borg_duration_seconds}",
        f"borg_archive_id={borg_archive_id}",

        f"borg_archive_id={borg_archive_id}",
        f"borg_archive_compressed_size_bytes={borg_archive_compressed_size_bytes}",
        f"borg_archive_deduplicated_size_bytes={borg_archive_deduplicated_size_bytes}",
        f"borg_archive_original_size_bytes={borg_archive_original_size_bytes}",
        f"borg_archive_files_count={borg_archive_files_count}",
        f"borg_cache_total_chunks_count={borg_cache_total_chunks_count}",
        f"borg_cache_total_unique_chunks_count={borg_cache_total_unique_chunks_count}",
        f"borg_cache_total_size_bytes={borg_cache_total_size_bytes}",
        f"borg_cache_total_compressed_size_bytes={borg_cache_total_compressed_size_bytes}",
        f"borg_cache_unique_compressed_size_bytes={borg_cache_unique_compressed_size_bytes}",
        f"borg_cache_unique_size_bytes={borg_cache_unique_size_bytes}"
    ]
    return ','.join(fields)


def write(borg_data, metrics_output_file):
    import time

    measurement = "create-backup.sh"
    tags = get_tags()
    fields = get_fields()
    timestamp = time.time_ns()
    line = f"{measurement},{tags} {fields} {timestamp}"

    with open(metrics_output_file, 'a') as file:
        file.write(line + '\n')
