import toml
import requests

def get_pypi_package_version(package_name):
    # Make a request to the PyPI JSON API
    url = f'https://pypi.org/pypi/{package_name}/json'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        try:
        # Parse the JSON response and extract the version
            package_info = response.json()
            version = package_info['info']['version']
            return version
        except KeyError:
            # If the JSON response does not contain version information
            print(f"Package '{package_name}' version not found.")
            return None
    else:
        print(f"Error: Could not fetch package '{package_name}'.")
        return None

def correctPackageVersion(currentRepositoryVersion: str, currentPyPiVersion: str):
    versionDelimiter = '.'
    if currentPyPiVersion == currentRepositoryVersion or currentPyPiVersion > currentRepositoryVersion:
        splittedVersion = currentPyPiVersion.split(versionDelimiter)
        incrementedLastVersion = int(splittedVersion[-1]) + 1
        splittedVersion[-1] = str(incrementedLastVersion)
        return versionDelimiter.join(splittedVersion)
    
    return currentRepositoryVersion


with open('Cargo.toml', 'r') as cargo_toml:
    toml_data = toml.load(cargo_toml)

currentPyPiVersion = get_pypi_package_version('rusty-chrono')
currentRepositoryVersion = toml_data['package']['version']
versionToPublish = correctPackageVersion(currentRepositoryVersion, currentPyPiVersion)
toml_data['package']['version'] = versionToPublish

with open('Cargo.toml', 'w') as cargo_toml:
    toml.dump(toml_data, cargo_toml)

print('Updated Cargo.toml to new version: ' + versionToPublish)
