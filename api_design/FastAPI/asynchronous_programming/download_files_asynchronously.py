"""
This script demonstrates how to download multiple files asynchronously 
using the httpx library for HTTP requests and
aiofiles for asychronous file operations.
"""

import asyncio
import tempfile
import time
from pathlib import Path
from loguru import logger

import aiofiles
import httpx


async def download_file(client: httpx.AsyncClient, url: str, dest_folder: Path) -> Path:
    """
    Download a single file asynchronously.
    Args:
        client (httpx.AsyncClient): An instance of httpx.AsyncClient for making HTTP requests
        url (str): The URL of the file to download
        dest_folder (Path): The destination folder to save the downloaded file
    """

    async with client.stream("GET", url) as response:
        response.raise_for_status()
        size_in_mb = int(response.headers.get("content-length")) // 1024
        num_bytes_downloaded = response.num_bytes_downloaded
        file_name = Path(response.url.path).name
        file_path = dest_folder / file_name

        # Use an asynchronous file API instead of synchronous open()
        async with aiofiles.open(file_path, "wb") as f:
            async for chunck in response.aiter_bytes(1024 * 1024): # 1 MB chunks
                await f.write(chunck)
                downloaded = response.num_bytes_downloaded - num_bytes_downloaded
                logger.info(f"{file_name} downloaded {downloaded // 1024} MB of {size_in_mb} MB from {url}")

        return file_path


async def download_files(client: httpx.AsyncClient, urls: list[str], dest_folder: Path) -> list[Path]:
    """
    Download multiple files asynchronously.
    Args:
        client (httpx.AsyncClient): An instance of httpx.AsyncClient for making HTTP requests
        urls (list[str]): List of file URLs to download
        dest_folder (Path): The destination folder to save the downloaded files

    Note:
        - All downloads run concurrently (not sequential)
        - httpx handles async streaming efficiently (no need to load the whole file into memory)
        - connection pooling reduces overhead of repeated connections
    """

    tasks = [download_file(client=client, url=url, dest_folder=dest_folder) for url in urls]
    results = await asyncio.gather(*tasks) # concurrent downlaoding

    return results


async def main(urls: list[str]):
    """
    Create a temporary workspace for files, where processing them and
    delete them automatically when the context manager exits.
    """
    
    with tempfile.TemporaryDirectory() as dest_folder:
        async with httpx.AsyncClient() as client:
            results = await download_files(client=client, urls=urls, dest_folder=Path(dest_folder))
            logger.info(f"saved_files: {[str(p) for p in results]}")


if __name__ == "__main__":
    urls = [
        "https://onlinetestcase.com/wp-content/uploads/2023/06/1.1-MB-1.jpg",
        "https://onlinetestcase.com/wp-content/uploads/2023/06/2.1-MB-1-scaled.jpg",
        "https://onlinetestcase.com/wp-content/uploads/2023/06/6.1-MB.jpg",
        "https://onlinetestcase.com/wp-content/uploads/2023/06/7.2-MB.jpg",
    ]

    start_time = time.time()
    asyncio.run(main(urls))
    total_time = time.time() - start_time
    logger.info("Took {total_time:.2f} seconds")