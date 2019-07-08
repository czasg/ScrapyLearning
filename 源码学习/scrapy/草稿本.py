import pkg_resources


def run_entry_point(data):
    group = 'package?'
    for entrypoint in pkg_resources.iter_entry_points(group=group):
        print('entrypoint:', entrypoint)
        plugin = entrypoint.load()
        plugin(data)

run_entry_point(100)