# Importing the necessary modules (Імпортуємо необхідні модулі)
import pkg_resources  # For obtaining the local Python packages and their versions (Для отримання інформації про локальні пакети Python та їх версії)
import subprocess  # For running shell commands to update packages (Для виконання команд оболонки для оновлення пакетів)
import asyncio  # For handling asynchronous tasks to fetch remote package versions (Для обробки асинхронних завдань отримання версій віддалених пакетів)
import time  # For measuring execution time (Для вимірювання часу виконання)
import aiohttp  # For making asynchronous HTTP requests (Для здійснення асинхронних HTTP-запитів)
from tqdm import (
    tqdm,
)  # For displaying progress bars during iterations (Для відображення панелі прогресу під час ітерацій)

# import winsound  # For playing a beep sound at the end of the program (Для відтворення звукового сигналу в кінці програми). This module uncomment on Windows only!!!


# Get the version of a package from PyPI asynchronously (Отримати версію пакету з PyPI асинхронно)
async def get_remote_package_version(session, package):
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                version = data["info"]["version"]
                return package, version
    except Exception as e:
        print(f"Error retrieving data for {package}: {e}")
        return package, None


# Get the dictionary of installed Python packages (Отримати словник встановлених пакетів Python)
def get_installed_python_packages():
    installed_packages = {}

    for package in pkg_resources.working_set:
        installed_packages[package.project_name] = package.version
    return installed_packages


# Get the versions of packages from PyPI asynchronously (Отримати версії пакетів з PyPI асинхронно)
async def get_remote_package_versions(packages):
    print("\n")
    async with aiohttp.ClientSession() as session:
        tasks = [get_remote_package_version(session, package) for package in packages]
        remote_versions = {}
        for task in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc="Requesting to(Запит до) PyPI",
        ):
            package, version = await task
            if version:
                remote_versions[package] = version
        return remote_versions


# Update the packages (Оновити пакети)
def update_packages(packages, local_packages):
    print("\n")
    with tqdm(
        total=len(packages),
        desc=f"Needs to update {len(packages)} of {len(local_packages)} installed packages (Потрібно оновити {len(packages)} з {len(local_packages)} інстальованих пакетів)",
    ) as pbar:
        for package in packages:
            command = f"pip install --upgrade {package}"
            subprocess.run(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            pbar.update(1)


if __name__ == "__main__":
    start_time = time.time()

    # Get the dictionary of local packages and their versions (Отримати словник локальних пакетів та їх версій)
    local_packages = get_installed_python_packages()

    # Get the versions of packages from PyPI (Отримати версії пакетів з PyPI)
    remote_packages = asyncio.run(get_remote_package_versions(local_packages.keys()))

    # Find packages to update (Знайти пакети для оновлення)
    packages_to_update = [
        package
        for package, local_version in local_packages.items()
        if package in remote_packages and remote_packages[package] > local_version
    ]

    if packages_to_update:
        # print(f"\nNeeds to update {len(remote_packages)} of {len(local_packages)} installed packages (Потрібно оновити {len(remote_packages)} з {len(local_packages)} інстальованих пакетів):\n")
        print("\nPackages to update (Пакети, які потрібно оновити):\n")
        for package in packages_to_update:
            print(
                f"{package} (current version(поточна версія): {local_packages[package]}, update to(оновити до): {remote_packages[package]})"
            )

        # Update the packages (Оновити пакети)
        update_packages(packages_to_update, local_packages)
    else:
        print(
            f"\nAll {len(local_packages)} packages are up to date (Усі {len(local_packages)} пакетів вже оновлені до останньої версії)."
        )

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Process completed successfully (Процес успішно завершено).")
    print(f"\n\nExecution time (Час виконання): {elapsed_time:.2f} seconds.")

    # Play a beep sound (Програти звуковий сигнал). # This module uncomment on Windows only!!!
    # winsound.Beep(800, 500)

    # Ensure the console doesn't close immediately after the program finishes (Забезпечити, щоб консоль не закривалася після завершення програми)
    input("Press Enter to exit (Натисніть Enter, щоб вийти)...")
