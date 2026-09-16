"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2021

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""

import os


INDEX_TEMPLATE = \
"""
<html>
<head>
<link rel="stylesheet" href="theme.css">
</head>
<body>
<h1>TST_OVEN_EOX6021_ST</h1>
<div>
{versions}
</div>
</body>
</html>
"""
VERSION_TEMPLATE = '  <button class="button" onclick="location.href=\'{version}/index.html\';" >{version}</button>'


def main():
    # Assign locations
    working_directory = os.path.split(os.path.realpath(__file__))[0]
    location_build = os.path.join(working_directory, "Build")
    location_landing_page = os.path.join(working_directory, 'Build', 'index.html')
    # Collect versions from filesystem
    versions = [directory for directory in os.listdir(location_build) if os.path.isdir(os.path.join(location_build, directory))]
    # Create html versions
    html_versions = '\n'.join([VERSION_TEMPLATE.format(version=v) for v in versions])
    # Insert html versions to html index
    html_index = INDEX_TEMPLATE.format(versions=html_versions)
    # Write to index file
    with open(location_landing_page, "w") as file:
        file.write(html_index)


if __name__ == '__main__':
    main()
